from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
import io 
import json
from random import shuffle, choice
import string
from math import ceil
from html import escape


TOKEN=''
bot = Bot(TOKEN)
dp= Dispatcher(bot=bot, storage=MemoryStorage())

class npass(StatesGroup):
    le  = State()


async def gener(le,al=0,dig=0,sym=0):
    letters = string.ascii_letters
    digits = string.digits
    specials = string.punctuation
    x=sum([al,dig,sym])
    all_ch=[]
    if al:
        all_ch+=[choice(letters) for _ in range(ceil(le/x))]
    if dig:
        all_ch+=[choice(digits) for _ in range(ceil(le/x))]
    if sym:
        all_ch+=[choice(specials) for _ in range(ceil(le/x))]
    shuffle(all_ch)
    return ''.join(all_ch[:le])

@dp.message_handler(commands=['start'])
async def start_cm(message: types.message):
    ikb=ReplyKeyboardMarkup(resize_keyboard=True)
    ikb.add(KeyboardButton('Create new password🧑🏻‍💻'))
    await bot.send_message(chat_id=message.from_user.id,
                            text='Hi! In this bot you can create passwords. Tap to the <b>Create new password🧑🏻‍💻</b> button and start!',
                            parse_mode="HTML",reply_markup=ikb
                            )
    await message.delete()

@dp.message_handler(regexp="Create new password🧑🏻‍💻")
async def anc(message: types.message, state: FSMContext):
	await bot.send_message(chat_id=message.from_user.id,
                            text='Whrite your password lentn, only numbers and greater than 7!🖊',
                            parse_mode="HTML"
                            )
	await npass.le.set()
	await message.delete()

@dp.message_handler(state=npass.le)
async def save_pho(message: types.Message, state: FSMContext):
	ikb=InlineKeyboardMarkup(row_width=1)
	ikb.add(InlineKeyboardButton(text='Numbers🔢',callback_data='Numbers🔢')).add(InlineKeyboardButton(text='Letters🆎',callback_data='Letters🆎')).add(InlineKeyboardButton(text='Symbols#️⃣',callback_data='Symbols#️⃣'))
	async with state.proxy() as data:
		data['pass']=set()
	try:
		if int(message.text)>7:
			async with state.proxy() as data:
				data['ch']=int(message.text)
			await bot.send_message(chat_id=message.from_user.id,
		                            text=f"Choose what your password should contain!🗂\nYou choose: {' '.join(data['pass'])}",
		                            parse_mode="HTML",reply_markup=ikb
		                            )

		else:
			print(1/0)
	except:
		await bot.send_message(chat_id=message.from_user.id,
	                            text='Only numbers and greater than 7!🖊',
	                            parse_mode="HTML"
	                            )

@dp.callback_query_handler(state=npass.le)
async def insert_to_(callback: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data=data
	ikb=InlineKeyboardMarkup(row_width=1)
	ikb.add(InlineKeyboardButton(text='Numbers🔢',callback_data='Numbers🔢')).add(InlineKeyboardButton(text='Letters🆎',callback_data='Letters🆎')).add(InlineKeyboardButton(text='Symbols#️⃣',callback_data='Symbols#️⃣'))
	if callback.data=='New':
		ikb=InlineKeyboardMarkup(row_width=1)
		ikb.add(InlineKeyboardButton(text='ReCreate♻️',callback_data='New'))
		async with state.proxy() as data:
			data=data
		le,al,dig,sym=data['ps']
		passw=await gener(le,al,dig,sym)
		await bot.edit_message_text(text=f'Your password is created: \n<pre>{escape(passw)}</pre>',
								chat_id=callback.from_user.id,
								message_id=callback.message.message_id,
								parse_mode='HTML',
								reply_markup=ikb
			)
	elif callback.data=='Create✅':
		async with state.proxy() as data:
			data=data
		le,al,dig,sym=data['ch'],1 if 'Letters🆎' in data['pass'] else 0,1 if 'Numbers🔢' in data['pass'] else 0,1 if 'Symbols#️⃣' in data['pass'] else 0
		passw=await gener(le,al,dig,sym)
		async with state.proxy() as data:
			data['ps']=[le,al,dig,sym]
		ikb=InlineKeyboardMarkup(row_width=1)
		ikb.add(InlineKeyboardButton(text='ReCreate♻️',callback_data='New'))
		await bot.send_message(text=f'''Your password is created: \n<pre>{escape(passw)}</pre>''',
								chat_id=callback.from_user.id,
								parse_mode='HTML',
								reply_markup=ikb
			)
		await callback.message.delete()

	elif callback.data not in data['pass']:
		async with state.proxy() as data:
			data['pass'].add(callback.data)
		if data['pass']!=set():
			ikb.add(InlineKeyboardButton(text='Create✅',callback_data='Create✅'))
		await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text=f"Choose what your password should contain!🗂\nYou choose: {' '.join(list(data['pass']))}", reply_markup=ikb)
	else:
		async with state.proxy() as data:
			data['pass'].remove(callback.data)
		if data['pass']!=set():
			ikb.add(InlineKeyboardButton(text='Create✅',callback_data='Create✅'))
		await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text=f"Choose what your password should contain!🗂\nYou choose: {' '.join(list(data['pass']))}", reply_markup=ikb)


if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)