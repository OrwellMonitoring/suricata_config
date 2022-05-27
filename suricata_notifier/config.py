import os
from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):

    load_dotenv()
    
    #SLACK ENV
    SLACK_URL: str = os.getenv("WEBHOOK_URL")
    SLACK_SEV1: str = os.getenv("SEV1_CHANNEL")
    SLACK_SEV2: str = os.getenv("SEV2_CHANNEL")
    SLACK_SEV3: str = os.getenv("SEV3_CHANNEL")
    SLACK_SEV4: str = os.getenv("SEV4_CHANNEL")
    SLACK_OTHER: str = os.getenv("OTHER_CHANNEL")

    # SURICATA ENV
    SURICATA_LOCATION: str = os.getenv("SURICATA_LOGS")

config = Settings()
