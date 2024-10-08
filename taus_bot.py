import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import util
from util import log
from common import TOKEN, IP, CHANNEL_ID, NOTI_LIST
import asyncio


class Client(discord.Client):

    async def update_presence(self):
        if util.check_status():
            custom_activity = discord.CustomActivity(name="Server Online")
            await discord.Client.change_presence(self=self,
                                                 status=discord.Status.online, activity=custom_activity)
        else:
            custom_activity = discord.CustomActivity(name="Server Offline")
            await discord.Client.change_presence(self=self,
                                                 status=discord.Status.idle, activity=custom_activity)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.check_channel())

    async def check_channel(self):
        await self.wait_until_ready()
        user = await self.fetch_user(199625217381892096)
        first = True
        counter = 0
        old_names = []
        new_names = []
        channel = self.get_channel(int(CHANNEL_ID))  # channel ID goes here
        while not self.is_closed():
            members = channel.members
            for memeber in members:
                name = memeber.name
                if name not in new_names:
                    new_names.append(name)
                log(old_names)
                if name not in old_names:
                    log("appended")
                    old_names.append(name)

                    if name in NOTI_LIST:
                        if user.dm_channel is not None:
                            await user.dm_channel.send(
                                content=f"{name} joined the voice call")
                        else:
                            await user.create_dm()
            if not first:
                if counter == 2:
                    log("Counter Reset")
                    for name in old_names:
                        if name not in new_names:
                            old_names.remove(name)
                            log(f"Removed {name}")
                    counter = 0
            else:
                old_names = new_names
                log(old_names)
                first = False
            log(f"\n\n{'-'*20}\nOld names: {old_names}\nNew Names: {new_names}\n{'-'*20}\n")
            counter += 1
            log(f"{'-'*20}\nClearing new names")
            new_names = []
            log(f"Old names: {old_names}\nNew Names: {new_names}\nCounter: {counter}\n{'-'*20}")
            await asyncio.sleep(30)  # task runs every 60 seconds

    async def on_ready(self):
        log(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.update_presence()

    async def on_message(self, message):
        msg = message.content
        if message.author.id == self.user.id:
            return

        if msg.startswith('$help') or msg.startswith('$h'):
            help_str = util.read_md("help")
            await message.reply(help_str)
            await self.update_presence()

        if msg.startswith('$server_status') or msg.startswith('$status'):
            await message.reply(util.send_cmd("status"))

        if msg.startswith('$server_start') or msg.startswith('$start'):
            await message.reply("Trying to start server, Please wait for a response before entering any other commands.")
            await message.reply(util.start_server())
            await asyncio.sleep(60)  # Check if server is online in 60 seconds
            await self.update_presence()

        if msg.startswith('$server_save') or msg.startswith('$save'):
            await message.reply("Trying to start save")
            await message.reply(util.send_cmd("save"))

        if msg.startswith('$server_stop') or msg.startswith('$stop'):
            await message.reply("Trying to stop server")
            await message.reply(util.send_cmd("quit"))
            await self.update_presence()

        if msg.startswith('$modlist'):
            mods = "modlist_1_2"
            util.sort_md(mods)
            sorted_mods = (mods+"_sorted")
            modlist = util.read_md(sorted_mods)
            if len(modlist) > 2000:
                chunks = modlist.split('\n')
                chunk = ""
                for i in range(len(chunks)):
                    if (i % 75 == 0 and i != 0) or len(chunk) > 1900 or i == len(chunks)-1:
                        await message.channel.send(chunk)
                        chunk = ""
                    else:
                        chunk += chunks[i] + "\n"
            else:
                await message.channel.send(modlist)

        if msg.startswith('$install'):
            rev = "1_2"
            modpack = discord.File(f"./modpacks/TauS_Modpack_{rev}.zip")
            await message.reply(f"Here is the current TauS Modpack Rev {rev}", file=modpack)

        if msg.startswith('$kick') and message.author.name == "0ddshadow":
            user = msg[6:]
            await message.reply(util.send_cmd("kick", user))

        if msg.startswith('$ban') and message.author.name == "0ddshadow":
            user = msg[6:]
            await message.reply(util.send_cmd("ban", user))


def init():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Client(intents=intents)
    bot.run(TOKEN)


if __name__ == "__main__":
    init()
