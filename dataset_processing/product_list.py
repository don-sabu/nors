import os
import pandas as pd
from tqdm import tqdm
import time


def generate_unique_product_list():
    products = {}
    data_path = "minimized_data/"
    users = os.listdir(data_path)
    for user in tqdm(users, desc="Processing Users"):

        train = pd.read_csv(data_path + user + "/train.csv")
        # test = pd.read_csv(data_path + user + "/test.csv")
        for index, row in train.iterrows():
            products[row['product_id']] = row['name']
        # for index, row in test.iterrows():
        #     products[row['product_id']] = row['name']

    # Create a DataFrame for unique products
    products_df = pd.DataFrame({'id': list(products.keys()),
                                'name': list(products.values())})

    # Save the unique products to a CSV file
    products_df.to_csv('minimized_products.csv', index=False)

    print("Unique Product List saved to products.csv")


def check_products():
    products = pd.read_csv('products.csv')
    users = os.listdir("data/")
    user_name = []
    index_no = []
    order_id = []
    product_id = []
    for user in tqdm(users, desc="Processing Users"):

        train = pd.read_csv("data/" + user + "/train.csv")
        test = pd.read_csv("data/" + user + "/test.csv")
        for index, row in train.iterrows():
            if products.loc[products['id'] == row['product_id'], 'name'].values[0] != row['name']:
                user_name.append(user)
                index_no.append(index)
                order_id.append(dict[row['order_id']])
                product_id.append(dict[row['product_id']])
                print(dict[row['product_id']], " - ", row['name'])
        for index, row in test.iterrows():
            if products.loc[products['id'] == row['product_id'], 'name'].values[0] != row['name']:
                user_name.append(user)
                index_no.append(index)
                order_id.append(dict[row['order_id']])
                product_id.append(dict[row['product_id']])
    data = {"user name": user_name,
            "index": index_no,
            "order ID": order_id,
            "product id": product_id}
    df = pd.DataFrame(data)
    df.to_csv('duplicate_products.csv', index=False)


generate_unique_product_list()
# check_products()
