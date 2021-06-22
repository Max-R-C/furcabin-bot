from discord.ext import commands
import discord
import json
import os


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        if not os.path.isfile(ctx.author.name + '_responses.json'):
            verified_role = discord.utils.get(ctx.guild.roles, name='VERIFIED')

            if verified_role not in ctx.author.roles:
                await ctx.send(ctx.author.mention + ', Please check your DMs!')
                dm = await ctx.author.create_dm()
                await dm.send(
                    'In order to become verified in the Furcabin server, please answer these following questions'
                    ' honestly. Your answers will be evaluated by a staff member. Thank you!')

                with open('verification.json', 'r') as f:
                    questions = json.load(f)
                    f.close()
                    await dm.send(embed=discord.Embed(title='Furcabin Verification question #1',
                                                      description=questions["questions"]["1"], color=0x3498db))

                json_data = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "",
                             "9": "", "10": "", "i": 1}
                with open(ctx.author.name + '_responses.json', 'w') as f:
                    json.dump(json_data, f)
                    f.close()
            else:
                await ctx.send('You have already been verified!')
        else:
            await ctx.send('You are already pending verification, or someone else with the same name is pending'
                           ' verification. If this is the case, please wait and ^verify again later.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            if not message.author.name == 'Furcabin Bot!':
                with open(message.author.name + '_responses.json', 'r') as f:
                    responses = json.load(f)
                    index = int(responses["i"])

                with open('verification.json', 'r') as f:
                    questions = json.load(f)
                    f.close()

                if index <= len(questions["questions"]):
                    with open(message.author.name + '_responses.json', 'w') as f:
                        if index < len(questions["questions"]):
                            await message.channel.send(embed=discord.Embed(title='Furcabin Verification question #' +
                            str(index + 1), description=questions["questions"][str(index + 1)], color=0x3498db))

                        responses[str(index)] = message.content
                        responses["i"] = str(index + 1)

                        json.dump(responses, f)
                        f.close()

                    if responses["i"] == str(len(questions["questions"]) + 1):
                        await message.channel.send(embed=discord.Embed(title='Thank you! :heart:', description=
                        'That was the last question! Your answers are now being'
                        ' reviewed by '
                        'Furcabin staff. Be patient, you will be notified when a decision'
                        ' is made.', color=0x3498db))

                        channel = self.bot.get_channel(questions["results_channel"])

                        responses_message = ''

                        for i in range(index):
                            i += 1
                            responses_message += questions["questions"][str(i)] + ' : ' + responses[str(i)] + '\n'

                        await channel.send(embed=discord.Embed(title='Verification request from ' +
                        message.author.name, description=responses_message, color=0x3498db))

    @commands.command()
    @commands.has_role('Modoworator')
    async def setverifyrequests(self, ctx):
        with open('verification.json', 'r') as f:
            j = json.load(f)
            j["results_channel"] = ctx.channel.id

            f.close()

        with open('verification.json', 'w') as f:
            json.dump(j, f)
            f.close()

        await ctx.send('Verification results will now be sent to this channel!')

    @commands.command()
    @commands.has_role('Modoworator')
    async def accept(self, ctx, arg1: discord.Member):
        if os.path.isfile(arg1.name + '_responses.json'):
            verify_role = discord.utils.get(ctx.guild.roles, name='VERIFIED')

            await arg1.add_roles(verify_role)

            await ctx.send(embed=discord.Embed(title='Furcabin Verification', description='Verified ' + arg1.mention +
            '! They now have access to the server!', color=0x3498db))

            dm = await arg1.create_dm()
            await dm.send(embed=discord.Embed(title='Furcabin Verification',
            description='You have been verified in the Furcabin server! Enjoy your stay!', color=0x3498db))

            os.remove(arg1.name + '_responses.json')
        else:
            await ctx.send(embed=discord.Embed(title='Furcabin Verification',
            description='That user has not submitted a verification request,'
                        ' or they have already been verified.', color=0x3498db))

    @commands.command()
    @commands.has_role('OwOner!')
    async def deny(self, ctx, arg1: discord.Member):
        if os.path.isfile(arg1.name + '_responses.json'):
            verified_role = discord.utils.get(ctx.guild.roles, name='VERIFIED')

            await arg1.remove_roles(verified_role)

            await ctx.send(embed=discord.Embed(title='Furcabin Verification',
            description='Denied ' + arg1.mention + '!', color=0x3498db))

            dm = await arg1.create_dm()
            await dm.send(embed=discord.Embed(title='Furcabin Verification',
            description='You have been denied entry in the Furcabin server!', color=0x3498db))

            os.remove(arg1.name + '_responses.json')
        else:
            await ctx.send(embed=discord.Embed(title='Furcabin Verification',
            description='That user has not submitted a verification request,'
                        ' or they have already been verified. ', color=0x3498db))
