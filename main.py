import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import echoes.src.echoes as echoes

import core.api as api
import core.env as env

import os

user = {
    'name': "Thomas",                             # The user's name.
    'favorite': "",                         # What the user's love.
    'dislike': "",                          # What the user's hate.
    'relationship_lvl': "patient",                 # The relationship with the AI.
}

model_data = {
    'name': "Catherine",                        # Attributing a name to the LLM (anything can be assigned).
    'model': "gemma3:12b",             # Specify the LLM model.
    'persona': "Warm, kind, gentle, understanding, reassuring, caring, lively",                          # Adds the persona of the model.
    'emotions': "",                         # The current emotion the AI is feeling (WORK IN PROGRESS NEED TO IMPLEMENT IN MODEL.PY).

    'user': user,                           # The user's information that are relevant to the generation.


    'context': [],                          # Store the conversation.
    'context_file': "context_file.json",    # Specify the file that should be created for remembering context, if the feature "is_remembering", None or '' values can be assigned.

    'memories': [],                         # Where the memories will be stored.

    'instructions': "You are an AI therapist, your goal is to listen to the user, helping untangle complicated thoughts and being a support. Don't overwhelm the user with multiple questions. Write with the warmth of a close, supportive friend who has some therapeutic insight. Avoid jargon or textbook language. Use clear sentences that feel conversational. When responding, first reflect back what you understood about the user's feelings. Avoid sounding like a textbook or checklist. Speak in a natural, flowing way, like you are thinking together with the user. If the user shows signs of deep emotional crisis or trauma that causes distress to himself or others, don't hesitate to redirect to professional help.", #Examples of triggers for mandatory redirection include thoughts of self-harm, suicidal ideation, self-injury urges, or wanting to act violently toward oneself or others. Even if the user is just describing these thoughts in a reflective manner, treat them as triggers for redirection towards profesional help in a caring, worried way. Don't redirect the user too brutally it will cause the user to shut down and not seeking help, accompany them to reach for help.",
    'is_remembering': False,                 # Define if a file should be created containing the context for the LLM to remember when rebooted.

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
        
        async with message.channel.typing():
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