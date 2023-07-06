import nextcord
from settings import Config


client = nextcord.Client()
BOT_TOKEN = input("Please input your Bot Token:")


@client.event
async def on_ready():
    print(
        f"Use this Link to invite your bot: https://discord.com/api/oauth2/authorize?client_id={client.application_id}&permissions=285212688&scope=bot"
    )


@client.event
async def on_guild_join(guild: nextcord.Guild):
    print(f"Bot joined {guild.name} ({guild.id})")
    config = Config("config.yml")
    config.GUILD_ID = guild.id
    config.BOT_TOKEN = BOT_TOKEN
    config.save()
    print("You can now use main.py to start the bot.")
    await client.close()


print("Please wait... Connecting with discord...")
client.run(BOT_TOKEN)
