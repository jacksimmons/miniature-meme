import discord
from discord.ext import commands

changed = False
kick = False
ban = False

dotw = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] #Day of the week
moty = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #Month of the year

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #---------------------------------------------------------------------------------

    @commands.group(
        name='create',
        description='Allows you to create various guild-related things.',
        aliases=[]
    )

    async def guildcreate(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument("Invalid subcommand passed.")
        pass

    @guildcreate.command(
        name='textchannel',
        description='''Creates a Text Channel in your current guild.
        Requires the Manage Channels permission.''',
        aliases=['text','tc']
    )

    @commands.has_permissions(manage_channels=True)
    async def createguildtextchannel(self, ctx, name: str="Text Channel", category: discord.CategoryChannel=None, position: int=None, topic: str=None, nsfw: bool=None, slowmode_delay: int=None, reason: str=None):
        tc = await ctx.guild.create_text_channel(name=name, position=position, slowmode_delay=slowmode_delay, nsfw=nsfw, topic=topic, category=category, reason=reason)
        await ctx.send(f"The text channel {tc.mention} has been created!")

    @guildcreate.command(
        name='voicechannel',
        description='''Creates a Voice Channel in your current guild.
        Requires the Manage Channels permission.''',
        aliases=['voice','vc']
    )

    @commands.has_permissions(manage_channels=True)
    async def createguildvoicechannel(self, ctx, name: str="Voice Channel", category: discord.CategoryChannel=None, position: int=None, user_limit: int=None, bitrate: int=None, reason: str=None):
        vc = await ctx.guild.create_voice_channel(name=name, category=category, position=position, user_limit=user_limit, bitrate=bitrate, reason=reason)
        await ctx.send(f"The voice channel {vc.mention} has been created!")

    #---------------------------------------------------------------------------------

    @commands.group(
        name='advancedguildinfo',
        description='''Gives you all the available information about this guild.
        Note: it is recommended to use this in a private channel to prevent any unwanted information being seen by normal users.''',
        aliases=['agi','asi']
    )

    @commands.has_permissions(administrator=True)
    async def advanced_guild_info(self, ctx):
        roles = ''
        categories = ''
        features = ''
        guild = ctx.guild

        for x in range(0, len(guild.roles)):
            if len(roles) < 250:
                if len(guild.roles[len(guild.roles)-(x+1)].name) >= 30:
                    roles += f', {guild.roles[len(guild.roles)-(x+1)].name[:30]}...'
                else:
                    if roles == '':
                        roles += f'{guild.roles[len(guild.roles)-(x+1)].name}'
                    else:
                        roles += f', {guild.roles[len(guild.roles)-(x+1)].name}'
            elif len(roles) >= 250:
                roles += f' ... {guild.default_role}'
                break

        for x in range(0, len(guild.categories)):
            if len(categories) < 250:
                if len(guild.categories[len(guild.categories)-(x+1)].name) >= 30:
                    categories += f'{guild.categories[len(guild.categories)-(x+1)].name[:30]}...'
                else:
                    if categories == '':
                        categories += f'{guild.categories[x]}'
                    else:
                        categories += f', {guild.categories[x]}'
            elif len(categories) >= 250:
                categories += f' ... {guild.categories[len(guild.categories)-(x+1)]}'
                break

        if guild.features == []:
            features = "None"
        else:
            for x in range(0, len(guild.features)):
                if features == '':
                    features = guild.features[x]
                else:
                    features += f', {guild.features[x]}'

        embed = discord.Embed(color=0x00ff00)
        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon_url}")
        embed.set_footer(text=f"Guild ID: {guild.id} | Guild Owner: {guild.owner} | Guild Owner ID: {guild.owner_id} | Shard ID: {guild.shard_id} | Chunked: {guild.chunked}", icon_url=f"{ctx.author.avatar_url}")

        embed2 = discord.Embed(color=0x00ff00)
        embed2.set_author(name=f"{guild.name} [Page 2/2]", icon_url=f"{guild.icon_url}")
        embed2.set_footer(text=f"System Channel: {guild.system_channel} | ")
#1
        embed.add_field(
        name="Region",
        value=f"{guild.region}",
        inline=True)
#2
        embed.add_field(
        name=f"Emoji [Limit: {guild.emoji_limit}]",
        value=f"{len(guild.emojis)}",
        inline=True)
#3
        embed.add_field(
        name=f"Channels [{len(guild.channels)}]",
        value=f"Text: {len(guild.text_channels)}, Voice: {len(guild.voice_channels)}",
        inline=True)
#4
        embed.add_field(
        name=f"Members [{len(guild.members)}]",
        value=f"Human: number, Bot: number",
        inline=False)
#5
        embed.add_field(
        name=f"Tier [Boosters: {len(guild.premium_subscribers)}]",
        value=f"{guild.premium_tier}",
        inline=True)
#6
        embed.add_field(
        name="File Upload Limit",
        value=f"{guild.filesize_limit/1000000}MB",
        inline=True)
#7
        embed.add_field(
        name="Bitrate Limit",
        value=f"{guild.bitrate_limit/1000} kbps",
        inline=True)
#8
        embed.add_field(
        name=f"AFK Channel [AFK: {int(guild.afk_timeout/60)}m]",
        value=f"{guild.afk_channel}",
        inline=True)

