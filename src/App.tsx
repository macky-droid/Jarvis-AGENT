/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ExternalLink, Terminal, Copy, Check, Sparkles, FolderTree, Compass, Layers, Wrench } from 'lucide-react';

export default function App() {
  const [copied, setCopied] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  const [isBuilding, setIsBuilding] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);

  const localUrl = 'http://localhost:4700';

  const copyUrl = () => {
    navigator.clipboard.writeText(localUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRebuild = async () => {
    setIsBuilding(true);
    try {
      const res = await fetch('/api/build', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setIframeKey((prev) => prev + 1);
      }
    } catch (e) {
      console.error('Rebuild failed', e);
    } finally {
      setIsBuilding(false);
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-slate-950 text-slate-100 flex flex-col font-sans select-none">
      {/* Top Banner Bar */}
      <header className="absolute top-0 left-0 right-0 h-14 z-30 px-4 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 flex items-center justify-between pointer-events-auto">
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-7 h-7 rounded-full bg-cyan-500/10 border border-cyan-500/30">
            <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_10px_#22d3ee]" />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wide uppercase bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent flex items-center gap-2">
              Knowledge Galaxy
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/50">
                v1.0
              </span>
            </h1>
          </div>
        </div>

        {/* Server & Links */}
        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-mono text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
            <span className="text-slate-400">Server:</span>
            <span className="text-cyan-300 font-semibold">{localUrl}</span>
            <button
              onClick={copyUrl}
              className="ml-1 p-1 hover:text-white transition-colors"
              title="Copy localhost URL"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
            </button>
          </div>

          <button
            onClick={handleRebuild}
            disabled={isBuilding}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-slate-900/90 hover:bg-slate-800 text-slate-300 border border-slate-700/80 transition-all disabled:opacity-50"
            title="Scan ./notes and recompile graph-data.js"
          >
            <Sparkles className={`w-3.5 h-3.5 text-amber-400 ${isBuilding ? 'animate-spin' : ''}`} />
            <span>{isBuilding ? 'Rebuilding...' : 'Rebuild Graph'}</span>
          </button>

          <button
            onClick={() => {
              const iframe = document.querySelector('iframe') as HTMLIFrameElement;
              if (iframe?.contentWindow) {
                iframe.contentWindow.postMessage({ type: 'OPEN_PHONE_MODAL' }, '*');
              }
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/30 transition-all shadow-[0_0_15px_rgba(56,189,248,0.15)]"
            title="Launch Jarvis Phone Booking Dispatcher"
          >
            <span>📞 Jarvis Call</span>
          </button>

          <a
            href={localUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 transition-all shadow-[0_0_15px_rgba(6,182,212,0.15)]"
          >
            <span>Open in Chrome</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          <button
            onClick={() => setShowGuide(!showGuide)}
            className={`px-3 py-1.5 text-xs font-medium rounded-full border transition-all ${
              showGuide
                ? 'bg-slate-800 text-white border-slate-600'
                : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 border-slate-800'
            }`}
          >
            Commands & Guide
          </button>
        </div>
      </header>

      {/* Embedded 3D Force Graph Viewer */}
      <main className="relative flex-1 w-full h-full pt-14">
        <iframe
          key={iframeKey}
          src="/viewer/index.html"
          title="3D Knowledge Galaxy Viewer"
          className="w-full h-full border-0"
          allow="accelerometer; camera; gyroscope; vr"
        />
      </main>

      {/* Guide Drawer Modal */}
      {showGuide && (
        <div className="absolute inset-y-14 right-0 w-96 max-w-full z-40 bg-slate-950/95 backdrop-blur-xl border-l border-slate-800 p-6 flex flex-col gap-5 overflow-y-auto shadow-2xl">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
              <Compass className="w-4 h-4 text-cyan-400" />
              Galaxy Architecture
            </h2>
            <button
              onClick={() => setShowGuide(false)}
              className="text-slate-400 hover:text-white text-xs px-2 py-1 rounded bg-slate-900 border border-slate-800"
            >
              ✕
            </button>
          </div>

          <div className="space-y-4 text-xs text-slate-300 leading-relaxed">
            <div>
              <div className="text-[11px] font-semibold text-cyan-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5" /> 1. Generate / Update Graph
              </div>
              <p className="text-slate-400 mb-2">
                Scan markdown notes in <code className="text-cyan-300">./notes</code> and generate <code className="text-cyan-300">viewer/graph-data.js</code>:
              </p>
              <pre className="p-2.5 rounded-lg bg-black/60 border border-slate-800 font-mono text-[11px] text-cyan-300 select-all overflow-x-auto">
                python3 build.py
              </pre>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5" /> 2. Run Local Server (Port 4700)
              </div>
              <p className="text-slate-400 mb-2">
                Serves exclusively the <code className="text-emerald-300">viewer/</code> folder with zero external dependencies:
              </p>
              <pre className="p-2.5 rounded-lg bg-black/60 border border-slate-800 font-mono text-[11px] text-emerald-300 select-all overflow-x-auto">
                python3 server.py
              </pre>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-purple-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <FolderTree className="w-3.5 h-3.5" /> 3. Sample Notes Included (25)
              </div>
              <p className="text-slate-400 mb-2">
                Crafted for <em>"Solstice Craft Roastery & Artisan Lab"</em> with deep cross-links:
              </p>
              <ul className="grid grid-cols-2 gap-1.5 font-mono text-[11px] text-slate-300">
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 operations (5)</li>
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 recipes (4)</li>
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 equipment (4)</li>
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 marketing (4)</li>
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 people (4)</li>
                <li className="p-1.5 bg-slate-900/60 rounded border border-slate-800/80">📁 finance (4)</li>
              </ul>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-amber-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5" /> 4. Linking Logic
              </div>
              <p className="text-slate-400">
                Nodes are linked when one note contains <code className="text-amber-300">[[wikilinks]]</code>, mentions another note's exact title, or shares wikilink destinations. Every node holds a strict numeric <code className="text-amber-300">id</code> matching its index.
              </p>
            </div>

            {/* Troubleshooting section */}
            <div className="pt-2 border-t border-slate-800">
              <div className="text-[11px] font-bold text-rose-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Wrench className="w-3.5 h-3.5" /> Troubleshooting (90% of all issues)
              </div>
              <div className="space-y-2">
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">Mic button does nothing</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Chrome → lock icon in address bar → allow Microphone. Must be Chrome/Edge.</div>
                </div>

                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">No sound</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Click anywhere on the page once, then ask again (browsers block audio before first interaction).</div>
                </div>

                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">Page looks stale after a change</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Hard reload: <kbd className="px-1 py-0.5 bg-black rounded text-[10px] text-slate-300">Cmd+Shift+R</kbd> (Mac) / <kbd className="px-1 py-0.5 bg-black rounded text-[10px] text-slate-300">Ctrl+Shift+R</kbd> (Windows).</div>
                </div>

                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">"model not configured"</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">You didn't paste your key into <code className="text-cyan-300">config.json</code>, or left the placeholder text in.</div>
                </div>

                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">Answers are generic</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Your notes folder path was wrong in Prompt 1 — re-run it with the full absolute path.</div>
                </div>

                <div className="p-2 rounded bg-slate-900/80 border border-slate-800">
                  <div className="font-semibold text-rose-300 text-[11px]">Anything else</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Paste the exact error into Claude Code and say "fix it." That's the whole method.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
