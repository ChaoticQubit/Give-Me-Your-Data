import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
DAILY_NOTE_BASE_PATH = os.getenv("DAILY_NOTE_BASE_PATH", "Daily Notes")
PROPERTY_NAME = os.getenv("PROPERTY_NAME", "github_commits")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in .env file")
if not OBSIDIAN_VAULT_PATH:
    raise ValueError("OBSIDIAN_VAULT_PATH is not set in .env file")
