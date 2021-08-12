import discord
from discord.ext.commands import Bot, when_mentioned_or

bot = Bot(description="Pdf Library", command_prefix=when_mentioned_or(";"), help_command=None )

GITHUB_LINK = "https://github.com/pseudocoder10/Lockout-Bot"


@bot.event
async def on_ready():
	print('I am ready')

@bot.command()
async def msz(ctx):
	s = discord.Embed(description='', color=0x008000)
	s.set_author(name="Book-Trackerr", icon_url=ctx.me.avatar_url)
	# s.set_footer(text='yooo')
	s.add_field(name=f"\n\n{book_name}", value=f"[Download]({link})",
                            inline=False)


	await ctx.channel.send(embed=s)

bot.run('ODM1OTQyNjY5MzkzMDY4MDMy.YIWyRw.gnGP2BCfJ9xjUJ-iPXw6IVyNJ8A')