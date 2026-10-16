"""
Pure Customer Success Management (CSM) domain logic.
Completely agnostic of external vendors, platforms, and proprietary tools.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import (
    Customer,
    Service,
    ServiceDelta,
    DeltaChangeType,
    OutageIncident,
    IncidentSeverity,
    CommunicationItem,
    CSMAlert,
    AlertSeverity,
    DailyBriefing,
)


class CSMLogicEngine:
    """Cognitive reasoning and heuristic rule engine for enterprise account governance."""

    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        self.settings = settings or {}
        sla_conf = self.settings.get("sla_thresholds", {})
        self.max_mttr_hours = sla_conf.get("max_mttr_hours", 4.0)
        self.outage_alert_hours = sla_conf.get("outage_alert_hours", 2.0)
        self.chronic_flapping_threshold = sla_conf.get("chronic_flapping_threshold", 3)

    def evaluate_deltas(self, deltas: List[ServiceDelta]) -> List[CSMAlert]:
        """Analyzes inventory deltas and emits proactive lifecycle alerts."""
        alerts: List[CSMAlert] = []
        for d in deltas:
            if d.change_type == DeltaChangeType.NEW_ACTIVATION:
                alerts.append(
                    CSMAlert(
                        alert_id=f"delta-act-{d.service_id}",
                        client_name=d.customer_name,
                        severity=AlertSeverity.MEDIUM,
                        category="Inventory Delta",
                        title=f"New Service Activation: Circuit {d.service_id}",
                        description=f"New service activated for {d.customer_name}. Details: {d.details}",
                        recommended_action="Confirm customer acceptance receipt and validate billing initiation date.",
                    )
                )
            elif d.change_type == DeltaChangeType.DISCONNECTION:
                alerts.append(
                    CSMAlert(
                        alert_id=f"delta-disc-{d.service_id}",
                        client_name=d.customer_name,
                        severity=AlertSeverity.HIGH,
                        category="Inventory Delta",
                        title=f"Disconnection Recorded: Circuit {d.service_id}",
                        description=f"Service cancellation recorded for {d.customer_name}. {d.details}",
                        recommended_action="Coordinate immediately with Account Executive to review churn risk and contract terms.",
                    )
                )
            elif d.change_type == DeltaChangeType.BANDWIDTH_CHANGE:
                alerts.append(
                    CSMAlert(
                        alert_id=f"delta-bw-{d.service_id}",
                        client_name=d.customer_name,
                        severity=AlertSeverity.LOW,
                        category="Inventory Delta",
                        title=f"Bandwidth Adjustment: Circuit {d.service_id}",
                        description=f"Bandwidth updated from '{d.old_value}' to '{d.new_value}'. {d.details}",
                        recommended_action="Verify service order addendum execution and repository storage.",
                    )
                )
        return alerts

    def evaluate_incidents(self, incidents: List[OutageIncident]) -> List[CSMAlert]:
        """Analyzes operational tickets, active outages, and SLA breach risks."""
        alerts: List[CSMAlert] = []
        circuit_counts: Dict[str, int] = {}

        for inc in incidents:
            circuit_counts[inc.service_id] = circuit_counts.get(inc.service_id, 0) + 1

            # Active incidents check
            if inc.status in ["Open", "In Progress"]:
                duration_str = f"{inc.duration_hours:.1f}h" if inc.duration_hours else "pending measurement"
                if inc.severity == IncidentSeverity.P1:
                    alerts.append(
                        CSMAlert(
                            alert_id=f"outage-p1-{inc.incident_id}",
                            client_name=inc.customer_name,
                            severity=AlertSeverity.CRITICAL,
                            category="Outage",
                            title=f"Active P1 Outage: {inc.customer_name} (Ticket #{inc.incident_id})",
                            description=f"Circuit {inc.service_id} experiencing total outage for {duration_str}. Route: {inc.affected_route or 'N/A'}.",
                            recommended_action="Issue proactive executive notification and escalate with Tier 2/3 engineering.",
                        )
                    )
                elif inc.severity == IncidentSeverity.P2:
                    alerts.append(
                        CSMAlert(
                            alert_id=f"degraded-p2-{inc.incident_id}",
                            client_name=inc.customer_name,
                            severity=AlertSeverity.HIGH,
                            category="Outage",
                            title=f"Degraded Service (P2): {inc.customer_name} (Ticket #{inc.incident_id})",
                            description=f"Circuit {inc.service_id} degraded or redundancy lost for {duration_str}.",
                            recommended_action="Monitor restoration milestone updates and alert field operations.",
                        )
                    )

            # SLA Breach evaluation
            if inc.sla_breached or (inc.duration_hours and inc.duration_hours >= self.max_mttr_hours):
                alerts.append(
                    CSMAlert(
                        alert_id=f"sla-breach-{inc.incident_id}",
                        client_name=inc.customer_name,
                        severity=AlertSeverity.CRITICAL,
                        category="SLA Risk",
                        title=f"SLA Breach Flagged: Ticket #{inc.incident_id}",
                        description=f"Ticket reached {inc.duration_hours or 'N/A'} hours, exceeding the standard {self.max_mttr_hours}h MTTR threshold.",
                        recommended_action="Prepare Root Cause Analysis (RCA) package and review SLA penalty credit clauses.",
                    )
                )

        # Chronic circuit recurrence check
        for service_id, count in circuit_counts.items():
            if count >= self.chronic_flapping_threshold:
                # Find matching customer name
                matching = next((i for i in incidents if i.service_id == service_id), None)
                client_name = matching.customer_name if matching else "Enterprise Account"
                alerts.append(
                    CSMAlert(
                        alert_id=f"chronic-{service_id}",
                        client_name=client_name,
                        severity=AlertSeverity.HIGH,
                        category="Chronic Route",
                        title=f"Chronic Circuit Flapping: Circuit {service_id}",
                        description=f"Circuit recorded {count} distinct incident events in recent inspection window.",
                        recommended_action="Request proactive optical route diagnostic and physical infrastructure audit.",
                    )
                )

        return alerts

    def evaluate_communications(self, communications: List[CommunicationItem]) -> List[CSMAlert]:
        """Identifies pending client requests requiring follow-up."""
        alerts: List[CSMAlert] = []
        for comm in communications:
            if comm.urgency == "Urgent" or comm.action_required:
                alerts.append(
                    CSMAlert(
                        alert_id=f"comm-{comm.item_id}",
                        client_name=comm.client_name,
                        severity=AlertSeverity.HIGH if comm.urgency == "Urgent" else AlertSeverity.MEDIUM,
                        category="Client Follow-up",
                        title=f"Pending Client Response: {comm.client_name}",
                        description=f"Subject: '{comm.subject}'. Sender: {comm.sender}. Summary: {comm.summary}",
                        recommended_action="Draft response or dispatch request to dedicated technical account owner.",
                    )
                )
        return alerts

    def assemble_daily_briefing(
        self,
        csm_name: str,
        total_accounts: int,
        deltas: List[ServiceDelta],
        incidents: List[OutageIncident],
        communications: List[CommunicationItem],
    ) -> DailyBriefing:
        """Assembles and synthesizes the full executive daily briefing."""
        all_alerts: List[CSMAlert] = []
        all_alerts.extend(self.evaluate_incidents(incidents))
        all_alerts.extend(self.evaluate_deltas(deltas))
        all_alerts.extend(self.evaluate_communications(communications))

        # Severity sorting order
        order = {
            AlertSeverity.CRITICAL: 0,
            AlertSeverity.HIGH: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.LOW: 3,
        }
        all_alerts.sort(key=lambda a: order.get(a.severity, 99))

        open_incidents = [i for i in incidents if i.status in ["Open", "In Progress"]]
        critical_alerts = [a for a in all_alerts if a.severity == AlertSeverity.CRITICAL]

        # Prioritized action items for sticky notes
        sticky_actions: List[str] = []
        for alert in all_alerts[:8]:
            tag = f"[{alert.severity.value}]"
            sticky_actions.append(f"{tag} {alert.client_name}: {alert.recommended_action}")

        # Generate Executive Markdown Document
        briefing_date = datetime.now().strftime("%Y-%m-%d")
        summary_md = self._build_markdown_summary(
            briefing_date=briefing_date,
            csm_name=csm_name,
            total_accounts=total_accounts,
            open_incidents=open_incidents,
            critical_alerts=critical_alerts,
            alerts=all_alerts,
            deltas=deltas,
            communications=communications,
            sticky_actions=sticky_actions,
        )

        return DailyBriefing(
            briefing_date=briefing_date,
            csm_name=csm_name,
            total_accounts_monitored=total_accounts,
            open_incidents_count=len(open_incidents),
            critical_alerts_count=len(critical_alerts),
            recent_deltas_count=len(deltas),
            alerts=all_alerts,
            recent_deltas=deltas,
            open_incidents=open_incidents,
            pending_communications=communications,
            action_items_sticky=sticky_actions,
            summary_markdown=summary_md,
        )

    def _build_markdown_summary(
        self,
        briefing_date: str,
        csm_name: str,
        total_accounts: int,
        open_incidents: List[OutageIncident],
        critical_alerts: List[CSMAlert],
        alerts: List[CSMAlert],
        deltas: List[ServiceDelta],
        communications: List[CommunicationItem],
        sticky_actions: List[str],
    ) -> str:
        lines: List[str] = [
            f"# Executive Daily Briefing: {briefing_date}",
            f"**Customer Success Manager:** {csm_name}",
            f"**Monitored Accounts:** {total_accounts} | **Active Outages:** {len(open_incidents)} | **Critical Alerts:** {len(critical_alerts)}",
            "",
            "## 1. Priority Tactical Actions",
        ]

        if not sticky_actions:
            lines.append("No critical action items detected. Portfolio operating within standard thresholds.")
        else:
            for act in sticky_actions:
                lines.append(f"- {act}")

        lines.extend(["", "## 2. Active Outages & SLA Risks"])
        if not open_incidents:
            lines.append("Zero active service-impacting outages.")
        else:
            for inc in open_incidents:
                dur = f"{inc.duration_hours:.1f}h" if inc.duration_hours else "N/A"
                lines.append(
                    f"- **[{inc.severity.value}] {inc.customer_name}** (Ticket #{inc.incident_id}): Circuit `{inc.service_id}`. Route: {inc.affected_route or 'N/A'}. Duration: {dur}."
                )

        lines.extend(["", "## 3. Inventory Deltas"])
        if not deltas:
            lines.append("No new service state changes recorded in current cycle.")
        else:
            for d in deltas:
                lines.append(f"- **{d.change_type.value}** ({d.customer_name}): Circuit `{d.service_id}`. {d.details}")

        lines.extend(["", "## 4. Pending Communications & Escalations"])
        if not communications:
            lines.append("No pending communications requiring immediate intervention.")
        else:
            for c in communications:
                urg = f"[{c.urgency}]" if c.urgency == "Urgent" else ""
                lines.append(f"- {urg} **{c.client_name}** from `{c.sender}`: {c.subject}")

        return "\n".join(lines)
