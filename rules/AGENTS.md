# Mousy Agent Guidelines & Behavioral Rules

When using the Mousy desktop coworker plugin:

1. **Verify Screen State Before Clicking**:
   - Always call `observe_screen()` to verify window boundaries, buttons, and coordinates before sending clicks or keystrokes.

2. **Smooth Cursor Interaction**:
   - Prefer `glide_mouse` before `click` so the user visually sees where the pointer is traveling.

3. **Surgical Diffs Over File Rewrites**:
   - Always use `edit_file` to replace target blocks and produce unified diffs rather than overwriting entire source files.

4. **Human-in-the-Loop Safety**:
   - Draft emails, pull requests, and web form fields directly on screen, but leave final submission to the user.
