import asyncpg
import json
import asyncio

host = ''
user = ''
password = ''
dbname = ''


#ЮЗЕР
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

async def add_u(idd, nick): 
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('INSERT INTO users (id, nick) VALUES ($1, $2) ON CONFLICT(id) DO NOTHING;', idd, nick)


async def add_pw(user_id, played_with_id): #ДОБАВЛЕНИЕ НОВОГО ДРУГА
	async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
	    async with pool.acquire() as conn:
	        await conn.execute('UPDATE users SET played_with = array_append(played_with, $1) WHERE id = $2', played_with_id, user_id)

async def pol_p(idd):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                SELECT u.id, u.victories, u.defeats, u.nick, u.total_games
                FROM users u
                WHERE u.id IN (SELECT unnest(played_with) FROM users WHERE id = $1)
            '''
            players_info = await conn.fetch(query, idd)
            
            return players_info

async def pol_sp(idd):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                SELECT u.id, u.victories, u.defeats, u.nick, u.total_games
                FROM users u
                WHERE u.id= $1
            '''
            players_info = await conn.fetch(query, idd)
            
            return players_info

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#ИГРЫ
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
async def add_g(winner_id, loser_id): #ДОБАВЛЕНИЕ НОВОЙ ИГРЫ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            await conn.execute('INSERT INTO games (winner_id, loser_id) VALUES ($1, $2)', winner_id, loser_id)