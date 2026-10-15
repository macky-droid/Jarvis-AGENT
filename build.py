#!/usr/bin/env python3
"""
build.py - Scans markdown notes and generates viewer/graph-data.js
Standard library only: os, re, json, sys, pathlib
"""
import os
import re
import json
import sys
from pathlib import Path

def extract_excerpt(text: str, max_chars: int = 700) -> str:
    """Clean markdown headings/tags and extract ~700 character excerpt."""
    # Remove markdown headers
    clean = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
    # Simplify bold/italics
    clean = re.sub(r'[*_]{1,3}([^*_]+)[*_]{1,3}', r'\1', clean)
    # Strip wikilink brackets [[Target|Alias]] -> Alias or Target
    def clean_wiki(match):
        inner = match.group(1)
        if '|' in inner:
            return inner.split('|', 1)[1]
        return inner
    clean = re.sub(r'\[\[(.*?)\]\]', clean_wiki, clean)
    # Simplify bullet points
    clean = re.sub(r'^\s*[-*+]\s+', '', clean, flags=re.MULTILINE)
    # Collapse multiple whitespaces/newlines
    clean = re.sub(r'\n+', '\n', clean).strip()
    
    if len(clean) <= max_chars:
        return clean
    # Truncate at word boundary near max_chars
    truncated = clean[:max_chars]
    last_space = truncated.rfind(' ')
    if last_space > max_chars - 60:
        truncated = truncated[:last_space]
    return truncated.strip() + "..."

def extract_wikilinks(text: str) -> set:
    """Extract all wikilink targets from text, normalized lowercase."""
    wikilinks = set()
    for match in re.finditer(r'\[\[(.*?)\]\]', text):
        raw = match.group(1).strip()
        target = raw.split('|')[0].strip()
        if target:
            wikilinks.add(target.lower())
    return wikilinks

def main():
    notes_dir = sys.argv[1] if len(sys.argv) > 1 else "./notes"
    viewer_dir = "./viewer"
    output_file = os.path.join(viewer_dir, "graph-data.js")

    if not os.path.exists(notes_dir):
        print(f"Error: Notes directory '{notes_dir}' does not exist.")
        sys.exit(1)

    os.makedirs(viewer_dir, exist_ok=True)

    # 1. Collect all .md files
    md_files = []
    for root, _, files in os.walk(notes_dir):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))

    # Sort deterministically
    md_files.sort()

    if not md_files:
        print(f"No .md files found in {notes_dir}")
        sys.exit(1)

    # 2. Build nodes array with numeric id = array index
    nodes = []
    node_lookup_by_label = {}  # lowercase label -> index
    raw_texts = []
    wikilinks_per_node = []

    for idx, fpath in enumerate(md_files):
        filename = os.path.basename(fpath)
        label = os.path.splitext(filename)[0]
        
        # Determine group from relative folder path
        rel_dir = os.path.relpath(os.path.dirname(fpath), notes_dir)
        group = "general" if rel_dir in (".", "") else rel_dir.replace(os.sep, "/")
        
        with open(fpath, "r", encoding="utf-8") as f:
            raw_content = f.read()

        excerpt = extract_excerpt(raw_content, 700)
        
        node = {
            "id": idx,  # CRITICAL: numeric id equal to its position in the nodes array
            "label": label,
            "name": label,
            "group": group,
            "excerpt": excerpt,
            "path": os.path.relpath(fpath, ".").replace(os.sep, "/")
        }
        nodes.append(node)
        node_lookup_by_label[label.lower()] = idx
        raw_texts.append(raw_content)
        wikilinks_per_node.append(extract_wikilinks(raw_content))

    # 3. Build links:
    # "Link two notes when one mentions the other's title or they share [[wikilinks]]."
    link_pairs = set()

    # Direct links: mentions or direct [[wikilinks]]
    for src_idx, src_node in enumerate(nodes):
        src_text = raw_texts[src_idx]
        src_wikis = wikilinks_per_node[src_idx]

        for tgt_idx, tgt_node in enumerate(nodes):
            if src_idx == tgt_idx:
                continue

            pair = (min(src_idx, tgt_idx), max(src_idx, tgt_idx))
            if pair in link_pairs:
                continue

            tgt_label_lower = tgt_node["label"].lower()
            
            # Check direct wikilink
            has_wikilink = tgt_label_lower in src_wikis
            
            # Check title mention in text
            # Use regex word boundary where appropriate
            has_mention = False
            escaped_label = re.escape(tgt_node["label"])
            if re.search(r'\b' + escaped_label + r'\b', src_text, re.IGNORECASE):
                has_mention = True

            if has_wikilink or has_mention:
                link_pairs.add(pair)

    # Check shared wikilinks between any two notes
    num_nodes = len(nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            pair = (i, j)
            if pair in link_pairs:
                continue
            # If they share at least one [[wikilink]] target
            shared = wikilinks_per_node[i].intersection(wikilinks_per_node[j])
            if shared:
                link_pairs.add(pair)

    # Format links array with numeric IDs
    links = [{"source": src, "target": tgt} for src, tgt in sorted(link_pairs)]

    # Compute node degree / val for visual richness
    degree = {i: 0 for i in range(len(nodes))}
    for l in links:
        degree[l["source"]] += 1
        degree[l["target"]] += 1
    for n in nodes:
        n["val"] = max(3, degree[n["id"]] * 1.5 + 4)

    graph_payload = {
        "nodes": nodes,
        "links": links
    }

    # Write viewer/graph-data.js
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("// Generated automatically by build.py\n")
        f.write("const GRAPH = ")
        f.write(json.dumps(graph_payload, indent=2))
        f.write(";\n")

    # Also mirror to public/viewer/ so Vite dev server can preview it on port 3000
    public_viewer = "./public/viewer"
    os.makedirs(public_viewer, exist_ok=True)
    with open(os.path.join(public_viewer, "graph-data.js"), "w", encoding="utf-8") as f:
        f.write("// Generated automatically by build.py\n")
        f.write("const GRAPH = ")
        f.write(json.dumps(graph_payload, indent=2))
        f.write(";\n")
    
    # Copy viewer/index.html to public/viewer/index.html
    viewer_index = os.path.join(viewer_dir, "index.html")
    if os.path.exists(viewer_index):
        with open(viewer_index, "r", encoding="utf-8") as src, open(os.path.join(public_viewer, "index.html"), "w", encoding="utf-8") as dst:
            dst.write(src.read())

    print(f"Scanned {len(nodes)} markdown notes from '{notes_dir}'.")
    print(f"Generated {len(links)} connections.")
    print(f"Wrote output to '{output_file}' and '{public_viewer}/graph-data.js'.")

if __name__ == "__main__":
    main()
