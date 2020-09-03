from dateutil import parser
from dateutil import tz
import logging
import discord
import buglebot


@buglebot.bot.command(pass_context=True)
async def set_orders_channel(ctx, *, channel: discord.TextChannel):
    logging.debug('Got set_orders_channel command')
    buglebot.db.guilds.update_one({'guild_id': ctx.guild.id}, {'$set': {'orders_channel_id': channel.id}})
    await ctx.message.channel.send('Orders channel set!')


@buglebot.bot.command(pass_context=True)
async def set_orders_header(ctx, *, header=''):
    logging.debug('Got set_orders_header command')
    buglebot.db.guilds.update_one({'guild_id': ctx.guild.id}, {'$set': {'orders_header_message': header}})
    await ctx.message.channel.send('Orders header set!')


@buglebot.bot.command(pass_context=True)
async def orders(ctx, time, orders_message):
    guildinfo = buglebot.db.guilds.find_one({'guild_id': ctx.guild.id})

    if guildinfo['orders_channel_id'] is None:
        # Error, no channel to send orders to!
        await ctx.send('No orders channel set! Set it with !buglebot set_orders_channel')
        return

    channel = buglebot.bot.get_channel(guildinfo['orders_channel_id'])
    if channel is None:
        await ctx.send('Could not find orders channel. Did it get deleted?')
        return

    try:
        time = time.replace('_', ' ')
        orders_time = parser.parse(time)
        # orders_time = orders_time.astimezone(tz.UTC)
        logging.debug(f'{orders_time}')
    except ValueError:
        await ctx.send(
            'Could not parse orders time. Make sure it is in the format "%Y-%m-%d\_%H:%M:%S%z".\n'
            'Ie. 2020-09-01\_18:00:00-0500 => Sept. 1st 2020 at 6PM EST.\n'
            'PLEASE NOTE the %z refers to your timezone offset. So EST is -0500, UTC is +0000, and CET is +0100'
        )
        return

    if guildinfo['orders_header_message']:
        orders_message = ' '.join((guildinfo['orders_header_message'], orders_message))

    message_info = await channel.send(orders_message)

    orders_record = {
        'time': orders_time,
        'message_id': message_info.id,
        'guild_id': message_info.guild.id,
        'channel_id': message_info.channel.id
    }

    buglebot.db.orders.insert_one(orders_record)