#9
        embed.add_field(
        name="2FA Level",
        value=f"{guild.mfa_level}",
        inline=True)
#10
        embed.add_field(
        name="Default Notifications",
        value=f"{str(guild.default_notifications[0]).title()}",
        inline=True)
#11
        embed.add_field(
        name="Verification Level",
        value=f"{str(guild.verification_level).title()}",
        inline=True)
#12
        embed.add_field(
        name="Explicit Content Filter",
        value=f"{str(guild.explicit_content_filter).title()}",
        inline=True)
#13
        embed.add_field(
        name="Guild Invite Splash",
        value=f"{guild.splash}",
        inline=True)
#14
        embed.add_field(
        name="Extra Info",
        value=f"System Channel: <#{guild.system_channel.id}>, Large Guild: {guild.large}, Unavailable: {guild.unavailable}",
        inline=False)
#before preantepenultimate 21
        embed.add_field(
        name="Guild Limits",
        value=f"Presences Limit: {guild.max_presences}, Member Limit: {guild.max_members}",
        inline=True)
#preantepenultimate 22
        embed.add_field(
        name="Premium Guild Features",
        value=f"{features.title()}",
        inline=False)
#antepenultimate 23
        embed.add_field(
        name="Server created",
        value=f"{dotw[guild.created_at.weekday()-1]}, {guild.created_at.day} {moty[guild.created_at.month-1]} {guild.created_at.year} at {guild.created_at.hour}:{guild.created_at.minute}",
        inline=False)
#penultimate 24
        embed.add_field(
        name=f"Roles [{len(guild.roles)}]",
        value=f"{roles}",
        inline=False)
#ultimate 25
        embed.add_field(
        name=f"Categories [{len(guild.categories)}]",
        value=f"{categories}",
        inline=False)

        await ctx.send(embed=embed)

    #---------------------------------------------------------------------------------

    @commands.group(
        name='setup',
        help='Allows you to set up the bot, enabling welcome messages and more.',
        aliases=['config']
    )

    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.BadArgument("Invalid subcommand passed.")
        pass


    #---------------------------------------------------------------------------------

    @commands.command(
        name='rename',
        description='Changes a user\'s nickname',
        aliases=['nick']
    )

    @commands.has_permissions(manage_nicknames=True)
    async def rename_command(self, ctx, who: discord.Member, *, nickname):
        if who.top_role < ctx.message.author.top_role or ctx.message.author.id == ctx.guild.owner_id:
            changed = False
            if nickname == 'None':
                nickname = None
            await who.edit(nick=nickname)
        else:
            await ctx.send(f"<@{ctx.message.author.id}>, you cannot perform action `{ctx.command}` on a user with an equal or higher top role.")

    #---------------------------------------------------------------------------------

    @commands.command(
        name='kick',
        description='Kicks a user',
        aliases=[]
    )

    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, who: discord.Member, *, reason = None):
        if who.top_role < ctx.message.author.top_role or ctx.message.author.id == ctx.guild.owner_id:
            await ctx.guild.kick(user=who, reason=reason)
            await ctx.send(f'{who} was kicked for {reason}.\nID: `{who.id}`')

        elif who.id == self.bot.user.id:
            await ctx.send(f'I cannot kick myself! If you want me to leave, you can use `{self.bot.get_prefix(ctx.message)}leave`.')

        elif who.id != ctx.message.author.id:
            await ctx.send(f'<@{ctx.message.author.id}>, you are unable to kick someone with an equal or higher rank to you.')

        else:
            await ctx.send(f'<@{ctx.message.author.id}>, you cannot kick yourself!')

    #---------------------------------------------------------------------------------

    #@commands.command(
    #    name='role',
    #    description='Gives a user a role',
    #    aliases=[]
    #)

    #@commands.has_permissions(manage_)

    #---------------------------------------------------------------------------------

    @commands.command(
        name='ban',
        description='Bans a user',
        aliases=[]
    )

    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx, who: discord.Member, *, reason = None):
        ban = False
        if who.top_role < ctx.message.author.top_role or ctx.message.author.id == ctx.guild.owner_id:
            await ctx.guild.ban(user=who, reason=reason)
            await ctx.send(f'{who} was banned for {reason}.\nID: `{who.id}`')

        elif who.id == self.bot.user.id:
            await ctx.send(f'I cannot kick myself! If you want me to leave, you can use {self.bot.get_prefix(ctx.message)}leave.')

        elif who.id != ctx.message.author.id:
            await ctx.send(f'<@{ctx.message.author.id}>, you are unable to ban someone with an equal or higher rank to you.')

        else:
            await ctx.send(f'<@{ctx.message.author.id}>, you cannot ban yourself!')

    #---------------------------------------------------------------------------------

    #@commands.command(
    #    name='leave',
    #    description='Makes the bot leave the server',
    #    aliases=[]
    #)

    #@commands.has_permissions(administrator=True)
    #async def leave_command(self, ctx):
    #    await ctx.send("Are you sure you want me to leave? [y/n]")
    #    await ctx.message.add_reaction(emoji='💬')

    #    def check(msg):
    #        return msg.author == ctx.message.author

    #    msg = await self.bot.wait_for('message', check=check)
    #    await ctx.send("Bye mom!")
    #    await ctx.guild.leave()

def setup(bot):
    bot.add_cog(Admin(bot))
