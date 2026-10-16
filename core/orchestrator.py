"""
Central Orchestrator for the Enterprise CSM Engine.
Coordinates the operational loop: Perception -> Reasoning -> Execution -> Memory.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from .models import (
    Customer,
    DailyBriefing,
    ServiceDelta,
    OutageIncident,
    CommunicationItem,
)
from .interfaces import (
    IInventorySource,
    IIncidentSource,
    ICommunicationChannel,
    IKnowledgeStore,
)
from .csm_logic import CSMLogicEngine


class CSMAgentOrchestrator:
    """Coordinates lifecycle execution across core reasoning and pluggable adapters."""

    def __init__(
        self,
        user_profile: Dict[str, Any],
        clients_config: List[Dict[str, Any]],
        settings: Dict[str, Any],
        inventory_source: IInventorySource,
        incident_source: IIncidentSource,
        communication_channel: ICommunicationChannel,
        knowledge_store: IKnowledgeStore,
        state_dir: str = "state",
    ):
        self.user_profile = user_profile
        self.clients_config = clients_config
        self.settings = settings
        self.inventory_source = inventory_source
        self.incident_source = incident_source
        self.communication_channel = communication_channel
        self.knowledge_store = knowledge_store
        self.state_dir = state_dir
        self.logic_engine = CSMLogicEngine(settings=settings)

    def run_daily_kickoff(
        self,
        client_filter: Optional[str] = None,
        dry_run: bool = False,
    ) -> DailyBriefing:
        """Executes the full perception-to-memory daily morning kickoff cycle."""
        csm_name = self.user_profile.get("csm", {}).get("name", "Enterprise CSM")
        total_accounts = len(self.clients_config)

        # 1. Perception Phase: ingest raw operational state from adapters
        deltas: List[ServiceDelta] = self.inventory_source.load_recent_deltas(
            client_id_or_name=client_filter
        )
        incidents: List[OutageIncident] = self.incident_source.get_open_incidents(
            client_id_or_name=client_filter
        )
        communications: List[CommunicationItem] = (
            self.communication_channel.get_pending_communications(
                client_id_or_name=client_filter
            )
        )

        # 2. Reasoning Phase: heuristic evaluation and executive synthesis
        briefing = self.logic_engine.assemble_daily_briefing(
            csm_name=csm_name,
            total_accounts=total_accounts,
            deltas=deltas,
            incidents=incidents,
            communications=communications,
        )

        # 3. Execution Phase: persist to knowledge store and sync sticky notes
        if not dry_run:
            self.knowledge_store.save_daily_briefing(briefing)
            self.knowledge_store.update_sticky_note(briefing.action_items_sticky)

            # 4. Memory Phase: record execution telemetry to persistent state
            self._update_run_history(briefing)

        return briefing

    def _update_run_history(self, briefing: DailyBriefing) -> None:
        """Persists run metrics to the state tracking store."""
        os.makedirs(self.state_dir, exist_ok=True)
        history_file = os.path.join(self.state_dir, "run_history.json")

        history: Dict[str, Any] = {"runs": []}
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = {"runs": []}

        run_record = {
            "timestamp": datetime.now().isoformat(),
            "briefing_date": briefing.briefing_date,
            "csm": briefing.csm_name,
            "open_incidents_count": briefing.open_incidents_count,
            "critical_alerts_count": briefing.critical_alerts_count,
            "recent_deltas_count": briefing.recent_deltas_count,
            "actions_count": len(briefing.action_items_sticky),
        }

        history.setdefault("runs", []).append(run_record)
        history["last_run"] = run_record

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
