from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import timedelta

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

'''
Users:
user_id, email, password, first_name, last_name

Sellers:
user_id, business_email, business_address

OrderContents:
order_id, product_id, seller_id, quantity

OrderFact:
order_id, buyer_id, total_price, fulfillment_status, time_stamp

Fulfills:
order_id, seller_id, fulfillment_status

HasInventory:
seller_id, product_id, quantity

Products:
product_id, product_name, seller_id, category, description, price

ReviewedProduct: 
user_id, product_id, review, timestamp

ReviewedSeller: 
user_id, seller_id, review, timestamp

SavedforLaterContents:
user_id, product_id, seller_id, quantity

CartContents: 
user_id, product_id, seller_id, quantity

Search: 
user_id, timestamp, search

HasInventory: 
seller_id, product_id, quantity

----------------- TODO  -----------------

Balance:
user_id, timestamp, balance

Wishes:
wish_id, user_id, product_id, time_stamp
'''


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            if uid % (0.1 * num_users) == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return


def gen_sellers(num_users, size):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        uid_subset = random.sample(range(num_users), int(size * num_users))
        
        for i, uid in enumerate(uid_subset):
            if i % (0.1 * num_users) == 0:
                print(f'{i}', end=' ', flush=True)
            
            profile = fake.profile()
            email = profile['mail']
            address = profile['address']
            
            writer.writerow([int(uid), email, address])
        
        print(f"{int(num_users * size)} sellers generated")
    return uid_subset


def gen_products(num_products, categories, seller_ids):
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        for pid in range(num_products):
            
            if pid % (0.1 * num_products) == 0:
                print(f'{pid}', end=' ', flush=True)
                
            
            # might want to change this, just produces random words...    
            product_name = fake.sentence(nb_words=4)[:-1]
            
            product_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'

            product_seller = random.choice(seller_ids)
            
            product_category = random.choice(categories)

            product_description = fake.sentence(nb_words=8)[:-1]

            writer.writerow([pid, product_name, product_seller, product_category, product_description, product_price])
        print(f"{num_products} products generated")
    return

###
def gen_orders(num_orders, num_users, fulfill_percentage):
    
    prod_df = pd.read_csv('Products.csv', names=['product_id', 'product_name', 'seller_id', 'category', 'description', 'price'])
    
    reset_flg1 = True
    reset_flg2 = True
    reset_flg3 = True
    
    for oid in range(num_orders):
        
        items_in_order = random.choice(range(1, 6))
        
        total_order_price = 0
        
        seller_lst = []
        
        fulfill_entire_order = True
        
        for _ in range(items_in_order):
            item_df = prod_df.iloc[random.choice(range(0, prod_df.shape[0]))]
            quantity = fake.random_int(min=1, max=20)
            total_order_price += (float(item_df['price']) * quantity)
            seller_lst.append(item_df['seller_id'])
            
            if reset_flg1:
            
                with open('OrderContents.csv', 'w') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, item_df['product_id'], item_df['seller_id'], quantity])
                reset_flg1 = False
            else:
                with open('OrderContents.csv', 'a') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, item_df['product_id'], item_df['seller_id'], quantity])
            
            fulfill = random.choices([True, False], weights=[fulfill_percentage, 1 - fulfill_percentage])[0]    
            
            fulfill_entire_order = fulfill_entire_order and fulfill
            
            if reset_flg2:
                with open('Fulfills.csv', 'w') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, item_df['seller_id'], fulfill])
                reset_flg2 = False

            else:
                with open('Fulfills.csv', 'a') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, item_df['seller_id'], fulfill])

        available_buyers = [x for x in range(num_users) if x not in [int(x) for x in seller_lst]]
        
        buyer = random.choice(available_buyers)
        
        total_order_price = np.round(total_order_price * 100, 2) / 100
        
        if reset_flg3:
            with open('OrderFact.csv', 'w') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, buyer, total_order_price, fulfill_entire_order, fake.date_time()])
            reset_flg3 = False
        else:
            with open('OrderFact.csv', 'a') as f:
                    writer = get_csv_writer(f)
                    writer.writerow([oid, buyer, total_order_price, fulfill_entire_order, fake.date_time()])
    return


