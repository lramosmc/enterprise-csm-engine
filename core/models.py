"""
Canonical and agnostic data models for Customer Success Management (CSM).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class IncidentSeverity(str, Enum):
    P1 = "P1"  # Complete service outage or critical circuit down
    P2 = "P2"  # Severe degradation, latency spike, or loss of redundancy
    P3 = "P3"  # Non-service impacting inquiry or minor configuration event


class AlertSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class DeltaChangeType(str, Enum):
    NEW_ACTIVATION = "NEW_ACTIVATION"
    DISCONNECTION = "DISCONNECTION"
    BANDWIDTH_CHANGE = "BANDWIDTH_CHANGE"
    STATUS_CHANGE = "STATUS_CHANGE"
    PARAMETER_CHANGE = "PARAMETER_CHANGE"
    OTHER = "OTHER"


@dataclass
class Customer:
    id: str
    name: str
    vertical: str
    domains: List[str] = field(default_factory=list)
    priority: str = "High"
    scope: str = "Global Infrastructure"
    account_executives: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Service:
    service_id: str
    customer_id: str
    customer_name: str
    product_name: str
    bandwidth: str
    status: str
    activation_date: Optional[str] = None
    mrc: Optional[float] = None
    currency: str = "USD"
    site_origin: Optional[str] = None
    site_destination: Optional[str] = None
    contract_term: Optional[str] = None
    service_order: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceDelta:
    service_id: str
    customer_name: str
    change_type: DeltaChangeType
    timestamp: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    details: str = ""
    is_fiber: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OutageIncident:
    incident_id: str
    customer_name: str
    service_id: str
    severity: IncidentSeverity
    start_time: str
    status: str  # "Open", "In Progress", "Resolved", "Closed"
    end_time: Optional[str] = None
    duration_hours: Optional[float] = None
    root_cause: Optional[str] = None
    sla_breached: bool = False
    affected_route: Optional[str] = None
    comments: str = ""


@dataclass
class CommunicationItem:
    item_id: str
    client_name: str
    sender: str
    subject: str
    timestamp: str
    summary: str
    action_required: bool = False
    urgency: str = "Normal"  # "Normal", "Urgent"
    client_domain: Optional[str] = None


@dataclass
class CSMAlert:
    alert_id: str
    client_name: str
    severity: AlertSeverity
    category: str  # "Outage", "Inventory Delta", "SLA Risk", "Follow-up"
    title: str
    description: str
    recommended_action: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DailyBriefing:
    briefing_date: str
    csm_name: str
    total_accounts_monitored: int
    open_incidents_count: int
    critical_alerts_count: int
    recent_deltas_count: int
    alerts: List[CSMAlert] = field(default_factory=list)
    recent_deltas: List[ServiceDelta] = field(default_factory=list)
    open_incidents: List[OutageIncident] = field(default_factory=list)
    pending_communications: List[CommunicationItem] = field(default_factory=list)
    action_items_sticky: List[str] = field(default_factory=list)
    summary_markdown: str = ""
