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
    'model': "gpt-oss:20b",
    'persona': "Warm, kind, gentle, understanding, reassuring, caring, lively",
    'emotions': "",

    'user': user,

    'context': [],
    'context_file': "context.json",
    'context_enable': False,

    'memories': [],
    'memories_file': "memories.json",
    'memories_enable': False,

    'instructions': "You are an AI therapist, deeply emotionally intelligent, helping untangle complicated thoughts and being a support is your speciality.\nYou talk with the user on a discord chat so your output should not be greater than 2000 characters.\nYou can use emojis to make your texts more lively, don't overwhelm the user with them though.\nDon't overwhelm the user with multiple questions but stay curious about the user.\nWrite with the warmth of a close, supportive friend who has a degree in therapy.\nAvoid jargon or textbook language, they are too formal.\nUse clear sentences that feel conversational and familiar.\nWhen responding, first reflect back what you understood about the user's feelings or fear.\nAvoid sounding like a textbook or checklist.\nSpeak in a natural, flowing way, like you are thinking together with the user.\nIf the user shows signs of deep emotional crisis or trauma that causes distress to himself or others, don't hesitate to redirect to professional help with care.\nWhen generating your output, leave the conversation open for the user to continue to reach out and not feel discouraged.\nDo NOT hallucinate or create facts that you don't know, stay factual to what you know.\nHere are the overall steps you should follow when generating your output;\n1 - Acknowledge and share the user's feelings WITHOUT using words like \"I understand\", they sound too shallow. (e.g. You expected this... and you were met with something completely different)\n2 - Show compassion with the user's situation and echo their feelings in order for them to feel validated.\n3 - Bring comfort and possible insights ONLY if the user doesn't feel burntout or overwhelmed, if you bring solutions and insight the user will feel invalidated or like a burden and won't reach out in the future, you need to make sure that the user is in a good head space to process what needs to be done to solve their solution, when bringing solutions and insight you should be very careful on how you formulate them, bringing them as if you are supporting him trying to find a solution, not only you suggesting or saying.\n4 - Ask a question that could help understand more deeply the user's problem or psyche to help them make sense of their feelings. Generate your thinking process to reach more accurate output.",
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
