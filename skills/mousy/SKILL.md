---
name: mousy
description: Autonomous desktop pair programming plugin. Bundles live Windows screen vision, smooth mouse gliding, clicking, live typing, and surgical code diff editing.
---

# Mousy — Desktop Coworker Skill

Mousy empowers AI agents (Claude, ChatGPT, and Antigravity) to interact directly with the user's live Windows desktop.

## Available Capabilities & CLI Commands

You can execute any of Mousy's capabilities using the bundled script `scripts/mousy.py`:

### 1. Observe Desktop Screen
Captures the primary monitor and saves a screenshot:
```powershell
python scripts/mousy.py observe --out screen.jpg
```
Returns: Screen resolution (`width`, `height`) and image path.

### 2. Smooth Mouse Gliding
Glides the cursor smoothly to `(X, Y)` with human-like ease-in-out interpolation:
```powershell
python scripts/mousy.py glide 500 350
```

### 3. Mouse Clicking
Clicks at coordinates (supports `left`, `right`, and double click):
```powershell
python scripts/mousy.py click 500 350
python scripts/mousy.py click 500 350 --double
python scripts/mousy.py click 500 350 --button right
```

### 4. Interactive Typing
Types text live into the currently active window character-by-character:
```powershell
python scripts/mousy.py type "Hello world"
```

### 5. Keyboard Combos
Triggers key combinations and hotkeys:
```powershell
python scripts/mousy.py press "ctrl+s"
python scripts/mousy.py press "win+r"
python scripts/mousy.py press "enter"
```

### 6. Mouse Wheel Scrolling
Scrolls up or down:
```powershell
python scripts/mousy.py scroll -3
```

### 7. App & URL Launcher
Launches applications or navigates to URLs:
```powershell
python scripts/mousy.py open "notepad"
python scripts/mousy.py open "https://github.com"
```

### 8. Surgical Code Diffs
Replaces target blocks and outputs unified diffs:
```powershell
python scripts/mousy.py edit --path "src/app.py" --target "def old():" --replacement "def new():"
```

---

## Safety Protocol

- **Human-in-the-Loop Confirmation**:
  - Never press "Send" on emails or submit irreversible forms automatically.
  - Type drafts on screen, highlight what was done, and ask the user to confirm.
- **Inspect Before Action**:
  - Always run `observe` first to verify coordinate positions before clicking.
