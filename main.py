import discord
import os

client = discord.Client()

chat_id={}  #dictionary for the different text_channels ids and their index in log

#connecting to server
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#checking for the state of the voice chats
@client.event
async def on_voice_state_update(member,before,after):
  #fetching name of channels
  channel = before.channel  if before.channel else after.channel
  channel_name = channel.name
  text_channel = discord.utils.get(member.guild.text_channels, name   = channel_name)

  #checking if member is joining or leaving chat
  if not before.channel and after.channel:  #joining channel

    #adding a role to allow them to access a private channel
    role = discord.utils.get(member.guild.roles, name = '{0} user'.format(channel_name))
    await member.add_roles(role)

    #setting the message log (Brute force. To be improved)
    if(len(channel.members) == 1):
      i=0
      for chat in member.guild.text_channels:
        for vc in member.guild.voice_channels:
          if(chat.name == vc.name):
            chat_id[chat.id]=i
            i+=1
      global log
      log= [[] for _ in range(i)]

  elif before.channel and not after.channel:  #leaving channel

    #removing their access to private channel
    role = discord.utils.get(member.guild.roles, name = '{0} user'.format(channel_name))
    await member.remove_roles(role)

    #checking number of channel users
    if(len(channel.members) == 0):
      await text_channel.delete_messages(log[chat_id.get(text_channel.id)])
        #print(log[chat_id.get(text_channel.id)])
  else:
    #for role in member.guild.roles:
    #  print(role.name)
    #  if role.name.find("user")!=-1:
    #    
    role = discord.utils.get(member.guild.roles, name = '{0} user'.format(before.channel.name))
    await member.remove_roles(role)
    role = discord.utils.get(member.guild.roles, name = '{0} user'.format(after.channel.name))
    await member.add_roles(role)

#saving the messages sent and that need to be deleted
@client.event
async def on_message(message):
  global log

  #checking if user is chatting in a channel that doesn't have a voice channel associated with it
  if(chat_id.get(message.channel.id) == None):
    return
  
  elif message.content.startswith("!save"): #checking if user wants to save messages

    #checking if user wants to save all the previous messages
    if message.content.find ("all") !=-1:
      log= [[] for _ in range(len(log))]  #empty log

    else: #deleting last message from log
      for sub in log:
        sub[:] = [ele for ele in sub if ele != log[chat_id.get  (message.channel.id)][-1]]

    #adding command to the list of elements to delete
    log[chat_id.get(message.channel.id)].append(message)

  else: #adding messages to log
    log[chat_id.get(message.channel.id)].append(message)
    return
  
client.run(os.getenv('TOKEN'))