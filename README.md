# 🔒 Reverse Shell Example (Educational Use Only)

> ⚠️ **Warning:** This code is intended **for educational purposes only** and should only be run in a **controlled lab environment** on systems you own. Using it on devices without permission is illegal. 🚫

## 📖 Description

This Python script demonstrates a basic **reverse shell connection** for educational purposes. It connects back to a predefined server IP and port and provides a shell over the network.

Key points:

- 🖧 Uses the `socket` module to establish a TCP connection.
- 🔄 Redirects standard input, output, and error streams to the socket.
- 🐚 Uses `pty.spawn("sh")` to spawn an interactive shell.

## 🛠 Requirements

- 🐍 Python 3.x
- 🌐 Network access to the target server (controlled lab environment)
- ✅ Permissions to run scripts and open network connections

## 🚀 Usage

1. Set up a listener on your machine (educational lab):
   ```bash
   nc -lvp 4444