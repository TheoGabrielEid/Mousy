#!/usr/bin/env python3
"""
Mousy Plugin Installer
======================
Automatically installs and registers Mousy as a native plugin for:
1. Claude Desktop (auto-writes to claude_desktop_config.json)
2. Antigravity & Gemini Agents (~/.gemini/config/plugins/mousy)
3. Claude Code CLI instructions
4. ChatGPT Custom GPT Action instructions
"""

import os
import sys
import json
import shutil
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    runner_path = root / "mousy_runner.py"
    python_exe = sys.executable

    print("\n" + "=" * 60)
    print(" 🐭 Mousy — Desktop Coworker Plugin Installer")
    print("=" * 60 + "\n")

    installed = []

    # 1. Antigravity Global Plugin Directory
    try:
        agy_plugin_dir = Path.home() / ".gemini" / "config" / "plugins" / "mousy"
        agy_plugin_dir.mkdir(parents=True, exist_ok=True)
        (agy_plugin_dir / "skills" / "mousy").mkdir(parents=True, exist_ok=True)
        (agy_plugin_dir / "rules").mkdir(parents=True, exist_ok=True)

        shutil.copy2(root / "plugin.json", agy_plugin_dir / "plugin.json")
        shutil.copy2(root / "skills" / "mousy" / "SKILL.md", agy_plugin_dir / "skills" / "mousy" / "SKILL.md")
        shutil.copy2(root / "rules" / "AGENTS.md", agy_plugin_dir / "rules" / "AGENTS.md")
        shutil.copy2(runner_path, agy_plugin_dir / "mousy_runner.py")

        mcp_cfg = {
            "mcpServers": {
                "mousy": {
                    "command": python_exe,
                    "args": [str(agy_plugin_dir / "mousy_runner.py")]
                }
            }
        }
        (agy_plugin_dir / "mcp_config.json").write_text(json.dumps(mcp_cfg, indent=2), encoding="utf-8")
        print(f"✓ Installed Antigravity global plugin at: {agy_plugin_dir}")
        installed.append("Antigravity Plugin")
    except Exception as e:
        print(f"✗ Antigravity install notice: {e}")

    # 2. Claude Desktop Integration
    try:
        claude_dir = Path(os.environ.get("APPDATA", "")) / "Claude"
        claude_cfg_file = claude_dir / "claude_desktop_config.json"
        if claude_dir.exists():
            cfg_data = {}
            if claude_cfg_file.exists():
                try:
                    cfg_data = json.loads(claude_cfg_file.read_text(encoding="utf-8"))
                except Exception:
                    cfg_data = {}
            if "mcpServers" not in cfg_data:
                cfg_data["mcpServers"] = {}
            
            cfg_data["mcpServers"]["mousy"] = {
                "command": python_exe,
                "args": [str(runner_path)]
            }
            claude_cfg_file.write_text(json.dumps(cfg_data, indent=2), encoding="utf-8")
            print(f"✓ Registered in Claude Desktop: {claude_cfg_file}")
            installed.append("Claude Desktop")
        else:
            print("ℹ Claude Desktop folder not found, skipping Claude Desktop auto-registration.")
    except Exception as e:
        print(f"✗ Claude Desktop install notice: {e}")

    print("\n" + "-" * 60)
    print(" INSTALLATION COMPLETE!")
    print("-" * 60)
    print("\n1. Claude Desktop:")
    print("   Restart Claude Desktop. You will see the hammer icon with Mousy tools.")
    print("\n2. Claude Code CLI:")
    print(f'   Run: claude mcp add mousy "{python_exe}" "{runner_path}"')
    print("\n3. ChatGPT:")
    print("   Go to chatgpt.com ➔ Explore GPTs ➔ Create ➔ Actions")
    print(f'   Import the schema from: {root / "openapi.json"}')
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
