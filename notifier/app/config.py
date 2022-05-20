from pydantic import BaseSettings
import os
# from dotenv import load_dotenv

# load_dotenv()

class Settings(BaseSettings):

    #SLACK ENV
    SLACK_URL: str = os.getenv("WEBHOOK_URL")

config = Settings()