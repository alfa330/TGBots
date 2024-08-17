import asyncpg
import json
import asyncio

host = ''
user = ''
password = ''
dbname = ''


#ЗАКАЗЩИКИ
#---------------------------------------------------------------------------------------------------------------------------------
async def all_id(idd): #ПОЛУЧИТЬ ВСЕ ПО АЙДИШКЕ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            try:
                query = "SELECT * FROM Customers WHERE CustomerID= $1;"
                customer_ids = await conn.fetch(query,idd)
                return customer_ids
            except:
                return None

async def add_c(data): #ЗАРЕГАТЬ ПОКУПАТЕЛЯ
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                INSERT INTO Customers (CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country, Phone)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT(CustomerID) DO NOTHING;
            '''
            await conn.execute(query,data['id'], data['acc'], data['cname'], data['adress'], data['city'], '66766', 'Kazakhstan', data['phone'])

#---------------------------------------------------------------------------------------------------------------------------------
#КОТЕГОРИИ
#---------------------------------------------------------------------------------------------------------------------------------
async def all_p(category_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                SELECT 
                    ProductID,
                    ProductName,
                    UnitPrice
                FROM 
                    Products
                WHERE
                    CategoryID = $1;
            '''
            rows = await conn.fetch(query, category_id)
            return rows
#---------------------------------------------------------------------------------------------------------------------------------
#ЗАКАЗЫ
#---------------------------------------------------------------------------------------------------------------------------------

async def crea_o(customer_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                INSERT INTO Orders (CustomerID)
                VALUES ($1)
                RETURNING OrderID;
            '''
            order_id = await conn.fetchval(query, customer_id)
            return order_id

async def crea_o_d(order_id,product_id, unit_price, quantity):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity )
                VALUES ($1, $2, $3, $4)
                RETURNING OrderDetailID;
            '''
            order_detail_id = await conn.fetchval(query, order_id, product_id, unit_price, quantity)

async def get_o_d(order_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            # Запрос для получения информации о заказе
            order_query = '''
                SELECT 
                    o.OrderID,
                    o.CustomerID,
                    o.OrderDate,
                    o.RequiredDate,
                    o.ShippedDate,
                    o.ShipAddress,
                    o.ShipCity,
                    o.ShipPostalCode,
                    o.ShipCountry,
                    c.CustomerName
                FROM 
                    Orders o
                    JOIN Customers c ON o.CustomerID = c.CustomerID
                WHERE 
                    o.OrderID = $1;
            '''
            order = await conn.fetchrow(order_query, order_id)
            # Запрос для получения деталей заказа
            details_query = '''
                SELECT 
                    od.OrderDetailID,
                    od.ProductID,
                    p.ProductName,
                    od.UnitPrice,
                    od.Quantity,
                    od.Discount
                FROM 
                    OrderDetails od
                    JOIN Products p ON od.ProductID = p.ProductID
                WHERE 
                    od.OrderID = $1;
            '''
            order_details = await conn.fetch(details_query, order_id)
            cart={}
            # Форматирование результата
            cart['order_info'] = {'nom': order['orderid'],'date': order['orderdate'].strftime('%Y-%m-%d %H:%M'),'adress': order['shipaddress'],'city': order['shipcity'],'count': order['shipcountry']}


            cart['prods']={}
            for detail in order_details:
                cart['prods'][detail['productname']] ={'price': detail['unitprice'], 'ent':detail['quantity']}

            return cart

async def get_o_i(customer_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            query = '''
                SELECT OrderID
                FROM Orders
                WHERE CustomerID = $1;
            '''
            order_ids = await conn.fetch(query, customer_id)
            return [record['orderid'] for record in order_ids]

async def del_ord(order_id):
    async with asyncpg.create_pool(user=user, password=password, database=dbname, host=host) as pool:
        async with pool.acquire() as conn:
            async with conn.transaction():
                delete_order_query = '''
                    DELETE FROM Orders
                    WHERE OrderID = $1;
                '''
                await conn.execute(delete_order_query, order_id)
                return f"Order with ID {order_id} and its details have been deleted."