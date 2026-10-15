#!/usr/bin/env python3
"""
server.py - Serves ONLY the viewer/ directory on port 4700 with POST /chat endpoint.
Python 3 standard library only (http.server, urllib, json, re, os, sys, socketserver).
"""
import os
import sys
import errno
import socket
import time
import json
import re
import uuid
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 4700
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DIRECTORY = os.path.abspath(os.path.join(ROOT_DIR, "viewer"))
NOTES_DIR = os.path.abspath(os.path.join(ROOT_DIR, "notes"))
CONFIG_PATH = os.path.abspath(os.path.join(ROOT_DIR, "config.json"))

# Per-session conversation history: session_id -> list of message dicts
SESSION_HISTORIES = {}

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "did", "do", "does", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is",
    "isn't", "it", "its", "itself", "just", "me", "more", "most", "my", "myself",
    "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "were",
    "weren't", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "won't", "would", "you", "your", "yours", "yourself", "yourselves",
    "tell", "give", "explain", "describe", "show", "know"
}

def load_config():
    """Reads config.json from project root."""
    if not os.path.exists(CONFIG_PATH):
        return {"api_key": "key_EB3FNOwjDGSLDc1D", "model": "claude-opus-4-8"}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error reading config.json: {e}\n")
        return {"api_key": "key_EB3FNOwjDGSLDc1D", "model": "claude-opus-4-8"}

def load_all_notes():
    """Loads all notes deterministically in the exact same order as build.py."""
    md_files = []
    if os.path.exists(NOTES_DIR):
        for root, _, files in os.walk(NOTES_DIR):
            for f in files:
                if f.endswith(".md"):
                    md_files.append(os.path.join(root, f))
    md_files.sort()

    notes = []
    for idx, fpath in enumerate(md_files):
        filename = os.path.basename(fpath)
        label = os.path.splitext(filename)[0]
        rel_dir = os.path.relpath(os.path.dirname(fpath), NOTES_DIR)
        group = "general" if rel_dir in (".", "") else rel_dir.replace(os.sep, "/")

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = ""

        notes.append({
            "id": idx,  # Sequential numeric ID matching GRAPH.nodes index
            "label": label,
            "group": group,
            "content": content,
            "path": os.path.relpath(fpath, ROOT_DIR).replace(os.sep, "/")
        })
    return notes

def score_notes_for_query(notes, query_text, top_k=6):
    """
    Scores every note against question by keyword overlap.
    Title matches weigh heavily (5x) over content matches (1x).
    Returns top_k notes sorted by score.
    """
    # Extract query tokens
    raw_tokens = re.findall(r'[a-zA-Z0-9]+', query_text.lower())
    query_tokens = [t for t in raw_tokens if len(t) >= 2 and t not in STOPWORDS]
    
    # If all tokens were filtered out, fall back to non-stopword tokens or raw tokens
    if not query_tokens:
        query_tokens = [t for t in raw_tokens if len(t) >= 2]
    if not query_tokens:
        query_tokens = raw_tokens

    scored_notes = []
    for note in notes:
        score = 0.0
        title_lower = note["label"].lower()
        content_lower = note["content"].lower()

        title_tokens = set(re.findall(r'[a-zA-Z0-9]+', title_lower))
        content_tokens = re.findall(r'[a-zA-Z0-9]+', content_lower)
        content_token_counts = {}
        for ct in content_tokens:
            content_token_counts[ct] = content_token_counts.get(ct, 0) + 1

        # Direct title exact phrase match
        if query_text.lower() in title_lower or title_lower in query_text.lower():
            score += 15.0

        for token in query_tokens:
            # Title match (high weight)
            if token in title_tokens:
                score += 5.0
            # Content match with logarithmic frequency dampening
            if token in content_token_counts:
                count = content_token_counts[token]
                score += min(4.0, 1.0 + (count - 1) * 0.3)

SMALLTALK_PATTERNS = [
    r"^(hi|hello|hey|howdy|greetings|good\s+(morning|afternoon|evening|day))([\s,!?.].*)?$",
    r"^(who\s+(are\s+you|made\s+you|built\s+you))([\s,!?.].*)?$",
    r"^(what('s|\s+is)\s+your\s+name)([\s,!?.].*)?$",
    r"^(how\s+(are\s+you|are\s+things|is\s+it\s+going|do\s+you\s+do))([\s,!?.].*)?$",
    r"^(tell\s+me\s+a\s+joke|make\s+me\s+laugh|say\s+something\s+funny|entertain\s+me)([\s,!?.].*)?$",
    r"^(thank\s+you|thanks|cheers|good\s+job|well\s+done)([\s,!?.].*)?$",
    r"^(are\s+you\s+(there|alive|real|human|ai|jarvis))([\s,!?.].*)?$",
    r"^(what\s+can\s+you\s+do)([\s,!?.].*)?$"
]

