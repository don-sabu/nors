import os
import pandas as pd


def generate_unique_product_list():
    products = {}
    users = os.listdir("data/")
    for user in users:

        train = pd.read_csv("data/" + user + "/train.csv")
        test = pd.read_csv("data/" + user + "/test.csv")
        for index, row in train.iterrows():
            products[row['product_id']] = row['name']
        for index, row in test.iterrows():
            products[row['product_id']] = row['name']


    # Create a DataFrame for unique products
    products_df = pd.DataFrame({'id': list(products.keys()),
                                'name':list(products.values())})

    # Save the unique products to a CSV file
    products_df.to_csv('products.csv', index=False)

    print("Unique Product List saved to products.csv")


# Example usage
generate_unique_product_list()
