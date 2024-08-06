# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from fedora_messaging import message

USER_SCHEMA = {
    "type": "object",
    "required": ["username", "badges_user_id"],
    "properties": {
        "username": {"type": "string"},
        "badges_user_id": {"type": "integer"},
    },
}


class TahrirMessage(message.Message):
    @property
    def app_name(self):
        return "tahrir"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/badges.png"

    @property
    def usernames(self):
        return [self.agent_name]

    @property
    def groups(self):
        return []

    @property
    def url(self):
        return None

    def __str__(self):
        return self.summary


class PersonLoginFirstV1(TahrirMessage):
    """The message sent when a user logs into tahrir for the first time"""

    @property
    def agent_name(self):
        return self.body["user"]["username"]

    @property
    def summary(self):
        return f"{self.agent_name} logged into badges for the first time"

    topic = "badges.person.login.first"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/tahrir",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user logs into tahrir for the first time",
        "type": "object",
        "required": ["user"],
        "properties": {
            "user": USER_SCHEMA,
        },
    }


class BadgeMessage(TahrirMessage):

    @property
    def recipient(self):
        return self.body["user"]["username"]

    @property
    def usernames(self):
        return [self.recipient]

    # No agent_name: the badges are awarded by the Badges system, not a user.


class BadgeAwardV1(BadgeMessage):
    """The message sent when a badge is awarded"""

    @property
    def summary(self):
        return f"{self.recipient} was awarded the badge `{self.body['badge']['name']}`"

    def __str__(self):
        return self.body["badge"]["description"]

    badge_schema: typing.ClassVar = {
        "type": "object",
        "required": ["badge_id", "description", "image_url", "name"],
        "properties": {
            "badge_id": {"type": "string"},
            "description": {"type": "string"},
            "image_url": {"type": "string"},
            "name": {"type": "string"},
        },
    }

    topic = "badges.badge.award"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/tahrir",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a badge is awarded",
        "type": "object",
        "required": ["user", "badge"],
        "properties": {
            "user": USER_SCHEMA,
            "badge": badge_schema,
        },
    }


class PersonRankAdvanceV1(BadgeMessage):
    """The message sent when a user's rank changes"""

    @property
    def recipient(self):
        return self.body["person"]["nickname"]

    @property
    def summary(self):
        return (
            f"{self.recipient}'s Badges rank changed from {self.body['old_rank']} "
            f"to {self.body['person']['rank']}"
        )

    person_schema: typing.ClassVar = {
        "type": "object",
        "required": ["bio", "email", "id", "nickname", "rank", "website"],
        "properties": {
            "bio": {"type": ["string", "null"]},
            "email": {"type": "string"},
            "id": {"type": "integer"},
            "nickname": {"type": "string"},
            "rank": {"type": "integer"},
            "website": {"type": ["string", "null"]},
        },
    }

    topic = "badges.person.rank.advance"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/tahrir",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user's rank changes",
        "type": "object",
        "required": ["old_rank", "person"],
        "properties": {
            "old_rank": {"type": ["integer", "null"]},
            "person": person_schema,
        },
    }
