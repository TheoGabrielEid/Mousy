---
name: mousy
description: Autonomous desktop pair programming plugin. Live screen vision, smooth mouse gliding, clicking, typing, and surgical code diff editing on Windows for Claude, ChatGPT, and AI agents.
---

# Mousy — Desktop Coworker Plugin

Mousy empowers AI agents to interact with the user's live Windows desktop and collaborate in real-time.

## Capabilities

1. **`observe_screen()`**:
   - Takes a real-time screenshot of the primary Windows monitor.
   - Returns resolution (`width`, `height`) and base64 JPEG data for multimodal vision models.

2. **`glide_mouse(x, y, duration=0.4)`**:
   - Smoothly moves the mouse cursor to `(x, y)` using human-like ease-in-out quadratic interpolation.

3. **`click(x, y, button="left", double=False)`**:
   - Glides cursor to coordinates and performs a left, right, or double click.

4. **`type_text(text, delay_ms=15)`**:
   - Types characters live into the currently active window character-by-character.

5. **`press_key(combo)`**:
   - Triggers key combinations (e.g., `enter`, `ctrl+s`, `win+r`, `alt+tab`, `ctrl+c`, `ctrl+v`).

6. **`scroll(amount=-3)`**:
   - Scrolls the mouse wheel up (positive) or down (negative).

7. **`open_app(target)`**:
   - Launches any Windows application or navigates to a URL in the browser.

8. **`edit_file(path, target, replacement)`**:
   - Surgically modifies code files and produces clean color unified diffs.

9. **`read_file(path, start_line=1, line_count=100)`**:
   - Reads chunks of files safely.

10. **`write_file(path, content)`**:
    - Creates or updates files.

---

## Safety Protocol

- **Never submit irreversible actions automatically**:
  - Never press "Send" on emails or click "Submit" on payment/account forms without human review.
  - Draft content live in the active window, leave it visible for the user, and prompt them to confirm.
- **Always observe before action**:
  - Call `observe_screen()` first to verify coordinate positions before clicking.
