from discord.ext import commands
import verification

commandPrefix = '^'

bot = commands.Bot(command_prefix=commandPrefix)

bot.add_cog(verification.Verification(bot))


@bot.command()
async def ctrl(ctx, arg1, arg2):
    if arg1 == 'verification':
        if arg2 == 'on':
            bot.add_cog(verification.Verification(bot))
            await ctx.send('Verification system has been turned on!')
        if arg2 == 'off':
            bot.remove_cog('Verification')
            await ctx.send('Verification system has been turned off!')


@bot.event
async def on_ready():
    print('Bot is online!')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Latency: ' + str(bot.latency * 1000) + ' milliseconds.')

#Discord bot token will replace the blank string
bot.run('')
