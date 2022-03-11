import os
from dotenv import load_dotenv

from discord.ext.commands import Cog
from discord.commands import slash_command
from discord import Embed

load_dotenv()
BOT_ID = int(os.getenv('BOT_ID'))


class Settings(Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="To allow the bot to respond to all the channels")
    async def allow_all(self, ctx):
        """Adds send_message perm for all the channels."""

        if not ctx.author.guild_permissions.administrator:
            try:
                return await ctx.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))
            except Exception:  # send a DM if send message perms is not enabled
                return await ctx.author.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))

        bot_user = ctx.guild.get_member(BOT_ID)
        channel_list = ctx.guild.channels
        for channel in channel_list:
            try:
                await channel.set_permissions(
                    bot_user,
                    send_messages=True, manage_permissions=True)
            except Exception:
                pass

        embed = Embed(
            description="The bot will now start responding to all the channels."
        )
        await ctx.channel.send(embed=embed)

    @slash_command(description="To disallow the bot from responding to all the channels")
    async def disallow_all(self, ctx):
        """Removes send_message perm for all the channels."""

        if not ctx.author.guild_permissions.administrator:
            try:
                return await ctx.send(  # send message in channel
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))
            except Exception:  # send a DM if send message perms is not enabled
                return await ctx.author.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))

        embed = Embed(
            description="The bot will now stop responding to all the channels."
        )

        bot_user = ctx.guild.get_member(BOT_ID)
        channel_list = ctx.guild.channels
        for channel in channel_list:
            try:
                await channel.set_permissions(
                    bot_user,
                    send_messages=False, manage_permissions=True)
            except Exception:
                pass

        try:
            await ctx.channel.send(embed=embed)
        except Exception:
            embed = Embed(
                description="The bot is not allowed to send messages in that channel. Ask one of the server admins to use the `,allow` command in that channel to enable it."
            )
            await ctx.author.send(embed=embed)

    @slash_command(description="To allow the bot to respond to this channel")
    async def allow(self, ctx):
        """Adds send_message perm for the current channel."""

        if not ctx.author.guild_permissions.administrator:
            try:
                return await ctx.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))
            except Exception:  # send a DM if send message perms is not enabled
                return await ctx.author.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))

        bot_user = ctx.guild.get_member(BOT_ID)
        await ctx.channel.set_permissions(
            bot_user,
            send_messages=True, manage_permissions=True)

        embed = Embed(
            description="The bot will now start responding to this channel."
        )
        await ctx.channel.send(embed=embed)

    @slash_command(description="To disallow the bot from responding to this channel")
    async def disallow(self, ctx):
        """Removes send_message perm for current channel."""

        if not ctx.author.guild_permissions.administrator:
            try:
                return await ctx.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))
            except Exception:  # send a DM if send message perms is not enabled
                return await ctx.author.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))

        embed = Embed(
            description="The bot won't respond to this channel anymore."
        )

        bot_user = ctx.guild.get_member(BOT_ID)
        await ctx.channel.set_permissions(
            bot_user,
            send_messages=False, manage_permissions=True)

        try:
            await ctx.channel.send(embed=embed)
        except Exception:
            embed = Embed(
                description="The bot is not allowed to send messages in that channel. Ask one of the server admins to use the `,allow` command in that channel to enable it."
            )
            await ctx.author.send(embed=embed)

    @slash_command(description="To delete all non-bot messages from the channel i.e. all the users except the bot.")
    async def clear_messages(self, ctx):
        """Clears all non-bot messages"""

        if not ctx.author.guild_permissions.administrator:
            try:
                return await ctx.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))
            except Exception:  # send a DM if send message perms is not enabled
                return await ctx.author.send(
                    embed=Embed(
                        description="You are missing Administrator permission to run this command."))

        message_history = await ctx.channel.history(
            limit=None).flatten()

        deleted_msgs = 0
        for message in message_history:
            if int(message.author.id) != BOT_ID:
                deleted_msgs += 1
                await message.delete()

        msg = await ctx.channel.send(
            embed=Embed(
                description='Deleted {} message(s)'.format(deleted_msgs-1)))

        await msg.delete(delay=3)  # Delete the bot's message


def setup(client):
    client.add_cog(Settings(client))
