"""
Unit tests for the CSMAgentOrchestrator and simulation mode.
"""

from typing import List, Optional
from core.models import ServiceDelta, OutageIncident, CommunicationItem, DailyBriefing
from core.interfaces import IInventorySource, IIncidentSource, ICommunicationChannel, IKnowledgeStore
from core.orchestrator import CSMAgentOrchestrator


class MockInventory(IInventorySource):
    def load_services(self, client_id_or_name=None):
        return []

    def load_recent_deltas(self, client_id_or_name=None):
        return []


class MockIncident(IIncidentSource):
    def get_open_incidents(self, client_id_or_name=None):
        return []

    def get_historical_incidents(self, days=7, client_id_or_name=None):
        return []


class MockCommunication(ICommunicationChannel):
    def get_pending_communications(self, client_id_or_name=None):
        return []


class MockKnowledgeStore(IKnowledgeStore):
    def __init__(self):
        self.saved_briefings = []
        self.sticky_notes = []

    def save_daily_briefing(self, briefing: DailyBriefing) -> bool:
        self.saved_briefings.append(briefing)
        return True

    def update_sticky_note(self, action_items: List[str]) -> bool:
        self.sticky_notes.append(action_items)
        return True

    def update_client_intelligence(self, client_id: str, content: str) -> bool:
        return True


def test_orchestrator_dry_run_does_not_persist(tmp_path):
    store = MockKnowledgeStore()
    orchestrator = CSMAgentOrchestrator(
        user_profile={"csm": {"name": "Test CSM"}},
        clients_config=[{"id": "1", "name": "Client A"}],
        settings={},
        inventory_source=MockInventory(),
        incident_source=MockIncident(),
        communication_channel=MockCommunication(),
        knowledge_store=store,
        state_dir=str(tmp_path),
    )

    briefing = orchestrator.run_daily_kickoff(dry_run=True)
    assert briefing.csm_name == "Test CSM"
    assert len(store.saved_briefings) == 0
    assert len(store.sticky_notes) == 0


def test_orchestrator_normal_run_persists(tmp_path):
    store = MockKnowledgeStore()
    orchestrator = CSMAgentOrchestrator(
        user_profile={"csm": {"name": "Test CSM"}},
        clients_config=[{"id": "1", "name": "Client A"}],
        settings={},
        inventory_source=MockInventory(),
        incident_source=MockIncident(),
        communication_channel=MockCommunication(),
        knowledge_store=store,
        state_dir=str(tmp_path),
    )

    briefing = orchestrator.run_daily_kickoff(dry_run=False)
    assert briefing.csm_name == "Test CSM"
    assert len(store.saved_briefings) == 1
    assert len(store.sticky_notes) == 1
