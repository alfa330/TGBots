from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
import random
from db_sea_battle import add_u, add_pw, add_g, pol_p, pol_sp

TOKEN=''
bot = Bot(TOKEN)
dp= Dispatcher(bot)

class gamer:
    def __init__(self, name):
        self.name =name    
        self.sost =0
        self.pole =[[[0,0] for aa in range(6)] for ii in range(6)]
        self.flat =0

        self.dr   =0 
        self.prev =0
    def sy(self,x,y,z=-1):
        if z==-1:
            return self.pole[int(x)][int(y)][0]
        else:
            self.pole[int(x)][int(y)][0]=z
    def sos(self,x,y,z=-1):
        if z==-1:
            return self.pole[int(x)][int(y)][1]
        else:
            self.pole[int(x)][int(y)][1]=z


sym=['🌊','❌','⭕️',]
nik={}

hels="""Добро пожаловать в наш Бот😁!

Тут можно сыграть в <b>Морской бой🛳</b> c вашими друзьями😼! 

<b>Начать игру⚓️</b> - нажмите на клавиатуре что бы начать игру🏖.

<b>Что делать❓</b> - нажмите если не знаете как можно играть😉.
"""

helf="""<b>Как играть:</b>

<b>1.</b> Оба игрока должны нажать <b>Начать игру⚓️</b>.

<b>2.</b> Введите <b>ID</b> друга или по кнопке <b>Мои игры🎮</b> выберите прошлого соперника, чтобы отправить приглашение в игру.

<b>3.</b> После успешного подключения выберите координаты короблей и с помощью своей меткости поражайте вражеские корабли.

"""



kb=ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Начать игру⚓️')).insert('Мои игры🎮').add('Что делать❓')

@dp.message_handler(commands=['start']) #Включает бота. Подключил его к базу
async def start_cm(message: types.message):
	global nik
	nik[message.from_user.id]=gamer(message.from_user.username)
	await add_u(message.from_user.id,message.from_user.username)
	await bot.send_message(chat_id=message.from_user.id,
                            text=hels,
                            parse_mode="HTML",reply_markup=kb
                            )
	await message.delete()

@dp.message_handler(regexp='Что делать❓')
async def helpp(message: types.message):
	await bot.send_message(chat_id=message.from_user.id,
                                text=helf,
                                parse_mode="HTML"
                                )


@dp.message_handler(regexp='Начать игру⚓️')
async def startgm(message: types.message):
	global nik
	nik[message.from_user.id].sost=1
	await bot.send_message(chat_id=message.from_user.id,
                            text=f"""Отправьте <b>ID</b> своего друга или выберите с кем поиграть по кнопке <b>Мои игры🎮</b> и ожидайте принятие от него🗺!\n\nВаш <b>ID - {message.from_user.id}</b>.
                            """,
                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
                            )
	await message.delete()

@dp.message_handler(regexp='Мои игры🎮')
async def mybat(message: types.message):
	global nik
	nik[message.from_user.id].sost=1
	t= await pol_sp(message.from_user.id)
	t=t[0]
	await bot.send_message(chat_id=message.from_user.id,
                            text=f"""Нажмите на <b>Бросить вызов🕹</b> если хотите сыграть с этим игроком ещё.\n\nВаша статистика:\n\nИгрок: <b>{t['nick']}🧑🏻‍💻</b>\nПобеды: <b>{t['victories']}⚔️</b>\nПроигрыши: <b>{t['defeats']}</b>🛟\n\nВ общем игр: <b>{t['total_games']}</b>⏳
                            """,
                            parse_mode="HTML"
                            )
	h = await pol_p(message.from_user.id)

	for t in h:
		ikb=InlineKeyboardMarkup(row_width=1)
		ikb.insert(InlineKeyboardButton(text='Бросить вызов🕹',callback_data='dddd'+' '+str(t['id'])))
		await bot.send_message(chat_id=message.from_user.id,
						text=f'''Игрок: <b>{t['nick']}🧑🏻‍💻</b>\nПобеды: <b>{t['victories']}⚔️</b>\nПроигрыши: <b>{t['defeats']}</b>🛟\n\nВ общем игр: <b>{t['total_games']}</b>⏳''',
						parse_mode='HTML',
						reply_markup=ikb
			)
	await message.delete()

