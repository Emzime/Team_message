import discord
from discord.ext import commands
from github import Github
from config import DISCORD_TOKEN, DISCORD_CHANNEL, GITHUB_TOKEN, GITHUB_REPO, GITHUB_FILE

# Initialise le client Discord avec les intentions
intents = discord.Intents.default()
# Active l'intention pour accéder aux informations des membres
intents.members = False

# Initialise le client Discord en utilisant les intentions
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration du bot Discord et GitHub
TOKEN = DISCORD_TOKEN
GITHUB_TOKEN = GITHUB_TOKEN
GITHUB_REPO = GITHUB_REPO


async def update_markdown_file():
    # Authentification GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)

    # Récupération du salon "subspace" par son nom
    subspace_channel = discord.utils.get(bot.get_all_channels(), name=DISCORD_CHANNEL)

    # Récupération du dernier message du salon
    async for message in subspace_channel.history(limit=1):
        # Nom de l'auteur du message
        author_name = message.author.name
        # Contenu du message
        message_content = message.content
        # Formatage du contenu avec le nom de l'auteur
        new_content = f"{author_name}: {message_content}"
        # Chemin relatif complet du fichier dans le dépôt GitHub
        file_path = GITHUB_FILE
        # Suppression du contenu actuel du fichier
        file = repo.get_contents(file_path)
        repo.update_file(file_path, "Mise à jour du fichier", new_content, file.sha)


# Événement on_message pour appeler la fonction de mise à jour du fichier
@bot.event
async def on_message(message):
    # Vérifie que le message provient du salon "subspace" et que l'auteur n'est pas le bot lui-même
    if message.channel.name == DISCORD_CHANNEL and message.author != bot.user:
        await update_markdown_file()

    # Traitement des commandes
    await bot.process_commands(message)


# Événement on_raw_message_edit pour appeler la fonction de mise à jour du fichier lorsque le dernier message est modifié
@bot.event
async def on_raw_message_edit(payload):
    # Récupération des données du message modifié
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Vérifie que la modification a eu lieu dans le salon "subspace" et que l'auteur n'est pas le bot lui-même
    if channel.name == DISCORD_CHANNEL and message.author != bot.user:
        await update_markdown_file()


# Événement de connexion du bot Discord
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')


# Démarrage du bot Discord
bot.run(TOKEN)
