"""
Knowledge Store Adapter for Markdown Vaults and Executive Dashboards.
Persists daily morning briefings, sticky notes, and client strategic dossiers.
"""

import os
from typing import List, Optional
from core.interfaces import IKnowledgeStore
from core.models import DailyBriefing


class MarkdownVaultAdapter(IKnowledgeStore):
    """Adapter for syncing intelligence to markdown vaults and workspace files."""

    def __init__(self, vault_root: str = "output/vault"):
        self.vault_root = vault_root
        os.makedirs(self.vault_root, exist_ok=True)

    def save_daily_briefing(self, briefing: DailyBriefing) -> bool:
        """Saves the executive morning briefing to a dated markdown document."""
        briefings_dir = os.path.join(self.vault_root, "Briefings")
        os.makedirs(briefings_dir, exist_ok=True)

        filename = f"Morning_Briefing_{briefing.briefing_date}.md"
        filepath = os.path.join(briefings_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(briefing.summary_markdown)
            return True
        except Exception:
            return False

    def update_sticky_note(self, action_items: List[str]) -> bool:
        """Updates the quick-access tactical sticky note."""
        sticky_path = os.path.join(self.vault_root, "Tactical_Sticky_Note.md")
        try:
            with open(sticky_path, "w", encoding="utf-8") as f:
                f.write("# Tactical Action Items (Daily Focus)\n\n")
                if not action_items:
                    f.write("No active alerts requiring immediate action.\n")
                else:
                    for item in action_items:
                        f.write(f"- [ ] {item}\n")
            return True
        except Exception:
            return False

    def update_client_intelligence(self, client_id: str, content: str) -> bool:
        """Appends intelligence notes to an individual client file."""
        clients_dir = os.path.join(self.vault_root, "Clients")
        os.makedirs(clients_dir, exist_ok=True)

        filepath = os.path.join(clients_dir, f"{client_id}.md")
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(f"\n\n## Update: {content}\n")
            return True
        except Exception:
            return False
