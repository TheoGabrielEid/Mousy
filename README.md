# 🐭 Mousy — Desktop Coworker Plugin for Claude & ChatGPT

<div align="center">

[![Platform](https://img.shields.io/badge/Platform-Windows_11-0078D4?style=flat-square&logo=windows)](https://microsoft.com)
[![Claude Plugin](https://img.shields.io/badge/Claude-Plugin-D97757?style=flat-square&logo=anthropic)](https://claude.ai)
[![ChatGPT Actions](https://img.shields.io/badge/ChatGPT-Custom_Actions-10A37F?style=flat-square&logo=openai)](https://chatgpt.com)
[![Antigravity](https://img.shields.io/badge/Antigravity-Agent_Plugin-4285F4?style=flat-square&logo=google)](https://deepmind.google)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

> **"Claude plugins are installable add-ons that bundle skills, rules, and scripts."**

**Give Claude and ChatGPT eyes on your Windows screen, smooth mouse gliding, and keyboard control.**  
Mousy is a pure plugin add-on that turns your favorite AI models into autonomous desktop pair programmers without any heavy desktop app bloat.

[Quickstart](#-quickstart) • [Claude Plugin Setup](#-claude-plugin-setup) • [ChatGPT Setup](#-chatgpt-setup) • [Full Guide](./GUIDE_CLAUDE_CHATGPT.md) • [Bundled Skills](#-bundled-skills)

</div>

---

## ⚡ Quickstart

Install the Mousy plugin directly into Claude:

```powershell
claude plugin add TheoGabrielEid/Mousy
```

Or clone and run the installer for Antigravity & Gemini agents:

```powershell
git clone https://github.com/TheoGabrielEid/Mousy.git
cd Mousy
pip install -r requirements.txt
python install.py
```

---

## 🔌 Claude Plugin Setup

Claude plugins are installable add-ons that bundle skills and rules.

### Install via Claude CLI:
```powershell
claude plugin add TheoGabrielEid/Mousy
```

### What Claude Can Do:
- **Inspect Display**: `observe` captures high-resolution screenshots for Claude's vision.
- **Glide Cursor**: `glide` moves the pointer with natural human-like ease-in-out interpolation.
- **Click Elements**: `click` coordinates on screen (left, right, double-click).
- **Interactive Typing**: `type` enters characters live into the currently focused window.
- **Surgical Diffs**: `edit` applies clean string replacements and outputs unified color diffs.

---

## 🤖 ChatGPT Setup

1. Open [chatgpt.com](https://chatgpt.com) ➔ **Explore GPTs** ➔ **+ Create**.
2. Under **Configure** ➔ **Actions**, import [`openapi.json`](./openapi.json).
3. If using web ChatGPT, route via local tunnel (`ngrok http 8765`).
4. Save and start chatting!

See [**GUIDE_CLAUDE_CHATGPT.md**](./GUIDE_CLAUDE_CHATGPT.md) for detailed walkthrough.

---

## 🛠️ Bundled Skills & Commands

Mousy bundles CLI utilities inside `scripts/mousy.py`:

| Action | Command | Description |
| :--- | :--- | :--- |
| **Observe** | `python scripts/mousy.py observe --out screen.jpg` | Captures primary screen for vision models. |
| **Glide** | `python scripts/mousy.py glide 500 300` | Smoothly glides cursor with human easing. |
| **Click** | `python scripts/mousy.py click 500 300` | Clicks left, right, or double-click. |
| **Type** | `python scripts/mousy.py type "Draft text"` | Types live into the active application. |
| **Press** | `python scripts/mousy.py press "ctrl+s"` | Presses hotkeys (`ctrl+s`, `win+r`, `enter`). |
| **Scroll** | `python scripts/mousy.py scroll -3` | Scrolls mouse wheel up or down. |
| **Open** | `python scripts/mousy.py open "notepad"` | Launches any application or browser URL. |
| **Edit** | `python scripts/mousy.py edit --path ...` | Surgically edits code files with unified diffs. |

---

## 🛡️ Human-in-the-Loop Safety

- **Confirmation Gate**: Mousy will never submit web forms or send emails automatically without human confirmation. It prepares drafts on screen and signals the user.
- **Non-destructive Diffs**: Edits are performed surgically with unified diffs.

---

## 📄 License

MIT License. Designed for AI agents and pair programming.
