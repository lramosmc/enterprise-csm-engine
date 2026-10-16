"""
Inventory Adapter for Spreadsheet and Delta Feed Ingestion.
Translates structured inventory state changes into canonical Service and ServiceDelta models.
"""

import json
import os
from typing import List, Optional, Dict, Any
from core.interfaces import IInventorySource
from core.models import Service, ServiceDelta, DeltaChangeType


class SpreadsheetInventoryAdapter(IInventorySource):
    """Adapter for reading active service portfolios and inventory deltas."""

    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file

    def load_services(self, client_id_or_name: Optional[str] = None) -> List[Service]:
        """Loads active service records from source or synthetic benchmark."""
        services: List[Service] = []
        if self.data_file and os.path.exists(self.data_file) and self.data_file.endswith(".json"):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw = json.load(f).get("services", [])
                    for s in raw:
                        services.append(
                            Service(
                                service_id=s.get("service_id", "SVC-001"),
                                customer_id=s.get("customer_id", "CUST-001"),
                                customer_name=s.get("customer_name", "Global Enterprise"),
                                product_name=s.get("product_name", "Dedicated Internet Access"),
                                bandwidth=s.get("bandwidth", "10 Gbps"),
                                status=s.get("status", "Active"),
                                activation_date=s.get("activation_date"),
                                mrc=s.get("mrc"),
                                currency=s.get("currency", "USD"),
                                site_origin=s.get("site_origin"),
                                site_destination=s.get("site_destination"),
                            )
                        )
            except Exception:
                pass

        if client_id_or_name:
            services = [
                s for s in services
                if s.customer_name.lower() == client_id_or_name.lower() or s.customer_id == client_id_or_name
            ]
        return services

    def load_recent_deltas(self, client_id_or_name: Optional[str] = None) -> List[ServiceDelta]:
        """Loads recent deltas (activations, disconnects, bandwidth modifications)."""
        deltas: List[ServiceDelta] = []
        if self.data_file and os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw_deltas = json.load(f).get("deltas", [])
                    for d in raw_deltas:
                        change_type = DeltaChangeType(d.get("change_type", "OTHER"))
                        deltas.append(
                            ServiceDelta(
                                service_id=d.get("service_id", "CKT-000"),
                                customer_name=d.get("customer_name", "Enterprise Account"),
                                change_type=change_type,
                                timestamp=d.get("timestamp", "2026-10-16T08:00:00"),
                                old_value=d.get("old_value"),
                                new_value=d.get("new_value"),
                                details=d.get("details", ""),
                                is_fiber=d.get("is_fiber", True),
                            )
                        )
            except Exception:
                pass

        # Fallback to realistic synthetic sample if file is not supplied or empty
        if not deltas and not self.data_file:
            deltas = [
                ServiceDelta(
                    service_id="CKT-FIBER-9041",
                    customer_name="Apex Cloud Infrastructure",
                    change_type=DeltaChangeType.NEW_ACTIVATION,
                    timestamp="2026-10-16T07:30:00",
                    details="100G Waves Circuit turned up between Equinix SP4 and Ashburn DC2.",
                    is_fiber=True,
                ),
                ServiceDelta(
                    service_id="CKT-ETH-1120",
                    customer_name="Nexus Financial Systems",
                    change_type=DeltaChangeType.DISCONNECTION,
                    timestamp="2026-10-15T19:00:00",
                    details="Legacy 1Gbps backup link decommissioned following data center migration.",
                    is_fiber=True,
                ),
                ServiceDelta(
                    service_id="CKT-DIA-3304",
                    customer_name="Quantum Analytics",
                    change_type=DeltaChangeType.BANDWIDTH_CHANGE,
                    timestamp="2026-10-16T06:15:00",
                    old_value="5 Gbps",
                    new_value="10 Gbps",
                    details="Capacity burst upgrade applied ahead of quarterly compute load.",
                    is_fiber=True,
                ),
            ]

        if client_id_or_name:
            deltas = [d for d in deltas if d.customer_name.lower() == client_id_or_name.lower()]
        return deltas
