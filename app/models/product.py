from flask import current_app as app



# TO DO
# browse and search/filter all products
# result list: show summary (img, name, avg. review rating), link to product page
# support browsing by category, searching for keywords (?), sorting by price (CHECK)
# product page: all prodcut details, list of sellers and their current quantity in stock
# for each seller provide interface for adding quantity to user cart. needs product reviews
# users can create new products for sale, user who created it can edit the product info


# sort functions to write
# sort by product id (base case)
# sort by price descending
# sort by price ascending
# filter by keyword
# filter by category


class Product:
    def __init__(self, id, name, creator_id, category, product_description, price):
        self.id = id
        self.name = name
        self.creator_id = creator_id
        self.category = category
        self.product_description = product_description
        self.price = price

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    
    # can make a bunch more of these, easy to make...
    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
''')
        return [Product(*row) for row in rows]
    
# filter by category
    @staticmethod
    def get_by_category(category):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE category = :category
''', 
category = category)
        return [Product(*row) for row in rows]
    

# PRICE FILTERS

# get all less than equal to price
    @staticmethod
    def get_all_less_than_equal_to_price(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price <= :price
''',
                              price=price)
        return [Product(*row) for row in rows]
    
# get all greater than equal to price
    @staticmethod
    def get_all_less_than_equal_to_price(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price >= :price
''',
                              price=price)
        return [Product(*row) for row in rows]
    
# get all equal to price
    @staticmethod
    def get_all_less_than_equal_to_price(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price >= :price
''',
                              price=price)
        return [Product(*row) for row in rows]

# PRICE SORTING

    @staticmethod
    def get_k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY price DESC, id
LIMIT :k
                              ''', k = k)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_cheapest(k):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY price, id
LIMIT :k
                              ''', k = k)
        return [Product(*row) for row in rows]
    

# MISC SORTING

# get k, sort by id
    @staticmethod
    def sortby_id(k):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY id
LIMIT :k
                              ''', k = k)
        return [Product(*row) for row in rows]
    


