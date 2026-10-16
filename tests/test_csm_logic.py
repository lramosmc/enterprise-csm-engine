"""
Unit tests for the CSM Logic Engine heuristics and rule processing.
"""

import pytest
from core.models import (
    ServiceDelta,
    DeltaChangeType,
    OutageIncident,
    IncidentSeverity,
    CommunicationItem,
    AlertSeverity,
)
from core.csm_logic import CSMLogicEngine


@pytest.fixture
def logic_engine():
    settings = {
        "sla_thresholds": {
            "max_mttr_hours": 4.0,
            "outage_alert_hours": 2.0,
            "chronic_flapping_threshold": 3,
        }
    }
    return CSMLogicEngine(settings=settings)


def test_evaluate_deltas_new_activation(logic_engine):
    deltas = [
        ServiceDelta(
            service_id="CKT-100",
            customer_name="Apex Cloud",
            change_type=DeltaChangeType.NEW_ACTIVATION,
            timestamp="2026-10-16T08:00:00",
            details="New 10G Wave deployed.",
        )
    ]
    alerts = logic_engine.evaluate_deltas(deltas)
    assert len(alerts) == 1
    assert alerts[0].severity == AlertSeverity.MEDIUM
    assert "New Service Activation" in alerts[0].title


def test_evaluate_deltas_disconnection(logic_engine):
    deltas = [
        ServiceDelta(
            service_id="CKT-200",
            customer_name="Nexus Financial",
            change_type=DeltaChangeType.DISCONNECTION,
            timestamp="2026-10-16T08:00:00",
            details="Circuit turned down.",
        )
    ]
    alerts = logic_engine.evaluate_deltas(deltas)
    assert len(alerts) == 1
    assert alerts[0].severity == AlertSeverity.HIGH
    assert "Disconnection Recorded" in alerts[0].title


def test_evaluate_p1_outage_alert(logic_engine):
    incidents = [
        OutageIncident(
            incident_id="INC-101",
            customer_name="Apex Cloud",
            service_id="CKT-100",
            severity=IncidentSeverity.P1,
            start_time="2026-10-16T06:00:00",
            status="In Progress",
            duration_hours=2.5,
            affected_route="Route North",
        )
    ]
    alerts = logic_engine.evaluate_incidents(incidents)
    assert any(a.severity == AlertSeverity.CRITICAL for a in alerts)


def test_evaluate_sla_breach_detection(logic_engine):
    incidents = [
        OutageIncident(
            incident_id="INC-102",
            customer_name="Horizon Telecom",
            service_id="CKT-300",
            severity=IncidentSeverity.P2,
            start_time="2026-10-16T00:00:00",
            status="Open",
            duration_hours=5.5,  # Exceeds max_mttr_hours of 4.0
            sla_breached=False,
        )
    ]
    alerts = logic_engine.evaluate_incidents(incidents)
    sla_alerts = [a for a in alerts if a.category == "SLA Risk"]
    assert len(sla_alerts) == 1
    assert sla_alerts[0].severity == AlertSeverity.CRITICAL


def test_chronic_circuit_flapping_detection(logic_engine):
    incidents = [
        OutageIncident(
            incident_id=f"INC-{i}",
            customer_name="Quantum Analytics",
            service_id="CKT-FLAP-99",
            severity=IncidentSeverity.P3,
            start_time="2026-10-16T01:00:00",
            status="Closed",
            duration_hours=0.5,
        )
        for i in range(3)
    ]
    alerts = logic_engine.evaluate_incidents(incidents)
    chronic_alerts = [a for a in alerts if a.category == "Chronic Route"]
    assert len(chronic_alerts) == 1
    assert "Chronic Circuit Flapping" in chronic_alerts[0].title


def test_assemble_daily_briefing(logic_engine):
    briefing = logic_engine.assemble_daily_briefing(
        csm_name="Luiz Ramos",
        total_accounts=5,
        deltas=[],
        incidents=[],
        communications=[],
    )
    assert briefing.csm_name == "Luiz Ramos"
    assert briefing.total_accounts_monitored == 5
    assert briefing.open_incidents_count == 0
    assert "# Executive Daily Briefing" in briefing.summary_markdown
