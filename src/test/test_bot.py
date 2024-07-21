from dotenv import load_dotenv
import discord, os, pytest

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID")
TOKEN = os.getenv("TOKEN")
bot = discord.Bot()

@pytest.fixture
def init():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    return client

@pytest.fixture
def on_ready(init):
    client = init

    return client

def test_bot(on_ready):
    client = on_ready

    assert client, "Could not initialize bot!"