import discord
import os
from keep_alive import keep_alive

client = discord.Client()

Vimal = "274578439783317514"
Cilian = "424781702779633684"

@client.event
async def on_ready():
    print("*Hackerman voice* I'm in")
    print(client.user)
    await client.change_presence(game=discord.Game(name='epic games'))
    return


@client.event
async def on_message(message):
      # we do not want the bot to reply to itself
	if message.author == client.user:
		return
       
	if message.content.startswith(';bot'):
		await client.delete_message(message)
		msg = message.content.split(' ')
		msg = ' '.join(msg[1:])
		print(message.author.id)
		if message.author.id == Vimal or message.author.id == Cilian:
			msg = (msg).format(message)
			await client.send_message(message.channel, msg)
			return
		return

   #clash with haoshaun's bot     
   # if message.content.startswith('vote:'):
		await client.add_reaction(message,"\U0001F44D")
		await client.add_reaction(message,"\U0001F44E")
		return

	if 'libtard' in message.content.lower(): 
		msg = 'libtard epic rekt 8)'.format(message)
		await client.send_message(message.channel,msg)
		return

	elif message.content.lower().startswith('hmm'):
		msg = '\U0001F914'.format(message)
		await client.send_message(message.channel, msg)
		return

	if 'ok this is epic' in message.content.lower() or 'okay this is epic' in message.content.lower():
		msg = ''.format(message) 
		await client.send_file(message.channel, 'my_image.jpg')
		return

	if message.content.lower() == ';details':
		em = discord.Embed(title='read my code!', url='https://repl.it/@VimalMuthuvel/pi-thon', colour=0xb949b5)
		em = em.set_author(name='Minininja',url='https://github.com/usvimal')
		await client.send_message(message.channel,embed=em)
		return
        
#keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
