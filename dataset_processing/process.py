import pandas as pd


def load_product_dict():
    # Load the product dictionary from products.csv
    products_df = pd.read_csv('products.csv')
    product_dict = {product: i for i, product in products_df.items()}
    return product_dict


def transform_to_encoded_data(product_dict):
    for user_id in range(1, 3):  # Update the range according to the number of users
        filename = f"user{user_id}.csv"
        user_df = pd.read_csv(filename)

        # Create a new DataFrame with encoded product data
        new_df = pd.DataFrame(columns=['orderid'] + list(product_dict.keys()))
        for order_id, group in user_df.groupby('orderid'):
            order_products = group['product'].map(product_dict).tolist()
            prod_series = pd.Series([0] * len(product_dict), index=product_dict.values())
            for product_num in order_products:
                prod_series[product_num] = 1
            new_df = new_df.append({'orderid': order_id, **prod_series}, ignore_index=True)

        # Save the new DataFrame to a new CSV file
        new_filename = f"encoded_user{user_id}.csv"
        new_df.to_csv(new_filename, index=False)

        print(f"Transformed user {user_id} data and saved to {new_filename}")


# Example usage
product_dict = load_product_dict()
transform_to_encoded_data(product_dict)