@dp.message_handler(regexp='Вперед⚔️')
async def battle(message: types.message):
	if nik[message.from_user.id].sost==2:
		ikb=InlineKeyboardMarkup(row_width=6)
		[[ikb.insert(InlineKeyboardButton(text=sym[nik[message.from_user.id].sy(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
		await bot.send_message(chat_id=message.from_user.id,
		                            text='Выберите 8 любых позиций где у вас будет ваш корабль!',
		                            parse_mode="HTML",reply_markup=ReplyKeyboardRemove()
		                            )
		msg = await bot.send_message(chat_id=message.from_user.id,
		                            text='Что бы убрать корабль нажмите на позицию ещё раз!',
		                            parse_mode="HTML",reply_markup=ikb.insert(InlineKeyboardButton(text='Готов🔍',callback_data='999'))
		                            )
		nik[message.from_user.id].prev=msg.message_id








@dp.message_handler()
async def syst(message: types.message):
	if nik[message.from_user.id].sost==0:#ошибка команд
		await bot.send_message(chat_id=message.from_user.id,
                                text='Похоже такой команды нет, нажмите <b>Что делать❓</b> что бы узнать подробности.' ,
                                parse_mode="HTML"
                                )

	
	if nik[message.from_user.id].sost==1:#приглашение на игру
			try:
				if nik[int(message.text)].sost==1:
					ukb=InlineKeyboardMarkup(row_width=2)
					ukb.add(InlineKeyboardButton(text='Принять🛡',callback_data=' '.join(['prin',str(message.from_user.id)]))).insert(InlineKeyboardButton(text='Отклонить🌀',callback_data=' '.join(['otkl',str(message.from_user.id)])))
					await bot.send_message(chat_id=int(message.text),
	                                text=f'Вам поступило приглашение на игру от <b>{message.from_user.username}</b>.',
	                                parse_mode="HTML",reply_markup=ukb
	                                )
				else:
					print(0/1)
			except:
				await bot.send_message(chat_id=message.from_user.id,
	                                text='Похоже ваш друг не нажал <b>Начать игру⚓️</b> или не правильный <b>ID</b>!\n\n<b>Попробуйте снова🌐</b>',
	                                parse_mode="HTML"
		                            ) 
	else:
		await message.delete()


#-----------------------------------------------------------------------------------------------------------------------------------------

@dp.callback_query_handler()
async def att(callback: types.CallbackQuery):
	global nik
	callback.data=[*map(str,callback.data.split())]
	if nik[callback.from_user.id].sost==1: #[True,message.from_user.id,message.text] Подключение
		callback.data[1]=int(callback.data[1])
		if callback.data[0]=='prin':
			kbb=ReplyKeyboardMarkup(resize_keyboard=True)
			kbb.add(KeyboardButton('Вперед⚔️'))
			nik[callback.from_user.id].sost,nik[callback.data[1]].sost=2,2
			nik[callback.from_user.id].dr,nik[callback.data[1]].dr=callback.data[1],callback.from_user.id
			await add_pw(callback.data[1],callback.from_user.id)
			await add_pw(callback.from_user.id,callback.data[1])
			await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Вы одобрили запрос✅</b>\n\nНажмите <b>Вперед⚔️</b> что бы начать игру.',
                                parse_mode="HTML",reply_markup=kbb
                                )
			await bot.send_message(chat_id=callback.data[1],
                                text='<b>Ваш запрос одобрен✅</b>\n\nНажмите <b>Вперед⚔️</b> что бы начать игру.',
                                parse_mode="HTML",reply_markup=kbb
                                )
		elif callback.data[0]=='otkl':
			await bot.send_message(chat_id=callback.data[1],
                                text='<b>Запрос отклонен🚫</b>',
                                parse_mode="HTML"
                                )
			await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Запрос отклонен🚫</b>',
                                parse_mode="HTML"
                                )
		else:
			try:
				if nik[callback.data[1]].sost==1:
					ukb=InlineKeyboardMarkup(row_width=2)
					ukb.add(InlineKeyboardButton(text='Принять🛡',callback_data=' '.join(['prin',str(callback.from_user.id)]))).insert(InlineKeyboardButton(text='Отклонить🌀',callback_data=' '.join(['otkl',str(callback.from_user.id)])))
					await bot.send_message(chat_id=int(callback.data[1]),
	                                text=f'Вам поступило приглашение на игру от <b>{callback.from_user.username}</b>.',
	                                parse_mode="HTML",reply_markup=ukb
	                                )
					await bot.send_message(chat_id=callback.from_user.id,
									text=f'Приглашение успешно отправлено ожидайте✅',
									parse_mode='HTML'
						)
				else:
					print(0/1)
			except:
				await bot.send_message(chat_id=callback.from_user.id,
	                                text='Похоже ваш друг не нажал <b>Начать игру⚓️</b> или не правильный <b>ID</b>!\n\n<b>Попробуйте снова🌐</b>',
	                                parse_mode="HTML"
		                            ) 


#-----------------------------------------------------------------------------------------------------------------------------------------

	elif nik[callback.from_user.id].sost==2:#Выбор кораблей
		if callback.data[0]=='999':#когда выбраны все корабли
			if nik[callback.from_user.id].flat==8:
				nik[callback.from_user.id].sost=3
				await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Вы готовы к бою⛱</b>\n\n<b>Ожидаем друга🛟</b>',
                                parse_mode="HTML",
                                )
				if nik[callback.from_user.id].sost==3 and nik[nik[callback.from_user.id].dr].sost==3:#Когда оба готовы
					await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Ваш друг тоже готов к бою🪝</b>\n\n<b>Пора начинать...🏴‍☠️</b>',
                                parse_mode="HTML"
                                )
					await bot.send_message(chat_id=nik[callback.from_user.id].dr,
                                text='<b>Ваш друг тоже готов к бою🪝</b>\n\n<b>Пора начинать...🏴‍☠️</b>',
                                parse_mode="HTML"
                                )
					k=[callback.from_user.id,nik[callback.from_user.id].dr][random.randint(0,1)]
					kb3=ReplyKeyboardMarkup(resize_keyboard=True)
					kb3.add(KeyboardButton(f'🛳 у вас: {nik[k].flat}/8')).insert(f'⛴ у соперника: {nik[nik[k].dr].flat}/8')
					await bot.send_message(chat_id=k,
								text='<b>Сейчас ваш ход🕹</b>',
                                parse_mode="HTML",reply_markup=kb3
						)
					ikb=InlineKeyboardMarkup(row_width=6)
					[[ikb.insert(InlineKeyboardButton(text=sym[nik[k].sy(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
					msg=await bot.send_message(chat_id=k,
								text='<b>❌ - где не было кораблей. ⭕️ - где вы попали.</b>',
                                parse_mode="HTML",reply_markup=ikb
						)
					await bot.send_message(chat_id=nik[k].dr,
								text='<b>Ход соперника🧜🏼‍♂️</b>',
                                parse_mode="HTML"
						)
					nik[k].prev=msg.message_id


			else:
				await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
				ikb=InlineKeyboardMarkup(row_width=6)
				[[ikb.insert(InlineKeyboardButton(text=sym[nik[callback.from_user.id].sos(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
				msg = await bot.send_message(chat_id=callback.from_user.id,text=f'Вы ещё не выбрали достаточно кораблей.\n\n<b>Выбрано: {nik[callback.from_user.id].flat}/8</b>',parse_mode="HTML",reply_markup=ikb.insert(InlineKeyboardButton(text='Готов🔍',callback_data='999')))
				nik[callback.from_user.id].prev=msg.message_id

		elif nik[callback.from_user.id].sos(callback.data[0],callback.data[1])==0:#еще идет выбор
			if nik[callback.from_user.id].flat!=8:
				nik[callback.from_user.id].sos(callback.data[0],callback.data[1] ,1)
				nik[callback.from_user.id].flat+=1
				await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
				ikb=InlineKeyboardMarkup(row_width=6)
				[[ikb.insert(InlineKeyboardButton(text=sym[nik[callback.from_user.id].sos(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
				msg = await bot.send_message(chat_id=callback.from_user.id,
				                            text='Что бы убрать корабль нажмите на позицию ещё раз!',
				                            parse_mode="HTML",reply_markup=ikb.insert(InlineKeyboardButton(text='Готов🔍',callback_data='999'))
				                            )
			elif nik[callback.from_user.id].flat==8:
				await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
				ikb=InlineKeyboardMarkup(row_width=6)
				[[ikb.insert(InlineKeyboardButton(text=sym[nik[callback.from_user.id].sos(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
				msg = await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Вы достигли лимита по короблям🪝</b>\n\nЕсли вы закончили с выбром короблей нажмите <b>Готов🔍</b>',
                                parse_mode="HTML",reply_markup=ikb.insert(InlineKeyboardButton(text='Готов🔍',callback_data='999'))
                                )
			nik[callback.from_user.id].prev=msg.message_id
			return await callback.answer(text=f'Выбрано: {nik[callback.from_user.id].flat}/8')




		else:
			print(1)
			nik[callback.from_user.id].sos(callback.data[0],callback.data[1] ,0)
			nik[callback.from_user.id].flat-=1
			ikb=InlineKeyboardMarkup(row_width=6)
			[[ikb.insert(InlineKeyboardButton(text=sym[nik[callback.from_user.id].sos(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
			await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
			msg = await bot.send_message(chat_id=callback.from_user.id,
			                            text='Что бы убрать корабль нажмите на позицию ещё раз!',
			                            parse_mode="HTML",reply_markup=ikb.insert(InlineKeyboardButton(text='Готов🔍',callback_data='999'))
			                            )
			nik[callback.from_user.id].prev=msg.message_id
			return await callback.answer(text=f'Выбрано: {nik[callback.from_user.id].flat}/8')
			



#-----------------------------------------------------------------------------------------------------------------------------------------
	if nik[callback.from_user.id].sost==3 and nik[nik[callback.from_user.id].dr].sost==3:
		p=0
		if  nik[nik[callback.from_user.id].dr].sos(callback.data[0],callback.data[1])==1:
			p=1
			nik[nik[callback.from_user.id].dr].sos(callback.data[0],callback.data[1] ,0)
			nik[nik[callback.from_user.id].dr].sy(callback.data[0],callback.data[1] ,2)
			await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
			nik[nik[callback.from_user.id].dr].flat-=1
			kb3=ReplyKeyboardMarkup(resize_keyboard=True)
			kb3.add(KeyboardButton(f'🛳 у вас: {nik[callback.from_user.id].flat}/8')).insert(f'⛴ у соперника: {nik[nik[callback.from_user.id].dr].flat}/8')
			await bot.send_message(chat_id=callback.from_user.id,
                                text=['🌊 Отлично, как стрела в цель! 🎯','🚀 Прямо в яблочко! Морской стиль! 🌊','🌈 Это как сокровище на дне океана – прямое попадание! 💰','🎯 Прямиком в цель, словно стрела Нептуна! 🌊'][random.randint(0,3)],
                                parse_mode="HTML",reply_markup=kb3
                                )
		elif nik[nik[callback.from_user.id].dr].sos(callback.data[0],callback.data[1])==0 and nik[nik[callback.from_user.id].dr].sy(callback.data[0],callback.data[1])==0:
			p=1
			nik[nik[callback.from_user.id].dr].sy(callback.data[0],callback.data[1] ,1)
			kb3=ReplyKeyboardMarkup(resize_keyboard=True)
			kb3.add(KeyboardButton(f'🛳 у вас: {nik[callback.from_user.id].flat}/8')).insert(f'⛴ у соперника: {nik[nik[callback.from_user.id].dr].flat}/8')
			await bot.delete_message(chat_id=callback.from_user.id, message_id=nik[callback.from_user.id].prev)
			await bot.send_message(chat_id=callback.from_user.id,
                                text=['<b>Никак, словно стрела, не достигла цели! 😢</b>','<b>Промах, не в яблочко! Морской стиль в ожидании. 😞</b>','<b>Это как потерянное сокровище на дне океана – упущенное попадание! 💔</b>','<b>Мимо цели, как вихрь, не по стилю Нептуна! 😔</b>'][random.randint(0,3)],
                                parse_mode="HTML",reply_markup=kb3
                                )
		else:
			await bot.send_message(chat_id=callback.from_user.id,
                                text='<b>Уже выбранная позиция💢</b>',
                                parse_mode="HTML"
                                )
		if nik[nik[callback.from_user.id].dr].flat==0 or nik[callback.from_user.id].flat==0:
			kb=ReplyKeyboardMarkup(resize_keyboard=True)
			kb.add(KeyboardButton('Начать игру⚓️')).insert('Мои игры🎮').add('Что делать❓')
			await bot.send_message(chat_id=callback.from_user.id if nik[callback.from_user.id].flat==0 else nik[callback.from_user.id].dr,
				text='<b>Все ваши корабли затоплены, но один проигрыш еще не конец...🔥</b>',parse_mode="HTML"
				)
			await bot.send_sticker(chat_id=nik[callback.from_user.id].dr,
				sticker=['CAACAgIAAxkBAAJpH2WBKXVrx78tgcVv4wxl6IVcJTPDAAKGAAOmysgMdfHgn18JJQIzBA','CAACAgIAAxkBAAJpIWWBKe0hnJ3zjqWyoOyFcCYuelqWAAL5FQACcJfxSgxcbEP4tXDpMwQ','CAACAgIAAxkBAAJpI2WBKfPbtAaWjpNYJKMqPz9bYYIzAAIIFgAC-oQ5SRmaxtqWQB91MwQ','CAACAgQAAxkBAAJpJWWBKrBK1ql1D9gTfqpX-OR8g2JdAALmCQACmJPQUqBNScBr-LtXMwQ'][random.randint(0,3)],
				reply_markup=kb,
                            )
			await add_g(callback.from_user.id if nik[callback.from_user.id].flat!=0 else nik[callback.from_user.id].dr,callback.from_user.id if nik[callback.from_user.id].flat==0 else nik[callback.from_user.id].dr)
			nik[nik[callback.from_user.id].dr]=gamer(nik[nik[callback.from_user.id].dr].name)


			await bot.send_message(chat_id=(callback.from_user.id if nik[callback.from_user.id].flat!=0 else nik[callback.from_user.id].dr),
				text='<b>Поздравляю с победой командир, так держать🔥</b>',parse_mode="HTML"
				)
			await bot.send_sticker(chat_id=callback.from_user.id,
				sticker=['CAACAgIAAxkBAAJpH2WBKXVrx78tgcVv4wxl6IVcJTPDAAKGAAOmysgMdfHgn18JJQIzBA','CAACAgIAAxkBAAJpIWWBKe0hnJ3zjqWyoOyFcCYuelqWAAL5FQACcJfxSgxcbEP4tXDpMwQ','CAACAgIAAxkBAAJpI2WBKfPbtAaWjpNYJKMqPz9bYYIzAAIIFgAC-oQ5SRmaxtqWQB91MwQ','CAACAgQAAxkBAAJpJWWBKrBK1ql1D9gTfqpX-OR8g2JdAALmCQACmJPQUqBNScBr-LtXMwQ'][random.randint(0,3)],
				reply_markup=kb
                            )
			nik[callback.from_user.id]=gamer(nik[callback.from_user.id].name)
			p=0
		if p:
			kb3=ReplyKeyboardMarkup(resize_keyboard=True)
			kb3.add(KeyboardButton(f'🛳 у вас: {nik[nik[callback.from_user.id].dr].flat}/8')).insert(f'⛴ у соперника: {nik[callback.from_user.id].flat}/8')
			await bot.send_message(chat_id=nik[callback.from_user.id].dr,
									text='<b>Сейчас ваш ход🕹</b>',
		                            parse_mode="HTML",reply_markup=kb3
								)
			ikb=InlineKeyboardMarkup(row_width=6)
			[[ikb.insert(InlineKeyboardButton(text=sym[nik[callback.from_user.id].sy(t,u)],callback_data=' '.join([str(t) ,str(u)]))) for u in range(6)] for t in range(6)]
			msg = await bot.send_message(chat_id=nik[callback.from_user.id].dr,
									text='<b>❌ - где не было кораблей. ⭕️ - где вы попали.</b>',
		                            parse_mode="HTML",reply_markup=ikb
								)
			await bot.send_message(chat_id=callback.from_user.id,
								text='<b>Ход соперника🧜🏼‍♂️</b>',
                                parse_mode="HTML"
						)
			nik[nik[callback.from_user.id].dr].prev=msg.message_id
		


if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)