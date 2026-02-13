const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const morgan = require('morgan');
const app = express();
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
app.listen(PORT,'0.0.0.0',()=>console.log(`Server running at: http://0.0.0.0:${PORT}`));