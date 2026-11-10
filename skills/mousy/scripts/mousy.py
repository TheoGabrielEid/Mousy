#!/usr/bin/env python3
"""
Mousy — Desktop Skill CLI Script
=================================
Bundled script for the Mousy Claude Plugin.
Allows agents to execute screen observation, mouse gliding, clicking,
live typing, and surgical file diff editing via simple CLI commands.
"""

import sys
import os
import io
import time
import json
import base64
import difflib
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
except ImportError:
    pyautogui = None

try:
    import mss
except ImportError:
    mss = None

try:
    from PIL import Image
except ImportError:
    Image = None


def observe_screen(output_file: str = "screen.jpg") -> Dict[str, Any]:
    """Capture screen and save to disk / return dimensions."""
    try:
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

        if mss and Image:
            try:
                mss_cls = getattr(mss, "MSS", getattr(mss, "mss", None))
                with mss_cls() as sct:
                    mon = sct.monitors[1]
                    shot = sct.grab(mon)
                    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
                    w, h = img.size
                    img.save(output_file, quality=80)
                    return {
                        "status": "success",
                        "width": w,
                        "height": h,
                        "saved_to": str(Path(output_file).resolve())
                    }
            except Exception:
                pass

        try:
            from PIL import ImageGrab
            shot = ImageGrab.grab()
            w, h = shot.size
            shot.convert("RGB").save(output_file, quality=80)
            return {
                "status": "success",
                "width": w,
                "height": h,
                "saved_to": str(Path(output_file).resolve())
            }
        except Exception:
            pass

        import ctypes
        w = ctypes.windll.user32.GetSystemMetrics(0) or 1920
        h = ctypes.windll.user32.GetSystemMetrics(1) or 1080
        return {
            "status": "display_active",
            "width": w,
            "height": h,
            "message": "Screen dimensions retrieved."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def glide_mouse(x: int, y: int, duration: float = 0.35) -> Dict[str, Any]:
    """Smoothly glide cursor with human easing."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        start_x, start_y = pt.x, pt.y
        target_x, target_y = int(x), int(y)
        
        steps = max(10, int(duration * 50))
        sleep_per_step = max(0.002, duration / steps)
        for i in range(1, steps + 1):
            t = i / steps
            ease_t = 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
            cx = int(start_x + (target_x - start_x) * ease_t)
            cy = int(start_y + (target_y - start_y) * ease_t)
            user32.SetCursorPos(cx, cy)
            time.sleep(sleep_per_step)
        user32.SetCursorPos(target_x, target_y)
        return {"status": "success", "from": [start_x, start_y], "to": [target_x, target_y]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def click(x: int, y: int, button: str = "left", double: bool = False) -> Dict[str, Any]:
    """Move to coordinates and perform a click."""
    try:
        glide_mouse(x, y, duration=0.2)
        time.sleep(0.04)
        import ctypes
        user32 = ctypes.windll.user32
        if button == "right":
            down_flag, up_flag = 0x0008, 0x0010
        elif button == "middle":
            down_flag, up_flag = 0x0020, 0x0040
        else:
            down_flag, up_flag = 0x0002, 0x0004
            
        user32.mouse_event(down_flag, 0, 0, 0, 0)
        user32.mouse_event(up_flag, 0, 0, 0, 0)
        if double:
            time.sleep(0.08)
            user32.mouse_event(down_flag, 0, 0, 0, 0)
            user32.mouse_event(up_flag, 0, 0, 0, 0)
        return {"status": "success", "clicked": [x, y], "button": button, "double": double}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def type_text(text: str, delay_ms: int = 15) -> Dict[str, Any]:
    """Type characters live into the currently active window."""
    try:
        if pyautogui:
            interval = max(0.005, min(delay_ms / 1000.0, 0.2))
            pyautogui.write(text, interval=interval)
            return {"status": "success", "typed_length": len(text)}
        
        # Native Windows SendKeys fallback
        escaped = text.replace("{", "{{}").replace("}", "{}}").replace("+", "{+}").replace("^", "{^}").replace("%", "{%}")
        ps_cmd = f"$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys('{escaped}')"
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, timeout=10)
        return {"status": "success", "typed_length": len(text)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def press_key(combo: str) -> Dict[str, Any]:
    """Press keyboard combination (e.g. 'enter', 'ctrl+s', 'win+r', 'alt+tab')."""
    try:
        if pyautogui:
            parts = [p.strip().lower() for p in combo.split("+")]
            if len(parts) == 1:
                pyautogui.press(parts[0])
            else:
                pyautogui.hotkey(*parts)
            return {"status": "success", "pressed": combo}

        key_map = {"enter": "{ENTER}", "tab": "{TAB}", "esc": "{ESC}", "backspace": "{BACKSPACE}"}
        key_val = key_map.get(combo.lower(), combo)
        ps_cmd = f"$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys('{key_val}')"
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, timeout=10)
        return {"status": "success", "pressed": combo}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def scroll(amount: int = -3) -> Dict[str, Any]:
    """Scroll mouse wheel up or down."""
    try:
        import ctypes
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, int(amount) * 120, 0)
        return {"status": "success", "amount": amount}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def open_app(target: str) -> Dict[str, Any]:
    """Launch application or URL."""
    try:
        if target.startswith(("http://", "https://")):
            import webbrowser
            webbrowser.open(target)
            return {"status": "success", "opened_url": target}
        else:
            subprocess.Popen(["powershell", "-NoProfile", "-Command", f"Start-Process '{target}'"], creationflags=0x08000000)
            return {"status": "success", "launched": target}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def edit_file(path: str, target: str, replacement: str) -> Dict[str, Any]:
    """Surgically edit code in a file and generate unified diff."""
    try:
        p = Path(path).resolve()
        if not p.exists():
            return {"status": "error", "message": f"File does not exist: {p}"}
        
        old_content = p.read_text(encoding="utf-8", errors="ignore")
        if target not in old_content:
            return {"status": "error", "message": f"Target content not found in {p.name}"}
        
        new_content = old_content.replace(target, replacement, 1)
        p.write_text(new_content, encoding="utf-8")
        
        diff = list(difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{p.name}",
            tofile=f"b/{p.name}",
            n=3
        ))
        diff_text = "".join(diff)
        
        return {
            "status": "success",
            "file": str(p),
            "diff": diff_text[:5000]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Mousy Plugin CLI Runner")
    subparsers = parser.add_subparsers(dest="command", help="Skill command to execute")

    # observe
    obs_p = subparsers.add_parser("observe", help="Capture live desktop screenshot")
    obs_p.add_argument("--out", default="screen.jpg", help="Output image file path")

    # glide
    glide_p = subparsers.add_parser("glide", help="Smoothly glide mouse to coordinates")
    glide_p.add_argument("x", type=int, help="Target X coordinate")
    glide_p.add_argument("y", type=int, help="Target Y coordinate")
    glide_p.add_argument("--duration", type=float, default=0.35, help="Glide duration in seconds")

    # click
    click_p = subparsers.add_parser("click", help="Click at coordinates")
    click_p.add_argument("x", type=int, help="Target X coordinate")
    click_p.add_argument("y", type=int, help="Target Y coordinate")
    click_p.add_argument("--button", default="left", choices=["left", "right", "middle"])
    click_p.add_argument("--double", action="store_true", help="Double click")

    # type
    type_p = subparsers.add_parser("type", help="Type text into active window")
    type_p.add_argument("text", type=str, help="Text to type")
    type_p.add_argument("--delay", type=int, default=15, help="Delay between keys in ms")

    # press
    press_p = subparsers.add_parser("press", help="Press key combo")
    press_p.add_argument("combo", type=str, help="Key or hotkey combo (e.g. 'ctrl+s')")

    # scroll
    scroll_p = subparsers.add_parser("scroll", help="Scroll mouse wheel")
    scroll_p.add_argument("amount", type=int, default=-3, help="Scroll notches (negative=down)")

    # open
    open_p = subparsers.add_parser("open", help="Launch app or open URL")
    open_p.add_argument("target", type=str, help="Application name or web URL")

    # edit
    edit_p = subparsers.add_parser("edit", help="Surgically edit file")
    edit_p.add_argument("--path", required=True, help="File path")
    edit_p.add_argument("--target", required=True, help="Exact target text to replace")
    edit_p.add_argument("--replacement", required=True, help="Replacement text")

    args = parser.parse_args()

    if args.command == "observe":
        res = observe_screen(output_file=args.out)
    elif args.command == "glide":
        res = glide_mouse(x=args.x, y=args.y, duration=args.duration)
    elif args.command == "click":
        res = click(x=args.x, y=args.y, button=args.button, double=args.double)
    elif args.command == "type":
        res = type_text(text=args.text, delay_ms=args.delay)
    elif args.command == "press":
        res = press_key(combo=args.combo)
    elif args.command == "scroll":
        res = scroll(amount=args.amount)
    elif args.command == "open":
        res = open_app(target=args.target)
    elif args.command == "edit":
        res = edit_file(path=args.path, target=args.target, replacement=args.replacement)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
