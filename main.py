import discord
from discord.ext import commands
bot = commands.Bot(command_prefix = '%', description = '')

logchanel = bot.get_channel(908112949594452028)

#		-----events-----

@bot.event
async def on_ready():
	print("Je suis près !")


#		-----commandes-----

@bot.command()
async def info(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfMember = server.member_count
	server_name = server.name
	message = f'Ici vous pourez vous amuser en participant aux events, parlent avec des gens.\nMais aussi, vous pouvez faire une demande de développement de site, de serveur ou de bot discord \n\nLe serveur possède\n- *{numberOfTextChannels} salon textuel* et *{numberOfVoiceChannels} salons Vocal*\n- Un total de *{numberOfMember} membres*'
	await ctx.send(message)

@bot.command()
async def getinfo(ctx, info):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfMember = server.member_count
	server_name = server.name

	if info == "membercount":
		getinfoMemberCountSend = f'Il y a {server.member_count} membres sur le serveur'
		await ctx.send(getinfoMemberCountSend)
	elif info == "numberchanel":
		NumberChanel = len(server.text_channels) + len(server.voice_channels)
		getinfoNumberChanel = f'Le serveur contient un total de {NumberChanel} salons'
		await ctx.send(getinfoNumberChanel)

	elif info == "servername":
		await ctx.send(server.name)

	else:
		await ctx.send(f"Faite plutôt %getinfo membercount/numberchanel/servername")

#		----- commande staff-----

@bot.command()
@commands.has_permissions (manage_messages = True)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

@bot.command()
@commands.has_permissions (kick_members = True)
async def kick(ctx, user : discord.User, *reason):
	reason =  " ".join(reason)
	await ctx.guild.kick(user, reason= reason)
	await ctx.send(f"{user} à été kick pour {reason}")

@bot.command()
@commands.has_permissions (ban_members = True)
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Banissemeent**", description = "Un modérateur à frapé !", color = 0xC70613)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url ='https://emoji.gg/assets/emoji/9005-abanhammer.gif')
	embed.add_field(name = "Membre banni", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)

	await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions (ban_members = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	username, userid = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == username and i.user.discriminator == userid:
			await ctx.guild.unban(i.user, reason = reason)
			embed = discord.Embed(title = "**Débanissemeent**", description = "Un modérateur à été cool !", color = 0x0674C7)
			embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
			embed.set_thumbnail(url ='https://emoji.gg/assets/emoji/9897-verified.gif')
			embed.add_field(name = "Membre de retour", value = user.name, inline = True)

			await ctx.send(embed = embed)
			return

	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des ban")


@bot.command()
@commands.has_permissions (ban_members = True)
async def bansid(ctx):
	ids=[]
	bans = await ctx.guild.bans()
	for i in bans:
		ids.append(str(i.user.id))
	await ctx.send("\n".join(ids))


async def createMutedRole(ctx):
	mutedRole = await ctx.guild.create_role(name = "Muet", 
											permissions = discord.Permissions(
												send_messages = False,
												speak = False),
											reason = "Création du role Muet")
	for channel in ctx.guild.channels:
		await channel.set_permissions(mutedRole, send_messages = False, speak = False)
	return mutedRole

async def getMutedRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "Muet":
			return role
	return await createMutedRole(ctx)


@bot.command()
@commands.has_permissions (kick_members = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
	mutedRole = await getMutedRole(ctx)
	await member.add_roles(mutedRole, reason = reason)
	await ctx.send(f"{member.mention} a été mute !")


@bot.command()
@commands.has_permissions (kick_members = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
	mutedRole = await getMutedRole(ctx)
	await member.remove_roles(mutedRole, reason = reason)
	await ctx.send(f"{member.mention} a été unmute !")
	

bot.run("OTA4MDQwOTMxNjA3OTY5ODI1.YYv9BA.dp53waBtcGYGY5NNrqMltka7ZTA")