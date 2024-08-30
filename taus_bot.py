import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import util

load_dotenv()
TOKEN = os.getenv('TOKEN')


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        msg = message.content
        if message.author.id == self.user.id:
            return

        if msg.startswith('$help') or msg.startswith('$h'):
            help_str = util.read_md("help")
            await message.reply(help_str)

        if msg.startswith('$server_status') or msg.startswith('$status'):
            await message.reply(util.send_cmd("status"))

        if msg.startswith('$server_start') or msg.startswith('$start'):
            await message.reply("Trying to start server, Please wait for a response before entering any other commands.")
            await message.reply(util.start_server())

        if msg.startswith('$server_save') or msg.startswith('$save'):
            await message.reply("Trying to start save")
            await message.reply(util.send_cmd("save"))

        if msg.startswith('$server_stop') or msg.startswith('$stop'):
            await message.reply("Trying to stop server")
            await message.reply(util.send_cmd("quit"))

        if msg.startswith('$modlist'):
            mods = "modlist_1_2"
            util.sort_md(mods)
            sorted_mods = (mods+"_sorted")
            modlist = util.read_md(sorted_mods)
            if len(modlist) > 2000:
                print("chunking")
                chunks = modlist.split('\n')
                chunk = ""
                for i in range(len(chunks)):
                    print(i)
                    if (i % 75 == 0 and i != 0) or len(chunk) > 1900 or i == len(chunks)-1:
                        await message.channel.send(chunk)
                        chunk = ""
                    else:
                        chunk += chunks[i] + "\n"
                print(chunks)
                print("done")
            else:
                await message.channel.send(modlist)

        if msg.startswith('$install'):
            rev = "1_2"
            modpack = discord.File(f"./modpacks/TauS_Modpack_{rev}.zip")
            await message.reply(f"Here is the current TauS Modpack Rev {rev}", file=modpack)

        if msg.startswith('$kick') and message.author.name == "0ddshadow":
            user = msg[6:]
            util.send_cmd("kick", user)


def init():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Client(intents=intents)
    bot.run(TOKEN)


if __name__ == "__main__":
    init()
