# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------

import json
import logging
import os
import re
from typing import Optional

import requests

from account import *
from app_service import *
from ep import *
from service_node import *
from user import *

class Bt:
    def __init__(self, api_url, access_key_id, access_key_secret, verbose: bool = True):
        logging.debug(f"Initialize Bt with api_url = {api_url}")
        self.api_url = api_url
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.jwt_token = None
        self.token_type = None
        self._verbose = verbose
        if verbose:
            print(f"api_uri = {self.api_url}")
            print(f"access_key_id = {self.access_key_id}")
            print(f"access_key_secret = {self.access_key_secret}")

    def auth_header(self):
        if self.jwt_token != None and self.token_type != None:
            return {"Authorization": self.token_type + " " + self.jwt_token}
        else:
            auth_info = {
                "username": self.access_key_id,
                "password": self.access_key_secret,
            }
            if self._verbose:
                print(auth_info)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            if self._verbose:
                print(self.api_url)
            response = requests.post(self.api_url + "/token", auth_info, headers)
            if response.status_code != 200:
                print(f"Login failed, response code = {response.status_code}")
                return None
            else:
                login_resp = response.json()
                if self._verbose:
                    print(login_resp)
                self.jwt_token = login_resp["access_token"]
                self.token_type = login_resp["token_type"]
                return {"Authorization": self.token_type + " " + self.jwt_token}

    # ----------------------------------------------------------------------------------------------------------------
    #  Account
    # ----------------------------------------------------------------------------------------------------------------
    def create_account(self, username, password, headers: str = None):
        data = {"username": username, "password": password}
        if self.api_url != None:
            api_url = self.api_url
        else:
            api_url = os.environ["API_URL"]
        response = requests.post(
            api_url + "/create-account", headers=headers, json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            acct = response.json()
            return (
                Account(
                    acct["username"],
                    acct["account_id"],
                    acct["access_key_id"],
                    acct["access_key_secret"],
                ),
                None,
            )


    def get_account(self, username: str = None):
        query = {"username": username}
        response = requests.get(
            self.api_url + "/list-account", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ret_accounts = []
            accounts = response.json()
            for acct in accounts:
                ret_accounts.append(
                    Account(
                        acct["username"],
                        acct["account_id"],
                        acct["access_key_id"],
                        acct["access_key_secret"],
                    )
                )
            return ret_accounts, None
            
    def remove_account(self, username: str):
        query = {"username": username}
        response = requests.post(
            self.api_url + "/remove-account", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json
        else:
            return response.json(), None

    def clean_account_resources(self, target_account_id: str):
        query = {"target_account_id": target_account_id}
        response = requests.post(
            self.api_url + "/cleanup-account", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def enable_account_trial(self, target_account_id: str, trial_period_days: str):
        query = {
            "target_account_id": target_account_id,
            "trial_period_days": trial_period_days,
        }
        response = requests.post(
            self.api_url + "/account-enable-trial",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def disable_account_trial(self, target_account_id: str):
        query = {
            "target_account_id": target_account_id,
        }
        response = requests.post(
            self.api_url + "/account-disable-trial",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  IAM User
    # ----------------------------------------------------------------------------------------------------------------
    def create_iam_user(
        self,
        account_id: str,
        username: str,
        role: str,
    ):
        data = {"account_id": account_id, "username": username, "role": role}

        response = requests.post(
            self.api_url + "/create-iam-user",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def get_iam_users(
        self,
        username: str = None,
    ):
        query = {"username": username}
        response = requests.get(
            self.api_url + "/list-iam-user", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def set_new_iam_user_password(
        self,
        iam_user_token: str,
        password: str,
    ):
        form_data = {
            "iam_user_token": iam_user_token,
            "password": password,
        }
        response = requests.post(
            self.api_url + "/new-iam-user-set-password",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=form_data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def update_iam_user(
        self,
        name: str = None,
        email: str = None,
        address: str = None,
        phone: str = None,
        password: str = None,
    ):
        data = {}
        data["name"] = name
        data["email"] = email
        data["address"] = address
        data["phone"] = phone
        data["password"] = password

        print(data)
        response = requests.post(
            self.api_url + "/update-iam-user",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def iam_user_enable_mfa(
        self,
        type: str = None,
    ):
        query = {"type": type}
        response = requests.post(
            self.api_url + "/iam-user-enable-mfa",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def iam_user_disable_mfa(
        self,
    ):
        response = requests.post(
            self.api_url + "/iam-user-disable-mfa",
            headers=self.auth_header(),
            params=None,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def iam_user_update_role(
        self,
        new_role: str,
        iam_user_id: str = None,
    ):
        query = {"new_role": new_role}
        if iam_user_id is not None:
            query["iam_user_id"] = iam_user_id

        response = requests.post(
            self.api_url + "/iam-user-update-role",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  SAML SSO
    # ----------------------------------------------------------------------------------------------------------------
    def create_account_idp(
        self,
        idp_name: str,
        entity_id: str,
        issuer: str,
        sso_url: str,
        certificate: str,
    ):
        data = {
            "idp_name": idp_name,
            "entity_id": entity_id,
            "issuer": issuer,
            "sso_url": sso_url,
            "certificate": certificate,
        }
        response = requests.post(
            self.api_url + "/create-account-idp",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def get_account_idp(self):
        response = requests.get(
            self.api_url + "/get-account-idp",
            headers=self.auth_header(),
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def remove_account_idp(self):
        response = requests.post(
            self.api_url + "/remove-account-idp",
            headers=self.auth_header(),
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def update_account_idp(
        self,
        idp_name: str,
        entity_id: str,
        issuer: str,
        sso_url: str,
        certificate: str,
    ):
        data = {}
        if idp_name:
            data["idp_name"] = idp_name
        if entity_id:
            data["entity_id"] = entity_id
        if issuer:
            data["issuer"] = issuer
        if sso_url:
            data["sso_url"] = sso_url
        if certificate:
            data["certificate"] = certificate

        response = requests.post(
            self.api_url + "/update-account-idp",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Service Node Group
    # ----------------------------------------------------------------------------------------------------------------
    def create_service_node_group(
        self,
        service_node_group_name: str,
        service_node_name: str = None,
        form_factor: str = None,
        shipping_addr: str = None,
        hosted_region: str = None,
        hosted_vpc_cidr: str = None,
        hosted_peer_ip: str = None,
        hosted_peer_prefix: str = None,
    ):
        data = {
            "service_node_group_name": service_node_group_name,
        }
        if service_node_name:
            data["service_node_name"] = service_node_name
        if form_factor:
            data["form_factor"] = form_factor
        if shipping_addr:
            data["shipping_addr"] = shipping_addr
        if hosted_region: 
            data["hosted_region"] = hosted_region
        if hosted_vpc_cidr:
            data["hosted_vpc_cidr"] = hosted_vpc_cidr
        if hosted_peer_ip: 
            data["hosted_peer_ip"] = hosted_peer_ip
        if hosted_peer_prefix:
            data["hosted_peer_prefix"] = hosted_peer_prefix
            
        response = requests.post(
            self.api_url + "/create-service-node-group",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            sng = response.json()
            return (
                ServiceNodeGroup(
                    sng["account_id"],
                    sng["service_node_group_name"],
                    sng["service_node_group_id"],
                    sng["form_factor"],
                    sng["shipping_addr"],
                    sng["hosted_region"],
                    sng["hosted_vpc_cidr"],
                    sng["hosted_peer_ip"],
                    sng["hosted_peer_prefix"],
                ),
                None,
            )

    def get_service_node_groups(self, service_node_group_name: str = None):
        query = {"service_node_group_name": service_node_group_name}
        response = requests.get(
            self.api_url + "/list-service-node-group",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ret_service_node_groups = []
            sngs = response.json()
            for sng in sngs:
                ret_service_node_groups.append(
                    ServiceNodeGroup(
                        sng["account_id"],
                        sng["service_node_group_name"],
                        sng["service_node_group_id"],
                        sng["form_factor"],
                        sng["shipping_addr"],
                        sng["hosted_region"],
                        sng["hosted_vpc_cidr"],
                        sng["hosted_peer_ip"],
                        sng["hosted_peer_prefix"],
                    )
                )
            return ret_service_node_groups, None

    def remove_service_node_group(self, service_node_group_id: str):
        query = {
            "service_node_group_id": service_node_group_id,
        }
        response = requests.post(
            self.api_url + "/remove-service-node-group",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Service Node
    # ----------------------------------------------------------------------------------------------------------------
    def create_service_node(
        self,
        service_node_group_id: str = None,
        service_node_name: str = None,
        new_service_node_group: bool = False,
        service_node_group_name: str = None,
    ):
        data = {
            "new_service_node_group": new_service_node_group,
        }
        if new_service_node_group == True:
            if service_node_group_name != None:
                data["service_node_group_name"] = service_node_group_name
            else:
                return (
                    None,
                    "Need service node group name to create new service node group",
                )
        else:
            if service_node_group_id != None:
                data["service_node_group_id"] = service_node_group_id
            elif service_node_group_name != None:
                data["service_node_group_name"] = service_node_group_name
            else:
                return None, "Need existing service node group id or name"

        if service_node_name != None:
            data["service_node_name"] = service_node_name

        response = requests.post(
            self.api_url + "/create-service-node", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            sn = response.json()
            return (
                ServiceNode(
                    sn["service_node_name"],
                    sn["service_node_id"],
                    sn["registered_at"],
                    sn["public_ip"],
                    sn["private_ip"],
                    sn["service_node_group_id"],
                    sn["admin_state"],
                    sn["op_state"],
                    sn["udp_tunnel_status"],
                    sn["form_factor"],
                    sn["shipping_addr"],
                ),
                None,
            )

    def get_service_node(
        self, service_node_group_id: str, service_node_name: str = None
    ):
        query = {
            "service_node_group_id": service_node_group_id,
        }
        if service_node_name != None:
            query["service_node_name"] = service_node_name
        response = requests.get(
            self.api_url + "/list-service-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ret_service_nodes = []
            sns = response.json()
            for sn in sns:
                if self._verbose:
                    print(f"sn: {sn}")
                ret_service_nodes.append(
                    ServiceNode(
                        sn["service_node_name"],
                        sn["service_node_id"],
                        sn["registered_at"],
                        sn["public_ip"],
                        sn["private_ip"],
                        sn["service_node_group_id"],
                        sn["admin_state"],
                        sn["op_state"],
                        sn["udp_tunnel_status"],
                        sn["form_factor"],
                        sn["shipping_addr"],
                    )
                )
            return ret_service_nodes, None

    def remove_service_node(self, service_node_id: str):
        query = {"service_node_id": service_node_id}
        response = requests.post(
            self.api_url + "/remove-service-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_service_node_detail(self, service_node_id: str):
        query = {"service_node_id": service_node_id}
        response = requests.get(
            self.api_url + "/get-service-node-detail",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            app_service_detail = response.json()
            return app_service_detail, None

    def set_service_node_form_factor(
        self, service_node_id: str, form_factor: str, shipping_addr: str = None
    ):
        data = {"node_id": service_node_id, "form_factor": form_factor}
        if shipping_addr:
            data["shipping_addr"] = shipping_addr
        response = requests.post(
            self.api_url + "/set-service-node-form-factor",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  App Service
    # ----------------------------------------------------------------------------------------------------------------
    def create_app_service(
        self,
        app_service_name: str,
        location: str,
        region: str,
        cloud_endpoint_service_name: str,
        service_node_group_id: str,
        fqdn: str,
        proto: str,
        port: str,
        network_mode_enabled: bool = False,
        real_subnets: Optional[str] = None,
        address_translation_enabled: bool = False,
        virtual_subnet_pools: Optional[str] = None,
        bgp_enabled: bool = False,
        bgp_local_asn: Optional[str] = None,
        bgp_peer_asn: Optional[str] = None,
        bgp_peer_ip: Optional[str] = None,
    ):
        # Sanity check app_service_name
        for c in app_service_name:
            if c.isalnum() or c == "-":
                pass
            else:
                return None, f"Invalid app_service_name {app_service_name}"

        data: dict[str, str | None | bool] = {
            "app_service_name": app_service_name,
            "location": location,
        }
        if location in ("aws", "azure"):
            if self._verbose:
                print(f"region = {region}")
            data["region"] = region
            data["cloud_endpoint_service_name"] = cloud_endpoint_service_name
            data["proto"] = proto
            data["port"] = port
        elif location == "onprem":
            if service_node_group_id != None:
                data["service_node_group_id"] = service_node_group_id
            data["fqdn"] = fqdn
            data["proto"] = proto
            data["port"] = port
            data["network_mode_enabled"] = bool(network_mode_enabled)
            data["real_subnets"] = real_subnets
            data["address_translation_enabled"] = bool(address_translation_enabled)
            data["virtual_subnet_pools"] = virtual_subnet_pools
            data["bgp_enabled"] = bool(bgp_enabled)
            data["bgp_local_asn"] = bgp_local_asn
            data["bgp_peer_asn"] = bgp_peer_asn
            data["bgp_peer_ip"] = bgp_peer_ip
        else:
            return None, f"Invalid location parameter {location}"

        if self._verbose:
            print(data)

        response = requests.post(
            self.api_url + "/create-app-service", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            app_service = response.json()
            if self._verbose:
                print(app_service)
            return (
                AppService(
                    app_service_name=app_service["app_service_name"],
                    app_service_id=app_service["app_service_id"],
                    account_id=app_service["account_id"],
                    admin_state=app_service["admin_state"],
                    op_state=app_service["op_state"],
                    deployment=app_service["deployment"],
                    fqdn=app_service["fqdn"],
                    proto=app_service["proto"],
                    port=app_service["port"],
                    service_down_timeout=app_service["service_down_timeout"],
                    primary_contact_id=app_service["primary_contact_id"],
                    secondary_contact_id=app_service["secondary_contact_id"],
                    size=app_service["size"],
                    health=app_service["health"],
                ),
                "",
            )

    def get_app_service(self, app_service_name: str = None):
        query = {"app_service_name": app_service_name}
        response = requests.get(
            self.api_url + "/list-app-service", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ret_app_services = []
            app_services = response.json()
            for app in app_services:
                ret_app_services.append(
                    AppService(
                        account_id=app["account_id"],
                        app_service_id=app["app_service_id"],
                        app_service_name=app["app_service_name"],
                        admin_state=app["admin_state"],
                        op_state=app["op_state"],
                        deployment=app["deployment"],
                        fqdn=app["fqdn"],
                        proto=app["proto"],
                        port=app["port"],
                        service_down_timeout=app["service_down_timeout"],
                        primary_contact_id=app["primary_contact_id"],
                        secondary_contact_id=app["secondary_contact_id"],
                        size=app["size"],
                        health=app["health"],
                    )
                )
            return ret_app_services, None

    def remove_app_service(self, app_service_id: str):
        query = {"app_service_id": app_service_id}
        response = requests.post(
            self.api_url + "/remove-app-service",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_app_service_detail(self, app_service_id: str):
        query = {"app_service_id": app_service_id}
        response = requests.get(
            self.api_url + "/get-app-service-detail",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            app_service_detail = response.json()
            return app_service_detail, None

    def add_app_service_hosting(
        self,
        app_service_id: str,
        location: str,
        region: str,
        cloud_endpoint_service_name: str,
        service_node_group_id: str,
        fqdn: str,
    ):
        data = {
            "app_service_id": app_service_id,
            "location": location,
        }
        if location in ("aws", "azure"):
            if self._verbose:
                print(f"region = {region}")
            data["region"] = region
            data["cloud_endpoint_service_name"] = cloud_endpoint_service_name
        elif location == "onprem":
            if service_node_group_id != None:
                data["service_node_group_id"] = service_node_group_id
            data["fqdn"] = fqdn
        else:
            return None, f"Invalid location parameter {location}"

        if self._verbose:
            print(data)

        response = requests.post(
            self.api_url + "/app-service-add-hosting",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            app_service = response.json()
            if self._verbose:
                print(app_service)
            return (
                AppService(
                    app_service_name=app_service["app_service_name"],
                    app_service_id=app_service["app_service_id"],
                    account_id=app_service["account_id"],
                    admin_state=app_service["admin_state"],
                    op_state=app_service["op_state"],
                    deployment=app_service["deployment"],
                    fqdn=app_service["fqdn"],
                    proto=app_service["proto"],
                    port=app_service["port"],
                    primary_contact_id=app_service["primary_contact_id"],
                    secondary_contact_id=app_service["secondary_contact_id"],
                    service_down_timeout=app_service["service_down_timeout"],
                    health=app_service["health"],
                ),
                None,
            )

    def get_app_service_hosting(
        self,
        app_service_id: str,
        hosting_type: str = None,
    ):
        query = {"app_service_id": app_service_id}
        if hosting_type is not None:
            query["hosting_type"] = hosting_type
        response = requests.get(
            self.api_url + "/app-service-get-hosting",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def remove_app_service_hosting(
        self,
        app_service_id: str,
        hosting_id: str,
    ):
        query = {
            "app_service_id": app_service_id,
            "hosting_id": hosting_id,
        }

        response = requests.post(
            self.api_url + "/app-service-remove-hosting",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            app_service = response.json()
            if self._verbose:
                print(app_service)
            return (
                AppService(
                    app_service_name=app_service["app_service_name"],
                    app_service_id=app_service["app_service_id"],
                    account_id=app_service["account_id"],
                    admin_state=app_service["admin_state"],
                    op_state=app_service["op_state"],
                    deployment=app_service["deployment"],
                    fqdn=app_service["fqdn"],
                    proto=app_service["proto"],
                    port=app_service["port"],
                    primary_contact_id=app_service["primary_contact_id"],
                    secondary_contact_id=app_service["secondary_contact_id"],
                    service_down_timeout=app_service["service_down_timeout"],
                    health=app_service["health"],
                ),
                None,
            )

    def resize_app_service(
        self,
        app_service_id: str,
        hosting_id: str,
        direction: str,
    ):
        query = {
            "app_service_id": app_service_id,
            "hosting_id": hosting_id,
            "direction": direction,
        }
        response = requests.post(
            self.api_url + "/resize-app-service",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def update_app_service_contacts(
        self,
        app_service_id: str,
        primary_contact_id: str = None,
        secondary_contact_id: str = None,
    ):
        query = {"app_service_id": app_service_id}
        if primary_contact_id is not None:
            query["primary_contact_id"] = primary_contact_id
        if secondary_contact_id is not None:
            query["secondary_contact_id"] = secondary_contact_id

        response = requests.post(
            self.api_url + "/set-app-service-contact",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return False, response.json()
        else:
            return True, None

    # ----------------------------------------------------------------------------------------------------------------
    #  EP Node Group
    # ----------------------------------------------------------------------------------------------------------------
    def create_ep_node_group(self, ep_node_group_name: str, ep_node_name: str = None):
        data = {"ep_node_group_name": ep_node_group_name}

        if ep_node_name != None:
            data["ep_node_name"] = ep_node_name

        if self._verbose:
            print(data)
        response = requests.post(
            self.api_url + "/create-endpoint-node-group",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            epng = response.json()
            return (
                EpNodeGroup(
                    epng["account_id"],
                    epng["ep_node_group_id"],
                    epng["ep_node_group_name"],
                ),
                None,
            )

    def get_ep_node_groups(self, ep_node_group_name: str = None):
        query = {"ep_node_group_name": ep_node_group_name}
        response = requests.get(
            self.api_url + "/list-endpoint-node-group",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ep_node_groups = []
            epngs = response.json()
            for item in epngs:
                ep_node_groups.append(
                    EpNodeGroup(
                        item["account_id"],
                        item["ep_node_group_id"],
                        item["ep_node_group_name"],
                    )
                )
            return ep_node_groups, None

    def remove_ep_node_group(self, ep_node_group_id: str):
        query = {"ep_node_group_id": ep_node_group_id}
        response = requests.post(
            self.api_url + "/remove-endpoint-node-group",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  EP Node
    # ----------------------------------------------------------------------------------------------------------------
    def create_ep_node(self, ep_node_group_id: str, ep_node_name: str):
        data = {
            "ep_node_group_id": ep_node_group_id,
            "ep_node_name": ep_node_name,
            "new_ep_node_group": False,
        }
        response = requests.post(
            self.api_url + "/create-endpoint-node",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            epn = response.json()
            return (
                EpNode(
                    epn["ep_node_id"],
                    epn["ep_node_name"],
                    epn["ep_node_group_id"],
                    epn["secondary_ips"],
                    epn["admin_state"],
                    epn["admin_state_change_at"],
                    epn["op_state"],
                    epn["op_state_change_at"],
                    epn["form_factor"],
                    epn["shipping_addr"],
                ),
                None,
            )

    def get_ep_nodes(self, ep_node_group_id: str, ep_node_name: str = None):
        query = {"ep_node_group_id": ep_node_group_id}
        if ep_node_name != None:
            query["ep_node_name"] = ep_node_name
        response = requests.get(
            self.api_url + "/list-endpoint-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            ep_nodes = []
            epns = response.json()
            for item in epns:
                ep_nodes.append(
                    EpNode(
                        item["ep_node_id"],
                        item["ep_node_name"],
                        item["ep_node_group_id"],
                        item["secondary_ips"],
                        item["admin_state"],
                        item["admin_state_change_at"],
                        item["op_state"],
                        item["op_state_change_at"],
                        item["form_factor"],
                        item["shipping_addr"],
                    )
                )
            return ep_nodes, None

    def remove_ep_node(self, ep_node_group_id: str, ep_node_id: str):
        query = {
            "ep_node_group_id": ep_node_group_id,
            "ep_node_id": ep_node_id,
        }
        response = requests.post(
            self.api_url + "/remove-endpoint-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_endpoint_node_detail(self, ep_node_id: str):
        query = {"ep_node_id": ep_node_id}
        response = requests.get(
            self.api_url + "/get-endpoint-node-detail",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            endpoint_node_detail = response.json()
            return endpoint_node_detail, None

    def add_endpoint_node_secondary_ips(self, ep_node_id: str, secondary_ips: str):
        query = {"ep_node_id": ep_node_id, "secondary_ips": secondary_ips}
        response = requests.post(
            self.api_url + "/add-endpoint-node-secondary-ips",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return False, response.json()
        return response.json(), None

    def set_endpoint_node_form_factor(
        self, ep_node_id: str, form_factor: str, shipping_addr: str = None
    ):
        data = {"node_id": ep_node_id, "form_factor": form_factor}
        if shipping_addr:
            data["shipping_addr"] = shipping_addr
        response = requests.post(
            self.api_url + "/set-endpoint-node-form-factor",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  EP
    # ----------------------------------------------------------------------------------------------------------------
    def create_ep(
        self,
        app_service_id: str,
        ep_node_group_id: str,
        ep_node_id: str,
        ep_name: str,
        ep_deployment: str,
        region: Optional[str] = None,
        consumer_principle: Optional[str] = None,
        verbose: bool = False,
        real_subnets: Optional[str] = None,
        bgp_enabled: bool = False,
        bgp_local_asn: Optional[str] = None,
        bgp_peer_asn: Optional[str] = None,
        bgp_peer_ip: Optional[str] = None,
    ):
        if ep_deployment == "agent":
            data = {
                "ep_name": ep_name,
                "app_service_id": app_service_id,
                "deployment": ep_deployment,
            }
        elif ep_deployment == "onprem":
            data = {
                "app_service_id": app_service_id,
                "ep_node_group_id": ep_node_group_id,
                "ep_node_id": ep_node_id,
                "ep_name": ep_name,
                "deployment": ep_deployment,
                "real_subnets": real_subnets,
                "bgp_enabled": bgp_enabled,
                "bgp_local_asn": bgp_local_asn,
                "bgp_peer_asn": bgp_peer_asn,
                "bgp_peer_ip": bgp_peer_ip,
            }
        elif ep_deployment == "aws":
            data = {
                "app_service_id": app_service_id,
                "ep_name": ep_name,
                "deployment": ep_deployment,
                "region": region,
                "consumer_principle": consumer_principle,
            }
        else:
            return None, f"Unknown ep deployment {ep_deployment}"
        if verbose:
            print(f"Create EP, input data = {data}")

        response = requests.post(
            self.api_url + "/create-endpoint", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            ep = response.json()
            return (
                Ep(
                    ep["account_id"],
                    app_service_id,
                    ep_node_id,
                    ep["ep_id"],
                    ep_name,
                    ep["admin_state"],
                    ep["admin_state_change_at"],
                    ep["op_state"],
                    ep["op_state_change_at"],
                    ep["deployment"],
                    ep["fqdn"],
                    ep["ip_addr"],
                    ep["size"],
                    ep["health"],
                    ep["primary_contact_id"],
                    ep["secondary_contact_id"],
                ),
                None,
            )

    def get_eps(
        self,
        app_service_id: str = None,
        ep_node_id: str = None,
        ep_name: str = None,
        verbose: bool = True,
    ):
        query = {
            "app_service_id": app_service_id,
            "ep_node_id": ep_node_id,
        }
        if ep_name != None:
            query["ep_name"] = ep_name

        response = requests.get(
            self.api_url + "/list-endpoint", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            eps = []
            result = response.json()
            for item in result:
                if verbose:
                    print(f"item = {item}")
                eps.append(
                    Ep(
                        item["account_id"],
                        app_service_id,
                        item["ep_node_id"],
                        item["ep_id"],
                        item["ep_name"],
                        item["admin_state"],
                        item["admin_state_change_at"],
                        item["op_state"],
                        item["op_state_change_at"],
                        item["deployment"],
                        item["fqdn"],
                        item["ip_addr"],
                        item["size"],
                        item["health"],
                        item["primary_contact_id"],
                        item["secondary_contact_id"],
                    )
                )
            return eps, None

    def remove_ep(self, ep_id: str):
        query = {"ep_id": ep_id}
        response = requests.post(
            self.api_url + "/remove-endpoint", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def approve_ep(self, ep_id: str):
        query = {"ep_id": ep_id}
        response = requests.post(
            self.api_url + "/approve-endpoint", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def reject_ep(self, ep_id: str):
        query = {"ep_id": ep_id}
        response = requests.post(
            self.api_url + "/reject-endpoint", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_endpoint_detail(self, ep_id: str):
        query = {"ep_id": ep_id}
        response = requests.get(
            self.api_url + "/get-endpoint-detail",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            endpoint_detail = response.json()
            return endpoint_detail, None

    def resize_endpoint_throughput(self, ep_id: str, direction: str):
        query = {"ep_id": ep_id, "direction": direction}
        response = requests.post(
            self.api_url + "/resize-endpoint-throughput",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return False, response.json()
        else:
            return response.json(), None

    def update_endpoint_contacts(
        self,
        ep_id: str,
        primary_contact_id: str = None,
        secondary_contact_id: str = None,
    ):
        query = {"ep_id": ep_id}
        if primary_contact_id is not None:
            query["primary_contact_id"] = primary_contact_id
        if secondary_contact_id is not None:
            query["secondary_contact_id"] = secondary_contact_id

        response = requests.post(
            self.api_url + "/set-endpoint-contact",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return False, response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  User Agent
    # ----------------------------------------------------------------------------------------------------------------
    def create_user_agent(
        self,
        name: str,
        email: str,
        description: str = None,
        ep_id: str = None,
    ):
        data = {
            "name": name,
            "email": email,
            "description": description,
            "ep_id": ep_id,
        }
        response = requests.post(
            self.api_url + "/create-user-agent", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            ua = response.json()
            return (
                UserAgent(
                    ua["name"],
                    ua["email"],
                    ua["user_agent_id"],
                ),
                None,
            )

    def get_user_agents(
        self,
        email: str = None,
    ):
        query = {}
        if email != None:
            query["email"] = email

        response = requests.get(
            self.api_url + "/list-user-agent", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            user_agents = []
            result = response.json()
            print(result)
            for item in result:
                user_agents.append(
                    UserAgent(
                        item["name"],
                        item["email"],
                        item["user_agent_id"],
                    )
                )
            return user_agents, None

    def remove_user_agent(self, user_agent_id: str):
        query = {"user_agent_id": user_agent_id}
        response = requests.post(
            self.api_url + "/remove-user-agent",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def attach_user_agent_to_ep(self, user_agent_id: str, ep_id: str):
        query = {"user_agent_id": user_agent_id, "ep_id": ep_id}
        response = requests.post(
            self.api_url + "/link-user-agent-to-ep",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def detach_user_agent_from_ep(self, user_agent_id: str, ep_id: str):
        query = {"user_agent_id": user_agent_id, "ep_id": ep_id}
        response = requests.post(
            self.api_url + "/unlink-user-agent-from-ep",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_linked_user_agent_ep(self, user_agent_id: str):
        query = {"user_agent_id": user_agent_id}
        response = requests.get(
            self.api_url + "/user-agent-get-linked-ep",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_unlinked_user_agent_ep(self, user_agent_id: str = None):
        if user_agent_id != None:
            query = {"user_agent_id": user_agent_id}
        else:
            query = None
        response = requests.get(
            self.api_url + "/user-agent-get-unlinked-ep",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Database Utils
    # ----------------------------------------------------------------------------------------------------------------
    def remove_table_content(self, table_name: str):
        query = {"table_name": table_name}
        response = requests.post(self.api_url + "/remove-table-content", params=query)
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def remove_all_table_content(self):
        response = requests.post(self.api_url + "/remove-all-table-content")
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Message
    # ----------------------------------------------------------------------------------------------------------------
    def get_latest_message(self, target_id: str, last_seen_msg_id: int):
        query = {"target_id": target_id, "latest_msg_id": last_seen_msg_id}
        response = requests.get(
            self.api_url + "/latest-messages", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Download OVA
    # ----------------------------------------------------------------------------------------------------------------
    def get_filename_from_cd(self, cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        print(cd)
        fname = re.findall("filename=(.+)", cd)
        if len(fname) == 0:
            return None
        return fname[0].lstrip('"').rstrip('"')

    def prepare_ep_node_vm(self, ep_node_id: str, filename: str = None):
        query = {"ep_node_id": ep_node_id}
        response = requests.get(
            self.api_url + "/prepare-epn-ova",
            headers=self.auth_header(),
            params=query,
            allow_redirects=True,
        )
        if response.status_code != 200:
            return False, response.json()

        return response.json(), None

    def prepare_service_node_vm(self, service_node_id: str, filename: str = None):
        query = {"service_node_id": service_node_id}
        response = requests.get(
            self.api_url + "/prepare-sn-ova",
            headers=self.auth_header(),
            params=query,
            allow_redirects=True,
        )
        if response.status_code != 200:
            return False, response.json()

        return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Get stats
    # ----------------------------------------------------------------------------------------------------------------
    def get_net_stats(
        self, id_list: list, start_time: str, end_time: str, appservice_id: str = None
    ):
        id_list_str = ",".join(id_list)
        query = {"ids": id_list_str, "start_time": start_time, "end_time": end_time}
        if appservice_id != None:
            query["app_service_id"] = appservice_id
        response = requests.get(
            self.api_url + "/get-net-stats",
            headers=self.auth_header(),
            params=query,
            allow_redirects=True,
        )
        if response.status_code != 200:
            return [], response.json()

        return response.json(), None

    def run_diag(self, node_id: str, command: str = None):
        """
        Run diagonstics on a node / gateway.
        """
        query = {
            "node_id": node_id,
            "command": command,
        }
        response = requests.post(
            self.api_url + "/run-diag",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def run_health_check(self, node_id: str):
        """
        Run health check on a node / gateway.
        """
        query = {
            "node_id": node_id,
        }
        response = requests.post(
            self.api_url + "/run-health-check",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def gen_cloud_init_data(self, node_id: str):
        """
        Generate cloud-init data for a node / gateway.
        """
        query = {
            "node_id": node_id,
        }
        response = requests.post(
            self.api_url + "/generate-node-cloud-init-data",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def upload_diag(self, node_id: str):
        """
        Request a node/gateway to upload diagnostics information.
        """
        query = {
            "node_id": node_id,
        }
        response = requests.post(
            self.api_url + "/upload-diag",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def measure_ep_latency(self, ep_id: str):
        query = {
            "ep_id": ep_id,
        }
        response = requests.post(
            self.api_url + "/measure-endpoint-latency",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def measure_app_service_latency(self, app_service_id: str):
        query = {
            "app_service_id": app_service_id,
        }
        response = requests.post(
            self.api_url + "/measure-app-service-latency",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def reset_ep(self, ep_id: str):
        query = {
            "ep_id": ep_id,
        }
        response = requests.post(
            self.api_url + "/reset-endpoint",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def upgrade_node(self, node_id: str, url: str):
        """
        Upgrade a node / gateway.
        """
        query = {
            "node_id": node_id,
            "url": url,
        }
        response = requests.post(
            self.api_url + "/upgrade-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def reset_node(self, node_id: str, hard: bool = False):
        """
        Reset a node / gateway.
        """
        query = {
            "node_id": node_id,
            "hard": hard,
        }
        response = requests.post(
            self.api_url + "/reset-node",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def enable_remote_access(self, node_id: str):
        """
        Enable remote access on a node / gateway.
        """
        query = {
            "node_id": node_id,
        }
        response = requests.post(
            self.api_url + "/enable-remote-access",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def disable_remote_access(self, node_id: str):
        """
        Disable remote access on a node / gateway.
        """
        query = {
            "node_id": node_id,
        }
        response = requests.post(
            self.api_url + "/disable-remote-access",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_connected_endpoints(self, node_id: str):
        query = {
            "node_id": node_id,
        }
        response = requests.get(
            self.api_url + "/get-connected-endpoints",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_endpoint_sessions(self, ep_id: str):
        query = {
            "ep_id": ep_id,
        }
        response = requests.get(
            self.api_url + "/get-endpoint-sessions",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return json.dumps(response.json()), None

    def get_top_talker(self, app_service_id: str, start_time: str, end_time: str):
        query = {
            "app_service_id": app_service_id,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get(
            self.api_url + "/get-top-talker-ep",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_ep_sessions(self, ep_id: str, start_time: str, end_time: str):
        query = {
            "ep_id": ep_id,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get(
            self.api_url + "/get-ep-sessions",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Billing
    # ----------------------------------------------------------------------------------------------------------------
    def get_stripe_publishable_key(self):
        response = requests.get(
            self.api_url + "/get-stripe-publishable-key",
            headers=self.auth_header(),
            params=None,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def get_billings(self):
        response = requests.get(
            self.api_url + "/get-billings",
            headers=self.auth_header(),
            params=None,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def create_payment_method(
        self,
        payment_type: str,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: int,
        name: str,
        email: str,
        phone: str,
        street_addr_1: str,
        street_addr_2: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
    ):
        data = {
            "payment_method_type": payment_type,
            "card_number": card_number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc,
            "name": name,
            "email": email,
            "phone": phone,
            "street_addr_1": street_addr_1,
            "street_addr_2": street_addr_2,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
        }
        api_url = os.environ["API_URL"]
        response = requests.post(
            api_url + "/create-stripe-payment", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def setup_strip_subscription(
        self,
        payment_type: str,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: int,
        name: str,
        email: str,
        phone: str,
        street_addr_1: str,
        street_addr_2: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
    ):
        data = {
            "payment_method_type": payment_type,
            "card_number": card_number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc,
            "name": name,
            "email": email,
            "phone": phone,
            "street_addr_1": street_addr_1,
            "street_addr_2": street_addr_2,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
        }
        api_url = os.environ["API_URL"]
        response = requests.post(
            api_url + "/create-stripe-payment", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, f"Cannot create payment method, error_code = {response.json()}"

        payment_method = response.json()
        print(f"payment method = {payment_method}")

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "street_addr_1": street_addr_1,
            "street_addr_2": street_addr_2,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "payment_method_id": payment_method["id"],
        }
        response = requests.post(
            api_url + "/setup-billing-stripe-subscription",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return (
                None,
                f"Cannot set up stripe subscription, error_code = {response.json()}",
            )

        return response.json(), None

    def remove_strip_subscription(self):
        query = {
            "provider": "stripe",
        }
        response = requests.post(
            self.api_url + "/remove-billing",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def set_preferred_billing_provider(self, provider: str):
        query = {"provider": provider}
        response = requests.post(
            self.api_url + "/set-preferred-billing",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def edit_app_service(
        self,
        app_service_id: Optional[str] = None,
        app_service_name: Optional[str] = None,
        fqdn: Optional[str] = None,
        proto: Optional[str] = None,
        port: Optional[str] = None,
        service_down_timeout: Optional[int] = None,
    ):
        data = {
            "app_service_id": app_service_id,
            "app_service_name": app_service_name,
            "fqdn": fqdn,
            "proto": proto,
            "port": port,
            "service_down_timeout": service_down_timeout,
        }
        response = requests.post(
            self.api_url + "/edit-app-service", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    # ----------------------------------------------------------------------------------------------------------------
    #  Contact
    # ----------------------------------------------------------------------------------------------------------------
    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        company_name: Optional[str] = None,
    ):
        data = {"email": email}
        if last_name is not None:
            data["last_name"] = last_name
        if first_name is not None:
            data["first_name"] = first_name
        if phone is not None:
            data["phone"] = phone
        if address is not None:
            data["address"] = address
        if company_name is not None:
            data["company_name"] = company_name

        response = requests.post(
            self.api_url + "/create-contact", headers=self.auth_header(), json=data
        )
        if response.status_code != 200:
            return None, response.json()
        else:
            return response.json(), None

    def get_contact(
        self,
        email: Optional[str] = None,
    ):
        query = {}
        if email is not None:
            query["email"] = email

        response = requests.get(
            self.api_url + "/get-contact", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            contacts = response.json()
            return contacts, None

    def get_contact_by_ep_id(
        self,
        ep_id: str,
    ):
        query = {"ep_id": ep_id}
        response = requests.get(
            self.api_url + "/get-contact-by-ep-id",
            headers=self.auth_header(),
            params=query,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            contacts = response.json()
            return contacts, None

    def remove_contact(
        self,
        email: str,
    ):
        query = {"email": email}
        response = requests.post(
            self.api_url + "/remove-contact", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            contacts = response.json()
            return contacts, None

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        company_name: Optional[str] = None,
    ):
        query = {"contact_id": contact_id}
        if email is not None:
            query["email"] = email
        if last_name is not None:
            query["last_name"] = last_name
        if first_name is not None:
            query["first_name"] = first_name
        if phone is not None:
            query["phone"] = phone
        if address is not None:
            query["address"] = address
        if company_name is not None:
            query["company_name"] = company_name
        response = requests.post(
            self.api_url + "/update-contact", headers=self.auth_header(), params=query
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def configure_node_lan_interface(
        self,
        node_id: str,
        enable: bool,
        primary_ipv4_address: Optional[str] = None,
        secondary_ipv4_addresses: Optional[str] = None,
    ):
        data = {
            "node_id": node_id,
            "enabled": enable,
            "primary_ipv4_address": primary_ipv4_address,
            "secondary_ipv4_addresses": secondary_ipv4_addresses,
        }
        response = requests.post(
            self.api_url + "/configure-lan-interface",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def configure_dhcp_relay(
        self,
        node_group_id: str,
        enable: bool,
        server_ip: Optional[str] = None,
    ):
        data = {
            "node_group_id": node_group_id,
            "enabled": enable,
            "server_ip": server_ip,
        }
        response = requests.post(
            self.api_url + "/configure-dhcp-relay",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None

    def configure_vrrp(
        self,
        node_group_id: str,
        enable: bool,
        virtual_ip: Optional[str] = None,
    ):
        data = {
            "node_group_id": node_group_id,
            "enabled": enable,
            "virtual_ip": virtual_ip,
        }
        response = requests.post(
            self.api_url + "/configure-vrrp",
            headers=self.auth_header(),
            json=data,
        )
        if response.status_code != 200:
            return [], response.json()
        else:
            return response.json(), None


def get_bt(
    api_url: str = None,
    access_key_id: str = None,
    access_key_secret: str = None,
    verbose: bool = True,
):
    if api_url == None:
        api_url = os.getenv("API_URL")
    if access_key_id == None:
        access_key_id = os.getenv("BBT_ACCESS_KEY_ID")
    if access_key_secret == None:
        access_key_secret = os.getenv("BBT_ACCESS_KEY_SECRET")
    return Bt(
        api_url=api_url,
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        verbose=verbose,
    )
