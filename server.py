import html
import json
import logging
from typing import Optional

import pydantic
import requests
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")


class Conf(pydantic.BaseSettings):
    """Notification Config"""

    slack_webhook_url: Optional[str] = None
    slack_channel: Optional[str] = None


class Message(pydantic.BaseModel):
    """Message Type from UA"""

    from_: str = pydantic.Field(..., alias="from")
    body: str


class Push:
    """Push to every services"""

    def __init__(self):
        self.conf = Conf()
        logger.info("%s", self.conf)

    def run(self, msg: Message):
        if self.conf.slack_webhook_url:
            self.run_slack(msg)

    def run_slack(self, msg: Message):
        """Slack incoming webhook"""
        payload = {
            "username": f"Push from {msg.from_}",
            "text": html.escape(msg.body),
        }
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("Slack: %s", payload)
        res = requests.post(self.conf.slack_webhook_url, data=json.dumps(payload), headers=headers)
        logger.info("<= %s", res.text)


app = FastAPI(name="osu")
push = Push()


@app.post("/osu")
def osu(msg: Message):
    """Receive a Message"""
    push.run(msg)
    return {"code": "OK"}
