import json
from pathlib import Path

from environs import Env
from loguru import logger

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')

with open(f"{path}/data/video_links.json", "r") as file:
    video_links = json.load(file)
