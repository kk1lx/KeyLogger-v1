from pynput import keyboard

def on_press(key):
    try:
        print(key.char, end="", flush=True)
    except AttributeError:
        if key == keyboard.Key.space:
            print(" ", end="", flush=True)
        elif key == keyboard.Key.enter:
            print("\n", end="", flush=True)
        else:
            print(f"[{key.name}]", end="", flush=True)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()