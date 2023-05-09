import openai
import discord
from discord.ext import commands
import langid

# Создаем Discord клиента
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# Авторизуемся в OpenAI API
openai.api_key = 'X'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Определяем язык сообщения, которое нужно перевести
    lang, conf = langid.classify(message.content)

    # Получаем ответ на сообщение с помощью OpenAI
    if lang == 'ru':
        engine_id = "text-davinci-002"
    else:
        engine_id = "text-davinci-002"
    response = openai.Completion.create(
        engine=engine_id,
        prompt=message.content,
        max_tokens=60,
        temperature=0.5,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    generated_text = response["choices"][0]["text"]
    
    # Отправляем ответ на сообщение в Discord
    await message.channel.send(generated_text)

    # Обрабатываем команды Discord
    await client.process_commands(message)

# Запускаем клиент Discord
client.run('X')
