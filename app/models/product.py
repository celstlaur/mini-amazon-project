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
SELECT *
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


# get by offset, sort by id
    @staticmethod
    def get_byoffset(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY id
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
    # can make a bunch more of these, easy to make...
    @staticmethod
    def get_len_prods():
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
''')
        return len(rows) if rows else 0
    
# get and sort by asc, sort by id
    @staticmethod
    def get_asc(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY price
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# get and sort by asc, sort by id
    @staticmethod
    def get_desc(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY price DESC
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category
    @staticmethod
    def get_by_category(category, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE category = :category
LIMIT :limit OFFSET :offset
''', 
category = category, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

# filter by category PRICE ASCENDING
    @staticmethod
    def get_by_category_asc(category, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE category = :category
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', 
category = category, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category PRICE DESCENDING
    @staticmethod
    def get_by_category_desc(category, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE category = :category
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category
    @staticmethod
    def getbycat_length(category):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE category = :category
''', 
category = category)
        return len(rows) if rows else 0
    
# filter by word in description
    @staticmethod
    def get_by_desc(keyword, limit, offset):
        key = "%" + keyword + "%"
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE product_description LIKE :key OR name LIKE :key
LIMIT :limit OFFSET :offset
''', 
key = key, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by word in description, PRICE ASCENDING
    @staticmethod
    def get_by_desc_asc(keyword, limit, offset):
        key = "%" + keyword + "%"
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE product_description LIKE :key OR name LIKE :key
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', 
key = key, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by word in description, PRICE DESCENDING
    @staticmethod
    def get_by_desc_desc(keyword, limit, offset):
        key = "%" + keyword + "%"
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE product_description LIKE :key OR name LIKE :key
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
key = key, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by word in description
    @staticmethod
    def getbydesc_length(keyword):
        key = "%" + keyword + "%"
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE product_description LIKE :key OR name LIKE :key
''', 
key = key)
        return len(rows) if rows else 0
    

# PRICE FILTERS

# get all less than equal to price
    @staticmethod
    def get_all_less_than_equal_to_price(price, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price <= :price
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''',
                              price=price, limit=limit, offset=offset)
        return [Product(*row) for row in rows]

# get all greater than equal to price
    @staticmethod
    def get_len_leq(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price <= :price
''',
                              price=price)
        return len(rows) if rows else 0
    
# get all greater than equal to price
    @staticmethod
    def get_all_greater_than_price(price, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price >= :price
ORDER BY price, ID
LIMIT :limit OFFSET :offset
''',
                              price=price, limit=limit, offset=offset)
        return [Product(*row) for row in rows]
    
# get all greater than equal to price
    @staticmethod
    def get_len_geq(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price >= :price
''',
                              price=price)
        return len(rows) if rows else 0
    

# PRICE SORTING

    @staticmethod
    def get_k_most_expensive(k, limit, offset):
        if k < limit:
            limit = k
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY price DESC, id
LIMIT :k OFFSET :offset
                              ''', limit = limit, offset = offset)
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

# get k, sort by id OFFSET INTRODUCED
    @staticmethod
    def sortby_id(k, limit, offset):
        if k < limit:
            limit = k
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
ORDER BY id
LIMIT :limit OFFSET :offset
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

    


