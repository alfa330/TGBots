from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
import io 
import json
from db_otamag import all_id, add_c, all_p, crea_o, crea_o_d, get_o_d, get_o_i, del_ord

TOKEN=''
bot = Bot(TOKEN)
dp= Dispatcher(bot=bot, storage=MemoryStorage())


hells=''' 
<b>👋 Hi there!</b>
    Welcome to our grocery store ! 🛒
    
    We’re delighted to have you here and ready to assist with all your shopping needs. In our store, you’ll find:
    <b>- Fresh fruits 🍎</b>
    <b>- Vegetables 🥦</b>
    <b>- Delicious bakery items 🍞</b>
    <b>- Sweets 🍬</b>
    <b>- Sushi 🍣</b>
    <b>- Fast food 🍔</b>
    <b>- Beverages 🥤</b>
    <b>- Dairy products 🧀</b>
    
    Click on the <b>Sign up🌐</b> button to register in our bot! 😊
    
    <b>Happy shopping! 🛍️</b>

'''
hells3=''' 
<b>👋 Hi there!</b>
    Welcome to our grocery store ! 🛒
    
    We’re delighted to have you here and ready to assist with all your shopping needs. In our store, you’ll find:
    <b>- Fresh fruits 🍎</b>
    <b>- Vegetables 🥦</b>
    <b>- Delicious bakery items 🍞</b>
    <b>- Sweets 🍬</b>
    <b>- Sushi 🍣</b>
    <b>- Fast food 🍔</b>
    <b>- Beverages 🥤</b>
    <b>- Dairy products 🧀</b>
    
    If you have any questions or need assistance, just let @Alfa3303 know. We’re always here to help! 😊
    
    <b>Happy shopping! 🛍️</b>

'''

hells2='''👋 Hi there! Welcome to our admin panel! 🛒

View all orders and manage them 📝.

Happy managing! 🛠️'''

class new_cost(StatesGroup):
    cname=   State()
    address= State()
    city=    State()
    phone=   State()

class new_ord(StatesGroup):
    magaz=   State()

@dp.message_handler(commands=['start']) #Включает бота. Подключил его к магазину
async def start_cm(message: types.message):
    if message.from_user.id in [1241056892]:
        ikb=InlineKeyboardMarkup(row_witdh=1)
        ikb.insert(InlineKeyboardButton(text='Add product🗂',callback_data='add_prod'))
        await bot.send_message(chat_id=message.from_user.id,
                            text=hells2,
                            parse_mode="HTML",
                            reply_markup=ikb
                            )
    elif await all_id(message.from_user.id)==[]:
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Sign up🌐'))
        await bot.send_message(chat_id=message.from_user.id,
                            text=hells,
                            parse_mode="HTML",
                            reply_markup=kb
                            )
    else:
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Magazine🛍')).insert(KeyboardButton('My orders📦'))
        await bot.send_message(chat_id=message.from_user.id,
                            text=hells3,
                            parse_mode="HTML",
                            reply_markup=kb
                            )
    await message.delete()


#---------------------------------------------------------------------------------------------------------------------------------
#РЕГИСТРАЦИЯ
#---------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(regexp='Sign up🌐')
async def sh_bo(message: types.message):
    await bot.send_message(text='<b>Registration stage</b>: 1 of 4📍\n\nWrite your contact name🖊',
                            chat_id=message.from_user.id,
                            parse_mode='HTML',
                            reply_markup= ReplyKeyboardRemove())
    await new_cost.cname.set()

