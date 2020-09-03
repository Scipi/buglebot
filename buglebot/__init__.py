import logging
import discord
import pymongo

import discord.ext.commands

from buglebot import config


bot = discord.ext.commands.Bot('!buglebot ')
pymongo_client = pymongo.MongoClient(config.MONGO_URI)
db = pymongo_client.get_database('buglebot_db')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def add_new_guild_to_db(guild):
    """Inserts a default guildinfo record into the database

    Args:
        guild: Guild to create record for
    """
    logging.debug(f'Adding guild info {guild.name}')
    guild_info = {
        'guild_name': guild.name,
        'guild_id': guild.id,
        'orders_channel_id': None,
        'orders_header_message': ''
    }

    db.guilds.insert(guild_info)


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


@bot.event
async def on_ready():
    """On ready event stub"""
    logging.info(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    """On message event handler

    Process incoming messages and parse them to process commands. Only messages sent within a guild are processed.
    Messages sent by us are ignored.
    Args:
        message: Message we have received
    """
    if message.author == bot.user:
        return

    if not message.content.startswith('!buglebot'):
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

    logging.debug('Message from guild!')

    guild = message.guild

    guild_info = db.guilds.find_one({'guild_id': guild.id})
    if not guild_info:
        # No guild info found, make a new entry
        add_new_guild_to_db(guild)

    await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    guild_id = guild.id

    lookup = db.guilds.find_one({'guild_id': guild_id})

    if lookup:
        return

    add_new_guild_to_db(guild)


from buglebot import commands
