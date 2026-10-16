"""
Abstract Interfaces and Contracts (Ports & Adapters) for the CSM Agent Engine.
Enables total decoupling between business reasoning and external enterprise data systems.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import (
    Customer,
    Service,
    ServiceDelta,
    OutageIncident,
    CommunicationItem,
    DailyBriefing,
)


class IInventorySource(ABC):
    """Port for retrieving active services and inventory state changes."""

    @abstractmethod
    def load_services(self, client_id_or_name: Optional[str] = None) -> List[Service]:
        """Loads active service records."""
        pass

    @abstractmethod
    def load_recent_deltas(self, client_id_or_name: Optional[str] = None) -> List[ServiceDelta]:
        """Loads recent deltas including activations, cancellations, and bandwidth adjustments."""
        pass


class IIncidentSource(ABC):
    """Port for querying operational tickets, service outages, and SLA metrics."""

    @abstractmethod
    def get_open_incidents(self, client_id_or_name: Optional[str] = None) -> List[OutageIncident]:
        """Retrieves active or ongoing operational incidents."""
        pass

    @abstractmethod
    def get_historical_incidents(
        self, days: int = 7, client_id_or_name: Optional[str] = None
    ) -> List[OutageIncident]:
        """Retrieves recent incident history for MTTR, chronic flapping, and SLA trend analysis."""
        pass


class ICommunicationChannel(ABC):
    """Port for reading client interactions and pending operator follow-ups."""

    @abstractmethod
    def get_pending_communications(
        self, client_id_or_name: Optional[str] = None
    ) -> List[CommunicationItem]:
        """Retrieves communications and requests awaiting CSM response or action."""
        pass


class IKnowledgeStore(ABC):
    """Port for storing and syncing executive briefings, action items, and client dossiers."""

    @abstractmethod
    def save_daily_briefing(self, briefing: DailyBriefing) -> bool:
        """Persists the consolidated morning briefing document."""
        pass

    @abstractmethod
    def update_sticky_note(self, action_items: List[str]) -> bool:
        """Updates the quick-access tactical action items sticky note."""
        pass

    @abstractmethod
    def update_client_intelligence(self, client_id: str, content: str) -> bool:
        """Updates the individual strategic client dossier."""
        pass