@dp.message_handler(state=new_cost.cname)                    #ИМЯ
async def authorr(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['id']  = message.from_user.id
        data['acc'] = message.from_user.username
        data['cname'] = message.text
    await message.answer(text=f'Great <b>{message.text}</b>\n\n<b>Registration stage</b>: 2 of 4📍\n\nWrite your adress📦',parse_mode='HTML')
    await new_cost.next()

@dp.message_handler(state=new_cost.address)                  #АДРЕСС
async def ytre(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text
    ikb=InlineKeyboardMarkup(row_width=2)
    ikb.insert(InlineKeyboardButton(text='Актау',callback_data='Актау')).insert(InlineKeyboardButton(text='Актобе',callback_data='Актобе')).insert(InlineKeyboardButton(text='Алматы',callback_data='Алматы')).insert(InlineKeyboardButton(text='Астана',callback_data='Астана')).insert(InlineKeyboardButton(text='Атырау',callback_data='Атырау')).insert(InlineKeyboardButton(text='Жанаозен',callback_data='Жанаозен')).insert(InlineKeyboardButton(text='Караганда',callback_data='Караганда')).insert(InlineKeyboardButton(text='Каскелен',callback_data='Каскелен')).insert(InlineKeyboardButton(text='Кокшетау',callback_data='Кокшетау')).insert(InlineKeyboardButton(text='Костанай',callback_data='Костанай')).insert(InlineKeyboardButton(text='Кызылорда',callback_data='Кызылорда')).insert(InlineKeyboardButton(text='Павлодар',callback_data='Павлодар')).insert(InlineKeyboardButton(text='Петропавловск',callback_data='Петропавловск')).insert(InlineKeyboardButton(text='Семей',callback_data='Семей')).insert(InlineKeyboardButton(text='Талдыкорган',callback_data='Талдыкорган')).insert(InlineKeyboardButton(text='Тараз',callback_data='Тараз')).insert(InlineKeyboardButton(text='Темиртау',callback_data='Темиртау')).insert(InlineKeyboardButton(text='Туркестан',callback_data='Туркестан')).insert(InlineKeyboardButton(text='Уральск',callback_data='Уральск')).insert(InlineKeyboardButton(text='Усть-Каменогорск',callback_data='Усть-Каменогорск')).insert(InlineKeyboardButton(text='Шымкент',callback_data='Шымкент'))
    await message.answer(text=f'Good, your adress <b>{message.text}</b>\n\n<b>Registration stage</b>: 3 of 4📍\n\nChoose your city🗺',
                        reply_markup=ikb,
                        parse_mode='HTML'
                        )
    await new_cost.next()

@dp.callback_query_handler(state=new_cost.city)  # ГОРОД
async def ytre(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = callback.data
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton(text='Send number📞', request_contact=True))
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Excellent, your city <b>{callback.data}</b>\n\n<b>Registration stage</b>: 4 of 4📍\n\nWe need your contact number, just click on the button📞',
        reply_markup=kb,
        parse_mode='HTML'
    )
    await new_cost.next()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=new_cost.phone)  # НОМЕР
async def contact_received(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Magazine🛍')).insert(KeyboardButton('My orders📦'))
    await message.answer(text=f"Thank you! Your contact number is: <b>{message.contact.phone_number}</b>", reply_markup=kb, parse_mode='HTML')
    await add_c(data)
    await state.finish()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='''
🎉Congratulations on registering with our grocery store bot!🎉

To get started, please choose one of the options below:
        
    🛍️ <b>Magazine</b> - Browse and shop for your favorite products.
    📦 <b>My orders</b> - View and manage your past and current orders.

Happy shopping! 😊
        ''',
        parse_mode='HTML'
    )
    
#---------------------------------------------------------------------------------------------------------------------------------
#МАГАЗИН
#---------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(regexp='Magazine🛍')
async def sh_bo(message: types.message,  state:FSMContext ):
    await new_ord.magaz.set()
    async with state.proxy() as data:
        data['cart']={'prods':{},'cost': 0, 'entit': 0,'mess': []}


    ikb = InlineKeyboardMarkup(row_width=2)
    categories = [
        ("🍎 Fruits", "1"),
        ("🥦 Vegetables", "2"),
        ("🍞 Bakery", "3"),
        ("🍫 Sweets", "4"),
        ("🍣 Sushi", "5"),
        ("🍔 Fast Food", "6"),
        ("🥤 Beverages", "7"),
        ("🧀 Dairy", "8")
    ]

    buttons = [InlineKeyboardButton(text, callback_data=data) for text, data in categories]
    ikb.add(*buttons)
    k=[]
    hh=0
    pp=0
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text='Order📦'))
    await bot.send_message(chat_id=message.from_user.id,text="To start placing an order please select a <b>category</b>🧑🏻‍💻\nJust click on the <b>+</b> at the bottom of the product you want to add and <b>-</b> if it’s the other way around📝",parse_mode='HTML',reply_markup=kb)
    mes= await bot.send_message(chat_id=message.from_user.id,text=f'''Great, let's go shopping🛒!\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.''',parse_mode='HTML',reply_markup=ikb)
    async with state.proxy() as data:
        data['cart']['mess'].append(mes)

