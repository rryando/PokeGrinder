import os
from datetime import datetime
from discord.ext import commands
from discord.channel import TextChannel
import asyncio

class Startup(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

        print("PokeGrinder is ready to grind!")
        print(f"Username: {self.client.user.name}" f"#{self.client.user.discriminator}")

         

        coolest_ascii_font = """\033[1;33m
       __________       __            ________      .__            .___            
       \______   \____ |  | __ ____  /  _____/______|__| ____    __| _/___________ 
        |     ___/  _ \|  |/ // __ \/   \  __\_  __ \  |/    \  / __ |/ __ \_  __ \\
        |    |  (  <_> )    <\  ___/\    \_\  \  | \/  |   |  \/ /_/ \  ___/|  | \/
        |____|   \____/|__|_  \\___  >\______  /__|  |__|___|  /\____ |\___  >__|   
                            \/    \/        \/              \/      \/    \/       
        """
        print(coolest_ascii_font)

        self.client.start_time = datetime.now().replace(microsecond=0)

        async def process_commands(self, command_id):
            channel: TextChannel = self.client.get_channel(self.client.channel)

            commands = [
                commands
                async for commands in channel.slash_commands(
                    command_ids=[command_id]
                )
            ]

            return commands

        command_ids = [1015311085441654824, 1015311085517156481, 1015311084812501026, 1015311084594405485, 1015311085307445253, 1015311084594405477, 1015311085517156475, 1015311084594405484, 1015311085307445249]
        tasks = [asyncio.create_task(process_commands(self, command_id)) for command_id in command_ids]
        commands = await asyncio.gather(*tasks)


        try:
            print("Loading slash commands...")

            self.client.pokemon = commands[0][0]
            print(f"/{commands[0][0]} loaded!")
            await asyncio.sleep(1)
            
            self.client.shop_buy = commands[1][0].children[1]
            print(f"/{commands[1][0]} {commands[1][0].children[1]} loaded!")
            await asyncio.sleep(1)
            
            self.client.fish = commands[2][0].children[2]
            print(f"/{commands[2][0]} {commands[2][0].children[2]} loaded!")
            await asyncio.sleep(1)

            self.client.egg_check = commands[3][0].children[0]
            self.client.egg_hold = commands[3][0].children[1]
            self.client.egg_hatch = commands[3][0].children[2]
            print(f"/{commands[3][0]} {commands[3][0].children[0]} {commands[3][0].children[1]} {commands[3][0].children[2]} loaded!")
            await asyncio.sleep(1)

            self.client.lb_all = commands[4][0].children[1]
            print(f"/{commands[4][0]} {commands[4][0].children[1]} loaded!")
            await asyncio.sleep(1)

            self.client.checklist = commands[5][0]
            print(f"/{commands[5][0]} loaded!")
            await asyncio.sleep(1)

            self.client.quest = commands[6][0].children[1]
            print(f"/{commands[6][0]} {commands[6][0].children[1]} loaded!")
            await asyncio.sleep(1)

            self.client.daily = commands[7][0]
            print(f"/{commands[7][0]} loaded!")
            await asyncio.sleep(1)

            self.client.hunt = commands[8][0].children[0]
            print(f"/{commands[8][0]} {commands[8][0].children[0]} loaded!")
            await asyncio.sleep(1)

            print("All slash commands loaded!")

            print("starting quest..")
            await self.client.quest()
            await asyncio.sleep(4)

            print("checking daily..")
            await self.client.daily()
            await asyncio.sleep(4)

            print("checking hunt..")
            await self.client.hunt()
            await asyncio.sleep(4)
            
            print("opening lootbox..")
            await self.client.lb_all()
            await asyncio.sleep(4)

            if self.client.config["auto-egg"] == "True":
                print("reading egg inv..")
                await self.client.egg_check()
                await asyncio.sleep(15)

            print("start capture..")
            await self.client.pokemon()
        except IndexError:
            print("Error: index out of range")
        
        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Startup(client))
