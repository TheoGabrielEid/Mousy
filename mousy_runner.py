#!/usr/bin/env python3
"""
Mousy — Autonomous Desktop Coworker Plugin Engine
==================================================
Lightweight plugin runtime for Claude, ChatGPT, and AI agents.
Enables live Windows screen vision, smooth mouse gliding, typing,
and surgical code editing without any GUI bloat.
"""

import sys
import os
import io
import time
import json
import base64
import difflib
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

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


# --- Core Plugin Capabilities ---

def observe_screen() -> Dict[str, Any]:
    """Capture screen and return dimensions and base64 JPEG image."""
    try:
        # DPI awareness for accurate coordinates
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

        # Try MSS first
        if mss and Image:
            try:
                mss_cls = getattr(mss, "MSS", getattr(mss, "mss", None))
                with mss_cls() as sct:
                    mon = sct.monitors[1]
                    shot = sct.grab(mon)
                    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
                    w, h = img.size
                    scale = min(1280 / max(w, h), 1.0)
                    if scale < 1.0:
                        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=75)
                    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                    return {
                        "status": "success",
                        "width": w,
                        "height": h,
                        "scaled_width": img.size[0],
                        "scaled_height": img.size[1],
                        "image_base64": b64
                    }
            except Exception:
                pass

        # Try PIL ImageGrab
        try:
            from PIL import ImageGrab
            shot = ImageGrab.grab()
            w, h = shot.size
            buf = io.BytesIO()
            shot.convert("RGB").save(buf, format="JPEG", quality=75)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return {
                "status": "success",
                "width": w,
                "height": h,
                "image_base64": b64
            }
        except Exception:
            pass

        # Fallback to system dimensions if display DC is locked in background
        import ctypes
        w = ctypes.windll.user32.GetSystemMetrics(0) or 1920
        h = ctypes.windll.user32.GetSystemMetrics(1) or 1080
        return {
            "status": "session_background",
            "width": w,
            "height": h,
            "message": "Desktop display session is currently backgrounded. Mouse coordinates and file editing remain fully active."
        }
    except Exception as e:
        return {"status": "error", "message": f"Screen observation notice: {str(e)}"}


def glide_mouse(x: int, y: int, duration: float = 0.4) -> Dict[str, Any]:
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

        # Native Windows SendKeys fallback
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
        
        # Calculate unified diff
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


def read_file(path: str, start_line: int = 1, line_count: int = 100) -> Dict[str, Any]:
    """Read lines safely from file."""
    try:
        p = Path(path).resolve()
        if not p.exists():
            return {"status": "error", "message": f"File does not exist: {p}"}
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        start = max(0, start_line - 1)
        end = start + line_count
        chunk = lines[start:end]
        return {
            "status": "success",
            "file": str(p),
            "total_lines": len(lines),
            "content": "\n".join(chunk)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write or overwrite file."""
    try:
        p = Path(path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"status": "success", "file": str(p), "bytes_written": len(content)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Dispatcher map
ACTIONS = {
    "observe_screen": observe_screen,
    "glide_mouse": glide_mouse,
    "click": click,
    "type_text": type_text,
    "press_key": press_key,
    "scroll": scroll,
    "open_app": open_app,
    "edit_file": edit_file,
    "read_file": read_file,
    "write_file": write_file
}


def run_stdio_worker():
    """Stdio protocol for Claude Desktop, Claude Code, and Antigravity."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            action = req.get("action") or req.get("method") or req.get("name")
            params = req.get("params") or req.get("arguments") or req.get("args") or {}
            
            if action in ACTIONS:
                res = ACTIONS[action](**params)
                sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
                sys.stdout.flush()
            elif action == "list_tools":
                tools = [
                    {"name": k, "description": v.__doc__}
                    for k, v in ACTIONS.items()
                ]
                sys.stdout.write(json.dumps({"id": req.get("id"), "result": tools}) + "\n")
                sys.stdout.flush()
            else:
                sys.stdout.write(json.dumps({"id": req.get("id"), "error": f"Unknown action {action}"}) + "\n")
                sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--action":
        action_name = sys.argv[2]
        action_args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        if action_name in ACTIONS:
            res = ACTIONS[action_name](**action_args)
            print(json.dumps(res, indent=2))
        else:
            print(json.dumps({"error": f"Unknown action: {action_name}"}))
    else:
        run_stdio_worker()
