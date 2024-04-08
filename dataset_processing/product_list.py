import pandas as pd


def generate_unique_product_list():
    unique_products = set()
    for user_id in range(1, 3):  # Update the range according to the number of users
        filename = f"user{user_id}.csv"
        user_df = pd.read_csv(filename)
        unique_products.update(user_df['product'].unique())

    # Create a DataFrame for unique products
    products_df = pd.DataFrame({'product': sorted(unique_products)})

    # Save the unique products to a CSV file
    products_df.to_csv('products.csv', index=False)

    print("Unique Product List saved to products.csv")


# Example usage
generate_unique_product_list()
