import os
import re
import random
import string
import asyncio
from itertools import cycle
from loguru import logger

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from utils.metadata import ao3_metadata, ffn_metadata

# to use repl+uptime monitor
from utils.bot_uptime import start_server

client = discord.Bot()

load_dotenv()
TOKEN = os.getenv('DISCORD_CANARY_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"

with open("data/status_quotes.txt", "r") as file:
    quotes = cycle(file.readlines())


# @tasks.loop(seconds=1)
# async def bot_status():
#     """
#     An activity status which cycles through the
#     status_quotes.txt every 15s
#     """

#     await client.wait_until_ready()

#     await client.change_presence(
#         activity=discord.Activity(
#             type=discord.ActivityType.watching,
#             name=(next(quotes)).strip()
#         )
#     )

#     await asyncio.sleep(15)


@client.slash_command(name="linkffn", description="To search for fanfiction in fanfiction.net")
async def linkffn(ctx, message):
    """
    To search for fanfiction in fanfiction.net
    """
    log_flag = False
    try:
        query = message.lower()
        await ctx.defer()

        if re.search("-log", query, re.IGNORECASE) \
                and int(ctx.author.id) == int(OWNER_ID):

            log_flag = True

        # unique id for each request
        request_id = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))

        if log_flag:
            # create log directory
            if not os.path.exists('data/logs'):
                os.makedirs('data/logs')

            logger.add(
                f"data/logs/{request_id}.log",
                format="{time:YYYY-MM-DD HH:mm:ss!UTC} | {level} | {file}:{function}:{line} - {message}")

        if ctx.author == client.user:
            return  # Do not reply to yourself

        if ctx.author.bot:
            return  # Do not reply to other bots

        if ctx.guild is None:
            logger.info("Not allowed to reply to DMs.")
            return  # Do not reply to DMs

        else:

            logger.info("linkffn command was used. Searching ffnet")
            logger.info("Sleeping for 1s to avoid ratelimit")
            await asyncio.sleep(1)

            msg = query.replace("-log", "")

            embed_pg = ffn_metadata(msg)

            if embed_pg is None:  # if not found in AO3, search in FFN
                logger.info(
                    "Fanfiction not found in FFN, trying to search AO3")
                embed_pg = ao3_metadata(msg)

            logger.info(
                f"Sending embed to Channel-> { ctx.channel.guild}:{ctx.channel.name}")
            try:
                sent_msg = await ctx.respond(embed=embed_pg, mention_author=False)
            except Exception:
                sent_msg = await ctx.channel.send(embed=embed_pg)

        if log_flag:
            try:
                await message.reply(file=discord.File(
                    f"data/logs/{request_id}.log"
                ), mention_author=False)

            except Exception:
                await ctx.channel.send(file=discord.File(
                    f"data/logs/{request_id}.log"
                ))

            # delete the log
            os.remove(f"data/logs/{request_id}.log")

    except Exception as e:
        print(e)
        if log_flag:
            # remove log if the bot is not allowed to send msgs to this channel
            os.remove(f"data/logs/{request_id}.log")

    finally:
        try:
            def check(reaction, user):
                return str(reaction.emoji) == '👎' and \
                    not user.bot and reaction.message.id == sent_msg.id and \
                    user.id == ctx.author.id

            await client.wait_for('reaction_add',
                                  check=check, timeout=30.0)
            await sent_msg.delete()

        except Exception:
            pass


@client.slash_command()
async def linkao3(ctx, message):
    """
    To search for fanfiction in archiveofourown.org
    """
    log_flag = False
    try:
        query = message.lower()
        await ctx.defer()

        if re.search("-log", query, re.IGNORECASE) \
                and int(ctx.author.id) == int(OWNER_ID):

            log_flag = True

        # unique id for each request
        request_id = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))

        if log_flag:
            # create log directory
            if not os.path.exists('data/logs'):
                os.makedirs('data/logs')

            logger.add(
                f"data/logs/{request_id}.log",
                format="{time:YYYY-MM-DD HH:mm:ss!UTC} | {level} | {file}:{function}:{line} - {message}")

        if ctx.author == client.user:
            return  # Do not reply to yourself

        if ctx.author.bot:
            return  # Do not reply to other bots

        if ctx.guild is None:
            logger.info("Not allowed to reply to DMs.")
            return  # Do not reply to DMs

        else:

            logger.info("linkao3 command was used. Searching ao3")
            logger.info("Sleeping for 1s to avoid ratelimit")
            await asyncio.sleep(1)

            msg = query.replace("-log", "")

            embed_pg = ao3_metadata(msg)

            if embed_pg is None:  # if not found in AO3, search in FFN
                logger.info(
                    "Fanfiction not found in AO3, trying to search FFN")
                embed_pg = ffn_metadata(msg)

            logger.info(
                f"Sending embed to Channel-> { ctx.channel.guild}:{ctx.channel.name}")
            try:
                sent_msg = await ctx.respond(embed=embed_pg, mention_author=False)
            except Exception:
                sent_msg = await ctx.channel.send(embed=embed_pg)

        if log_flag:
            try:
                await ctx.reply(file=discord.File(
                    f"data/logs/{request_id}.log"
                ), mention_author=False)

            except Exception:
                await ctx.channel.send(file=discord.File(
                    f"data/logs/{request_id}.log"
                ))

            # delete the log
            os.remove(f"data/logs/{request_id}.log")

    except Exception as e:
        print(e)
        if log_flag:
            # remove log if the bot is not allowed to send msgs to this channel
            os.remove(f"data/logs/{request_id}.log")

    finally:
        try:
            def check(reaction, user):
                return str(reaction.emoji) == '👎' and \
                    not user.bot and reaction.message.id == sent_msg.id and \
                    user.id == ctx.author.id

            await client.wait_for('reaction_add',
                                  check=check, timeout=30.0)
            await sent_msg.delete()

        except Exception:
            pass


# bot_status.start()
start_server()
client.load_extension("cogs.settings")
client.load_extension("cogs.help")
client.run(TOKEN)
