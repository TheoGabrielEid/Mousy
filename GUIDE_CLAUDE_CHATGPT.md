# How to Add the Mousy Plugin to Claude & ChatGPT

> **"Claude plugins are installable add-ons that bundle skills, rules, and scripts."**

Mousy is a pure plugin that gives Claude and ChatGPT direct eyes on your Windows screen, smooth mouse gliding, live typing, and surgical code editing.

---

## 1. Claude (Claude Code & Claude CLI)

### Installation
Install Mousy directly into Claude with the official plugin command:

```powershell
claude plugin add TheoGabrielEid/Mousy
```

*(Or from a local cloned directory:)*
```powershell
claude plugin add "C:\Users\theog\OneDrive\Desktop\Coding Projects\Mousy"
```

### How Claude Uses the Mousy Plugin
Once installed, Claude loads Mousy's bundled skills and rules automatically:
- **Screen Vision**: Claude executes `observe` to view your screen.
- **Mouse Control**: Claude glides your pointer and clicks buttons with human easing.
- **Interactive Typing**: Claude types drafts live into your active window.
- **Code Diffs**: Claude edits files with surgical diffs.

You can simply tell Claude:
```
> observe my screen and review the code open in VS Code
> glide the mouse to the center and click
> draft a polite email response in my active browser tab
```

---

## 2. ChatGPT (chatgpt.com & Custom GPTs)

You can connect ChatGPT to Mousy using Custom GPT Actions.

### Step 1: Open ChatGPT GPT Builder
1. Go to [chatgpt.com](https://chatgpt.com).
2. Click **Explore GPTs** in the sidebar.
3. Click **+ Create** (top right).

### Step 2: Configure the Custom GPT
In the **Configure** tab:
- **Name**: `Mousy Desktop Coworker`
- **Description**: `Autonomous pair programmer plugin with live screen vision and mouse control.`
- **Instructions**:
  ```text
  You are Mousy, an autonomous desktop coworker plugin.
  You interact with the user's live Windows computer through the bundled Mousy actions.
  Always inspect the screen using observe_screen before clicking or typing.
  Draft content live on screen, and always ask the user for confirmation before sending emails or submitting irreversible forms.
  ```

### Step 3: Add Mousy Plugin Actions
1. Under **Actions**, click **Create new action**.
2. Click **Import from URL** or paste the contents of [`openapi.json`](./openapi.json).
3. If using web-based ChatGPT, route traffic through a secure local tunnel:
   ```powershell
   ngrok http 8765
   ```
   Set the server URL in `openapi.json` to your tunnel address.
4. Click **Save**.

Now ChatGPT on web or mobile can see your Windows desktop and control the mouse!

---

## 3. Antigravity & Gemini Agents

Run the 1-click installer:
```powershell
python install.py
```
This automatically registers Mousy into `~/.gemini/config/plugins/mousy/`.
The agent will discover `skills/mousy/SKILL.md` and `rules/AGENTS.md` automatically.
