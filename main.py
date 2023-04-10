import requests
import os
import discord
from discord.ext.commands import Bot , context
from discord.ext import commands , tasks
from keep_alive import keep_alive
import tmdbsimple as tmdb
import urllib3
from itertools import cycle
channels =[1009462217416126605,900424201998041160]

status = cycle(['4K Ultra HD','65" 165 Ekran','Uydu Alıcılı','Smart LED TV'])


urllib3.disable_warnings()

tmdb.API_KEY = 'f4be9ffe9b2357fcd3217e7d3e0b05f6'

client = discord.Client()
client = commands.Bot(command_prefix="!") 
@client.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")



@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


@client.command(name='film')
async def film(ctx):
  if ctx.message.channel.id in channels:
    await  ctx.send("Filmin ismini girin:")
    def check(msg):

      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.movie(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
                
    response = requests.get(f"https://api.themoviedb.org/3/movie/{idList[0]}?api_key={tmdb.API_KEY}&language=tr-TR")
    credits = requests.get(f"https://api.themoviedb.org/3/movie/{idList[0]}/credits?api_key={tmdb.API_KEY}")
    data = response.json()
    players = credits.json()
    title = data["title"]
    original_title = data["original_title"]
    poster ="https://image.tmdb.org/t/p/original"+data["poster_path"]
    ov = data["overview"]
    homepage = data["homepage"]

    release_date = data["release_date"]
    revenue = data["revenue"]
    a= format(int(revenue), ',').split(',')
    money = ",".join(a)
    vote_average = data["vote_average"]
    vote_count = data["vote_count"]
    runtime = data["runtime"]
    
    l0 = players["crew"]
    d0 = {}
    a0 = []
    for i in l0:
      d0.update(i)    
      if d0["job"] == "Director":
        a0.append(d0["name"])
      joined_string0 = " , ".join(a0)

    l1 = players["cast"]
    d1 = {}
    a1 = []
    b1 = []
    for i in l1:
      d1.update(i)
      a1.append(d1["name"]+" "+"**("+d1["character"]+")**" )
    b1 = a1[0:5]
    joined_string1 = " , ".join(b1)

    l2 = data["genres"]
    d2 = {}
    a2 = []
    for i in l2:
      d2.update(i)
      a2.append(d2["name"])
    joined_string2 = " , ".join(a2)
    await ctx.send(poster)
    await ctx.send(f"***<@{msg.author.id}> Tarafından öneriliyor.***\n\n**Filmin İsmi:**{title}\t\t\t\t **Filmin Orijinal İsmi:**{original_title}\n\n**Yönetmen(ler):**{joined_string0}\n\n**Oyuncular:**{joined_string1}\n\n**Yayınlanma Tarihi:** *{release_date}*\n\n**Türler:**{joined_string2}\n\n**Uzunluk:** *{runtime}* dakika\n\n**Özet:**{ov}\n\n**Gişe Hasılatı:** *{money}* :dollar:\n\n**Aldığı oy ortalaması:** *{vote_average}* :star:\t\t\t\t **Aldığı oy sayısı:** *{vote_count}*\n\n***Filmin Web Sitesi:<{homepage}>***\n\n***Daha detaylı bilgi için:<https://www.themoviedb.org/movie/{idList[0]}>***")  
  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")  

@client.command(name='dizi')
async def dizi(ctx):
  if ctx.message.channel.id in channels:
    await ctx.send("Dizinin ismini girin:")
    def check(msg):

      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.tv(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()

    idList = []
    for s in search.results:
      idList.append(s["id"])
                
    response = requests.get(f"https://api.themoviedb.org/3/tv/{idList[0]}?api_key={tmdb.API_KEY}&language=tr-TR")
    credits = requests.get(f"https://api.themoviedb.org/3/tv/{idList[0]}/credits?api_key={tmdb.API_KEY}")
    players = credits.json()
    data = response.json()
    name = data["name"]
    original_name = data["original_name"]
    poster ="https://image.tmdb.org/t/p/original"+data["poster_path"]
    ov = data["overview"]
    episode_run_time = data["episode_run_time"]
    first_air_date = data["first_air_date"]
    vote_average = data["vote_average"]
    vote_count = data["vote_count"]
    number_of_episodes = data["number_of_episodes"]
    number_of_seasons = data["number_of_seasons"]
    homepage = data["homepage"]
    l3 = players["cast"]
    d3 = {}
    a3 = []
    b3 = []
    for i in l3:
      d3.update(i)
      a3.append(d3["name"]+" "+"**("+d3["character"]+")**" )
    b3 = a3[0:5]
    joined_string3 = " , ".join(b3)
    l4 = data["genres"]
    d4 = {}
    a4 = []
    for i in l4:
      d4.update(i)
      a4.append(d4["name"])
    joined_string4 = " , ".join(a4)
    await ctx.send(poster)
    await ctx.send(f"***<@{msg.author.id}> Tarafından öneriliyor.***\n\n**Dizinin İsmi:**{name}\t\t\t\t **Dizinin Orijinal İsmi:**{original_name}\n\n**Oyuncular:**{joined_string3}\n\n**Yayınlanma Tarihi:** *{first_air_date}*\n\n**Türler:**{joined_string4}\n\n**Bölüm Uzunluğu:** *{episode_run_time[0]}* dakika\n\n**Özet:**{ov}\n\n**Sezon Sayısı:** *{number_of_seasons}*\n\n**Bölüm Sayısı:** *{number_of_episodes}*\n\n**Aldığı oy ortalaması:** *{vote_average}* :star:\t\t\t\t **Aldığı oy sayısı:** *{vote_count}*\n\n***Dizinin Web Sitesi:<{homepage}>***\n\n***Daha detaylı bilgi için:<https://www.themoviedb.org/tv/{idList[0]}>***")
  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")   


@client.command(name='benzerfilm')
async def benzerfilm(ctx):
  if ctx.message.channel.id in channels:
    await ctx.send("Filmin ismini girin:")
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.movie(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
    response = requests.get(f"https://api.themoviedb.org/3/movie/{idList[0]}/similar?api_key={tmdb.API_KEY}&language=tr-TR")
    name = requests.get(f"https://api.themoviedb.org/3/movie/{idList[0]}?api_key={tmdb.API_KEY}&language=tr-TR")
    filmname = name.json()
    original_title = filmname["original_title"]
    data = response.json()
    l5 = data["results"]
    d5 = {}
    a5 = []
    b5 = []
    for i in l5:
        d5.update(i)
        a5.append(d5["original_title"])
    b5 = a5[0:10]
    joined_string5 = "\n".join(b5)
    await ctx.send(f"***{original_title}*** **filmine benzer filmler:** ")
    await ctx.send(f"***{joined_string5}***")
  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")  

@client.command(name='benzerdizi')
async def benzerdizi(ctx):
  if ctx.message.channel.id in channels:
    await  ctx.send("Dizinin ismini girin:")
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.tv(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
    response = requests.get(f"https://api.themoviedb.org/3/tv/{idList[0]}?api_key={tmdb.API_KEY}&language=tr-TR")
    similar = requests.get(f"https://api.themoviedb.org/3/tv/{idList[0]}/similar?api_key={tmdb.API_KEY}")
    data = response.json()
    similartv = similar.json()
    name = data["name"]
    l6 = similartv["results"]
    d6 = {}
    a6 = []
    b6 = []
    for i in l6:
        d6.update(i)
        a6.append(d6["name"])
    b6 = a6[0:10]
    joined_string6 = "\n".join(b6)
    await ctx.send(f"***{name}*** **dizisine benzer diziler:** ")
    await ctx.send(f"***{joined_string6}***")
  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")    

@client.command(name='filmoyuncu')
async def filmoyuncu(ctx):
  if ctx.message.channel.id in channels:
    await  ctx.send("Oyuncunun ismini girin:")
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.person(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
    persons = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}?api_key={tmdb.API_KEY}&language=en-US")
    credits = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}//combined_credits?api_key={tmdb.API_KEY}&language=en-US")
    person = persons.json()
    players = credits.json()
    
    name = person["name"]
    bio = person["biography"]
    bplace = person["place_of_birth"]
    bday = person["birthday"]
    dday = person["deathday"]
    poster ="https://image.tmdb.org/t/p/original"+person["profile_path"]

    l7 = players["cast"]
    d7 = {}
    a7 = []
    b7 = bio.split('\n\n')
    for i in l7:
      d7.update(i)
      if d7["media_type"] == "movie":    
        a7.append(d7["title"]+" **("+d7["release_date"]+")**")
    n = 25
    # using list comprehension 
    x = [a7[i:i + n] for i in range(0, len(a7), n)]   
    await ctx.send(f"***<@{msg.author.id}> merak etmiş.***")
    await ctx.send(poster)
    await ctx.send("***Biyografi:***")
    k = 0
    while k < len(b7):
      await ctx.send(f"**{b7[k]}**")
      k = k + 1 
    await ctx.send(f"***Doğum Tarihi:*** *{bday}*\n***Doğum Yeri:*** *{bplace}*")
    if dday != None:
      await ctx.send(f"***Ölüm Tarihi:*** *{dday}*")
    
       
    await ctx.send(f"***{name} adlı oyuncunun filmleri:***")
    l = 0
    while l < len(x):
      joined_string = " , ".join(x[l])
      await ctx.send(joined_string)
      l = l + 1

  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")

@client.command(name='dizioyuncu')
async def dizioyuncu(ctx):
  if ctx.message.channel.id in channels:
    await  ctx.send("Oyuncunun ismini girin:")
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.person(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
    persons = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}?api_key={tmdb.API_KEY}&language=en-US")
    credits = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}//combined_credits?api_key={tmdb.API_KEY}&language=en-US")
    person = persons.json()
    players = credits.json()
    
    name = person["name"]
    bio = person["biography"]
    bplace = person["place_of_birth"]
    bday = person["birthday"]
    dday = person["deathday"]
    poster ="https://image.tmdb.org/t/p/original"+person["profile_path"]

    l8 = players["cast"]
    d8 = {}
    a8 = []
    b8 = bio.split('\n\n')
    for i in l8:
      d8.update(i)
      if d8["media_type"] == "tv":    
        a8.append(d8["name"]+" **("+d8["first_air_date"]+")**")
    n = 25
    # using list comprehension 
    x = [a8[i:i + n] for i in range(0, len(a8), n)]   
    await ctx.send(f"***<@{msg.author.id}> merak etmiş.***")
    await ctx.send(poster)
    await ctx.send("***Biyografi:***")
    k = 0
    while k < len(b8):
      await ctx.send(f"**{b8[k]}**")
      k = k + 1
    await ctx.send(f"***Doğum Tarihi:*** *{bday}*\n***Doğum Yeri:*** *{bplace}*")
    if dday != None:
      await ctx.send(f"***Ölüm Tarihi:*** *{dday}*")
    
       
    await ctx.send(f"***{name} adlı oyuncunun dizileri:***")
    l = 0
    while l < len(x):
      joined_string = " , ".join(x[l])
      await ctx.send(joined_string)
      l = l + 1

  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")

@client.command(name='yönetmen')
async def yönetmen(ctx):
  if ctx.message.channel.id in channels:
    await  ctx.send("Yönetmenin ismini girin:")
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel     
    msg = await client.wait_for('message', check=check)
    search = tmdb.Search()
    response = search.person(query=f"{msg.content}")
    async for msg in msg.channel.history(limit = 3):
      await msg.delete()
    idList = []
    for s in search.results:
      idList.append(s["id"])
    persons = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}?api_key={tmdb.API_KEY}&language=en-US")
    credits = requests.get(f"https://api.themoviedb.org/3/person/{idList[0]}//combined_credits?api_key={tmdb.API_KEY}&language=en-US")
    person = persons.json()
    players = credits.json()
    
    name = person["name"]
    bio = person["biography"]
    bplace = person["place_of_birth"]
    bday = person["birthday"]
    dday = person["deathday"]
    poster ="https://image.tmdb.org/t/p/original"+person["profile_path"]

    l9 = players["crew"]
    d9 = {}
    a9 = []
    b9 = bio.split('\n\n')
    for i in l9:
      d9.update(i)
      if d9["job"] == "Director":    
        a9.append(d9["title"]+" **("+d9["release_date"]+")**")
    n = 25
    # using list comprehension 
    x = [a9[i:i + n] for i in range(0, len(a9), n)]   
    await ctx.send(f"***<@{msg.author.id}> merak etmiş.***")
    await ctx.send(poster)
    await ctx.send("***Biyografi:***")
    k = 0
    while k < len(b9):
      await ctx.send(f"**{b9[k]}**")
      k = k + 1 
    await ctx.send(f"***Doğum Tarihi:*** *{bday}*\n***Doğum Yeri:*** *{bplace}*")
    if dday != None:
      await ctx.send(f"***Ölüm Tarihi:*** *{dday}*")
    
       
    await ctx.send(f"***{name} adlı yönetmenin filmleri:***")
    l = 0
    while l < len(x):
      joined_string = " , ".join(x[l])
      await ctx.send(joined_string)
      l = l + 1

  else:
    await ctx.reply("Bu komutu burada kullanamazsın :rage: :rage:")



keep_alive()
client.run(os.getenv('TOKEN'))




