#!/usr/bin/env python3
"""
Context Saver - Automatically saves and restores conversation context.
This script helps maintain project state across sessions.
"""

import os
import sys
import io
import json
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class ContextSaver:
    def __init__(self, project_dir=None):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.context_dir = self.project_dir / ".context"
        self.context_dir.mkdir(exist_ok=True)
        
    def save_session_summary(self, goal, progress, decisions, context_notes):
        """Save session summary to session-summary.md"""
        filepath = self.context_dir / "session-summary.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        content = f"""# Session Summary - {timestamp}

## Current Goal
{goal}

## Progress So Far
{progress}

## Key Decisions
{decisions}

## Important Context
{context_notes}

---

"""
        # Append to existing file or create new one
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
            content = existing + content
        else:
            content = "# Context Session History\n\n" + content
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✓ Session summary saved to {filepath}")
        
    def save_code_changes(self, changes, files_modified, todos):
        """Save code changes to code-changes.md"""
        filepath = self.context_dir / "code-changes.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        content = f"""# Code Changes - {timestamp}

## Latest Changes
{changes}

## Files Modified
{files_modified}

## TODOs / Next Steps
{todos}

---

"""
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
            content = existing + content
        else:
            content = "# Code Changes History\n\n" + content
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✓ Code changes saved to {filepath}")
        
    def save_project_state(self, branch, last_commit, untracked, uncommitted, env_notes, open_issues):
        """Save project state to project-state.md"""
        filepath = self.context_dir / "project-state.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        content = f"""# Project State - {timestamp}

## Working State
- Branch: {branch}
- Last commit: {last_commit}
- Untracked files: {untracked}
- Uncommitted changes: {uncommitted}

## Environment
{env_notes}

## Open Issues
{open_issues}

---

"""
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
            content = existing + content
        else:
            content = "# Project State History\n\n" + content
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✓ Project state saved to {filepath}")
        
    def restore_context(self):
        """Restore context from saved files"""
        context = {}
        
        for filename in ["session-summary.md", "code-changes.md", "project-state.md"]:
            filepath = self.context_dir / filename
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    context[filename] = f.read()
            else:
                context[filename] = None
                
        return context
        
    def quick_save(self, message):
        """Quick save a note to the context"""
        filepath = self.context_dir / "quick-notes.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"## {timestamp}\n{message}\n\n"
        
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
            content = existing + content
        else:
            content = "# Quick Notes\n\n" + content
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✓ Note saved to {filepath}")


def main():
    """CLI interface for context saver"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Save and restore conversation context")
    parser.add_argument("action", choices=["save", "restore", "note"], help="Action to perform")
    parser.add_argument("--project-dir", help="Project directory (default: current)")
    parser.add_argument("--message", help="Quick note message")
    
    args = parser.parse_args()
    
    saver = ContextSaver(args.project_dir)
    
    if args.action == "restore":
        context = saver.restore_context()
        print("\n=== Restored Context ===\n")
        for filename, content in context.items():
            if content:
                print(f"\n--- {filename} ---")
                print(content[:500] + "..." if len(content) > 500 else content)
            else:
                print(f"\n--- {filename} --- (not found)")
                
    elif args.action == "note" and args.message:
        saver.quick_save(args.message)
        
    else:
        print("Usage:")
        print("  context-saver save --project-dir /path/to/project")
        print("  context-saver restore --project-dir /path/to/project")
        print("  context-saver note --message 'Your note here'")


if __name__ == "__main__":
    main()
