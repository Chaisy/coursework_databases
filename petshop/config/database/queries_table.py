from typing import Optional, List, Dict
from uuid import UUID

from fastapi import HTTPException

from schemas.schemas import User, Good, UserProfile, Animal, Firm, Coupon, Role, Category, GoodUpdate, GoodCreate, \
    LogCreate
from config.project_config import Database

class DatabaseQueries:



    @staticmethod
    async def get_user_coupons(login: str) -> Optional[List[dict]]:
        user = await Database.get_user_by_login(login)
        if not user:
            return None

        query = """
                SELECT u.Name AS User, c.Id AS CouponId, c.Sale
                FROM Coupons c 
                JOIN Users u ON u.CouponId = c.Id 
                WHERE u.Name = $1;
            """
        try:
            result = await Database.fetch(query, user['name'])
            return [dict(row) for row in result] if result else []
        except Exception as e:
            print(f"Error in get_user_coupons: {e}")
            return None


    @staticmethod
    async def get_goods_with_category() -> List[dict]:
        query = """
                SELECT g.Id, g.Title, c.Title AS Category
                FROM Goods g
                LEFT JOIN CategoriesOfGood c ON g.CategoryOfGoodId = c.Id;
            """
        try:
            result = await Database.fetch(query)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error in get_goods_with_category: {e}")
            return []



    
    @staticmethod
    async def get_good_by_animal(animal_get: str) -> Optional[List[dict]]:
        if not animal_get:
            return None
        query = """
                SELECT g.Id, g.Title, a.Type AS Animal
                FROM Goods g
                LEFT JOIN Animals a ON g.AnimalId = a.Id 
                WHERE a.Type = $1;
            """
        try:
            result = await Database.fetch(query, animal_get)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error in get_good_by_animal: {e}")
            return None


    @staticmethod
    async def get_users() -> List[dict]:
        query = "SELECT u.Id, u.name, u.banned, u.login, u.roleid, u.couponid FROM Users u;"
        try:
            result = await Database.fetch(query)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error in get_users: {e}")
            return []

    @staticmethod
    async def get_user_profile(user_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Users WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, user_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in get_user_profile: {e}")
            return None

    @staticmethod
    async def update_user(user_id: UUID, update_data: dict) -> bool:
        
        set_clause = []
        values = []
        index = 1  

        
        if update_data.get("login"):
            set_clause.append(f"Login = ${index}")
            values.append(update_data["login"])
            index += 1
        if update_data.get("password"):
            set_clause.append(f"Password = ${index}")
            values.append(update_data["password"])
            index += 1
        if update_data.get("name"):
            set_clause.append(f"Name = ${index}")
            values.append(update_data["name"])
            index += 1

        
        if not set_clause:
            return False

        
        query = f"""
            UPDATE Users
            SET {', '.join(set_clause)}
            WHERE Id = ${index}
            RETURNING Id;
        """
        values.append(user_id)

        try:
            result = await Database.fetchrow(query, *values)
            return result is not None
        except Exception as e:
            print(f"Error in update_user: {e}")
            return False

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        
        cart_deleted = await DatabaseQueries.delete_cart(user_id)
        if not cart_deleted:
            print("Error: Cart could not be deleted.")

        query = """
            DELETE FROM Users WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, user_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_user: {e}")
            return False

    @staticmethod
    async def create_user(login: str, password: str, name: str) -> Optional[UserProfile]:
        default_role_id = 'b3b9d771-010e-432d-9f06-f36e2269465f'  
        query = """
                INSERT INTO Users (Login, Password, Name, RoleId, CouponId, Banned)
                VALUES ($1, $2, $3, $4, NULL, FALSE)  -- Значения по умолчанию для RoleId, CouponId, и Banned
                RETURNING Id, Login, Name, RoleId, CouponId, Banned;
            """
        try:
            
            result = await Database.fetchrow(query, login, password, name, default_role_id)
            if result:
                
                await DatabaseQueries.create_cart(result['id'])

                
                user = UserProfile(**result)  
                return user  
            return None
        except Exception as e:
            print(f"Error in create_user: {e}")
            return None

    @staticmethod
    async def get_all_animals():
        query = "SELECT * FROM Animals;"
        rows = await Database.fetch(query)
        return [dict(row) for row in rows]


    @staticmethod
    async def get_animal(animal_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Animals WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, animal_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in get_animal: {e}")
            return None

    @staticmethod
    async def create_animal(animal_type: str) -> Optional[Animal]:
        query = """
            INSERT INTO Animals (Type)
            VALUES ($1)
            RETURNING Id, Type;
        """
        try:
            result = await Database.fetchrow(query, animal_type)

            if result:
                
                return Animal(id=result["id"], type=result["type"])
            return None
        except Exception as e:
            print(f"Error in create_animal: {e}")
            return None

    @staticmethod
    async def delete_animal(animal_id: UUID) -> bool:
        query = """
            DELETE FROM Animals WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, animal_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_animal: {e}")
            return False

    @staticmethod
    async def get_all_firms():
        query = "SELECT * FROM Firms;"
        rows = await Database.fetch(query)
        return [dict(row) for row in rows]

    @staticmethod
    async def get_firm(firm_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Firms WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, firm_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in get_firm: {e}")
            return None


    @staticmethod
    async def create_firm(firm_name: str) -> Optional[dict]:
        query = """
            INSERT INTO Firms (Naming)
            VALUES ($1)
            RETURNING Id, Naming;
        """
        try:
            result = await Database.fetchrow(query, firm_name)

            if result:
                
                return Firm(id=result["id"], naming=result["naming"])
            return None
        except Exception as e:
            print(f"Error in create_firm: {e}")
            return None

    @staticmethod
    async def delete_firm(firm_id: UUID) -> bool:
        query = """
            DELETE FROM Firms WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, firm_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_firm: {e}")
            return False

    @staticmethod
    async def get_all_coupons():
        query = "SELECT * FROM Coupons;"
        rows = await Database.fetch(query)
        return [dict(row) for row in rows]

    @staticmethod
    async def get_coupon(coupon_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Coupons WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, coupon_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in get_coupon: {e}")
            return None


    @staticmethod
    async def create_coupon(coupon_sale: int) -> Optional[dict]:
        query = """
            INSERT INTO Coupons (Sale)
            VALUES ($1)
            RETURNING Id, Sale;
        """
        try:
            result = await Database.fetchrow(query, coupon_sale)


            if result:
                
                return Coupon(id=result["id"], sale=result["sale"])
            return None
        except Exception as e:
            print(f"Error in create_coupon: {e}")
            return None

    @staticmethod
    async def delete_coupon(coupon_id: UUID) -> bool:
        query = """
            DELETE FROM Coupons WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, coupon_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_coupon: {e}")
            return False


    @staticmethod
    async def get_all_roles():
        query = "SELECT * FROM Roles;"
        rows = await Database.fetch(query)
        return [dict(row) for row in rows]

    @staticmethod
    async def get_role(role_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Roles WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, role_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in get_role: {e}")
            return None


    @staticmethod
    async def create_role(role_name: str) -> Optional[dict]:
        query = """
            INSERT INTO Roles (Name)
            VALUES ($1)
            RETURNING Id, Name;
        """
        try:
            result = await Database.fetchrow(query, role_name)

            if result:
                
                return Role(id=result["id"], name=result["name"])
            return None
        except Exception as e:
            print(f"Error in create_role: {e}")
            return None

    @staticmethod
    async def delete_role(role_id: UUID) -> bool:
        query = """
            DELETE FROM Roles WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, role_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_role: {e}")
            return False


    @staticmethod
    async def get_all_categories():
        query = "SELECT * FROM Categoriesofgood;"
        rows = await Database.fetch(query)
        return [dict(row) for row in rows]

    @staticmethod
    async def get_category(category_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Categoriesofgood WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, category_id)
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error in category get: {e}")
            return None


    @staticmethod
    async def create_category(category_title: str) -> Optional[dict]:
        query = """
            INSERT INTO Categoriesofgood (TITLE)
            VALUES ($1)
            RETURNING Id, Title;
        """
        try:
            result = await Database.fetchrow(query, category_title)

            if result:
                
                return Category(id=result["id"], title=result["title"])
            return None
        except Exception as e:
            print(f"Error in create_category: {e}")
            return None

    @staticmethod
    async def delete_category(category_id: UUID) -> bool:
        query = """
            DELETE FROM Categoriesofgood WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, category_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_role: {e}")
            return False

    @staticmethod
    async def create_cart(user_id: UUID) -> Optional[dict]:
        query = """
            INSERT INTO Carts (UserId, Goods)
            VALUES ($1, $2)
            RETURNING Id, UserId, Goods;
        """
        try:
            
            result = await Database.fetchrow(query, user_id, [])
            if result:
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in create_cart: {e}")
            return None

    @staticmethod
    async def add_good_to_cart(cart_id: UUID, good_id: UUID) -> Optional[dict]:
        
        query_check_good = "SELECT 1 FROM Goods WHERE Id = $1 LIMIT 1;"
        good_exists = await Database.fetchval(query_check_good, good_id)

        if not good_exists:
            raise HTTPException(status_code=404, detail="Good not found")

        
        query = """
            UPDATE Carts
            SET Goods = array_append(Goods, $1)
            WHERE Id = $2
            RETURNING Id, UserId, Goods;
        """
        try:
            result = await Database.fetchrow(query, good_id, cart_id)
            if result:
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in add_good_to_cart: {e}")
            return None

    @staticmethod
    async def remove_good_from_cart(cart_id: UUID, good_id: UUID) -> Optional[dict]:
        query = """
            UPDATE Carts
            SET Goods = array_remove(Goods, $1)
            WHERE Id = $2
            RETURNING Id, UserId, Goods;
        """
        try:
            result = await Database.fetchrow(query, good_id, cart_id)
            if result:
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in remove_good_from_cart: {e}")
            return None

    @staticmethod
    async def get_cart_goods(cart_id: UUID) -> Optional[List[UUID]]:
        query = """
            SELECT Goods
            FROM Carts
            WHERE Id = $1;
        """
        try:
            result = await Database.fetchval(query, cart_id)
            if result is not None:
                return result  
            return None
        except Exception as e:
            print(f"Error in get_cart_goods: {e}")
            return None


    @staticmethod
    async def get_cart_by_user_id(user_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Carts WHERE UserId = $1;"
        try:
            result = await Database.fetchrow(query, user_id)
            if result:
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in get_cart_by_user_id: {e}")
            return None

    @staticmethod
    async def delete_cart(cart_id: UUID) -> bool:
        query = """
            DELETE FROM Carts WHERE Id = $1 RETURNING Id;
        """
        try:
            result = await Database.fetchrow(query, cart_id)
            return result is not None  
        except Exception as e:
            print(f"Error in delete_cart: {e}")
            return False

    @staticmethod
    async def create_order(user_id: UUID) -> Optional[dict]:
        query = """
            INSERT INTO Orders (UserId)
            VALUES ($1)
            RETURNING Id, UserId, Goods;
        """
        try:
            result = await Database.fetchrow(query, user_id)
            if result:
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in create_order: {e}")
            return None

    @staticmethod
    async def get_all_orders() -> List[dict]:
        query = """
            SELECT Id, UserId, Goods
            FROM Orders;
        """
        try:
            results = await Database.fetch(query)
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error in get_all_orders: {e}")
            return []

    @staticmethod
    async def get_order_by_id1(order_id: UUID):
        query = "SELECT * FROM Orders WHERE Id = $1"
        result = await Database.fetchrow(query, order_id)
        return result

    @staticmethod
    async def delete_order(order_id: UUID):
        query = "DELETE FROM Orders WHERE Id = $1 RETURNING Id"
        try:
            result = await Database.fetchval(query, order_id)
            return result is not None
        except Exception as e:
            print(f"Error deleting order {order_id}: {e}")
            return False

    @staticmethod
    async def add_good_to_order(user_id: UUID, good_id: UUID) -> Optional[dict]:
        
        good_exists = await DatabaseQueries.check_good_exists(good_id)
        if not good_exists:
            raise HTTPException(status_code=400, detail="Good not found")

        
        query_get_cart = """
            SELECT Id
            FROM Carts
            WHERE UserId = $1;
        """
        cart_id = await Database.fetchval(query_get_cart, user_id)
        if cart_id:
            await DatabaseQueries.remove_good_from_cart(cart_id, good_id)

        
        query_get_order = """
            SELECT Id
            FROM Orders
            WHERE UserId = $1 AND cardinality(Goods) > 0;
        """
        existing_order_id = await Database.fetchval(query_get_order, user_id)

        
        if not existing_order_id:
            create_order_query = """
                INSERT INTO Orders (UserId, Goods)
                VALUES ($1, ARRAY[$2]::UUID[])
                RETURNING Id, UserId, Goods;
            """
            try:
                result = await Database.fetchrow(create_order_query, user_id, good_id)
                if result:
                    return dict(result)  
                return None
            except Exception as e:
                print(f"Error in create_order within add_good_to_order: {e}")
                raise HTTPException(status_code=500, detail="Failed to create order")
        else:
            
            add_good_query = """
                UPDATE Orders
                SET Goods = array_append(Goods, $1)
                WHERE Id = $2
                RETURNING Id, UserId, Goods;
            """
            try:
                result = await Database.fetchrow(add_good_query, good_id, existing_order_id)
                if result:
                    return dict(result)  
                return None
            except Exception as e:
                print(f"Error in add_good_to_order: {e}")
                raise HTTPException(status_code=500, detail="Failed to add good to order")

    @staticmethod
    async def check_good_exists(good_id: UUID) -> bool:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM Goods
                WHERE Id = $1
            );
        """
        try:
            result = await Database.fetchval(query, good_id)
            return result
        except Exception as e:
            print(f"Error in check_good_exists: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during good existence check")

    @staticmethod
    async def remove_good_from_order(order_id: UUID, good_id: UUID) -> Optional[dict]:
        query = """
            UPDATE Orders
            SET Goods = array_remove(Goods, $1)
            WHERE Id = $2
            RETURNING Id, UserId, Goods;
        """
        try:
            result = await Database.fetchrow(query, good_id, order_id)

            if result:
                
                if not result["goods"]:
                    delete_order_query = """
                        DELETE FROM Orders
                        WHERE Id = $1;
                    """
                    await Database.execute(delete_order_query, order_id)
                    return {"detail": "Order deleted because it was empty"}
                return dict(result)  
            return None
        except Exception as e:
            print(f"Error in remove_good_from_order: {e}")
            raise HTTPException(status_code=500, detail="Failed to remove good from order")

    @staticmethod
    async def get_order_goods(order_id: UUID) -> Optional[List[UUID]]:
        query = """
            SELECT Goods
            FROM Orders
            WHERE Id = $1;
        """
        try:
            print(f"Result from database for order {order_id}: {Database.fetchval(query, order_id)}")
            result = await Database.fetchval(query, order_id)
            if result is not None:
                return result  
            return None
        except Exception as e:
            print(f"Error in get_order_goods: {e}")
            return None

    @staticmethod
    async def get_orders_by_user_id(user_id: UUID) -> List[dict]:
        query = """
            SELECT Id, UserId, Goods
            FROM Orders
            WHERE UserId = $1;
        """
        try:
            results = await Database.fetch(query, user_id)
            print(f"result:{results}")
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error in get_orders_by_user_id: {e}")
            return []

    @staticmethod
    async def remove_order(order_id: UUID) -> bool:
        query = """
            DELETE FROM Orders
            WHERE Id = $1;
        """
        try:
            result = await Database.execute(query, order_id)
            return result == "DELETE 1"
        except Exception as e:
            print(f"Error in remove_order: {e}")
            return False


    @staticmethod
    async def get_all_goods() -> List[Good]:
        query = """
                SELECT g.Id, g.Title, g.FirmId, g.CategoryOfGoodId, g.AnimalId, g.Price, g.ImageURL
                FROM Goods g;
            """
        try:
            results = await Database.fetch(query)
            return [Good(**result) for result in results]
        except Exception as e:
            print(f"Error in get_all_goods: {e}")
            return []

    @staticmethod
    async def get_good_by_id(good_id: UUID) -> Optional[Good]:
        query = """
                SELECT g.Id, g.Title, g.FirmId, g.CategoryOfGoodId, g.AnimalId, g.Price, g.ImageURL
                FROM Goods g WHERE g.Id = $1;
            """
        try:
            result = await Database.fetchrow(query, good_id)
            if result:
                return Good(**result)
            return None
        except Exception as e:
            print(f"Error in get_good_by_id: {e}")
            return None



    @staticmethod
    async def delete_good(good_id: UUID) -> bool:
        query = "DELETE FROM Goods WHERE Id = $1 RETURNING Id;"
        try:
            result = await Database.fetchrow(query, good_id)
            if result:
                return True
            return False
        except Exception as e:
            print(f"Error in delete_good: {e}")
            return False

    @staticmethod
    async def update_good(good_id: UUID, good_update: GoodUpdate) -> Optional[Good]:
        
        query_get_current = "SELECT * FROM Goods WHERE Id = $1;"
        current_good = await Database.fetchrow(query_get_current, good_id)
        if not current_good:
            raise HTTPException(status_code=404, detail="Good not found")

        # Извлекаем текущие данные
        current_good = dict(current_good)

        # Если новые значения переданы, проверяем их
        if good_update.firmId:
            firm_exists = await DatabaseQueries.check_firm_exists(good_update.firmId)
            if not firm_exists:
                raise HTTPException(status_code=400, detail="Firm not found")
        if good_update.categoryOfGoodId:
            category_exists = await DatabaseQueries.check_category_exists(good_update.categoryOfGoodId)
            if not category_exists:
                raise HTTPException(status_code=400, detail="Category not found")
        if good_update.animalId:
            animal_exists = await DatabaseQueries.check_animal_exists(good_update.animalId)
            if not animal_exists:
                raise HTTPException(status_code=400, detail="Animal not found")

        # Проверка на дублирование названия (если название обновляется)
        if good_update.title and good_update.title != current_good["title"]:
            existing_good_query = """
                SELECT 1
                FROM Goods
                WHERE Title = $1 AND Id != $2;
            """
            existing_good = await Database.fetchval(existing_good_query, good_update.title, good_id)
            if existing_good:
                raise HTTPException(status_code=400, detail="A good with this title already exists")

        # Обновляем только переданные значения, остальные оставляем как есть
        updated_values = {
            "title": good_update.title or current_good["title"],
            "firmId": good_update.firmId or current_good["firmid"],
            "categoryOfGoodId": good_update.categoryOfGoodId or current_good["categoryofgoodid"],
            "animalId": good_update.animalId or current_good["animalid"],
            "price": good_update.price or current_good["price"],
            "imageURL": good_update.imageURL or current_good["imageurl"],
        }

        # Формируем запрос на обновление
        query_update = """
            UPDATE Goods
            SET Title = $1, FirmId = $2, CategoryOfGoodId = $3, AnimalId = $4, Price = $5, ImageURL = $6
            WHERE Id = $7
            RETURNING Id, Title, FirmId, CategoryOfGoodId, AnimalId, Price, ImageURL;
        """
        try:
            result = await Database.fetchrow(
                query_update,
                updated_values["title"],
                updated_values["firmId"],
                updated_values["categoryOfGoodId"],
                updated_values["animalId"],
                updated_values["price"],
                updated_values["imageURL"],
                good_id,
            )
            if result:
                return Good(**result)
            return None
        except Exception as e:
            print(f"Error in update_good: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def check_firm_exists(firm_id: UUID) -> bool:
        query = "SELECT 1 FROM Firms WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, firm_id)
            return result is not None
        except Exception as e:
            print(f"Error in check_firm_exists: {e}")
            return False

    @staticmethod
    async def check_category_exists(category_id: UUID) -> bool:
        query = "SELECT 1 FROM CategoriesOfGood WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, category_id)
            return result is not None
        except Exception as e:
            print(f"Error in check_category_exists: {e}")
            return False

    @staticmethod
    async def check_animal_exists(animal_id: UUID) -> bool:
        query = "SELECT 1 FROM Animals WHERE Id = $1;"
        try:
            result = await Database.fetchrow(query, animal_id)
            return result is not None
        except Exception as e:
            print(f"Error in check_animal_exists: {e}")
            return False

    @staticmethod
    async def add_good(good: GoodCreate) -> Optional[Good]:
        # Проверка на существование фирм, категорий и животных
        firm_exists = await DatabaseQueries.check_firm_exists(good.firmId)
        category_exists = await DatabaseQueries.check_category_exists(good.categoryOfGoodId)
        animal_exists = await DatabaseQueries.check_animal_exists(good.animalId)

        if not firm_exists:
            raise HTTPException(status_code=400, detail="Firm not found")
        if not category_exists:
            raise HTTPException(status_code=400, detail="Category not found")
        if not animal_exists:
            raise HTTPException(status_code=400, detail="Animal not found")

        # Проверка на наличие товара с таким же названием
        existing_good_query = """
            SELECT 1
            FROM Goods
            WHERE Title = $1
        """
        existing_good = await Database.fetchval(existing_good_query, good.title)

        if existing_good:
            raise HTTPException(status_code=400, detail="A good with this title already exists")

        # Если все проверки пройдены, добавляем товар
        query = """
            INSERT INTO Goods (Title, FirmId, CategoryOfGoodId, AnimalId, Price, ImageURL)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING Id, Title, FirmId, CategoryOfGoodId, AnimalId, Price, ImageURL;
        """
        try:
            result = await Database.fetchrow(
                query, good.title, good.firmId, good.categoryOfGoodId, good.animalId, good.price, good.imageURL
            )
            if result:
                return Good(**result)
            return None
        except Exception as e:
            print(f"Error in add_good: {e}")
            return None

    @staticmethod
    async def get_logging() -> Optional[list]:
        query = """
            SELECT * FROM Logs
            ORDER BY Timestamp DESC;
        """
        try:
            result = await Database.fetch(query)
            return [dict(record) for record in result]
        except Exception as e:
            print(f"Error in get_logging: {e}")
            return None

    @staticmethod
    async def get_logging_by_user(user_id: UUID) -> Optional[list]:
        query = """
            SELECT * FROM Logs
            WHERE UserId = $1
            ORDER BY Timestamp DESC;
        """
        try:
            result = await Database.fetch(query, user_id)
            return [dict(record) for record in result]
        except Exception as e:
            print(f"Error in get_logging_by_user: {e}")
            return None

    @staticmethod
    async def add_log(log: LogCreate) -> Optional[dict]:
        query = """
            INSERT INTO Logs (UserId, Role, Action, Result)
            VALUES ($1, $2, $3, $4)
            RETURNING Id, UserId, Role, Action, Timestamp,  Result;
        """
        try:
            result = await Database.fetchrow(
                query,
                log.userid,
                log.role,
                log.action,
                log.result
            )
            return dict(result) if result else None
        except Exception as e:
            print(f"Error in add_log: {e}")
            return None



    async def get_user_by_login(username: str):
        query = """
            SELECT 
                Id, 
                Login, 
                Password, 
                Name, 
                RoleId, 
                Banned
            FROM Users
            WHERE Login = $1
        """
        try:
            user = await Database.fetchrow(query, username)
            if not user:
                return None
            # Преобразуем результат в словарь для работы с Python-кодом
            return {
                "id": user["id"],
                "login": user["login"],
                "password": user["password"],
                "name": user["name"],
                "roleId": user["roleid"],
                "banned": user["banned"],
            }
        except Exception as e:
            print(f"Error in get_user_by_login: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch user from database")

    @staticmethod
    async def get_role_by_id(role_id: UUID) -> Optional[dict]:
        query = "SELECT * FROM Roles WHERE Id = $1;"
        try:
            # Выполняем запрос к базе данных
            result = await Database.fetchrow(query, role_id)
            print(result["name"])
            if result:
                # Возвращаем результат в виде словаря
                return result["name"]
            return None
        except Exception as e:
            # Логируем ошибку, если она возникла
            print(f"Error in get_role: {e}")
            return None


    @staticmethod
    async def add_log_from_dict(log: Dict):
        query = """
            INSERT INTO Logs (UserId, Role, Action, Result, Timestamp)
            VALUES ($1, $2, $3, $4, $5)
        """
        try:
            await Database.execute(
                query,
                log.get("user_id"),
                log.get("role"),
                log.get("action"),
                log.get("result"),
                log.get("timestamp")
            )
        except Exception as e:
            print(f"Error in add_log_from_dict: {e}")

    @staticmethod
    async def get_user_by_id(user_id: UUID):
        query = "SELECT * FROM Users WHERE Id = $1"
        return await Database.fetchrow(query, user_id)

    @staticmethod
    async def update_user_ban_status(user_id: UUID, banned: bool):
        query = "UPDATE Users SET Banned = $1 WHERE Id = $2 RETURNING Id"
        try:
            result = await Database.fetchval(query, banned, user_id)
            return result is not None
        except Exception as e:
            print(f"Error updating ban status for user {user_id}: {e}")
            return False



