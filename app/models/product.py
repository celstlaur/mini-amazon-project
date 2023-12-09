from flask import current_app as app, flash
from flask_login import current_user
from .inventory import Inventory
from .feedbackitem import FeedbackItem


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
    def __init__(self, id, name, creator_id, category, product_description, price, image):
        self.id = id
        self.name = name
        self.creator_id = creator_id
        self.category = category
        self.product_description = product_description
        self.price = price
        self.image = image

# Products:
# product_id, product_name, seller_id, category, description, price


    @staticmethod
    def edit_product_name(id, name):
        try:

            rows = app.db.execute(""" UPDATE Products
                                   SET name = :name
                                   WHERE id = :id """, name = name, id = id)

            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None
        

    @staticmethod
    def edit_product_image(id, image):
        try:

            rows = app.db.execute(""" UPDATE Products
                                   SET image = :image
                                   WHERE id = :id """, image = image, id = id)

            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def edit_product_category(id, category):
        try:
            if category not in ["Red", "Blue", "Green", "Yellow", "Purple"]:
                print("Not an acceptable category!")
                return False
            rows = app.db.execute(""" UPDATE Products
                                   SET category = :category
                                   WHERE id = :id """, category = category, id = id)

            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def edit_product_desc(id, desc):
        try:

            rows = app.db.execute("""UPDATE Products
                                   SET product_description = :desc
                                   WHERE id = :id """, desc = desc, id = id)

            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def edit_product_price(id, price):
        try:

            rows = app.db.execute("""UPDATE Products
                                   SET price = :price
                                   WHERE id = :id """, price = price, id = id)

            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None
    
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
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
''')
        return [Product(*row) for row in rows]


# get by offset, sort by id
    @staticmethod
    def get_byoffset(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
ORDER BY id
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
    # can make a bunch more of these, easy to make...
    @staticmethod
    def get_len_prods():
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
''')
        return len(rows) if rows else 0
    
