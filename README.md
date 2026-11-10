# 🐭 Mousy — Desktop Coworker Plugin for Claude & ChatGPT

<div align="center">

[![Platform](https://img.shields.io/badge/Platform-Windows_11-0078D4?style=flat-square&logo=windows)](https://microsoft.com)
[![Claude Desktop](https://img.shields.io/badge/Claude_Desktop-Plugin-D97757?style=flat-square&logo=anthropic)](https://claude.ai)
[![ChatGPT Actions](https://img.shields.io/badge/ChatGPT-Custom_Actions-10A37F?style=flat-square&logo=openai)](https://chatgpt.com)
[![Antigravity](https://img.shields.io/badge/Antigravity-Agent_Plugin-4285F4?style=flat-square&logo=google)](https://deepmind.google)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**Give Claude and ChatGPT eyes on your screen, a mouse pointer to guide, and keyboard control.**  
Mousy is a pure, lightweight plugin that turns your favorite AI models into autonomous desktop pair programmers.

[Quickstart](#-quickstart) • [Claude Desktop Setup](#-claude-desktop-setup) • [ChatGPT Setup](#-chatgpt-setup) • [Setup Guide](./GUIDE_CLAUDE_CHATGPT.md) • [Capabilities](#-plugin-capabilities)

</div>

---

## ⚡ Quickstart

Clone the repository and run the 1-click installer:

```powershell
git clone https://github.com/TheoGabrielEid/Mousy.git
cd Mousy
pip install -r requirements.txt
python install.py
```

`install.py` automatically configures **Claude Desktop** and **Antigravity**!

---

## 🔌 Claude Desktop Setup

1. Open `%APPDATA%\Claude\claude_desktop_config.json`
2. Add `"mousy"`:

```json
{
  "mcpServers": {
    "mousy": {
      "command": "python",
      "args": [
        "C:\\path\\to\\Mousy\\mousy_runner.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop. The hammer icon will show all Mousy tools.

---

## 🤖 ChatGPT Setup

1. Go to [chatgpt.com](https://chatgpt.com) ➔ **Explore GPTs** ➔ **+ Create**.
2. Under **Configure** ➔ **Actions**, import [`openapi.json`](./openapi.json).
3. If using web ChatGPT, route via local tunnel (`ngrok http 8765`).
4. Save and start chatting!

See [**GUIDE_CLAUDE_CHATGPT.md**](./GUIDE_CLAUDE_CHATGPT.md) for full instructions.

---

## 🛠️ Plugin Capabilities

| Tool | Action |
| :--- | :--- |
| `observe_screen` | Captures primary screen for vision models (returns resolution and base64 JPEG). |
| `glide_mouse` | Moves cursor with smooth ease-in-out quadratic interpolation. |
| `click` | Left click, right click, or double click at coordinates. |
| `type_text` | Types text directly into the focused application character-by-character. |
| `press_key` | Presses hotkeys (`ctrl+s`, `win+r`, `enter`, `alt+tab`, etc.). |
| `scroll` | Scrolls mouse wheel up or down. |
| `open_app` | Launches any program or opens a URL in default browser. |
| `edit_file` | Surgically edits code files and returns clean unified diffs. |
| `read_file` | Safely inspects file contents. |
| `write_file` | Writes or creates files. |

---

## 🛡️ Safety Architecture

- **Human Confirmation Gate**: Mousy will never submit web forms or press "Send" on emails automatically. It prepares the draft on screen and asks for your confirmation.
- **Non-destructive Editing**: Code changes are performed with surgical string replacements and unified diffs.

---

## 📄 License

MIT License. Designed for AI agents and pair programming.
