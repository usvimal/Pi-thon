import discord

games = [
	(discord.ActivityType.playing, '| Connected to ' + str(len(bot.guilds)) + ' servers | Connected to ' + str(
		len(set(bot.get_all_members()))) + ' users'),
	(discord.ActivityType.playing, 'epic games'),
	(discord.ActivityType.watching, 'paint dry..'),
	(discord.ActivityType.watching, 'you right now'),
	(discord.ActivityType.listening, 'some moosic')
]

gamestimer = 180
