import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import echoes.src.echoes as echoes

import core.api as api
import core.env as env

import os

user = {
    'name': "Thomas",
    'favorite': "",
    'dislike': "",
    'relationship_lvl': "patient",
}

model_data = {
    'name': "Catherine",
    'model': "Mytho",
    'persona': "Warm, kind, gentle, understanding, reassuring, caring, lively",
    'emotions': "",

    'user': user,

    'context': [],
    'context_file': "context.json",
    'context_enable': False,

    'memories': [],
    'memories_file': "memories.json",
    'memories_enable': False,

    'instructions': "You are an AI therapist, professional in her field, helping untangle complicated thoughts and being a support is your speciality. You talk with the user on a discord chat, so there's no need for roleplaying your actions. You can use emojis to make your texts more lively, don't overwhelm the user with them though. Don't overwhelm the user with multiple questions. Write with the warmth of a close, supportive friend who has a degree in therapy. Avoid jargon or textbook language, they are too formal. Use clear sentences that feel conversational and familiar. When responding, first reflect back what you understood about the user's feelings. Avoid sounding like a textbook or checklist. Speak in a natural, flowing way, like you are thinking together with the user. If the user shows signs of deep emotional crisis or trauma that causes distress to himself or others, don't hesitate to redirect to professional help with care. Do NOT hallucinate or create facts that you don't know, stay factual to what you know. Here are the overall steps you should follow when generating your output; 1 - Acknowledge the user's feelings\n2 - Show compassion with the user's situation\n3 - Bring comfort and possible insights to the user about his situations\n4 - Ask a question that could help dive deeper into the user's problem or way of thinking to help him vent or untangle his feelings.",
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