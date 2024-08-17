
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from random import randint
import time
from places import mesta
import asyncpg
import json
import asyncio

host = ''
user = ''
password = ''
dbname = ''

TOKEN=''
bot = Bot(TOKEN)
dp= Dispatcher(bot)

hels="""Добро пожаловать в наш Бот😁!

Тут можно познакомиться с нашими заядлыми кадрами из отдела😼! 

<b>Заполнить анкету📝</b> - нажмите на клавиатуре что бы я добавил вас в список😁.

<b>Что делать❓</b> - нажмите если не знаете как можно заполнить анкету😉.
"""

hell="""
<b>Личная информация:</b> Заполняйте имя, возраст и место проживания. р📝

<b>Навыки и качества:</b> Выделите ключевые навыки и качества с помощью эмодзи. ✨

<b>Интересы и хобби:</b> Подчеркните увлечения. 🎨

<b>Контактная информация:</b> Укажите  свой инстаграм. 🌐

Если все понятно то нажмите <b>Заполнить анкету📝</b> и приступайте розить оригинальностью🤩.
"""


nicks={}#имя/возраст/через н био/через н должность/через н инст/
ggg=randint(0,len(nicks))

async def upsert_user(user_id, name, age, bio, profile, job):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''
    INSERT INTO users (user_id, name, age, bio, profile, job) 
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT (user_id) DO UPDATE SET
        name = EXCLUDED.name,
        age = EXCLUDED.age,
        bio = EXCLUDED.bio,
        profile = EXCLUDED.profile,
        job = EXCLUDED.job
    ''', user_id, name, age, bio, profile, job)



kb=ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Заполнить анкету📝')).insert('Что делать❓')

@dp.message_handler(commands=['start']) #Включает бота. Подключил его к анкетнику
async def start_cm(message: types.message):
    global nicks
    nicks[message.from_user.id]=['Не указано','Не указано','Не указано','Не указано','Не указано',0]
    print(message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id,
                            text=hels,
                            parse_mode="HTML",reply_markup=kb
                            )
    await message.delete()

@dp.message_handler(regexp="Что делать❓") # Что вообще нужно написать
async def ancent(message: types.message):
    await bot.send_message(chat_id=message.from_user.id,
                            text=hell,
                            parse_mode="HTML",reply_markup=kb
                            )
    await message.delete()

kbn=ReplyKeyboardMarkup(resize_keyboard=True) #вторая клава
kbn.add('Имя👩🏼‍💻').insert('Возраст⏳').add('Обо мне\n💁🏻‍♂️💁🏻‍♀️').insert('Мой профиль🌐').insert('Должность👩🏻‍🎓👨🏻‍🎓').insert('Отправить✅')


polee=''
@dp.message_handler(lambda message: message.text  in ["Заполнить анкету📝", 'Поправить анкету📝']) 
async def ancentdffs(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=7
    await bot.send_message(chat_id=message.from_user.id,
                            text="Анкету можно заполнять как хотите✅\n\nНо берите во внимание что анкету <b>рассматривают</b>😉.",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.from_user.id,
                            text='Выбирайте и корректируйте информацию о вас 🤙🏼!\n\nВ конце нажмите <b>Отправить✅</b> когда закончите🙂.',
                            parse_mode="HTML",reply_markup=kbn)
    await message.delete()


@dp.message_handler(regexp="Имя👩🏼‍💻")
async def nm(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=1
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Ваше имя пожалуйста👩🏼‍💻</b>",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )
    

@dp.message_handler(regexp="Возраст⏳")
async def age(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=2
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Ваш возраст пожалуйста⏳</b>",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )

@dp.message_handler(regexp="Обо мне\n💁🏻‍♂️💁🏻‍♀️")
async def bio(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=3
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Коротко из вашей биографии💁🏻‍♂️💁🏻‍♀️</b>",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )

@dp.message_handler(regexp="Мой профиль🌐")
async def inst(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=4
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Название социальной сети и ваш ник🌐</b>",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )

@dp.message_handler(regexp="Должность👩🏻‍🎓👨🏻‍🎓")
async def dol(message: types.message):
    global nicks
    nicks[message.from_user.id][5]=5
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>И кем же вы работаете?👩🏻‍🎓👨🏻‍🎓</b>",
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )

@dp.message_handler(regexp="Отправить✅")
async def senddfgfg(message: types.message):
    global nicks
    if 'Не указано' in nicks[message.from_user.id]:
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Охххх</b> похоже какое то поле не было заполнено💢\n\nПо кнопкам на клавиатуре можете дополнить анкету📝! " ,
                                parse_mode="HTML",reply_markup=kbn
                                )
    else:
        await upsert_user(message.from_user.id,nicks[message.from_user.id][0],int(nicks[message.from_user.id][1]),nicks[message.from_user.id][2],nicks[message.from_user.id][4],nicks[message.from_user.id][3])
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Поправить анкету📝')).insert('Gooooooo🗺')
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Классная анкета🫡 Жаль что я бот...🫠</b>\n\nНо не переживай😌 Что бы погулять с коллегой в прекрасном месте нажми <b>Gooooooo🗺</b>!",
                                parse_mode="HTML",reply_markup=kb
                                )
@dp.message_handler(regexp="Gooooooo🗺")
async def senddsf(message: types.message):
    global nicks
    
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Поправить анкету📝')).insert('Gooooooo🗺')
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Ищу кого нибудь вам на party🔮</b>",
                            parse_mode="HTML",reply_markup=kb
                            )
    await bot.send_sticker(chat_id=message.from_user.id,sticker="CAACAgUAAxkBAAJjV2Vos5G9tq41ZxU3VS0T3iGeSNF5AAIRAgACjncpV7JCuBOpLVzgMwQ",reply_markup=kb
                            )
    time.sleep(2)
    r=1
    while r:
        l=randint(1,len(nicks))
        ll=1
        for k in nicks:
            if 'Не указано' not in nicks[k] and k!=message.from_user.id and l==ll:
                r=0
                
                await bot.send_sticker(chat_id=message.from_user.id,sticker="CAACAgUAAxkBAAJjWWVouAABHa8-HY0Ia9aTztZ_UW7vVgAC5AUAAuFFKFcRGai3DMAJ4zME",reply_markup=kb
                            )
                await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Нашел🎉! Вот его анкета:</b>",
                            parse_mode="HTML",reply_markup=kb
                            )
                await bot.send_message(chat_id=message.from_user.id,
                            text=f"""
<b>Имя👩🏼‍💻: </b>{nicks[k][0]} <b>Возраст⏳: </b>{nicks[k][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[k][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[k][3]}\n
<b>Профиль🌐</b> : {nicks[k][4]}\n
                             """,
                            parse_mode="HTML",reply_markup=kb
                            )
                
                break
            ll+=1
    dd=randint(0,18)
    await bot.send_message(chat_id=message.from_user.id,
                                text='Место в котором вы можете провести время💞\n\n'+mesta[dd]['название']+'\n\n'+mesta[dd]['описание'],
                                parse_mode="HTML",reply_markup=kb)
    

                



@dp.message_handler()
async def musor(message: types.message):
    global nicks
    global polee
    if nicks[message.from_user.id][5]==0:
        await bot.send_message(chat_id=message.from_user.id,
                            text='Наверно такой команды нету🥲.\n\nНажмите <b>Что делать❓</b> для инструкции!',
                            parse_mode="HTML",reply_markup=kb
                            )
    if nicks[message.from_user.id][5]==7:
        await bot.send_message(chat_id=message.from_user.id,
                            text='Наверно такой команды нету🥲.\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )
    if nicks[message.from_user.id][5]==1:
        nicks[message.from_user.id][0]=message.text
        polee=f"""
<b>Имя👩🏼‍💻: </b>{nicks[message.from_user.id][0]} <b>Возраст⏳: </b>{nicks[message.from_user.id][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[message.from_user.id][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[message.from_user.id][3]}\n
<b>Профиль🌐</b> : {nicks[message.from_user.id][4]}\n
"""
        await bot.send_message(chat_id=message.from_user.id,
                            text=f'<b>Отлично🥰.</b> Теперь ваша анкета выглядит так:\n\n{polee}\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )

        nicks[message.from_user.id][5]=7
    if nicks[message.from_user.id][5]==2:
        nicks[message.from_user.id][1]=message.text
        polee=f"""
<b>Имя👩🏼‍💻: </b>{nicks[message.from_user.id][0]} <b>Возраст⏳: </b>{nicks[message.from_user.id][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[message.from_user.id][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[message.from_user.id][3]}\n
<b>Профиль🌐</b> : {nicks[message.from_user.id][4]}\n
"""
        await bot.send_message(chat_id=message.from_user.id,
                            text=f'<b>Отлично🥰.</b> Теперь ваша анкета выглядит так:\n\n{polee}\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )
        nicks[message.from_user.id][5]=7
    if nicks[message.from_user.id][5]==3:
        nicks[message.from_user.id][2]=message.text
        polee=f"""
<b>Имя👩🏼‍💻: </b>{nicks[message.from_user.id][0]} <b>Возраст⏳: </b>{nicks[message.from_user.id][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[message.from_user.id][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[message.from_user.id][3]}\n
<b>Профиль🌐</b> : {nicks[message.from_user.id][4]}\n
"""
        await bot.send_message(chat_id=message.from_user.id,
                            text=f'<b>Отлично🥰.</b> Теперь ваша анкета выглядит так:\n\n{polee}\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )
        nicks[message.from_user.id][5]=7

    if nicks[message.from_user.id][5]==4:
        nicks[message.from_user.id][4]=message.text
        polee=f"""
<b>Имя👩🏼‍💻: </b>{nicks[message.from_user.id][0]} <b>Возраст⏳: </b>{nicks[message.from_user.id][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[message.from_user.id][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[message.from_user.id][3]}\n
<b>Профиль🌐</b> : {nicks[message.from_user.id][4]}\n
"""
        await bot.send_message(chat_id=message.from_user.id,
                            text=f'<b>Отлично🥰.</b> Теперь ваша анкета выглядит так:\n\n{polee}\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )
        nicks[message.from_user.id][5]=7

    if nicks[message.from_user.id][5]==5:
        nicks[message.from_user.id][3]=message.text
        polee=f"""
<b>Имя👩🏼‍💻: </b>{nicks[message.from_user.id][0]} <b>Возраст⏳: </b>{nicks[message.from_user.id][1]}\n
<b>Обо мне💁🏻‍♂️💁🏻‍♀️:</b>\n
{nicks[message.from_user.id][2]}\n
<b>Должность👩🏻‍🎓👨🏻‍🎓:</b>\n
{nicks[message.from_user.id][3]}\n
<b>Профиль🌐</b> : {nicks[message.from_user.id][4]}\n
"""
        await bot.send_message(chat_id=message.from_user.id,
                            text=f'<b>Отлично🥰.</b> Теперь ваша анкета выглядит так:\n\n{polee}\n\nПо кнопкам на клавиатуре можете менять анкету📝!',
                            parse_mode="HTML",reply_markup=kbn
                            )
        nicks[message.from_user.id][5]=7




if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)