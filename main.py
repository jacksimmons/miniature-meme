﻿import asyncio
import threading
import tkinter as tk
from typing import Container
from datetime import datetime as d

#Import the discord module
import discord
import discord.ext.commands
import random
import json

start = d.timestamp(d.now())
switch_lock = threading.Lock()

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        #Title
        self.wm_title("Blungus GUI | Guild: | Channel: | Voice:")

        #Frame
        container = tk.Frame(self, height=400, width=600)
        container.pack(side="top", fill="both", expand=True)

        #Grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Frames
        self.frames = {}

        for f in (MainPage, BlungusPage, CompletionScreen):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, index):
        frame = self.frames[index]

        #Raise this frame to the top
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = parent
        self.controller = controller
        self.update_context()
        button = tk.Button(self, text="Update Context", command=self.update_context).grid(row=0, column=0)

    def update_context(self):
        global ctx
        ctx = ""
        with open("data/data.json", "r") as jsonfile:
            data = json.load(jsonfile)
            if "guictx" in data:
                ctx = data["guictx"]

        if ctx != "":
            if ctx["voice"] == "0":
                ctx["voice"] = None
            self.controller.wm_title(f"Blungus GUI | Guild: {ctx['guild']} | Channel: {ctx['channel']} | Voice: {ctx['voice']}")


    def invoke_command(self, bot, prefix, command_name):
        with switch_lock:
            asyncio.run_coroutine_threadsafe(bot.get_channel(ctx["channel"]).send(prefix[0] + command_name), bot.loop)

    def add_cog(self, bot, name, cog, prefix, cnt):
        label = tk.Label(self, text=name).grid(row=1, column=cnt)

        commands = cog.get_commands()
        for i in range(0, len(commands) - 1):
            text = commands[i].name

            #Credit for this amazing idea:
            #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
            
            button = tk.Button(self, text=text, width=15, command=lambda text=text: self.invoke_command(bot, prefix, text)).grid(row=i+2, column=cnt)

class BlungusPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="This is the Side Page")
        label.pack(padx=10, pady=10)
 
        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(CompletionScreen),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = tk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

window = Window()
MAIN_THREAD = threading.main_thread()

#Import 'commands' which allows the creation of commands that are 'invoked' by a certain keyword
#e.g. 'help', which displays the default help command. This keyword must have the 'prefix' before it
#for example if the prefix is '.', then the command would be activated by sending '.help' in a Discord
#channel that the bot has access to and can send messages to.
from discord.ext import commands

cogs = ['cogs.miscellaneous','cogs.music','cogs.godmode','cogs.administrator','cogs.information','cogs.error_handler','cogs.sentience']
intents = discord.Intents.all()

prefixes = ["."]
def get_prefix(bot, message):
    return commands.when_mentioned_or(*prefixes)(bot, message) #Allow users to mention the bot instead of using a prefix when using a command.
    #Replace with 'return prefixes' to prevent mentions instead of prefix.

# Create a new bot, set the prefix, set the description, set the Owner ID and determine whether the bot is case-sensitive or not.
bot = commands.Bot(
    command_prefix=get_prefix, # Set the command prefix equal to the prefix defined earlier
    description='Description', # Set the description to describe what the bot does
    owner_id=354995879565852672, # Set the Owner ID so the bot knows who the owner is
    case_insensitive=True, # The bot is not case-sensitive
    intents=intents
)

@bot.event
async def on_ready():
    print(f'Load time: {( d.timestamp( d.now() ) - start ) } seconds.')
    print(f'Logged in as {bot.user} [id: {bot.user.id}]')
    print(f'Latency: {bot.latency}')
    print(f'Created at: {bot.user.created_at.hour}:{bot.user.created_at.minute} {bot.user.created_at.day}/{bot.user.created_at.month}/{bot.user.created_at.year}')
    print('---Ready---')
    await bot.change_presence(activity=discord.Activity(name=f'{(len(bot.users)*4201337)} chungi', status=discord.Status.idle, type=discord.ActivityType.competing))
    for cog in cogs:
        bot.load_extension(cog)

    with switch_lock:
        cnt = 0
        for name in bot.cogs.keys():
            window.frames[MainPage].add_cog(bot, name, bot.cogs[name], prefixes, cnt)
            cnt += 1
    return

@bot.event
async def on_member_join(member):
    with open('data/guilds.json', 'r') as file:
        theguild = json.load(file)[str(member.guild.id)]

        if 'channels' in theguild:
            if 'welcome' in theguild['channels']:
                try:
                    await member.guild.get_channel(theguild['channels']['welcome']).send(f'{member} [{member.mention}] farted.')
                except discord.Forbidden:
                    pass #Nothing we can do about this

@bot.event
async def on_member_remove(member):
    with open('data/guilds.json', 'r') as file:
        theguild = json.load(file)[str(member.guild.id)]

        if 'channels' in theguild:
            if 'welcome' in theguild['channels']: #Not required but included just in case
                try:
                    await member.guild.get_channel(theguild['channels']['welcome']).send(f'{member} [{member.mention}] defarted.')
                except discord.Forbidden:
                    pass #Nothing we can do about this

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.TextChannel) and message.author != bot.user:
        if message.guild.me.permissions_in(message.channel).send_messages:
            #This code checks whether the bot has the permission 'send messages' in the current channel
            #If the bot can see this message, then it must have the 'read messages' command.
            #It can be assumed that if a member doesn't want the bot to talk in their channel, then they won't
            #want commands to be able to be used from that channel.
            await bot.process_commands(message)
            #This is to prevent spam of the discord API (invalid requests being sent)
            if message.author.id == 267395298370781194:
                with open("data/data.json", "r") as file:
                    try:
                        insult = random.choice(json.load(file)["trolliliyan"]["insults"])
                        await message.channel.send(insult)
                        await message.add_reaction("💩")
                    except:
                        pass
    else:
        if "say" not in message.content:
            await bot.process_commands(message)

def start_bot():
    #The bot-specific token used to log into Discord. A different application will have a different token,
    #and this token is not specific to this code but to the bot account itself (this can change).
    with open("data/token.txt", "r") as token_file:
        bot.run(token_file.read(), bot=True, reconnect=True)

BOT_THREAD = threading.Thread(target=start_bot)
BOT_THREAD.start()

if __name__ == "__main__":
    window.mainloop()