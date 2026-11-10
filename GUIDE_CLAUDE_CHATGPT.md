# How to Add Mousy to Claude & ChatGPT

This guide walks you step-by-step through adding the **Mousy Plugin** to Claude and ChatGPT.

---

## 1. Claude Desktop (Windows)

Mousy turns Claude Desktop into an autonomous coworker that can see your screen, click buttons, type text, and edit code.

### Method A: 1-Click Automatic Install
Run the installer from your terminal:
```powershell
python install.py
```
This automatically updates your Claude Desktop configuration file.

### Method B: Manual Configuration
1. Press `Win + R` and open:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
2. Add `"mousy"` inside `"mcpServers"`:
   ```json
   {
     "mcpServers": {
       "mousy": {
         "command": "python",
         "args": [
           "C:\\Users\\theog\\OneDrive\\Desktop\\Coding Projects\\Mousy\\mousy_runner.py"
         ]
       }
     }
   }
   ```
3. Restart **Claude Desktop**.
4. In the bottom bar, click the **Hammer** icon. You will see Mousy's tools:
   - `observe_screen`: Live screen capture
   - `glide_mouse`: Smooth cursor movement
   - `click`: Mouse clicks
   - `type_text`: Keystroke typing
   - `edit_file`: Surgical code diff editing

---

## 2. Claude Code (CLI)

Add Mousy to your Claude Code workspace with a single command:

```powershell
claude mcp add mousy python "C:\Users\theog\OneDrive\Desktop\Coding Projects\Mousy\mousy_runner.py"
```

Verify in Claude Code:
```
> observe my screen and tell me which windows are open
```

---

## 3. ChatGPT (chatgpt.com & Custom GPT Actions)

You can connect ChatGPT directly to Mousy on your PC using Custom GPT Actions.

### Step 1: Open ChatGPT GPT Builder
1. Log in to [chatgpt.com](https://chatgpt.com).
2. Click **Explore GPTs** in the left sidebar.
3. Click the **+ Create** button (top right).

### Step 2: Configure Your Custom GPT
Switch to the **Configure** tab and enter:
- **Name**: `Mousy Desktop Coworker`
- **Description**: `Autonomous pair programmer with live screen vision, mouse gliding, and file editing.`
- **Instructions**:
  ```text
  You are Mousy, an autonomous desktop coworker.
  You interact with the user's live Windows computer through Mousy Actions.
  Always inspect the screen using observe_screen before clicking or typing.
  Draft content live on screen, and always ask the user for confirmation before sending emails or submitting irreversible forms.
  ```

### Step 3: Add Mousy Actions
1. Scroll down to **Actions** and click **Create new action**.
2. Click **Import from URL** or paste the contents of [`openapi.json`](./openapi.json).
3. If using web-based ChatGPT:
   - Start a local tunnel so ChatGPT can communicate with your computer:
     ```powershell
     # Using ngrok:
     ngrok http 8765

     # Or using Cloudflare Tunnel:
     cloudflared tunnel --url http://127.0.0.1:8765
     ```
   - In the OpenAPI schema, set the server URL to your tunnel address (e.g., `https://your-tunnel.ngrok-free.app`).
4. Set **Authentication** to **None** (or API Key if you set one).
5. Click **Save** (choose **Only me** or share with team).

### Step 4: Test in ChatGPT
In your ChatGPT conversation:
- *"Capture my screen and check if my terminal has any errors."*
- *"Glide the mouse to the center and click."*

---

## 4. Antigravity & Gemini Agents

Mousy is fully compatible with Google Antigravity and Gemini CLI:
1. Copy or clone Mousy into:
   ```
   ~/.gemini/config/plugins/mousy/
   ```
   (Or run `python install.py` which does this automatically).
2. The agent automatically discovers:
   - `skills/mousy/SKILL.md`
   - `rules/AGENTS.md`
   - Direct tool executions
