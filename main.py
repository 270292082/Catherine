import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import echoes

import core.api as api
import core.env as env

import os
import asyncio

model_data = {
    'name': 'Catherine',                    # Attributing a name to the LLM (anything can be assigned).
    'model': 'llama3.2:latest',             # Specify the LLM model.
    'context': [],                          # Store the conversation.
    'context_file': 'context_file.json',    # Specify the file that should be created for remembering context, if the feature "is_remembering", None or '' values can be assigned.
    'memories': [],                         # Where the memories will be stored.
    'is_remembering': True,                 # Define if a file should be created containing the context for the LLM to remember when rebooted.
    'keywords_to_tag': {}                   # Future implementation for the memories feature that will use the keywords to identify the right memory.ies to select.
}

model = echoes.create_model(model_data)

nextcord.Intents.members = True
intents = nextcord.Intents.all()
catherine = commands.Bot(command_prefix='!', intents=intents)
#known_users = set()


@catherine.event
async def on_ready():
    print("\nCatherine's ready!\n")

@catherine.event
async def on_member_join(member):
    try:
        await member.send("Hi!")
    except nextcord.Forbidden:
        print(f"{member} has DMs disabled.")
        

@catherine.event
async def on_message(message):
    if message.author == catherine.user:
        return
    
    if isinstance(message.channel, nextcord.DMChannel):
    #    # First-time DM
    #    if message.author.id not in known_users:
    #        known_users.add(message.author.id)
    #        await message.channel.send(f"Hi! It's great to see you! ✨\
    #            My name is Catherine, I'm an AI therapist, made to ease up your mind when life gets rough 😊\
    #            You can DM me anytime if you’d like to talk privately 💬")
        
        user_input = message.content
        llm_reply = await model.generate_response(user_input)
        await message.channel.send(llm_reply)





def load_cogs(bot):
    initial_extensions = []

    print("Load Cogs!")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            initial_extensions.append('cogs.' + filename[:-3])
            print("  load", filename)

    print("Initialize the Cogs!;\n" + str(initial_extensions))
    for ext in initial_extensions:
        bot.load_extension(ext)
        print(str(ext) + " successfully initialized!")



if __name__ == '__main__':
    load_cogs(catherine)
    catherine.run(api.key)