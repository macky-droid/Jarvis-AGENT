import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import net from 'net';
import { createServer as createViteServer } from 'vite';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function isPortActive(port: number): Promise<boolean> {
  return new Promise((resolve) => {
    const socket = net.createConnection({ port, host: '127.0.0.1' });
    socket.once('connect', () => {
      socket.destroy();
      resolve(true);
    });
    socket.once('error', () => {
      resolve(false);
    });
  });
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Serve static viewer files
  app.use('/viewer', express.static(path.join(__dirname, 'viewer')));

  // Forward /chat to Python server on 4700
  app.post(['/chat', '/api/chat'], async (req, res) => {
    try {
      const response = await fetch('http://127.0.0.1:4700/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body),
      });
      const data = await response.json();
      res.status(response.status).json(data);
    } catch (err: any) {
      res.status(502).json({ error: 'Failed to contact Python backend on port 4700', details: err?.message });
    }
  });

  // Forward /remember to Python server on 4700
  app.post(['/remember', '/api/remember'], async (req, res) => {
    try {
      const response = await fetch('http://127.0.0.1:4700/remember', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body),
      });
      const data = await response.json();
      res.status(response.status).json(data);
    } catch (err: any) {
      res.status(502).json({ error: 'Failed to contact Python backend on port 4700', details: err?.message });
    }
  });

  // API endpoint to trigger build.py
  app.post('/api/build', (_req, res) => {
    const buildProcess = spawn('python3', ['build.py'], { cwd: __dirname });
    let output = '';
    buildProcess.stdout.on('data', (d) => { output += d.toString(); });
    buildProcess.stderr.on('data', (d) => { output += d.toString(); });
    buildProcess.on('close', (code) => {
      res.json({ success: code === 0, output });
    });
  });

  // Ensure Python viewer server runs on port 4700
  async function ensurePythonServer() {
    const active = await isPortActive(4700);
    if (active) {
      console.log('[DevServer] Python server is already active on port 4700.');
      return;
    }

    console.log('[DevServer] Launching Python server (server.py) on port 4700...');
    const py = spawn('python3', ['server.py'], {
      cwd: __dirname,
      stdio: 'inherit',
    });

    py.on('exit', async (code) => {
      console.log(`[DevServer] Python server process exited (code ${code}).`);
      // Wait 3 seconds before checking whether to restart
      setTimeout(async () => {
        const stillActive = await isPortActive(4700);
        if (!stillActive) {
          ensurePythonServer();
        }
      }, 3000);
    });
  }

  await ensurePythonServer();

  // Mount Vite in dev mode
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.join(__dirname, 'dist')));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(__dirname, 'dist', 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`[DevServer] Fullstack server running on http://0.0.0.0:${PORT}`);
    console.log(`[DevServer] Python viewer running on http://localhost:4700`);
  });
}

startServer().catch((err) => {
  console.error('[DevServer] Failed to start:', err);
  process.exit(1);
});
