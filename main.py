import os
from PyPDF2 import PdfWriter, PdfReader
from pages import page_start
from classifier import questionify
from converter import pages_to_image

import discord
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_NAME = "NSBHS Question bank"
CHANNEL_NAME = "4u-mathematics-stacking"

def main():
    folder_path = "examples"
    
    questions = []
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        pages = PdfReader(file_path).pages
        start_page = page_start(pages)
        pages = pages[start_page:]
        paper_name = file_path.split("-")[0].split("/")[-1]
        questions.extend(questionify(paper_name, pages, ext1=False))


    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        channel = discord.utils.get(client.get_all_channels(), guild__name=SERVER_NAME, name=CHANNEL_NAME)
        tags = channel.available_tags
        for question in questions:
            images = pages_to_image(question.pages)
            thread = await channel.create_thread(name=question.paper, content='', files=images, applied_tags=sorted([tag for tag in tags if tag.name in question.tags], key=lambda x : len(x.name))[:5], auto_archive_duration=4320)
                
        await client.close()
    
    client.run(DISCORD_TOKEN)


def clear_channel():
    """Clears all threads in the channel
    """
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        channel = discord.utils.get(client.get_all_channels(), guild__name=SERVER_NAME, name=CHANNEL_NAME)
        for thread in channel.threads:
            await thread.delete()
        await client.close()
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
