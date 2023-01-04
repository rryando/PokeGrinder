import json
import asyncio
from discord.ext import commands
import random

config = open(r"config.json")
config = json.load(config)

client = commands.Bot(command_prefix="!@#$%^&*())(*&^%$#@!/")
client.config = config

client.token, client.channel = config["token"], config["channel"]
client.timer, client.delay, client.timeout, client.auto_buy = (
    config["timer"],
    config["delay"],
    config["timeout"],
    config["auto_buy"],
)

if config["captcha_solver"] == "True":
    from modules.captcha_solver import solve

    client.captcha_solver = solve




async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    await client.load_extension("cogs.hunting")
    # if config["fish"] == "True":
    #     client.fish_enable = config["fish"]
    #     client.timer_fish = config["timer_fish"]
    #     await client.load_extension("cogs.fishing")
    


asyncio.run(load_cogs())
client.run(client.token)
