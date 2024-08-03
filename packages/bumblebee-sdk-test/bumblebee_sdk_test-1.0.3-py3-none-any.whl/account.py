# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------


class Account:
    def __init__(
        self, username: str, account_id: int, access_key_id: str, access_key_secret: str
    ):
        self.username = username
        self.account_id = account_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def to_dict(self):
        return {
            "username": self.username,
            "account_id": self.account_id,
            "access_key_id": self.access_key_id,
            "access_key_secret": self.access_key_secret,
        }
