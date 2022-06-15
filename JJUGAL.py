import urllib
import discord
from bs4 import BeautifulSoup
import requests
import openpyxl
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import time
from youtube_dl import YoutubeDL
import asyncio
from discord.ext import commands









client = commands.Bot(command_prefix='.')
TOKEN = "OTU0NzE3OTI5Mzc3NzY3NDQ2.YjXMXA.nV1gravRe1K27H4dsXB5UBka5D8"


@client.event
async def on_ready():
    print(client.user.id)
    print("준비완료")
    game = discord.Game("도감 검사")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command()
async def 주꾸미(ctx):
    print(ctx.content)
    await ctx.channel.send("주꾸미와 갈비 알리미 입니다.")

@client.command()
async def 쭈갈(ctx):
    embed = discord.Embed(color=0x00ff00)
    embed.set_footer(text="맛집이다(이젠 없어졌다.)")
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/635144119882088451/954736054513041418/download.jpg")
    await ctx.channel.send(embed=embed)

@client.command()
async def 청소(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


# @client.command()
# async def 참가(ctx):
#     if ctx.author.voice and ctx.author.voice.channel:
#         channel = ctx.author.voice.channel
#         await channel.connect()
# @client.command()
# async def 나가(ctx):
# 	await client.voice_clients[0].disconnect()
@client.command()
async def 컴(ctx):
    try:
        global vc
        vc = await vc.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 사람이 없다")
@client.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
        await ctx.send("나 나가요")
    except:
        await ctx.send("이미 없다")

@client.command()
async def p(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "성능좋은", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")


@client.command(name = '도감')
async def dogam(ctx, *, message=None):
    search = message
    try:
        baseurl = "https://pokemon.fandom.com/ko/wiki/" + search + "_(포켓몬)"
        original_html = requests.get(baseurl).text
        html = BeautifulSoup(original_html, "html.parser")
        pokeName = html.find("div", attrs={"class": "name-ko"}).get_text()
        pokeImg = html.find("div", attrs={"class": "image rounded"}).find("img").get('data-src')
        pokeNum = html.find("div", attrs={"class": "index"}).get_text()
        pokeType = html.find("span", attrs={"class": "split-cell-wrap text-center"}).get_text()
        pokeNumc = html.find("table", attrs={"style": "width:100%"}).get_text().strip().replace("도감 번호", "")
        pokeChar = html.find_all("span", attrs={"class": "ajaxttlink"})
        pokeChar_list = []
        for i in pokeChar:
            pokeChar_list.append(i.get_text())
        embed1 = discord.Embed(title=message + " (이)로구나!", description="", color=0x62c1cc)
        embed1.set_thumbnail(url=pokeImg)
        embed1.add_field(name="이름", value=pokeName)
        embed1.add_field(name="타입", value=pokeType)
        embed1.add_field(name="특성", value="\n".join([i for i in pokeChar_list]))
        embed1.add_field(name="전국도감 번호", value=pokeNum, inline=False)
        embed1.add_field(name="도감 번호", value=pokeNumc)
        await ctx.send(embed=embed1)
        print(pokeImg)
    except:
        await ctx.send("아쉽게 도감에는 그런 포켓몬이 없구나...")







client.run(TOKEN)