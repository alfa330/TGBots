import asyncpg
import json
import asyncio

host = ''
user = ''
password = ''
dbname = ''


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#ЮЗЕР
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
async def add_user(idd):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''INSERT INTO users (id, cart, u_orders) VALUES ( $1 , '{}', '{}') ON CONFLICT(id) DO NOTHING;''', idd)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#КНИГИ
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
async def add_book(data):                     #ДОПНУТЬ КНИГУ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO books (title, author, front_cover_photo, back_cover_photo, price, genre, rating)
                VALUES ($1, $2, $3, $4, $5, $6, $7);
            ''', data['title'], data['author'], data['f_photo'], data['c_photo'], data['price'], data['genre'], data['rating'])

async def gnbi( last_selected_id, genre):     #ПОЛУЧАЕМ КНИГУ ПО ЖАНРУ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT id, title, author, front_cover_photo, back_cover_photo, price, genre, rating
                FROM books
                WHERE genre = $1 AND id > $2
                ORDER BY id ASC
                LIMIT 1;
            ''', genre, last_selected_id)
            return row

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#ЗАКАЗЫ
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
async def add_order(data):          #ДОПНУТЬ В СПИСОК ЗАКАЗОВ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO orders (user_id, book_id, delivery_address)
                VALUES ($1, $2, $3);
            ''', data['user_id'], data['book_id'], data['adress'])

async def goi(user_id):             #ПОСМОТРЕТЬ ВСЕ КНИГИ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT 
                    o.order_id,
                    o.order_status,
                    b.title,
                    o.order_date,
                    b.price
                FROM 
                    orders o
                INNER JOIN 
                    books b ON o.book_id = b.id
                WHERE
                    o.user_id = $1;
            ''', user_id)
            return rows
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#КОРЗИНА
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
async def ab_c(book_id, user_id):    #ДОПНУТЬ КНИГУ В КОРЗИНУ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''
                UPDATE users 
                SET cart = array_append(cart, $1) 
                WHERE id = $2;
            ''', book_id, user_id)


async def del_kor(book_id, user_id): #УДАЛИТЬ ЭЛЕМЕНТ КОРЗИНЫ 
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('''UPDATE users SET cart = array_remove(cart, $1) WHERE id = $2;''', book_id, user_id)


async def kp_b(user_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                SELECT b.*
                FROM books b
                JOIN users u ON b.id = ANY(u.cart)
                WHERE u.id = $1;
            '''
            rows = await conn.fetch(query, user_id)
            return rows





