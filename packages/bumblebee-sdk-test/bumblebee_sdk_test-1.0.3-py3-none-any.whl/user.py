# --------------------------------------------------------------------------------
# Copyright (C) [2023] [Bumblebee Networks Inc.]
# All rights reserved. Unauthorized use is prohibited.
# --------------------------------------------------------------------------------


class UserAgent:
    def __init__(
        self,
        name: str,
        email: str,
        user_agent_id: str,
    ):
        self.name = name
        self.email = email
        self.user_agent_id = user_agent_id

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "user_agent_id": self.user_agent_id,
        }