# get and sort by asc, sort by id
    @staticmethod
    def get_asc(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
ORDER BY price
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# get and sort by asc, sort by id
    @staticmethod
    def get_desc(limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
ORDER BY price DESC
LIMIT :limit OFFSET :offset
                              
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category
    @staticmethod
    def get_by_category(category, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

# get all filters
    @staticmethod
    def get_filtered(category, keyword, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', category = category, key = keyword, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]

# get all filters LENGTH
    @staticmethod
    def get_filtered(category, keyword, stars, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
''', category = category, key = keyword, minp = minp, maxp=maxp, stars = stars)
        return len(rows) if rows else 0
    
# filter by category and stars
    @staticmethod
    def get_catstars(category, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]

# filter by category and stars LENGTH
    @staticmethod
    def get_catstars_len(category, stars, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
''', category = category, minp = minp, maxp=maxp, stars = stars)
        return len(rows) if rows else 0
    
# filter by category and key
    @staticmethod
    def get_catkey(category, keyword, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, key = keyword, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category and key LENGTH
    @staticmethod
    def get_catkey_len(category, keyword, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
ORDER BY price, id
''', category = category, minp = minp, maxp=maxp, key = keyword)
        return len(rows) if rows else 0
    
# filter by category and v filters
    @staticmethod
    def get_catfilter(category, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category and v filters LENGTH
    @staticmethod
    def get_catfilter_len(category, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp
ORDER BY price, id
''', category = category, minp = minp, maxp=maxp)
        return len(rows) if rows else 0

# filter by keyword and stars
    @staticmethod
    def get_keystars(keyword, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', key = keyword, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by keyword and stars LENGTH
    @staticmethod
    def get_keystars_len(keyword, stars, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
''', key = keyword, minp = minp, maxp=maxp, stars = stars)
        return len(rows) if rows else 0
    
# filter by stars and v filters
    @staticmethod
    def get_starsfilter(stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
LIMIT :limit OFFSET :offset
''',minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter stars and v filters LENGTH
    @staticmethod
    def get_starsfilter_len(stars, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price, id
''',minp = minp, maxp=maxp, stars = stars)
        return len(rows) if rows else 0
    
# filter by key
    @staticmethod
    def get_keyfiltered(keyword, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
                            
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', key = keyword, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]

# filter by key LENGTH
    @staticmethod
    def get_keyfiltered_len(keyword, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
                            
ORDER BY price, id
''', key = keyword, minp = minp, maxp=maxp)
        return len(rows) if rows else 0
    
# filter by min and max only
    @staticmethod
    def get_minmax(limit, offset, minp, maxp):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp                    
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by min and max only LENGTH
    @staticmethod
    def get_minmax_len(minp, maxp):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp                    
ORDER BY price, id
''', minp = minp, maxp=maxp)
        return [Product(*row) for row in rows]
    
# filter by min and max only
    @staticmethod
    def get_minmax_desc(limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp                    
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

# filter by key desc
    @staticmethod
    def get_keyfiltered_desc(keyword, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
                            
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', key = keyword, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
    
# filter by keyword and stars
    @staticmethod
    def get_starsfilter_desc(stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''',minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by keyword and stars
    @staticmethod
    def get_keystars_desc(keyword, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', key = keyword, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category and stars
    @staticmethod
    def get_catfilter_desc(category, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# filter by category and stars
    @staticmethod
    def get_catkey_desc(category, keyword, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, key = keyword, limit = limit, offset = offset)
        return [Product(*row) for row in rows]


# filter by category and stars
    @staticmethod
    def get_catstars_desc(category, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', category = category, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]


# filter by category PRICE DESCENDING WITH KEYWORD
    @staticmethod
    def get_filtered_desc(category, keyword, stars, limit, offset, minp = 0, maxp = 99999999999999999):

        rows = app.db.execute('''
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price >= :minp AND price <= :maxp)
INTERSECT
(SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE product_description LIKE :key OR name LIKE :key )
INTERSECT
                              
                            (SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id)
                            
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', category = category, key = keyword, minp = minp, maxp=maxp, stars = stars, limit = limit, offset = offset)
        return [Product(*row) for row in rows]

# filter by category PRICE DESCENDING WITH KEYWORD
    @staticmethod
    def get_adv_filter_asc(category, keyword, minp, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND ( product_description LIKE :key OR name LIKE :key ) AND price >= :minp AND price <= :maxp
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', 
category = category, key = keyword, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# ASC KEY MAXP CATEGORY
    @staticmethod
    def get_akcmax(category, keyword, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND ( product_description LIKE :key OR name LIKE :key ) AND price <= :maxp
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', 
category = category, key = keyword, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

# ASC MAXP CATEGORY
    @staticmethod
    def get_acmax(category, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price <= :maxp
ORDER BY price, id
LIMIT :limit OFFSET :offset
''', 
category = category, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# DESC MAXP CATEGORY
    @staticmethod
    def get_dcmax(category, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price <= :maxp
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
# DESC CATEGORY
    @staticmethod
    def get_dkc(category, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND price <= :maxp
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_akcmax_len(category, keyword, maxp):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND ( product_description LIKE :key OR name LIKE :key ) AND price <= :maxp
ORDER BY price, id
''', 
category = category, key = keyword, maxp=maxp)
        return len(rows) if rows else 0
    

    
    @staticmethod
    def get_adv_filter_desc(category, keyword, minp, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND ( product_description LIKE :key OR name LIKE :key ) AND price >= :minp AND price <= :maxp
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, key = keyword, minp = minp, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
    

# DESC KEY MAXP CATEGORY
    @staticmethod
    def get_dkcmax(category, keyword, maxp, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND ( product_description LIKE :key OR name LIKE :key ) AND price <= :maxp
ORDER BY price DESC, id
LIMIT :limit OFFSET :offset
''', 
category = category, key = keyword, maxp=maxp, limit = limit, offset = offset)
        return [Product(*row) for row in rows]
        
    
    
# filter by category PRICE DESCENDING WITH KEYWORD
    @staticmethod
    def get_adv_filter_len(category, keyword, minp, maxp):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE category = :category AND product_description LIKE :key OR name LIKE :key AND price >= :minp AND price <= :maxp
ORDER BY price DESC, id
''', 
category = category, key = keyword, minp = minp, maxp=maxp)
        return len(rows) if rows else 0

    
# filter by category
    @staticmethod
    def getbycat_length(category):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price <= :price
''',
                              price=price)
        return len(rows) if rows else 0
    
# get all greater than equal to price
    @staticmethod
    def get_all_greater_than_price(price, limit, offset):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
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
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
WHERE price >= :price
''',
                              price=price)
        return len(rows) if rows else 0
    
    

# MISC SORTING

# get k, sort by id OFFSET INTRODUCED
    @staticmethod
    def sortby_id(k, limit, offset):
        if k < limit:
            limit = k
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price, image
FROM Products
ORDER BY id
LIMIT :limit OFFSET :offset
                              ''', limit = limit, offset = offset)
        return [Product(*row) for row in rows]

# Products:
# product_id, product_name, seller_id, category, description, price

    @staticmethod
    def create_new_product(name, creator_id, category, product_description, price, image):

        if category not in ["Red", "Blue", "Green", "Yellow", "Purple"]:
            flash("Not an acceptable category!", "danger")
            return False, 0

        rows1 = app.db.execute('''
SELECT *
FROM Products
''')
        pid =  len(rows1) if rows1 else 0

        try:
        

            rows = app.db.execute("""INSERT INTO Products(id, name, creator_id, category, product_description, price, image)
                                VALUES(:pid, :product_name, :seller_id, :category, :description, :price, :image)""",
                                  pid=pid,
                                  product_name = name,
                                  seller_id =creator_id,
                                  category = category,
                                  description = product_description,
                                  price = price,
                                  image = image)

            return True, pid
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_product_avgstars(product_id):
        avg = app.db.execute('''
                            SELECT AVG(CAST(stars AS FLOAT)) AS average_stars
                            FROM ReviewedProduct
                            WHERE product_id = :product_id''', product_id = product_id)
        if avg == [(None,)]:
            return None

        return str(round(float(str(avg[0]).lstrip('(').rstrip(',)')), 2)) if avg else 0
    
    @staticmethod
    def get_num_product_ratings(product_id):
        num = app.db.execute('''
                            SELECT COUNT(*) AS num_reviews
                            FROM ReviewedProduct
                            WHERE product_id = :product_id''', product_id = product_id)

        #formatted_avg = str(round(float(str(avg[0]).lstrip('(').rstrip(',)')), 2))
        return str(num[0]).lstrip('(').rstrip(',)') if num else 0
    
    @staticmethod
    def get_seller_avgstars(seller_id):
        avg = app.db.execute('''
                            SELECT AVG(CAST(stars AS FLOAT)) AS average_stars
                            FROM ReviewedSeller
                            WHERE seller_id = :seller_id''', seller_id = seller_id)

        #formatted_avg = str(round(float(str(avg[0]).lstrip('(').rstrip(',)')), 2))
        return str(round(float(str(avg[0]).lstrip('(').rstrip(',)')), 2)) if avg else 0
    
    @staticmethod
    def get_num_seller_ratings(seller_id):
        num = app.db.execute('''
                            SELECT COUNT(*) AS num_reviews
                            FROM ReviewedSeller
                            WHERE seller_id = :seller_id''', seller_id = seller_id)

        #formatted_avg = str(round(float(str(avg[0]).lstrip('(').rstrip(',)')), 2))
        return str(num[0]).lstrip('(').rstrip(',)') if num else 0
    
    @staticmethod
    def get_product_reviews(product_id):
        rows = app.db.execute('''
                            SELECT review, stars
                            FROM ReviewedProduct
                            WHERE product_id = :product_id
                            ORDER BY stars DESC''', product_id = product_id)
        
        all_reviews = [{'review': row[0], 'stars': row[1]} for row in rows]

        return all_reviews if all_reviews else []

    @staticmethod
    def get_seller_reviews(seller_id):
        rows = app.db.execute('''
                            SELECT review, stars
                            FROM ReviewedSeller
                            WHERE seller_id = :seller_id
                            ORDER BY stars DESC''', seller_id = seller_id)
        
        all_reviews = [{'review': row[0], 'stars': row[1]} for row in rows]

        return all_reviews if all_reviews else []
    

    @staticmethod
    def get_prods_by_star(stars, limit, offset):
        rows = app.db.execute('''
                            SELECT id, name, creator_id, category, product_description, price, image
FROM Products RIGHT JOIN (SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id) AS avg ON avg.product_id = Products.id
                            LIMIT :limit OFFSET :offset
                            ''', stars = stars, limit = limit, offset = offset)
    

        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_prods_by_star_len(stars):
        rows = app.db.execute('''
                            SELECT product_id
                            FROM 
                            (SELECT AVG(CAST(stars AS FLOAT)) AS average_stars, product_id
                            FROM ReviewedProduct GROUP BY product_id) AS avg_prods
                            WHERE CEILING(average_stars) = :stars
                            ORDER BY product_id''', stars = stars)
    

        return len(rows) if rows else 0
        

    

    


