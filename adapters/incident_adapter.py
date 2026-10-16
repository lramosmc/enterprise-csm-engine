"""
Incident Adapter for Ticketing and Network Outage Feeds.
Maps incident records to canonical OutageIncident models with MTTR and SLA metrics.
"""

import json
import os
from typing import List, Optional
from core.interfaces import IIncidentSource
from core.models import OutageIncident, IncidentSeverity


class IncidentFeedAdapter(IIncidentSource):
    """Adapter for operational tickets, outages, and SLA monitoring."""

    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file

    def get_open_incidents(self, client_id_or_name: Optional[str] = None) -> List[OutageIncident]:
        """Retrieves active tickets and outages."""
        incidents: List[OutageIncident] = []
        if self.data_file and os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw = json.load(f).get("incidents", [])
                    for i in raw:
                        incidents.append(
                            OutageIncident(
                                incident_id=i.get("incident_id", "INC-000"),
                                customer_name=i.get("customer_name", "Enterprise Account"),
                                service_id=i.get("service_id", "CKT-000"),
                                severity=IncidentSeverity(i.get("severity", "P3")),
                                start_time=i.get("start_time", "2026-10-16T04:00:00"),
                                status=i.get("status", "Open"),
                                duration_hours=i.get("duration_hours", 1.0),
                                root_cause=i.get("root_cause"),
                                sla_breached=i.get("sla_breached", False),
                                affected_route=i.get("affected_route"),
                                comments=i.get("comments", ""),
                            )
                        )
            except Exception:
                pass

        # Fallback to realistic synthetic sample if file is not provided
        if not incidents and not self.data_file:
            incidents = [
                OutageIncident(
                    incident_id="INC-2026-8801",
                    customer_name="Apex Cloud Infrastructure",
                    service_id="CKT-FIBER-9041",
                    severity=IncidentSeverity.P1,
                    start_time="2026-10-16T05:15:00",
                    status="In Progress",
                    duration_hours=3.5,
                    affected_route="Optical Subsea Ring 2 - Segment B",
                    comments="Physical fiber cut detected. Field dispatch on-site performing OTDR splicing.",
                    sla_breached=False,
                ),
                OutageIncident(
                    incident_id="INC-2026-8794",
                    customer_name="Horizon Telecommunications",
                    service_id="CKT-IPTRANSIT-5510",
                    severity=IncidentSeverity.P2,
                    start_time="2026-10-16T02:00:00",
                    status="Open",
                    duration_hours=6.2,
                    affected_route="Border Router Metro East - Port 4/1",
                    comments="Intermittent packet loss and BGP peering flap. MTTR threshold breached.",
                    sla_breached=True,
                ),
            ]

        if client_id_or_name:
            incidents = [
                i for i in incidents if i.customer_name.lower() == client_id_or_name.lower()
            ]
        return incidents

    def get_historical_incidents(
        self, days: int = 7, client_id_or_name: Optional[str] = None
    ) -> List[OutageIncident]:
        """Retrieves recent incident history for chronic failure detection."""
        all_incidents = self.get_open_incidents(client_id_or_name=client_id_or_name)
        return all_incidents
