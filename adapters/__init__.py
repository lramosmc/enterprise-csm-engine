"""
Adapter exports for external systems integration.
"""

from .inventory_adapter import SpreadsheetInventoryAdapter
from .incident_adapter import IncidentFeedAdapter
from .communication_adapter import CommunicationChannelAdapter
from .vault_adapter import MarkdownVaultAdapter

__all__ = [
    "SpreadsheetInventoryAdapter",
    "IncidentFeedAdapter",
    "CommunicationChannelAdapter",
    "MarkdownVaultAdapter",
]
