"""
Communication Channel Adapter.
Inspects email threads and client communications awaiting operator response.
"""

import json
import os
from typing import List, Optional
from core.interfaces import ICommunicationChannel
from core.models import CommunicationItem


class CommunicationChannelAdapter(ICommunicationChannel):
    """Adapter for reading client interactions and escalation threads."""

    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file

    def get_pending_communications(
        self, client_id_or_name: Optional[str] = None
    ) -> List[CommunicationItem]:
        """Retrieves messages requiring operator attention."""
        items: List[CommunicationItem] = []
        if self.data_file and os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw = json.load(f).get("communications", [])
                    for c in raw:
                        items.append(
                            CommunicationItem(
                                item_id=c.get("item_id", "COMM-001"),
                                client_name=c.get("client_name", "Enterprise Account"),
                                sender=c.get("sender", "client@enterprise.com"),
                                subject=c.get("subject", "Status Inquiry"),
                                timestamp=c.get("timestamp", "2026-10-16T08:00:00"),
                                summary=c.get("summary", ""),
                                action_required=c.get("action_required", False),
                                urgency=c.get("urgency", "Normal"),
                                client_domain=c.get("client_domain"),
                            )
                        )
            except Exception:
                pass

        # Fallback to realistic synthetic sample if file is not supplied
        if not items and not self.data_file:
            items = [
                CommunicationItem(
                    item_id="COMM-1092",
                    client_name="Apex Cloud Infrastructure",
                    sender="noc-lead@apexcloud.internal",
                    subject="URGENT: Executive escalation regarding Subsea Ring 2 restoration timeline",
                    timestamp="2026-10-16T07:45:00",
                    summary="Customer Director of Infrastructure requesting hourly restoration updates and engineering incident report.",
                    action_required=True,
                    urgency="Urgent",
                    client_domain="apexcloud.internal",
                ),
                CommunicationItem(
                    item_id="COMM-1088",
                    client_name="Nexus Financial Systems",
                    sender="procurement@nexusfinancial.com",
                    subject="Decommission confirmation for CKT-ETH-1120 billing stop",
                    timestamp="2026-10-15T20:10:00",
                    summary="Inquiring whether billing has officially stopped for the turned-down circuit.",
                    action_required=True,
                    urgency="Normal",
                    client_domain="nexusfinancial.com",
                ),
            ]

        if client_id_or_name:
            items = [
                item for item in items if item.client_name.lower() == client_id_or_name.lower()
            ]
        return items
