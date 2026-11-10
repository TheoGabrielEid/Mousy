#!/usr/bin/env python3
"""
Mousy Plugin Installer
======================
Installs the Mousy plugin for Claude, ChatGPT, and AI agents.
Plugins are installable add-ons that bundle skills, rules, and scripts.
"""

import os
import sys
import json
import shutil
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    python_exe = sys.executable

    print("\n" + "=" * 60)
    print(" 🐭 Mousy — Desktop Coworker Plugin Installer")
    print("=" * 60 + "\n")

    installed = []

    # 1. Antigravity & Gemini Global Plugin Directory (~/.gemini/config/plugins/mousy)
    try:
        agy_plugin_dir = Path.home() / ".gemini" / "config" / "plugins" / "mousy"
        agy_plugin_dir.mkdir(parents=True, exist_ok=True)
        (agy_plugin_dir / "skills" / "mousy").mkdir(parents=True, exist_ok=True)
        (agy_plugin_dir / "rules").mkdir(parents=True, exist_ok=True)
        (agy_plugin_dir / "scripts").mkdir(parents=True, exist_ok=True)

        shutil.copy2(root / "plugin.json", agy_plugin_dir / "plugin.json")
        shutil.copy2(root / "skills" / "mousy" / "SKILL.md", agy_plugin_dir / "skills" / "mousy" / "SKILL.md")
        shutil.copy2(root / "rules" / "AGENTS.md", agy_plugin_dir / "rules" / "AGENTS.md")
        shutil.copy2(root / "scripts" / "mousy.py", agy_plugin_dir / "scripts" / "mousy.py")

        print(f"✓ Installed Antigravity global plugin: {agy_plugin_dir}")
        installed.append("Antigravity Plugin")
    except Exception as e:
        print(f"✗ Antigravity install notice: {e}")

    # 2. Workspace Plugin (.agents/plugins/mousy)
    try:
        ws_plugin_dir = Path(r"c:\Users\theog\OneDrive\Desktop\Coding Projects\.agents\plugins\mousy")
        ws_plugin_dir.mkdir(parents=True, exist_ok=True)
        (ws_plugin_dir / "skills" / "mousy").mkdir(parents=True, exist_ok=True)
        (ws_plugin_dir / "rules").mkdir(parents=True, exist_ok=True)
        (ws_plugin_dir / "scripts").mkdir(parents=True, exist_ok=True)

        shutil.copy2(root / "plugin.json", ws_plugin_dir / "plugin.json")
        shutil.copy2(root / "skills" / "mousy" / "SKILL.md", ws_plugin_dir / "skills" / "mousy" / "SKILL.md")
        shutil.copy2(root / "rules" / "AGENTS.md", ws_plugin_dir / "rules" / "AGENTS.md")
        shutil.copy2(root / "scripts" / "mousy.py", ws_plugin_dir / "scripts" / "mousy.py")
        print(f"✓ Installed Workspace plugin: {ws_plugin_dir}")
        installed.append("Workspace Plugin")
    except Exception as e:
        print(f"✗ Workspace plugin notice: {e}")

    print("\n" + "-" * 60)
    print(" INSTALLATION COMPLETE!")
    print("-" * 60)
    print("\n1. Claude Code CLI:")
    print(f'   Run: claude plugin add "{root}"')
    print('   Or directly from GitHub: claude plugin add TheoGabrielEid/Mousy')
    print("\n2. ChatGPT:")
    print("   Go to chatgpt.com ➔ Explore GPTs ➔ Create ➔ Actions")
    print(f'   Import the schema from: {root / "openapi.json"}')
    print("\n3. Antigravity & Gemini Agents:")
    print("   The Mousy plugin is already loaded globally and ready to use.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