def gen_search(num_search, num_users):
    with open('Search.csv', 'w') as f:
        writer = get_csv_writer(f)
        for sid in range(num_search):
            if sid % (0.1 * num_users) == 0:
                print(f'{sid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users - 1)
            timestamp = fake.date_time()
            search_text = fake.sentence(nb_words=10)[:-1]
            writer.writerow([uid, timestamp, search_text])
        print(f'{num_search} generated searches')
    return


def gen_hasinventory(prod_name):
    prod = pd.read_csv(prod_name, names=['product_id', 'product_name', 'seller_id', 'category', 'description', 'price'])
    with open('HasInventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        for i in range(prod.shape[0]):
            if i % (0.1 * prod.shape[0]) == 0:
                print(f'{i}', end=' ', flush=True)
            pid = prod['product_id'].iloc[i]
            sid = prod['seller_id'].iloc[i]
            quantity = fake.random_int(min=0, max=100)
            writer.writerow([sid, pid, quantity])
        print(f"{prod.shape[0]} hasinventory rows generated")
    return

####
def gen_savedforlatercontents(num_saved, num_users, hasinv_name):
    hasi = pd.read_csv(hasinv_name, names=['seller_id', 'product_id', 'quantity'])
    with open('SavedForLaterContents.csv', 'w') as f:
        writer = get_csv_writer(f)
        for i in range(num_saved):
            if i % (0.1 * num_saved) == 0:
                print(f'{i}', end=' ', flush=True)
            pid = hasi['product_id'].iloc[i]
            sid = hasi['seller_id'].iloc[i]
            if hasi['quantity'].iloc[i] != 0:
                quantity = fake.random_int(min=1, max=hasi['quantity'].iloc[i])
                uid = fake.random_int(min=0, max=num_users)
                writer.writerow([uid, pid, sid, quantity])
        print(f"{num_saved} savedforlatercontents rows generated")
    return
        
#####       
def gen_cartcontents(num_cart, num_users, hasinv_name):
    hasi = pd.read_csv(hasinv_name, names=['seller_id', 'product_id', 'quantity'])
    with open('CartContents.csv', 'w') as f:
        writer = get_csv_writer(f)
        for i in range(num_cart):
            if i % (0.1 * num_cart) == 0:
                print(f'{i}', end=' ', flush=True)
            pid = hasi['product_id'].iloc[i]
            sid = hasi['seller_id'].iloc[i]
            if hasi['quantity'].iloc[i] != 0:
                quantity = fake.random_int(min=1, max=hasi['quantity'].iloc[i])
                uid = fake.random_int(min=0, max=num_users)
                writer.writerow([uid, pid, sid, quantity])
        print(f"{num_cart} cartcontents rows generated")
    return


def gen_reviewedproduct(fact_name, contents_name, size):
    
    fact = pd.read_csv(fact_name, names=['order_id', 'buyer_id', 'total_price', 'fulfillment_status', 'time_stamp'])
    contents = pd.read_csv(contents_name, names=['order_id', 'product_id', 'seller_id', 'quantity'])

    df = pd.merge(contents, fact, on='order_id', how='left')[['product_id', 'buyer_id', 'time_stamp']]
    index_subset = random.sample(range(df.shape[0]), int(size * df.shape[0]))
    
    with open('ReviewedProduct.csv', 'w') as f:
        writer = get_csv_writer(f)
    
        for i in index_subset:
            pid = df.iloc[i]['product_id']
            bid = df.iloc[i]['buyer_id']
            days_to_add = fake.random_int(min=7, max=21)
            hours_to_add = fake.random_int(min=0, max=23)
            minutes_to_add = fake.random_int(min=0, max=59)
            timestamp = pd.to_datetime(df.iloc[i]['time_stamp']) + timedelta(days=days_to_add, hours=hours_to_add, minutes=minutes_to_add)
            review_text = fake.sentence(nb_words=10)[:-1]
            writer.writerow([bid, pid, review_text, timestamp])
    print(f"{int(size * df.shape[0])} product reviews generated")
    return
    
      
def gen_reviewedseller(fact_name, contents_name, size):
    
    fact = pd.read_csv(fact_name, names=['order_id', 'buyer_id', 'total_price', 'fulfillment_status', 'time_stamp'])
    contents = pd.read_csv(contents_name, names=['order_id', 'product_id', 'seller_id', 'quantity'])

    df = pd.merge(contents, fact, on='order_id', how='left')[['seller_id', 'buyer_id', 'time_stamp']]
    index_subset = random.sample(range(df.shape[0]), int(size * df.shape[0]))
    
    with open('ReviewedSeller.csv', 'w') as f:
        writer = get_csv_writer(f)
        for i in index_subset:
            sid = df.iloc[i]['seller_id']
            bid = df.iloc[i]['buyer_id']
            days_to_add = fake.random_int(min=7, max=21)
            hours_to_add = fake.random_int(min=0, max=23)
            minutes_to_add = fake.random_int(min=0, max=59)
            timestamp = pd.to_datetime(df.iloc[i]['time_stamp']) + timedelta(days=days_to_add, hours=hours_to_add, minutes=minutes_to_add)
            review_text = fake.sentence(nb_words=10)[:-1]
            writer.writerow([bid, sid, review_text, timestamp])
    print(f"{int(size * df.shape[0])} seller reviews generated")
    return


def gen_wishes(num_wishes, num_users, num_products):
    with open('Wishes.csv', 'w') as f:
        writer = get_csv_writer(f)
        for wid in range(num_wishes):
            uid = fake.random_int(min=0, max=num_users)
            pid = fake.random_int(min=0, max=num_products)
            time_stamp = fake.date_time()
            writer.writerow([wid, uid, pid, time_stamp])
    print(f"{num_wishes} rows in wishes generated")
    return


def gen_balance(num_users):
    with open('Balance.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            time_stamp = fake.date_time()
            balance = f'{str(fake.random_int(max=10000))}.{fake.random_int(max=99):02}'
            writer.writerow([uid, time_stamp, balance])
    print(f"{num_users} rows in balance generated")
    return


## PARAMETERS ##
num_users = 500 # number of generated users
num_products = 500 # number of generated products
num_orders = 100 # number of rows in order fact, order contents can have between [num_orders, 5 * num_orders]
num_search = 100 # number of generated rows in Search.csv
num_saved = 100 # number of generated rows in SavedForLaterContents.csv
num_cart = 100 # number of generated rows in CartContents.csv
num_wishes = 100 # number of generated rows in Wishes.csv

product_categories = ['Red', 'Blue', 'Green', 'Yellow', 'Purple'] # figured this would be better than random category names in case we want to use them for something, can be any str list of any len > 1...

seller_percentage = 0.25 # percentage of users that will be assigned as sellers
fulfill_percentage = 0.9 # percentage of item, buyer pairs that are set to 'True' in OrderContents... OrderFact only shows fulfilled=True if all items are fulfilled 
reviewed_seller_percentage = 0.5 # percentage of valid seller, buyer pairs that are reviewed
reviewed_product_percentage = 0.5 # percentage of valid product, buyer pairs that are reviewed

## --------------------------------------------------------------------------------------------- ##

## GENERATORS, DO NOT MODIFY ##
gen_users(num_users)
valid_seller_ids = gen_sellers(num_users, seller_percentage)  
gen_products(num_products, product_categories, valid_seller_ids)
gen_orders(num_orders, num_users, fulfill_percentage) 
gen_search(num_search, num_users)
gen_hasinventory('Products.csv')
gen_savedforlatercontents(num_saved, num_users, 'HasInventory.csv')
gen_cartcontents(num_cart, num_users, 'HasInventory.csv')
gen_reviewedproduct('OrderFact.csv', 'OrderContents.csv', reviewed_product_percentage) 
gen_reviewedseller('OrderFact.csv', 'OrderContents.csv', reviewed_seller_percentage)
gen_wishes(num_wishes, num_users, num_products)
gen_balance(num_users)