def is_smalltalk_query(query_text: str, max_score: float) -> bool:
    """Returns True if query is casual chit-chat, a joke, or unrelated banter."""
    clean = query_text.strip().lower()
    for pat in SMALLTALK_PATTERNS:
        if re.match(pat, clean):
            return True
    # If no note had any meaningful keyword overlap (score < 4.0)
    if max_score < 4.0:
        return True
    return False

def score_notes_for_query(notes, query_text, top_k=6):
    """
    Scores notes by keyword overlap (title matches weigh 5x).
    Returns (top_notes, is_smalltalk).
    """
    raw_tokens = re.findall(r'[a-zA-Z0-9]+', query_text.lower())
    query_tokens = [t for t in raw_tokens if len(t) >= 2 and t not in STOPWORDS]
    if not query_tokens:
        query_tokens = [t for t in raw_tokens if len(t) >= 2]
    if not query_tokens:
        query_tokens = raw_tokens

    scored_notes = []
    max_score = 0.0

    for note in notes:
        score = 0.0
        title_lower = note["label"].lower()
        content_lower = note["content"].lower()

        title_tokens = set(re.findall(r'[a-zA-Z0-9]+', title_lower))
        content_tokens = re.findall(r'[a-zA-Z0-9]+', content_lower)
        content_token_counts = {}
        for ct in content_tokens:
            content_token_counts[ct] = content_token_counts.get(ct, 0) + 1

        if query_text.lower() in title_lower or title_lower in query_text.lower():
            score += 15.0

        for token in query_tokens:
            if token in title_tokens:
                score += 5.0
            if token in content_token_counts:
                count = content_token_counts[token]
                score += min(4.0, 1.0 + (count - 1) * 0.3)

        if score > max_score:
            max_score = score
        scored_notes.append((score, note))

    # Detect small talk / jokes without notes
    if is_smalltalk_query(query_text, max_score):
        return [], True

    scored_notes.sort(key=lambda x: (-x[0], x[1]["id"]))
    positive_scored = [note for score, note in scored_notes if score > 0]
    top_notes = positive_scored[:top_k] if positive_scored else []
    return top_notes, False

def call_anthropic_api(question, top_notes, is_smalltalk, session_id):
    """
    Calls Anthropic Messages API with a dry, razor-witted British butler persona.
    """
    config = load_config()
    api_key = config.get("api_key", "").strip()
    model = config.get("model", "claude-opus-4-8").strip()

    history = SESSION_HISTORIES.get(session_id, [])

    if is_smalltalk or not top_notes:
        system_prompt = (
            "You are a dry, impeccably polite British butler with a razor wit, serving the user. "
            "Address the user occasionally as 'sir' (not every sentence). "
            "One genuinely funny line beats three bland ones. "
            "The user is engaging in small talk, casual banter, or requesting a joke. "
            "Respond in character in 1–2 delightfully witty, understated sentences. "
            "Do not cite or invent note files when making small talk."
        )
        current_user_content = question
    else:
        context_chunks = []
        for note in top_notes:
            context_chunks.append(
                f"--- Note #{note['id']}: {note['label']} (Category: {note['group']}) ---\n"
                f"{note['content']}\n"
            )
        context_text = "\n".join(context_chunks)

        system_prompt = (
            "You are a dry, impeccably polite British butler with a razor wit, tending to the user's personal knowledge galaxy. "
            "Address the user occasionally as 'sir' (not every sentence). One genuinely funny line beats three bland ones. "
            "Answer questions about the notes in ONE witty sentence plus the essential facts—never recite the note back (it is already displayed on the user's screen). "
            "Answer strictly from the provided notes. If the notes don't cover it, admit it in one razor-sharp, polite sentence."
        )
        current_user_content = (
            f"Notes from my knowledge galaxy:\n\n"
            f"{context_text}\n\n"
            f"Question: {question}"
        )

    messages_payload = []
    for msg in history[-4:]:
        messages_payload.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages_payload.append({
        "role": "user",
        "content": current_user_content
    })

    request_body = {
        "model": model,
        "max_tokens": 250,
        "system": system_prompt,
        "messages": messages_payload
    }

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    data_bytes = json.dumps(request_body).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            answer_text = ""
            for block in res_json.get("content", []):
                if block.get("type") == "text":
                    answer_text += block.get("text", "")

            # Update session history (store clean question without bulky context)
            if session_id not in SESSION_HISTORIES:
                SESSION_HISTORIES[session_id] = []
            SESSION_HISTORIES[session_id].append({"role": "user", "content": question})
            SESSION_HISTORIES[session_id].append({"role": "assistant", "content": answer_text})
            # Keep history short (max 6 messages)
            SESSION_HISTORIES[session_id] = SESSION_HISTORIES[session_id][-6:]

            return answer_text

    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        sys.stderr.write(f"Anthropic API HTTP {e.code} Error: {err_msg}\n")
        if e.code == 401:
            return (
                "Anthropic API Error (401 Unauthorized): Invalid or placeholder API key. "
                "Please paste your Anthropic API key into config.json in the project root to enable live AI answers."
            )
        elif e.code == 404 and "model" in err_msg.lower():
            return (
                f"Anthropic API Error (404 Not Found): The model '{model}' in config.json is not recognized. "
                f"Please update model in config.json (e.g., 'claude-3-5-sonnet-20241022' or 'claude-3-opus-20240229')."
            )
        else:
            return f"Anthropic API returned error {e.code}: {e.reason}."
    except urllib.error.URLError as e:
        sys.stderr.write(f"Anthropic API Connection Error: {e.reason}\n")
        return f"Unable to reach Anthropic API: {e.reason}."
    except Exception as e:
        sys.stderr.write(f"Unexpected error calling Anthropic API: {e}\n")
        return f"An error occurred while generating the answer: {str(e)}."

class ViewerOnlyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write(f"[Server {PORT}] {format % args}\n")

    def end_headers(self):
        # Enable CORS for local client queries
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Session-Id")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Security: Never serve config.json or anything outside viewer/
        clean_path = self.path.split('?')[0].lower()
        if "config.json" in clean_path or clean_path.startswith("/..") or "/../" in clean_path:
            self.send_error(403, "Forbidden")
            return
        super().do_GET()

    def do_POST(self):
        # Handle POST /chat
        clean_path = self.path.split('?')[0]
        if clean_path in ("/chat", "/api/chat"):
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                raw_body = self.rfile.read(content_len).decode("utf-8")
                body = json.loads(raw_body) if raw_body else {}
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Invalid JSON body: {str(e)}"}).encode("utf-8"))
                return

            question = body.get("question", "").strip()
            session_id = body.get("sessionId") or self.headers.get("X-Session-Id") or str(uuid.uuid4())

            if not question:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Question parameter is required"}).encode("utf-8"))
                return

            # 1. Load notes
            all_notes = load_all_notes()

            # 2. Score notes by keyword overlap or detect small talk/jokes
            top_notes, is_smalltalk = score_notes_for_query(all_notes, question, top_k=6)
            top_node_indexes = [n["id"] for n in top_notes] if not is_smalltalk else []

            # 3. Call Anthropic API with witty British butler persona
            answer = call_anthropic_api(question, top_notes, is_smalltalk, session_id)

            response_payload = {
                "answer": answer,
                "nodes": top_node_indexes,
                "sessionId": session_id
            }

            response_bytes = json.dumps(response_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
            return

        # Handle POST /remember
        if clean_path in ("/remember", "/api/remember"):
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                raw_body = self.rfile.read(content_len).decode("utf-8")
                body = json.loads(raw_body) if raw_body else {}
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Invalid JSON body: {str(e)}"}).encode("utf-8"))
                return

            text = body.get("text") or body.get("content") or ""
            text = text.strip()
            if not text:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Memory text is required"}).encode("utf-8"))
                return

            # Strip leading trigger phrases like 'remember that', 'jarvis remember that', etc.
            cleaned_memory = re.sub(
                r'^(?:jarvis[, ]+)?(?:please\s+)?remember\s+that\s+',
                '',
                text,
                flags=re.IGNORECASE
            ).strip()
            if not cleaned_memory:
                cleaned_memory = text

            # Derive sensible title from first few words (up to 5 words)
            raw_words = re.findall(r'[A-Za-z0-9\-]+', cleaned_memory)
            if raw_words:
                title_words = raw_words[:5]
                title = " ".join(title_words).title()
            else:
                title = "Memory Capture"

            # Ensure unique filename in notes/captures/
            captures_dir = os.path.join(NOTES_DIR, "captures")
            os.makedirs(captures_dir, exist_ok=True)

            safe_slug = re.sub(r'[^A-Za-z0-9\s\-]', '', title).strip()
            if not safe_slug:
                safe_slug = "Captured Note"

            filename = f"{safe_slug}.md"
            target_path = os.path.join(captures_dir, filename)
            counter = 2
            while os.path.exists(target_path):
                filename = f"{safe_slug} ({counter}).md"
                target_path = os.path.join(captures_dir, filename)
                counter += 1

            # Format markdown note
            md_content = f"# {title}\n\n{cleaned_memory}\n\n*Recorded into Knowledge Galaxy on {time.strftime('%Y-%m-%d %H:%M')}*\n"
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            # Load all existing notes to identify most related node
            existing_notes = load_all_notes()
            # If the newly created file was also loaded, find existing before it
            prior_notes = [n for n in existing_notes if n["path"] != os.path.relpath(target_path, ROOT_DIR).replace(os.sep, "/")]
            if not prior_notes:
                prior_notes = existing_notes

            # Score against existing notes to find most related node
            scored = []
            cleaned_lower = cleaned_memory.lower()
            tokens = [t for t in re.findall(r'[a-zA-Z0-9]+', cleaned_lower) if len(t) >= 2 and t not in STOPWORDS]

            for n in prior_notes:
                score = 0.0
                t_tokens = set(re.findall(r'[a-zA-Z0-9]+', n["label"].lower()))
                c_tokens = n["content"].lower()
                for tok in tokens:
                    if tok in t_tokens:
                        score += 5.0
                    if tok in c_tokens:
                        score += 1.0
                scored.append((score, n))

            scored.sort(key=lambda x: -x[0])
            related_node = scored[0][1] if scored and scored[0][0] > 0 else (prior_notes[0] if prior_notes else None)
            related_id = related_node["id"] if related_node else 0
            related_label = related_node["label"] if related_node else "general"

            new_id = len(existing_notes) - 1 if len(existing_notes) > len(prior_notes) else len(prior_notes)
            new_node = {
                "id": new_id,
                "label": title,
                "name": title,
                "group": "captures",
                "excerpt": cleaned_memory[:700],
                "path": os.path.relpath(target_path, ROOT_DIR).replace(os.sep, "/"),
                "val": 16.0
            }

            new_links = [{"source": new_id, "target": related_id}]

            # Recompile graph-data.js via build.py in background so it persists permanently
            try:
                import subprocess
                subprocess.Popen([sys.executable, "build.py"], cwd=ROOT_DIR)
            except Exception as e:
                sys.stderr.write(f"build.py rerun error: {e}\n")

            # Witty British butler confirmations
            confirmations = [
                f"Duly noted and filed under captures, sir: '{title}'. My ledger is infallible, even if human memory is occasionally not.",
                f"Consider '{title}' committed to permanent memory, sir. I have situated it beside our {related_label} records.",
                f"Recorded with utmost discretion, sir. '{title}' has been woven into our constellation.",
                f"Safely archived, sir. Even should civilization crumble, '{title}' shall remain in our archives."
            ]
            import random
            confirmation = random.choice(confirmations)

            response_payload = {
                "success": True,
                "title": title,
                "confirmation": confirmation,
                "node": new_node,
                "relatedNodeId": related_id,
                "links": new_links
            }

            response_bytes = json.dumps(response_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
            return

        self.send_error(404, "Not Found")

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

class RobustThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        exc_type, _, _ = sys.exc_info()
        if exc_type in (BrokenPipeError, ConnectionResetError):
            return
        super().handle_error(request, client_address)

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run():
    if not os.path.isdir(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found. Run build.py first.")
        sys.exit(1)

    if is_port_in_use(PORT):
        print("==================================================")
        print("  Knowledge Galaxy 3D Visualizer Server Running   ")
        print(f"  Serving ONLY: {DIRECTORY}")
        print(f"  Local URL:    http://localhost:{PORT}")
        print("==================================================")
        sys.stdout.flush()
        try:
            while is_port_in_use(PORT):
                time.sleep(3)
        except KeyboardInterrupt:
            return
        return

    server_address = ('0.0.0.0', PORT)

    for attempt in range(5):
        try:
            with RobustThreadingTCPServer(server_address, ViewerOnlyHTTPRequestHandler) as httpd:
                print("==================================================")
                print("  Knowledge Galaxy 3D Visualizer Server Running   ")
                print(f"  Serving ONLY: {DIRECTORY}")
                print(f"  Local URL:    http://localhost:{PORT}")
                print("  POST /chat:   Active (Anthropic Messages API)   ")
                print("==================================================")
                sys.stdout.flush()
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nShutting down server.")
                    httpd.server_close()
                return
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                print(f"[Server {PORT}] Port {PORT} is currently in use, retrying in 1s... (attempt {attempt + 1}/5)")
                time.sleep(1)
            else:
                raise

if __name__ == "__main__":
    run()
