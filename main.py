"""
Main Application Entrypoint for Enterprise CSM Engine.
Executes the Daily Morning Kickoff and proactive Customer Success intelligence.
"""

import os
import sys
import argparse
import json
import yaml
from typing import Dict, Any, List

# Ensure UTF-8 output encoding across Windows consoles
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core import (
    CSMAgentOrchestrator,
    DailyBriefing,
)
from adapters import (
    SpreadsheetInventoryAdapter,
    IncidentFeedAdapter,
    CommunicationChannelAdapter,
    MarkdownVaultAdapter,
)


def load_yaml_file(filepath: str) -> Any:
    """Safely loads and parses a YAML configuration file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise CSM Engine: Autonomous Daily Kickoff and Global Account Governance."
    )
    parser.add_argument(
        "--client",
        type=str,
        default=None,
        help="Filter execution for a specific account (e.g., 'Apex Cloud Infrastructure').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute analysis in simulation mode without writing changes to disk or state history.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display summary metrics from the latest recorded execution in state/run_history.json.",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        default="config",
        help="Directory containing YAML configuration files.",
    )

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, args.config_dir)
    state_dir = os.path.join(base_dir, "state")
    data_dir = os.path.join(base_dir, "data")

    # Status check mode
    if args.status:
        history_file = os.path.join(state_dir, "run_history.json")
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            last_run = data.get("last_run")
            if last_run:
                print("\n==================================================")
                print("       ENTERPRISE CSM ENGINE: LAST RUN STATUS     ")
                print("==================================================")
                print(f" Timestamp:        {last_run.get('timestamp')}")
                print(f" Operator:         {last_run.get('csm')}")
                print(f" Active Outages:   {last_run.get('open_incidents_count')}")
                print(f" Critical Alerts:  {last_run.get('critical_alerts_count')}")
                print(f" Inventory Deltas: {last_run.get('recent_deltas_count')}")
                print(f" Action Items:     {last_run.get('actions_count')}")
                print("==================================================\n")
                return
        print("No previous execution history found in state/run_history.json.")
        return

    # 1. Load Configurations
    try:
        user_profile = load_yaml_file(os.path.join(config_dir, "user_profile.yaml"))
        clients_data = load_yaml_file(os.path.join(config_dir, "clients.yaml"))
        settings = load_yaml_file(os.path.join(config_dir, "settings.yaml"))
        clients_list = clients_data.get("clients", [])
    except Exception as e:
        print(f"[Initialization Error] Failed to load configurations: {e}")
        sys.exit(1)

    csm_info = user_profile.get("csm", {})
    paths_info = user_profile.get("paths", {})

    print("\n" + "=" * 65)
    print("        ENTERPRISE CSM ENGINE: DAILY MORNING KICKOFF")
    print(f" Operator:     {csm_info.get('name')} ({csm_info.get('role')})")
    print(f" Portfolio:    {csm_info.get('segment')}")
    print("=" * 65 + "\n")

    # 2. Instantiate Adapters
    vault_root = paths_info.get("vault_root", os.path.join(base_dir, "output", "vault"))
    inventory_file = os.path.join(data_dir, "sample_inventory_deltas.json")
    incident_file = os.path.join(data_dir, "sample_incidents.json")
    comm_file = os.path.join(data_dir, "sample_communications.json")

    inventory_source = SpreadsheetInventoryAdapter(
        data_file=inventory_file if os.path.exists(inventory_file) else None
    )
    incident_source = IncidentFeedAdapter(
        data_file=incident_file if os.path.exists(incident_file) else None
    )
    communication_channel = CommunicationChannelAdapter(
        data_file=comm_file if os.path.exists(comm_file) else None
    )
    knowledge_store = MarkdownVaultAdapter(vault_root=vault_root)

    # 3. Instantiate Orchestrator
    orchestrator = CSMAgentOrchestrator(
        user_profile=user_profile,
        clients_config=clients_list,
        settings=settings,
        inventory_source=inventory_source,
        incident_source=incident_source,
        communication_channel=communication_channel,
        knowledge_store=knowledge_store,
        state_dir=state_dir,
    )

    if args.dry_run:
        print("[Simulation Mode / Dry Run: Zero changes will be written to disk]\n")

    # 4. Execute Operational Cycle
    briefing: DailyBriefing = orchestrator.run_daily_kickoff(
        client_filter=args.client,
        dry_run=args.dry_run,
    )

    # 5. Render Executive Console Dashboard
    print("-----------------------------------------------------------------")
    print("                      EXECUTIVE BRIEFING SUMMARY                  ")
    print("-----------------------------------------------------------------")
    print(f" Briefing Date:             {briefing.briefing_date}")
    print(f" Accounts Monitored:        {briefing.total_accounts_monitored}")
    print(f" Active Outages:            {briefing.open_incidents_count}")
    print(f" Critical Alerts:           {briefing.critical_alerts_count}")
    print(f" Inventory State Changes:   {briefing.recent_deltas_count}")
    print("-----------------------------------------------------------------\n")

    print("--- TOP TACTICAL ACTION ITEMS ---")
    if not briefing.action_items_sticky:
        print("  All monitored services operating within nominal parameters.")
    else:
        for idx, item in enumerate(briefing.action_items_sticky, 1):
            print(f"  {idx}. {item}")

    print("\n--- CRITICAL & HIGH SEVERITY ALERTS ---")
    priority_alerts = [a for a in briefing.alerts if a.severity.value in ["CRITICAL", "HIGH"]]
    if not priority_alerts:
        print("  Zero critical or high severity alerts flagged.")
    else:
        for a in priority_alerts:
            print(f"  * [{a.severity.value}] {a.client_name}: {a.title}")
            print(f"    Action: {a.recommended_action}")

    if not args.dry_run:
        print(f"\n[Knowledge Store] Morning briefing generated at: {vault_root}/Briefings/")
        print(f"[Knowledge Store] Tactical sticky note updated at: {vault_root}/Tactical_Sticky_Note.md")
        print("[State Store] Execution recorded in state/run_history.json")

    print("\n" + "=" * 65 + "\n")


if __name__ == "__main__":
    main()
