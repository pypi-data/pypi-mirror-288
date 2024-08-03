# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------


from typing import Optional


class AppService:
    def __init__(
        self,
        account_id: int,
        app_service_id: int,
        app_service_name: str,
        admin_state: str,
        op_state: str,
        deployment: str,
        fqdn: str,
        proto: str,
        port: str,
        service_down_timeout: int,
        primary_contact_id: str,
        secondary_contact_id: str,
        size: Optional[int] = None,
        health: Optional[float] = None,
    ):
        self.account_id = account_id
        self.app_service_id = app_service_id
        self.app_service_name = app_service_name
        self.admin_state = admin_state
        self.op_state = op_state
        self.deployment = deployment
        self.fqdn = fqdn
        self.proto = proto
        self.port = port
        self.service_down_timeout = service_down_timeout
        self.primary_contact_id = primary_contact_id
        self.secondary_contact_id = secondary_contact_id
        self.size = size
        self.health = health

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "app_service_id": self.app_service_id,
            "app_service_name": self.app_service_name,
            "admin_state": self.admin_state,
            "op_state": self.op_state,
            "deployment": self.deployment,
            "fqdn": self.fqdn,
            "proto": self.proto,
            "port": self.port,
            "service_down_timeout": self.service_down_timeout,
            "primary_contact_id": self.primary_contact_id,
            "secondary_contact_id": self.secondary_contact_id,
            "size": self.size,
            "health": self.health,
        }
