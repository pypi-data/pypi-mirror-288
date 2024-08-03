# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------


class EpNode:
    def __init__(
        self,
        ep_node_id: str,
        ep_node_name: str,
        ep_node_group_id: int,
        secondary_ips: str,
        admin_state: str,
        admin_state_change_at: str,
        op_state: str,
        op_state_change_at: str,
        form_factor: str,
        shipping_addr: str,
    ):
        self.ep_node_id = ep_node_id
        self.ep_node_name = ep_node_name
        self.ep_node_group_id = ep_node_group_id
        self.secondary_ips = secondary_ips
        self.admin_state = admin_state
        self.admin_state_change_at = admin_state_change_at
        self.op_state = op_state
        self.op_state_change_at = op_state_change_at
        self.form_factor = form_factor
        self.shipping_addr = shipping_addr

    def to_dict(self):
        return {
            "ep_node_id": self.ep_node_id,
            "ep_node_name": self.ep_node_name,
            "ep_node_group_id": self.ep_node_group_id,
            "secondary_ips": self.secondary_ips,
            "admin_state": self.admin_state,
            "admin_state_change_at": self.admin_state_change_at,
            "op_state": self.op_state,
            "op_state_change_at": self.op_state_change_at,
            "form_factor": self.form_factor,
            "shipping_addr": self.shipping_addr,
        }


class EpNodeGroup:
    def __init__(self, account_id: int, ep_node_group_id: int, ep_node_group_name: str):
        self.ep_node_group_id = ep_node_group_id
        self.ep_node_group_name = ep_node_group_name
        self.account_id = account_id

    def get_ep_nodes(self, bt):
        # Get ep node in the ep node group
        return bt.get_ep_nodes(self.ep_node_group_id)

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "ep_node_group_id": self.ep_node_group_id,
            "ep_node_group_name": self.ep_node_group_name,
        }


class Ep:
    def __init__(
        self,
        account_id: int,
        app_service_id: str,
        ep_node_id: str,
        ep_id: str,
        ep_name: str,
        admin_state: str,
        admin_state_change_at: str,
        op_state: str,
        op_state_change_at: str,
        deployment: str,
        fqdn: str,
        ip_addr: str,
        size: str,
        health: str,
        primary_contact_id: str,
        secondary_contract_id: str,
    ):
        self.account_id = account_id
        self.app_service_id = app_service_id
        self.ep_node_id = ep_node_id
        self.ep_id = ep_id
        self.ep_name = ep_name
        self.admin_state = admin_state
        self.admin_state_change_at = admin_state_change_at
        self.op_state = op_state
        self.op_state_change_at = op_state_change_at
        self.deployment = deployment
        self.fqdn = fqdn
        self.ip_addr = ip_addr
        self.size = size
        self.health = health
        self.primary_contact_id = primary_contact_id
        self.secondary_contract_id = secondary_contract_id

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "app_service_id": self.app_service_id,
            "ep_node_id": self.ep_node_id,
            "ep_id": self.ep_id,
            "ep_name": self.ep_name,
            "admin_state": self.admin_state,
            "admin_state_change_at": self.admin_state_change_at,
            "op_state": self.op_state,
            "op_state_change_at": self.op_state_change_at,
            "deployment": self.deployment,
            "fqdn": self.fqdn,
            "ip_addr": self.ip_addr,
            "size": self.size,
            "health": self.health,
            "primary_contact_id": self.primary_contact_id,
            "secondary_contact_id": self.secondary_contract_id,
        }
