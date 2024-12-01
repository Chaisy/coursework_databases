class User:
    def __init__(self, id_, login, password, name, role, coupon=None, banned=False):
        self.id = id_
        self.login = login
        self.password = password
        self.name = name
        self.role_id = role
        self.coupon_id = coupon
        self.banned = banned

class Role:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

class Coupon:
    def __init__(self, id_, sale):
        self.id = id_
        self.sale = sale

class Cart:
    def __init__(self, id_, user_id):
        self.id = id_
        self.user_id = user_id

class Firm:
    def __init__(self, id_, naming):
        self.id = id_
        self.naming = naming

class Animal:
    def __init__(self, id_, type_name):
        self.id = id_
        self.type = type_name

class CategoryOfGood:
    def __init__(self, id_, title):
        self.id = id_
        self.title = title

class Good:
    def __init__(self, id_, title, firm, category_of_good, animal):
        self.id = id_
        self.title = title
        self.firm_id = firm
        self.category_of_good_id = category_of_good
        self.animal_id = animal

class Order:
    def __init__(self, id_, user_id):
        self.id = id_
        self.user_id = user_id

        
        
        
        
        
        
