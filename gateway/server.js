const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const express = require('express');
const QRCode = require('qrcode');
const pino = require('pino');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(express.json());

const PORT = 3001;
const SESSION_DIR = path.join(__dirname, 'auth_session');

let sock = null;
let currentQR = null;
let connectionStatus = 'initializing';
let connectedUser = null;

async function startWhatsApp() {
  if (!fs.existsSync(SESSION_DIR)) {
    fs.mkdirSync(SESSION_DIR, { recursive: true });
  }

  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);

  sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
    logger: pino({ level: 'silent' }),
    browser: ['Tamimah Prospecting Agent', 'Chrome', '1.0.0']
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      currentQR = await QRCode.toDataURL(qr);
      connectionStatus = 'qr_ready';
      console.log('>>> [WhatsApp Gateway] New QR code generated. Ready for scanning.');
    }

    if (connection === 'close') {
      const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
      connectionStatus = 'disconnected';
      connectedUser = null;
      console.log('>>> [WhatsApp Gateway] Connection closed. Reconnecting:', shouldReconnect);
      if (shouldReconnect) {
        setTimeout(startWhatsApp, 3000);
      }
    } else if (connection === 'open') {
      connectionStatus = 'connected';
      currentQR = null;
      connectedUser = sock.user?.id || 'Connected';
      console.log('>>> [WhatsApp Gateway] WhatsApp connected successfully! Account:', connectedUser);
    }
  });
}

// REST Endpoints
app.get('/status', (req, res) => {
  res.json({
    status: connectionStatus,
    user: connectedUser,
    hasQR: Boolean(currentQR)
  });
});

app.get('/qr', (req, res) => {
  if (connectionStatus === 'connected') {
    return res.send(`<html><body style="font-family:sans-serif;text-align:center;padding:50px;">
      <h2 style="color:green;">&#10004; WhatsApp is Connected!</h2>
      <p>Account: ${connectedUser}</p>
    </body></html>`);
  }
  if (!currentQR) {
    return res.send(`<html><body style="font-family:sans-serif;text-align:center;padding:50px;">
      <h2>Generating QR Code...</h2>
      <p>Please refresh in 2 seconds.</p>
      <script>setTimeout(() => location.reload(), 2000);</script>
    </body></html>`);
  }
  res.send(`<html><body style="font-family:sans-serif;text-align:center;padding:40px;background:#f8fafc;">
    <h2>Scan with WhatsApp on your Phone</h2>
    <p>Open <b>WhatsApp &gt; Settings &gt; Linked Devices &gt; Link a Device</b></p>
    <div style="margin:20px auto;"><img src="${currentQR}" style="width:280px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1);"/></div>
    <p style="color:#64748b;">This page will auto-refresh once linked.</p>
    <script>
      setInterval(async () => {
        const r = await fetch('/status');
        const d = await r.json();
        if (d.status === 'connected') location.reload();
      }, 2500);
    </script>
  </body></html>`);
});

app.post('/send', async (req, res) => {
  try {
    const { to, message } = req.body;
    if (!sock || connectionStatus !== 'connected') {
      return res.status(400).json({ success: false, error: 'WhatsApp not connected. Scan QR first.' });
    }
    if (!to || !message) {
      return res.status(400).json({ success: false, error: 'Missing "to" or "message" parameter.' });
    }

    // Format phone number to WhatsApp JID: e.g. 96891234567@s.whatsapp.net
    let cleaned = to.replace(/[^0-9]/g, '');
    // If sent to 'me' or self, send to connected user JID
    let jid = cleaned ? `${cleaned}@s.whatsapp.net` : sock.user.id;
    if (to === 'me' || to === 'self') {
      jid = sock.user.id.split(':')[0] + '@s.whatsapp.net';
    }

    const sent = await sock.sendMessage(jid, { text: message });
    console.log(`>>> [WhatsApp Gateway] Message sent successfully to ${jid}`);
    return res.json({ success: true, messageId: sent.key.id, to: jid });
  } catch (err) {
    console.error('>>> [WhatsApp Gateway] Error sending message:', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`>>> [WhatsApp Gateway] Running on http://localhost:${PORT}`);
  startWhatsApp();
});
