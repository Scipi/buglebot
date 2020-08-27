import logging
import discord
import pymongo
from bugle_bot import config


client = discord.Client()
pymongo_client = pymongo.MongoClient(config.MONGO_URI)
db = pymongo_client.get_database('buglebot_db')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_string = message.content

    if not message_string.startswith('!buglebot'):
        return

    logging.debug('Got message!')

    if not message.guild:
        # Message not sent within a guild No context with which to work, so send a default response and leave
        await message.channel.send(' ' .join((
                'Hi. This bot only works within servers and not PMs. Please add this bot to a server and see it\'s',
                'commands with !buglebot help.'
            ))
        )
        return

    guild = message.guild
    guild_id = message.guild.id

    guild_info = db.guilds.find_one({'guild_id': guild_id})

    if not guild_info:
        # No guild info found, make a new entry
        logging.debug(f'Adding guild info {guild.name}')
        guild_info = {
            'guild_name': guild.name,
            'guild_id': guild_id,
            'orders_channel_id': None,
            'announcement_roles': []
        }

        db.guilds.insert(guild_info)

    cmd_string = message_string.split('!buglebot ')[1]

    logging.debug(f'Got CMD string: {cmd_string}')

    if cmd_string.startswith('help'):
        # Help message
        pass

    if cmd_string.startswith('set_orders_channel'):
        parsed_msg = cmd_string.split()
        if len(parsed_msg) < 2:
            # Error
            logging.debug('set_orders_channel command received with no channel')
            await message.channel.send('Please specify a text channel name')

        channel_name = parsed_msg[1]
        channels = [c.id for c in guild.text_channels if c.name == channel_name]
        if channels:
            db.guilds.update_one({'guild_id': guild_id}, {'$set': {'orders_channel_id': channels[0]}})
            await message.channel.send('Orders channel set!')
        else:
            logging.debug(f'No channel found: {guild.name}: {channel_name}')
            await message.channel.send(f'Unable to find text channel with name {channel_name}')


@client.event
async def on_guild_join(guild):
    guild_id = guild.id

    lookup = db.guilds.find_one({'guild_id': guild_id})

    if lookup:
        return

    guild_info = {
        'guild_name': guild.name,
        'guild_id': guild_id,
        'orders_channel_id': None,
        'announcement_roles': []
    }

    db.guilds.insert(guild_info)