@dp.callback_query_handler(state=new_ord.magaz)
async def inser(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        mesid=data['cart']['mess'][0]
    if callback.data[0]!='p' and callback.data[0]!='b':
        prod= await all_p(int(callback.data))
        for t in prod:
            ikb=InlineKeyboardMarkup(row_width=2)
            ikb.insert(InlineKeyboardButton(text='-1',callback_data=f"pm${t['productid']}${t['productname']}${int(t['unitprice']*458)}")).insert(InlineKeyboardButton(text='+1',callback_data=f"pp${t['productid']}${t['productname']}${int(t['unitprice']*458)}"))
            mes = await bot.send_message(chat_id=callback.from_user.id,
                                        text=f"Name: <b>{t['productname']}</b>\nPrice: <b>{int(t['unitprice']*458)}₸</b>",
                                        parse_mode='HTML',
                                        reply_markup=ikb
                )
            async with state.proxy() as data:
                data['cart']['mess'].append(mes.message_id)
        await bot.edit_message_text(chat_id=callback.from_user.id, message_id=mesid.message_id,text=mesid.text, reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Categories⬅️',callback_data='back')),parse_mode='HTML')
    
    elif callback.data[0:2]=='pp':
        prod=callback.data[3:].split('$')
        idd=prod[0]
        prname=prod[1]
        pri=prod[2]
        async with state.proxy() as data:
            cart=data.get('cart')
        try:
            cart['prods'][prname]['ent']+=1
        except:
            cart['prods'][prname]={'id':int(idd),'price':int(pri),'ent':1}
        k=[]
        hh=0
        pp=0
        for t in cart['prods']:
            name = t
            t=cart['prods'][t]
            if t['ent']*t['price']!=0:
                k.append(f"<b>{name}</b> X{t['ent']} {t['ent']*t['price']}₸\n")
                hh+=t['ent']*t['price']
                pp+=t['ent']
            else:
                del cart ['prods'][name]
        async with state.proxy() as data:
            data['cart']=cart
        await bot.edit_message_text(chat_id=callback.from_user.id,message_id=mesid.message_id,text=f'''Great, let's go shopping🛒!\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.''',parse_mode='HTML',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Categories⬅️',callback_data='back')))
        async with state.proxy() as data:
            data['cart']['mess'][0].text=f'''Great, let's go shopping🛒!\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.'''
    
    elif callback.data[0:2]=='pm':
        prod=callback.data[3:].split('$')
        idd=prod[0]
        prname=prod[1]
        pri=prod[2]
        async with state.proxy() as data:
            cart=data.get('cart')
        try:
            cart['prods'][prname]['ent']-=1
            k=[]
            hh=0
            pp=0
            keys_to_delete = []
            for t in cart['prods']:
                name = t
                t=cart['prods'][t]
                if t['ent']*t['price']!=0:
                    k.append(f"<b>{name}</b> X{t['ent']} {t['ent']*t['price']}₸\n")
                    hh+=t['ent']*t['price']
                    pp+=t['ent']
                else:
                    keys_to_delete.append(name)
            for name in keys_to_delete:
                del cart['prods'][name]
            async with state.proxy() as data:
                data['cart']=cart
            await bot.edit_message_text(chat_id=callback.from_user.id,message_id=mesid.message_id,text=f'''Great, let's go shopping🛒!\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.''',parse_mode='HTML',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Categories⬅️',callback_data='back')))
            async with state.proxy() as data:
                data['cart']['mess'][0].text=f'''Great, let's go shopping🛒!\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.'''
        except:
            await callback.answer(text=f'Продукта нет в корзине🛒') 
        
    elif callback.data=='back':
        for t in data['cart']['mess'][1:]:
            await bot.delete_message(chat_id=callback.from_user.id,message_id=t)
        async with state.proxy() as data:
            data['cart']['mess'][1:]=[]
        ikb = InlineKeyboardMarkup(row_width=2)
        categories = [
            ("🍎 Fruits", "1"),
            ("🥦 Vegetables", "2"),
            ("🍞 Bakery", "3"),
            ("🍫 Sweets", "4"),
            ("🍣 Sushi", "5"),
            ("🍔 Fast Food", "6"),
            ("🥤 Beverages", "7"),
            ("🧀 Dairy", "8")
        ]

        buttons = [InlineKeyboardButton(text, callback_data=data) for text, data in categories]
        ikb.add(*buttons)

        await bot.edit_message_text(chat_id=callback.from_user.id, message_id=mesid.message_id,text=mesid.text, reply_markup=ikb,parse_mode='HTML')
    await bot.answer_callback_query(callback.id, cache_time=0)

@dp.message_handler(regexp='Order📦', state=new_ord.magaz)
async def orderr(message:types.message, state:  FSMContext):
    async with state.proxy() as data:
        cart=data.get('cart')
    cart['mess'][0]=cart['mess'][0].message_id
    if cart['prods']!={}:
        order_id =await crea_o(message.from_user.id)
        for t in cart['prods']:
            t=cart['prods'][t]
            await crea_o_d(order_id,t['id'], t['price'], t['ent'])
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Magazine🛍')).insert(KeyboardButton('My orders📦'))
        await bot.send_message(chat_id=message.from_user.id,
                                text=f"Your order number <b>#{order_id}</b> has been successfully completed✅\n\nClick <b>My orders📦</b> to view the details.",
                                parse_mode='HTML',
                                reply_markup=kb
            )
        await state.finish()
    else:
        await state.finish()
        kb=ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Magazine🛍')).insert(KeyboardButton('My orders📦'))
        await bot.send_message(chat_id=message.from_user.id,
                                text=f"Your order has not been completed - empty cart❌\n\nClick <b>My orders📦</b> to view your orders.",
                                parse_mode='HTML',
                                reply_markup=kb
            )
    for t in cart['mess']:
        await bot.delete_message(chat_id=message.from_user.id,message_id=t)

@dp.message_handler(regexp='My orders📦')
async def orderr(message:types.message, state:  FSMContext):
    ids= await get_o_i(message.from_user.id)
    for idd in ids:
        cart=await get_o_d(idd)
        order_info=cart['order_info']
        ord_i=f"""
            🆔 Order ID: {order_info['nom']}
 📅 Order Date: {order_info['date']}
 📍 Shipping Address: {order_info['adress']}
 🏙️ City: {order_info['city']}
 🌍 Country: {order_info['count']}
            """
        k=[]
        hh=0
        pp=0
        for t in cart['prods']:
            name = t
            t=cart['prods'][t]
            if t['ent']*t['price']!=0:
                k.append(f"<b>{name}</b> X{t['ent']} {t['ent']*t['price']}₸\n")
                hh+=t['ent']*t['price']
                pp+=t['ent']
            else:
                del cart ['prods'][name]
        async with state.proxy() as data:
            data['cart']=cart
        await bot.send_message(chat_id=message.from_user.id,text=f'''{ord_i}\n\nYour cart:\n {' '.join(k)}\nTotal: {hh}₸ {pp} pt.''',parse_mode='HTML',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Cancel the order❌',callback_data='del'+str(order_info['nom']))))
    await message.delete()
@dp.callback_query_handler()
async def inserss(callback: types.CallbackQuery, state: FSMContext):
    if callback.data[:3]=='del':
        await callback.answer(text=await del_ord(int(callback.data[3:])))
        await bot.delete_message(chat_id=callback.from_user.id,message_id=callback.message.message_id)

if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)