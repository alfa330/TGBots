from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
import io 
import json
from Books_db import add_user,add_book,kp_b,del_kor,add_order,gnbi,ab_c,goi


TOKEN=''
bot = Bot(TOKEN)
dp= Dispatcher(bot=bot, storage=MemoryStorage())

storage = MemoryStorage()
class New_book(StatesGroup):
    title=   State()
    author=  State()
    genre=   State()
    price=   State()
    rating=  State()
    f_photo= State()
    c_photo= State()
    
class new_ord(StatesGroup):
    city=    State()
    adress = State()


hells=''' 
<b>Добро пожаловать в наш уютный книжный магазин! 📖✨ Мы рады видеть тебя здесь.</b>

У нас ты найдешь огромный выбор книг на любой вкус и возраст. 📚🌈 Новинки, бестселлеры, классика - всё, что нужно для приятного чтения.

Не знаешь, с чего начать? Мы всегда готовы помочь с выбором и подсказать самые интересные книги. 💬💡

Желаем приятных покупок и увлекательного чтения! 📚🛒🎉

'''

hells2='''Добро пожаловать в админ панель магазина книг, вы можете добавить книгу нажав на кнопку!'''


@dp.message_handler(commands=['start']) #Включает бота. Подключил его к магазину
async def start_cm(message: types.message):
    await add_user(message.from_user.id)
    if message.from_user.id in [1241056892, 883052245]:
        ikb=InlineKeyboardMarkup(row_witdh=1)
        ikb.insert(InlineKeyboardButton(text='Добавить книгу📚',callback_data='add_book'))
        await bot.send_message(chat_id=message.from_user.id,
                            text=hells2,
                            parse_mode="HTML",
                            reply_markup=ikb
                            )
    else:
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Посмотреть книги📚')).insert(KeyboardButton('Моя Корзина🗑')).add(KeyboardButton('Мои Заказы📦'))
        await bot.send_message(chat_id=message.from_user.id,
                            text=hells,
                            parse_mode="HTML",
                            reply_markup=kb
                            )
    await message.delete()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#ВЫБОР ЧТО ДЕЛАТЬ ПОЛЬЗ
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(regexp='Моя Корзина🗑')
async def sh_bo(message: types.message):
    h=await kp_b(message.from_user.id)
    for t in h:
        media1 = [types.InputMediaPhoto(media=t['front_cover_photo']), types.InputMediaPhoto(media=t['back_cover_photo'])]
        msg1=await bot.send_media_group(chat_id=message.from_user.id, media=media1)
        ikb=InlineKeyboardMarkup(row_witdh=2)
        ikb.insert(InlineKeyboardButton(text='Заказать🛒',callback_data='ord'+str(t['id']))).insert(InlineKeyboardButton(text='Убрать с корзины❌',callback_data='del'+str(t['id'])+'$'+str(msg1[0].message_id)+'$'+str(msg1[1].message_id)))
        await bot.send_message(chat_id=message.from_user.id,
                                text=f"<b>Название</b>: {t['title']}\n<b>Автор</b>:{t['author']}\n\n<b>Цена</b>: {t['price']}₸ <b>Жанр</b>: {t['genre']} <b>Рейтинг</b>: {t['rating']}|5",
                                parse_mode='HTML',
                                reply_markup=ikb
            )
    await bot.send_message(chat_id=message.from_user.id,text=f'Это все ваши книги в корзине!📖\n\nВсего: <b>{len(h)}</b>\n\nЧто бы добавить ещё, можете подобрать книгу по вкусу в <b>Посмотреть книги📚</b>',parse_mode='HTML')

@dp.message_handler(regexp='Посмотреть книги📚')
async def sh_qa(message: types.message):
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.row(
        InlineKeyboardButton(text='Фантастика🛸', callback_data='shwФантастика🛸$0'),
        InlineKeyboardButton(text='Детектив🔍', callback_data='shwДетектив🔍$0'),
        InlineKeyboardButton(text='Роман💖', callback_data='shwРоман💖$0')
    )
    ikb.row(
        InlineKeyboardButton(text='Приключения🌍', callback_data='shwПриключения🌍$0'),
        InlineKeyboardButton(text='Фэнтези🐉', callback_data='shwФэнтези🐉$0'),
        InlineKeyboardButton(text='Триллер🔥', callback_data='shwТриллер🔥$0')
    )
    ikb.row(
        InlineKeyboardButton(text='Хоррор💀', callback_data='shwХоррор💀$0'),
        InlineKeyboardButton(text='Научное🔬', callback_data='shwНаучное🔬$0'),
        InlineKeyboardButton(text='Классика📖', callback_data='shwКлассика📖$0')
    )
    await bot.send_message(text='Что бы начать смотреть книги выберите <b>Жанр📜</b>',chat_id=message.from_user.id,parse_mode='HTML',reply_markup=ikb)

