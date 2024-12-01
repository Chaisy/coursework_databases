from config.project_config import Database

class TableCreator:
    # Функция для создания таблицы Roles
    @staticmethod
    async def create_roles_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Roles (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),      
                Name VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Coupons
    @staticmethod
    async def create_coupons_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Coupons (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        
                Sale INTEGER NOT NULL UNIQUE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Users
    @staticmethod
    async def create_users_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Users (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Login VARCHAR (64) NOT NULL UNIQUE,
                Password VARCHAR (64) NOT NULL,
                Name VARCHAR (64) NOT NULL UNIQUE,
                RoleId UUID REFERENCES Roles (Id) ON DELETE SET NULL,
                CouponId UUID REFERENCES Coupons (Id) ON DELETE SET NULL,
                Banned BOOLEAN DEFAULT FALSE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Carts
    @staticmethod
    async def create_carts_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Carts (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),       
                UserId UUID NOT NULL REFERENCES Users (Id) ON DELETE CASCADE,
                Goods UUID[] DEFAULT '{}'
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Firms
    @staticmethod
    async def create_firms_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Firms (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),      
                Naming VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Animals
    @staticmethod
    async def create_animals_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Animals (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Type VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы CategoriesOfGood
    @staticmethod
    async def create_categories_of_good_table():
        query = '''
            CREATE TABLE IF NOT EXISTS CategoriesOfGood (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Title VARCHAR(64) NOT NULL UNIQUE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Goods
    @staticmethod
    async def create_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Goods (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
                Title VARCHAR (64) NOT NULL,
                FirmId UUID REFERENCES Firms (Id) ON DELETE CASCADE,
                CategoryOfGoodId UUID REFERENCES CategoriesOfGood (Id) ON DELETE CASCADE,
                AnimalId UUID REFERENCES Animals (Id) ON DELETE CASCADE
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы Orders
    @staticmethod
    async def create_orders_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Orders (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                UserId UUID REFERENCES Users (Id) ON DELETE SET NULL,
                Goods UUID[] DEFAULT ARRAY[]::UUID[]
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы OrderGoods
    @staticmethod
    async def create_order_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS OrderGoods (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                OrderId UUID REFERENCES Orders (Id) ON DELETE CASCADE,
                GoodId UUID REFERENCES Goods (Id) ON DELETE CASCADE,
                Count INTEGER NOT NULL DEFAULT 1,   
                DateTime TIMESTAMP NOT NULL, 
                UNIQUE (OrderId, GoodId)
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания таблицы CartsGoods
    @staticmethod
    async def create_carts_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS CartsGoods (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                CartId UUID REFERENCES Carts (Id) ON DELETE CASCADE,
                GoodId UUID REFERENCES Goods (Id) ON DELETE CASCADE,
                Count INTEGER NOT NULL DEFAULT 1,
                UNIQUE (CartId, GoodId)
            );
            '''
        await Database.connection.execute(query)

    @staticmethod
    async def create_logging_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Logs (
            Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            UserId UUID REFERENCES Users (Id) ON DELETE SET NULL,
            Role VARCHAR(255),
            Action VARCHAR(255),
            Result VARCHAR(255)
            );
            '''
        await Database.connection.execute(query)

    # Функция для создания всех таблиц
    @staticmethod
    async def create_all_tables():
        await TableCreator.create_roles_table()
        await TableCreator.create_coupons_table()
        await TableCreator.create_users_table()
        await TableCreator.create_carts_table()
        await TableCreator.create_firms_table()
        await TableCreator.create_animals_table()
        await TableCreator.create_categories_of_good_table()
        await TableCreator.create_goods_table()
        await TableCreator.create_orders_table()
        await TableCreator.create_order_goods_table()
        await TableCreator.create_carts_goods_table()
        await TableCreator.create_logging_table()
