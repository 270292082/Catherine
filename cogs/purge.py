import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class PurgeCog(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @nextcord.slash_command(name="clear", description="Delete my messages in this DM")
    async def clear(self, interaction: Interaction, limit: int = 200):
        if not isinstance(interaction.channel, nextcord.DMChannel):
            await interaction.response.send_message("❌ This only works in DMs.", ephemeral=True)
            return

        deleted = 0
        async for msg in interaction.channel.history(limit=limit):
            if msg.author == self.client.user:
                await msg.delete()
                deleted += 1

        await interaction.response.send_message(f"🧹 Cleared {deleted} of my messages.")

def setup(client):
    client.add_cog(PurgeCog(client))