import discord
from discord.ext import commands
import yaml
import update
import asyncio
with open("./config.yml", 'r') as file:
    config = yaml.load(file, Loader = yaml.Loader)


client = commands.Bot(command_prefix =config['Prefix'])
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your order ids"))
    print('License Bot - READY !')

@client.command()
async def redeem(ctx, arg1):
    valid=False
    await ctx.message.delete()
    update.update()
    with open(config['SerialFile']) as license_file:
        lines = license_file.read().splitlines()
        if arg1 in lines:
            embed2=discord.Embed(title=config['ValidTitle'], color=0x00ff00)
            embed2.add_field(name=config['ValidName'], value=config['ValidValue'], inline=False)
            embed2.set_author(
                            name = ctx.author.name,
                            icon_url = ctx.author.avatar_url)
            embed2.set_footer(text=config['ValidFooter'])
            mess = await ctx.send(embed=embed2)
            role = discord.utils.get(ctx.guild.roles, name=config['RoleName'])
            user = ctx.message.author
            await user.add_roles(role)
            print('Valid orderid: ', str(user), arg1)
            valid = True
        elif arg1+"used" in lines:
            embed2=discord.Embed(title=config['UsedTitle'], color=0xFF0000)
            embed2.set_author(name = ctx.author.name,icon_url = ctx.author.avatar_url)
            embed2.set_footer(text=config['UsedFooter'])
            mess = await ctx.send(embed=embed2)
            print('Used OrderID: ', str(ctx.message.author), arg1)
        else:
            embed2=discord.Embed(title=config['InvalidTitle'], color=0xFF0000)
            embed2.set_author(
                            name = ctx.author.name,
                            icon_url = ctx.author.avatar_url)
            embed2.set_footer(text=config['InvalidFooter'])
            mess = await ctx.send(embed=embed2)
            print('Invalid orderid: ', str(ctx.message.author), arg1)
        if valid:
            with open(config['SerialFile'],"r+") as f:
                file_content = f.readlines()
                f.seek(0)
                for line in file_content:
                    if arg1+"used" in line:
                        f.write(line)
                    elif arg1 in line and arg1+"used" not in line:
                        f.write(line.strip()+"used\n")
                    else:
                        f.write(line)
                f.truncate()
        await asyncio.sleep(2)
        await mess.delete()

client.run(config['TOKEN'])
