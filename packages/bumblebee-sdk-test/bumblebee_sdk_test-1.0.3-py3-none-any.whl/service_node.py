# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------


class ServiceNodeGroup:
    def __init__(
        self,
        account_id: str,
        service_node_group_name: str,
        service_node_group_id: str,
        form_factor: str,
        shipping_addr: str,
        hosted_region: str,
        hosted_vpc_cidr: str,
        hosted_peer_ip: str,
        hosted_peer_prefix: str,
    ):
        self.account_id = account_id
        self.service_node_group_name = service_node_group_name
        self.service_node_group_id = service_node_group_id
        self.form_factor = form_factor
        self.shipping_addr = shipping_addr
        self.hosted_region = hosted_region
        self.hosted_vpc_cidr = hosted_vpc_cidr
        self.hosted_peer_ip = hosted_peer_ip
        self.hosted_perr_prefix = hosted_peer_prefix

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "service_node_group_name": self.service_node_group_name,
            "service_node_group_id": self.service_node_group_id,
            "form_factor": self.form_factor,
            "shipping_addr": self.shipping_addr,
            "hosted_region": self.hosted_region,
            "hosted_vpc_cidr": self.hosted_vpc_cidr,
            "hosted_peer_ip": self.hosted_peer_ip,
            "hosted_peer_prefix": self.hosted_perr_prefix,
        }


class ServiceNode:
    def __init__(
        self,
        service_node_name: str,
        service_node_id: str,
        registered_at: str,
        public_ip: str,
        private_ip: str,
        service_node_group_id: str,
        admin_state: str,
        op_state: str,
        udp_tunnel_status: str,
        form_factor: str,
        shipping_addr: str,
    ):
        self.service_node_name = service_node_name
        self.service_node_id = service_node_id
        self.registered_at = registered_at
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.service_node_group_id = service_node_group_id
        self.admin_state = admin_state
        self.op_state = op_state
        self.udp_tunnel_status = udp_tunnel_status
        self.form_factor = form_factor
        self.shipping_addr = shipping_addr

    def to_dict(self):
        return {
            "service_node_name": self.service_node_name,
            "service_node_id": self.service_node_id,
            "registered_at": self.registered_at,
            "public_ip": self.public_ip,
            "private_ip": self.private_ip,
            "service_node_group_id": self.service_node_group_id,
            "admin_state": self.admin_state,
            "op_state": self.op_state,
            "udp_tunnel_status": self.udp_tunnel_status,
            "form_factor": self.form_factor,
            "shipping_addr": self.shipping_addr,
        }
