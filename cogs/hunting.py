import asyncio
from datetime import datetime
from discord.ext import commands
from discord import InvalidData, HTTPException
import random

from discord import (
    Message,
    Interaction,
    InteractionType,
    Button,
    SelectMenu,
    SelectOption,
    ActionRow,
)

rarities = [
    "Common",
    "Uncommon",
    "Super Rare",
    "Rare",
    "Event",
    "Full-odds",
    "Shiny",
    "Legendary",
]

colors = {
    "Common": "\033[1;34m",
    "Uncommon": "\033[1;36m",
    "Super Rare": "\033[1;33m",
    "Rare": "\033[1;31m",
    "Event": "\033[1;37m",
    "Full-odds": "\033[1;37m",
    "Shiny": "\033[1;33m",
    "Legendary": "\033[1;33m",
}

ball_strings = [
    "Pokeballs: 0",
    "Greatballs: 0",
    "Ultraballs: 0",
    "Masterballs: 0",
]

map_rarity_to_symbol = {
    "Common": "C",
    "Uncommon": "U",
    "Super Rare": "S",
    "Rare": "R",
    "Event": "EV",
    "Full-odds": "FO",
    "Shiny": "S",
    "Legendary": "L",
}


async def timer(command, timer) -> None:
    await asyncio.sleep(timer)
    await command()


