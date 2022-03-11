from discord import Embed


def get_embed(page=0):
    page_limit = 3

    if page == 0:
        embed = Embed(
            title="Bot Usage Instructions",
            description="All the commands are slash commands now! Blame Discord ;)"
        )
        embed.add_field(
            name="AO3 Searching:",
            value="`/linkao3 [fic name]` or `linkao3 [fic name] series` \
            \n **Example:**\n1) `linkao3 rogue knight` \n2) `linkao3 prince of slytherin series`",
            inline=False
        )

        embed.add_field(
            name="FFN Searching:",
            value="`/linkffn [fic name]` \
            \n **Example:**\n`linkffn cadmean victory`",
            inline=False
        )

    elif page == 1:
        embed = Embed(
            title="Bot Configuration",
            description="**Do not give administrator permission to the bot.**\nTo use these commands, you need administrator permission."
            "\nGo to the channel you want to add/remove and use the below commands."
        )
        embed.add_field(
            name="To allow the bot to respond to all the channels",
            value="`/allow_all`", inline=False
        )
        embed.add_field(
            name="To disallow the bot from responding to all the channels",
            value="`/disallow_all`", inline=False
        )
        embed.add_field(
            name="To allow the bot to respond to this channel",
            value="`/allow`", inline=False
        )

        embed.add_field(
            name="To disallow the bot from responding to this channel",
            value="`/disallow`", inline=False
        )

        embed.add_field(
            name="To delete all non-bot messages from the channel i.e. all the users except the bot. Useful for archive channels.",
            value="`/clr-msgs`", inline=False
        )

        embed.add_field(
            name="To delete a bot message if it violates the server rules, the user who requested the bot to find the fanfiction can react with 👎."
            "It's only possible to delete a message if it's done before 30s after the bot has replied.",
            value="\u200b", inline=False
        )

    elif page == 2:
        embed = Embed(
            title="Bot Support",
            description="Join the Bot's Discord Support Server if you want to report any bugs or want to suggest new features." +
            "\n[Discord Support Server](https://discord.gg/bRzzr3EBqH)"
        )

    else:
        embed = Embed(
            description="No more pages found!"
        )

    page_footer = f"Page: {str(page+1)}/{str(page_limit)}"
    embed.set_footer(text=page_footer)

    return embed, page_limit
