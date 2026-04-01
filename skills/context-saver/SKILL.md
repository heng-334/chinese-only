---
name: context-saver
description: >
  Automatically saves conversation context, key decisions, code changes, and project state to files
  so they persist across session restarts. MUST be invoked at the START of EVERY new session to check
  for saved context and offer the user a choice to restore or start fresh. Use this skill whenever
  you're working on a project that might span multiple sessions, when you want to preserve important
  context, decisions, or progress, or when you're worried about losing your work due to context clearing.
  Also use when the user mentions "save context", "remember this", "pick up where we left off",
  "session might end", "don't lose this", "new session", "started a new chat", or any situation where
  continuity across sessions would be valuable. Always check for .context/ directory when a session begins.
---

# Context Saver

Automatically preserves conversation context, decisions, and project state across sessions.

## When to Save Context

Save context **proactively** whenever any of these happen:

1. **Important decisions made** - Architecture choices, design decisions, technology selections
2. **Code changes completed** - After finishing a feature, bugfix, or refactoring
3. **User explicitly asks** - "Save this", "remember this", "don't lose this"
4. **Natural checkpoints** - After completing a logical unit of work
5. **Session might end** - User mentions restarting, context clearing, or ending the session
6. **Complex discussions** - Multi-step problem solving where context would be hard to reconstruct

## What to Save

Always save to the project's `.context/` directory (create it if needed):

### 1. `session-summary.md` - Current session overview
```markdown
# Session Summary - YYYY-MM-DD

## Current Goal
What we're trying to accomplish

## Progress So Far
- What's been done
- What's in progress
- What's next

## Key Decisions
- Decision 1 and why
- Decision 2 and why

## Important Context
- Project structure notes
- Non-obvious constraints
- User preferences discovered
```

### 2. `code-changes.md` - Recent code modifications
```markdown
# Code Changes - YYYY-MM-DD

## Latest Changes
- File path: what changed and why
- File path: what changed and why

## Files Modified
- List of all touched files with brief descriptions

## TODOs / Next Steps
- What still needs to be done
```

### 3. `project-state.md` - Project status snapshot
```markdown
# Project State - YYYY-MM-DD

## Working State
- Current branch
- Last commit message
- Untracked files
- Uncommitted changes

## Environment
- Tools/versions being used
- Configuration notes
- Dependencies added

## Open Issues
- Bugs discovered but not fixed
- Questions that need answers
- Risks or concerns
```

## How to Save

1. **Check if `.context/` exists** - Create it if not
2. **Update all three files** - Always keep them in sync
3. **Append to history** - Don't overwrite, add dated entries
4. **Be concise but complete** - Include enough detail to reconstruct context

## Session Start Behavior

**Every time a new session starts, you MUST:**

1. **Check for `.context/` directory** in the current working directory
2. **If context files exist**, present the user with a choice:

   ```
   检测到之前保存的对话上下文：
   
   📁 上次会话摘要 (YYYY-MM-DD):
   - 目标: [简述]
   - 进度: [简述]
   - 下一步: [简述]
   
   请选择：
   1️⃣  恢复之前的对话 - 继续上次的工作
   2️⃣  创建新的对话 - 清除上下文，重新开始
   
   (回复 1 或 2)
   ```

3. **If user chooses "恢复" (Restore):**
   - Read all three `.context/` files
   - Summarize the previous state
   - Continue from where things left off
   - Update the context files with current session info

4. **If user chooses "新建" (New):**
   - Ask for confirmation: "确定要清除之前的上下文吗？这将无法恢复之前的工作进度。"
   - If confirmed, archive old context (optional) or clear the files
   - Start fresh with empty context
   - Save new session info

5. **If no `.context/` directory exists:**
   - Start normally, no prompt needed
   - Begin saving context as work progresses

## How to Restore

When user chooses to restore context:

1. **Read all three files** to understand previous state
2. **Acknowledge what was saved** and confirm you can continue
3. **Update the files** with current session info

## Automation Rules

- **Save after every meaningful change** - Don't wait for the user to ask
- **Save before potentially destructive operations** - So you can recover if something goes wrong
- **Save at natural breakpoints** - When switching topics or completing tasks
- **Keep it current** - Old entries are fine, but the "current" section should always be up to date
- **Use clear timestamps** - So you can track when things happened

## Example Workflow

```
User: "Let's add authentication to the app"
[Work happens...]
[Feature complete]
→ SAVE: Update all three .context/ files with what was done

User: "I might need to restart my computer"
→ SAVE: Final checkpoint with current state

[Session ends]

[New session starts]
→ RESTORE: Read .context/ files
→ "I see we were working on authentication. Last time we completed login flow and middleware. 
   The next step was adding session management. Want to continue?"
```

## Proactive Saving

Don't wait to be asked. Save context whenever it would be helpful:

- After explaining a complex problem
- After making architecture decisions  
- After completing any non-trivial code change
- When you notice the conversation has reached a milestone
- Before running commands that might change state

The goal is that **no context is ever lost**. If a session ends unexpectedly, the next session should be able to pick up exactly where things left off.