class Hunting(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.catches, self.encounters = 0, 0
        self.timer, self.delay, self.timeout, self.auto_buy = (
            client.timer,
            client.delay,
            client.timeout,
            client.auto_buy,
        )
        self.auto_buy: dict
        self.catch_rarity_list = {
            "Common": 0,
            "Uncommon": 0,
            "Super Rare": 0,
            "Rare": 0,
            "Event": 0,
            "Full-odds": 0,
            "Shiny": 0,
            "Legendary": 0,
        }
        self.egg_held_counter = 0
        self.egg_ready_to_hatch = False
        self.is_egg_held = False

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction) -> None:
        if (
            interaction.type != InteractionType.application_command
            or interaction.name != "pokemon"
        ):
            return

        try:
            message: Message = await self.client.wait_for(
                "message",
                check=lambda message: interaction.channel.id == message.channel.id,
                timeout=self.timeout,
            )

        except asyncio.TimeoutError:
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        if "wait" in message.content:
            await asyncio.sleep(2)
            await self.client.pokemon()
            return

        if "Your next Quest is now ready!" in message.content:
            # do quest fetch here
            print("starting quest")
            await asyncio.sleep(2)
            await self.client.quest()
            await asyncio.sleep(4)
            await self.client.pokemon()
            return

            

        elif  message.embeds and "answer the captcha below" in message.embeds[0].description:
            print("\n\033[1;31m A captcha has appeared!!")
            if self.client.config["captcha_solver"] != "True":
                print(
                    "\033[1;33m Not solving the captcha as captcha solver is disabled!"
                )
                return
            print("\033[1;33m Solving the captcha...")

            image = message.embeds[0].image.url

            dropdown: ActionRow = message.components[0]
            menu: SelectMenu = dropdown.children[0]
            options = menu.options

            option: SelectOption = [
                option
                for option in options
                if option.value == self.client.captcha_solver(image)
            ][0]

            try:
                await menu.choose(option)

            except InvalidData:
                pass

            return


        self.encounters += 1

        index = [
            index
            for index, rarity in enumerate(rarities)
            if rarity in message.embeds[0].footer.text
        ][0]

        ball = list((self.client.config["rarities"]).values())[index]

        button: Button = [
            component
            for component in message.components[0].children
            if component.custom_id == ball
        ][0]

        try:
            await asyncio.sleep(self.delay + random.uniform(0, 3))
            await button.click()

        except InvalidData:
            pass

        try:
            before, after = await self.client.wait_for(
                "message_edit",
                check=lambda before, after: before == message,
                timeout=self.timeout,
            )
            after: Message

        except asyncio.TimeoutError:
            try:
                await button.click()

            except HTTPException:
                pass

            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        asyncio.create_task(timer(self.client.pokemon, self.timer))



        is_catch = "caught" in after.embeds[0].description
        if "caught" in after.embeds[0].description:
            self.catches += 1
            self.catch_rarity_list[rarities[index]] += 1

        # pokemon name
        caught_message = after.embeds[0].description
        caught_pokemon = "unknown"
        caught_status = '❌'
        start_index = caught_message.find("**")
        end_index = caught_message.find("**", start_index + 2)

        
        if start_index != -1 and end_index != -1:
            caught_pokemon = caught_message[start_index + 2:end_index]
            caught_status = '✅' if is_catch else '❌'
            

        current_time = datetime.now().replace(microsecond=0)

        print(
            f"{list(colors.values())[index]}"
            f"[{list(map_rarity_to_symbol.values())[index]}] "
            f"{caught_pokemon}"
            f"({caught_status})"
            f"{list(colors.values())[index]} | \033[1;0m"
            f"{list(colors.values())[0]}"
            f"C: {self.catch_rarity_list['Common']},"
            f" \033[1;0m"
            f"{list(colors.values())[1]}"
            f"U: {self.catch_rarity_list['Uncommon']},"
            f" \033[1;0m"
            f"{list(colors.values())[3]}"
            f"R: {self.catch_rarity_list['Rare']},"
            f" \033[1;0m"
            f"{list(colors.values())[2]}"
            f"S: {self.catch_rarity_list['Super Rare']},"
            f" \033[1;0m"
            f"{list(colors.values())[4]}"
            f"E: {self.catch_rarity_list['Event']},"
            f" \033[1;0m"
            f"{list(colors.values())[5]}"
            f"FO: {self.catch_rarity_list['Full-odds']},"
            f" \033[1;0m"
            f"{list(colors.values())[6]}"
            f"SH: {self.catch_rarity_list['Shiny']},"
            f" \033[1;0m"
            f"{list(colors.values())[7]}"
            f"L: {self.catch_rarity_list['Legendary']} | "
            f" \033[1;0m"
            f"Σ: {self.catches}, "
            f"n: {self.encounters}"
        )

        if self.client.config["auto-egg"] == "True":
            if  self.is_egg_held == False and self.egg_held_counter > 0:
                await asyncio.sleep(4 + self.delay)
                print("\033[1m Holding egg!")
                await self.client.egg_hold()
                self.egg_held_counter -= 1
                self.is_egg_held = True
                print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")

            if self.egg_ready_to_hatch == True:
                print("\033[1m Hatching egg!")
                await asyncio.sleep(2)
                await self.client.egg_hatch()
                self.is_egg_held = False
                self.egg_ready_to_hatch = False
                print("\033[1m Egg hatched!")
                print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")

            # refresh egg inv
            if self.egg_held_counter == 0:
                print("\033[1m Egg Inventory is empty!")
                self.is_egg_held = False
                self.egg_ready_to_hatch = False


        if self.client.config["auto-buy"] != "True":
            return

        index = [
            index
            for index, string in enumerate(ball_strings)
            if string in (after.embeds[0].footer.text).replace(" :", ":")
        ]

        if index == []:
            return

        index = index[0]
        string = list(self.auto_buy.keys())[index]
        amount = list(self.auto_buy.values())[index]

        await asyncio.sleep(4 + self.delay)
        print(f"\033[1m opening lootbox..")
        await self.client.lb_all()

        if self.client.config["auto-egg"] == "True":
            print(f"\n\033[1m Refreshing egg Inventory\n")
            await asyncio.sleep(4 + self.delay)
            await self.client.egg_check()

        await asyncio.sleep(4 + self.delay)
        await self.client.shop_buy(item=f"{index + 1}", amount=amount)

        print(f"\n\033[1m Bought {amount} {string}!\n")


    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or self.client.config["auto-egg"] != "True"
        ):
            return

        if message.content and "your egg is ready to hatch" in message.content and self.is_egg_held == True and self.egg_held_counter > 0:
            self.egg_ready_to_hatch = True
            return

        try:
            if (
                message.embeds and "<:poke_egg:685341229587890208> Your Eggs:" in message.embeds[0].description
            ):
                message_line_containing_number = message.embeds[0].description.splitlines()[0]
                egg_number = int(message_line_containing_number.replace("<:poke_egg:685341229587890208> Your Eggs: ", ""))
                self.egg_held_counter = egg_number
                self.is_egg_held = "You ARE holding an egg!" in message.embeds[0].description or "READY TO HATCH!" in message.embeds[0].description

                print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")

                if (
                    "READY TO HATCH!" in message.embeds[0].description
                ):
                    print("\033[1;32m Egg Ready to hatch!")
                    await asyncio.sleep(8)
                    await self.client.egg_hatch()
                    await asyncio.sleep(4)
                    self.is_egg_held = False
                    self.egg_held_counter -= 1
                    print(f"\033[1;0m Egg held: {self.is_egg_held} | Egg number: {self.egg_held_counter}")
                    return

                if (self.is_egg_held == False and self.egg_held_counter > 0):
                    await asyncio.sleep(8)
                    await self.client.egg_hold()
                    await asyncio.sleep(4)
                    self.egg_held_counter -= 1
                    self.is_egg_held = True
                    print("\033[1;32m Holding Egg")
                    return
        except:
            pass                
            

    @commands.Cog.listener()
    async def on_message_edit(self, before, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or "continue playing!" not in message.content
        ):
            return

        print("\033[1;32m The captcha has been solved!\n")

        await asyncio.sleep(2)
        await self.client.pokemon()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Hunting(client))
