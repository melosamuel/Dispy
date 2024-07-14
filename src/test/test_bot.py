import discord, pytest 

@pytest.fixture
def init():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    return client

@pytest.fixture
def on_ready(init):
    client = init

    print(f"Logged in as {client.user}")

    return client

def test_bot(on_ready):
    client = on_ready

    assert client, "Could not initialize the bot, please check your code!"