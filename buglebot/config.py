import os


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