@dp.message_handler(regexp='Мои Заказы📦')
async def sh_or(message: types.message):
    h= await goi(message.from_user.id)
    x= 0
    for t in h:
        x+= t['price']
        await bot.send_message(chat_id=message.from_user.id,
                                text=f"<b>Номер заказа</b>: {t['order_id']}\n<b>Название</b>: {t['title']}\n\n<b>Цена</b>: {t['price']}₸\n<b>Дата</b>: {t['order_date'].strftime('%Y-%m-%d %H:%M:%S')} <b>Статус</b>: {t['order_status']}",
                                parse_mode='HTML'
            )
    await bot.send_message(chat_id=message.from_user.id,
                            text=f'Цена ваших заказов: <b>{x}₸</b>\n\nВ общем книг: <b>{len(h)}</b>📖',
                            parse_mode='HTML'
        )
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Допнуть новую книгу
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=New_book.title)        #ТЕМА
async def nazv(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await bot.send_message(text='<b>Этап добавления книги</b>: 2 из 7📍\n\nНапишите ФИО автора книги🧑🏻‍💻',chat_id=message.from_user.id,parse_mode='HTML')
    await New_book.next()

@dp.message_handler(state=New_book.author)       #АВТОР
async def authorr(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['author'] = message.text
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.row(
        InlineKeyboardButton(text='Фантастика🛸', callback_data='Фантастика🛸'),
        InlineKeyboardButton(text='Детектив🔍', callback_data='Детектив🔍'),
        InlineKeyboardButton(text='Роман💖', callback_data='Роман💖')
    )
    ikb.row(
        InlineKeyboardButton(text='Приключения🌍', callback_data='Приключения🌍'),
        InlineKeyboardButton(text='Фэнтези🐉', callback_data='Фэнтези🐉'),
        InlineKeyboardButton(text='Триллер🔥', callback_data='Триллер🔥')
    )
    ikb.row(
        InlineKeyboardButton(text='Хоррор💀', callback_data='Хоррор💀'),
        InlineKeyboardButton(text='Научное🔬', callback_data='Научное🔬'),
        InlineKeyboardButton(text='Классика📖', callback_data='Классика📖')
    )
    await bot.send_message(text='<b>Этап добавления книги</b>: 3 из 7📍\n\nВыберите жанр книги',chat_id=message.from_user.id,parse_mode='HTML',reply_markup=ikb)
    await New_book.next()

@dp.callback_query_handler(state=New_book.genre) #ЖАНР
async def genree(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['genre'] = callback.data
    await bot.send_message(text='<b>Этап добавления книги</b>: 4 из 7📍\n\nСтоимость данной книги в тенге💸',chat_id=callback.from_user.id,parse_mode='HTML')
    await New_book.next()

@dp.message_handler(state=New_book.price)        #ЦЕНА
async def prs(message: types.message, state: FSMContext):
    try:
        float(message.text)
        async with state.proxy() as data:
            data['price'] = message.text
        await bot.send_message(text='<b>Этап добавления книги</b>: 5 из 7📍\n\nРейтинг этой книги с 2 цифрами после запятой📊',chat_id=message.from_user.id,parse_mode='HTML')
        await New_book.next()
    except:
        await bot.send_message(text='Пишите лишь цифры без каких либо знаков или букв💢',chat_id=message.from_user.id,parse_mode='HTML')

@dp.message_handler(state=New_book.rating)       #РЕЙТИНГ
async def rtng(message: types.message, state: FSMContext):
    try:
        if float(message.text)<=5:
            async with state.proxy() as data:
                data['rating'] = message.text
            await bot.send_message(text='<b>Этап добавления книги</b>: 6 из 7📍\n\nФото этой книги с передней стороны, не группируя!📷',chat_id=message.from_user.id,parse_mode='HTML')
            await New_book.next()
        else:
            1/0
    except:
        await bot.send_message(text='Пишите лишь цифры без каких либо знаков или букв не больше 5💢',chat_id=message.from_user.id,parse_mode='HTML')

@dp.message_handler(content_types=['photo'], state=New_book.f_photo) #С ПЕРЕДИ
async def save_otoud(message: types.message, state: FSMContext):
    if message.media_group_id:
        await bot.send_message(chat_id=message.from_user.id,
                                        text= f'Отправляйте указанное фото по отдельности❌',
                                        parse_mode="HTML"
                                        )
    else:
        async with state.proxy() as data:
            data['f_photo'] = message.photo[-1].file_id
        await bot.send_message(chat_id=message.from_user.id,
                                        text= f'<b>Этап добавления книги</b>: 7 из 7📍\n\nФото этой книги с задней стороны, не группируя!📷',
                                        parse_mode="HTML"
                                        )
        await New_book.next()

@dp.message_handler(content_types=['photo'], state=New_book.c_photo) #СЗАДИ - ФИНИШ
async def save_phod(message: types.message, state: FSMContext):
    if message.media_group_id:
        await bot.send_message(chat_id=message.from_user.id,
                                        text= f'Отправляйте указанное фото по отдельности❌',
                                        parse_mode="HTML"
                                        )
    else:
        ikb=InlineKeyboardMarkup(row_witdh=1)
        ikb.insert(InlineKeyboardButton(text='Добавить книгу📚',callback_data='add_book'))
        async with state.proxy() as data:
            data['c_photo'] = message.photo[-1].file_id
        await bot.send_message(chat_id=message.from_user.id,
                                        text= f'<b>Ваша книга успешно сохранена✅</b>',
                                        parse_mode="HTML",
                                        reply_markup=ikb
                                        )
        await add_book(data)
        await state.finish()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#ОФОРМЛЕНИЕ ЗАКАЗА
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(state=new_ord.city) #ГОРОД
async def cityy(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['adress']=callback.data
    await bot.send_message(text=f'Отлично ваш город <b>{callback.data}</b>🔥\n\nНапишите адресс доставки📦',chat_id=callback.from_user.id,parse_mode='HTML')
    await new_ord.next()

@dp.message_handler(state=new_ord.adress)      #АДРЕСС
async def adr(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['adress']=data['adress']+' - '+message.text
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Посмотреть книги📚')).insert(KeyboardButton('Моя Корзина🗑')).add(KeyboardButton('Мои Заказы📦'))   
    await bot.send_message(text=f'''Отлично место доставки <b>{data['adress']}</b>🔥\n\nЗайдите в <b>Мои Заказы📦</b> что бы смотреть за статусом вашего заказа✅''', 
                            chat_id=message.from_user.id, 
                            parse_mode='HTML', 
                            reply_markup=kb)
    await add_order(data)
    t=data
    await bot.send_message(chat_id=1241056892,
                                text=f"<b>Заказчик</b>: @{message.from_user.username}\n<b>Айди книги</b>: {t['book_id']}",
                                parse_mode='HTML'
            )
    await state.finish()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------


@dp.callback_query_handler()
async def inser(callback: types.CallbackQuery, state: FSMContext):
    
    if callback.data[:3]=='del':    #УДАЛИТЬ КНИГУ ИЗ КОРЗИНЫ
        await del_kor(int(callback.data[3:callback.data.index('$')]),callback.from_user.id)
        msg1=callback.data[callback.data.index('$')+1:].split('$')
        await bot.delete_message(chat_id=callback.from_user.id,message_id=int(msg1[0]))
        await bot.delete_message(chat_id=callback.from_user.id,message_id=int(msg1[1]))
        await bot.delete_message(chat_id=callback.from_user.id,message_id=callback.message.message_id)
    
    if callback.data[:3]=='ord':    #НАЗНАЧИТЬ ЗАКАЗ
        async with state.proxy() as data:
            data['user_id']=callback.from_user.id
            data['book_id']=int(callback.data[3:])
        ikb=InlineKeyboardMarkup(row_width=2)
        ikb.insert(InlineKeyboardButton(text='Актау',callback_data='Актау')).insert(InlineKeyboardButton(text='Актобе',callback_data='Актобе')).insert(InlineKeyboardButton(text='Алматы',callback_data='Алматы')).insert(InlineKeyboardButton(text='Астана',callback_data='Астана')).insert(InlineKeyboardButton(text='Атырау',callback_data='Атырау')).insert(InlineKeyboardButton(text='Жанаозен',callback_data='Жанаозен')).insert(InlineKeyboardButton(text='Караганда',callback_data='Караганда')).insert(InlineKeyboardButton(text='Каскелен',callback_data='Каскелен')).insert(InlineKeyboardButton(text='Кокшетау',callback_data='Кокшетау')).insert(InlineKeyboardButton(text='Костанай',callback_data='Костанай')).insert(InlineKeyboardButton(text='Кызылорда',callback_data='Кызылорда')).insert(InlineKeyboardButton(text='Павлодар',callback_data='Павлодар')).insert(InlineKeyboardButton(text='Петропавловск',callback_data='Петропавловск')).insert(InlineKeyboardButton(text='Семей',callback_data='Семей')).insert(InlineKeyboardButton(text='Талдыкорган',callback_data='Талдыкорган')).insert(InlineKeyboardButton(text='Тараз',callback_data='Тараз')).insert(InlineKeyboardButton(text='Темиртау',callback_data='Темиртау')).insert(InlineKeyboardButton(text='Туркестан',callback_data='Туркестан')).insert(InlineKeyboardButton(text='Уральск',callback_data='Уральск')).insert(InlineKeyboardButton(text='Усть-Каменогорск',callback_data='Усть-Каменогорск')).insert(InlineKeyboardButton(text='Шымкент',callback_data='Шымкент'))
        await bot.send_message(chat_id=callback.from_user.id,
                                text='Хороший выбор, введите информацию для доставки✅',
                                parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                                )
        await bot.send_message(chat_id=callback.from_user.id,
                                text='Выберите ваш город🗺\nЕсли же его нету в списке можете выбрать ближайший✔️',
                                parse_mode="HTML",reply_markup=ikb
                                )
        await new_ord.city.set()
    
    if callback.data=='add_book':   #НАЧАЛО ДОБАВЛЕНИЯ КНИГИ
        await bot.send_message(text='<b>Этап добавления книги</b>: 1 из 7📍\n\nНапишите название книги🖊',chat_id=callback.from_user.id,parse_mode='HTML')
        await New_book.title.set()

    if callback.data[:3]=='shw':    #ПОДБОР КНИГ
        idd=int(callback.data[callback.data.index('$')+1:])
        t= await gnbi(idd,callback.data[3:callback.data.index('$')])
        if t!=None:
            media1 = [types.InputMediaPhoto(media=t['front_cover_photo']), types.InputMediaPhoto(media=t['back_cover_photo'])]
            msg1 = await bot.send_media_group(chat_id=callback.from_user.id, media=media1)
            ikb=InlineKeyboardMarkup(row_witdh=2)
            ikb.insert(InlineKeyboardButton(text='Заказать📦',callback_data='ord'+str(t['id']))).insert(InlineKeyboardButton(text='В корзину🛒',callback_data='adc'+str(t['id']))).insert(InlineKeyboardButton(text=f'''Ещё {callback.data[3:callback.data.index('$')]}''',callback_data=callback.data[:callback.data.index('$')+1]+str(t['id'])))
            await bot.send_message(chat_id=callback.from_user.id,
                                    text=f"<b>Название</b>: {t['title']}\n<b>Автор</b>:{t['author']}\n\n<b>Цена</b>: {t['price']}₸ <b>Жанр</b>: {t['genre']} <b>Рейтинг</b>: {t['rating']}|5",
                                    parse_mode='HTML',
                                    reply_markup=ikb
                )
        else:
            await bot.send_message(chat_id=callback.from_user.id,
                            text=f'''Пока что вы посмотрели все книги в жанре <b>{callback.data[3:callback.data.index('$')]}</b>\n\nСкоро будут новые🔥 Можете выбрать и другие жанры по кнопке <b>Посмотреть книги📚</b>''',
                            parse_mode='HTML'
                )

    if callback.data[:3]=='adc':    #ДОБАВЛЕНИЕ КНИГИ В КРЗ
        await callback.answer(text=f'+1 книга в корзину🛒') 
        await ab_c(int(callback.data[3:]), callback.from_user.id)



if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)