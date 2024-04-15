import pandas as pd
from tqdm import tqdm
import os


def transform():
    data_path = "minimized_data/"
    output_data_path = 'transformed_data/'
    users = os.listdir(data_path)
    for user in tqdm(users, desc="Processing Users"):
        train_df = pd.read_csv(data_path + user + "/train.csv")
        unique_id_list = pd.read_csv('prodid_to_uniqueid_mapped.csv')
        unique_id_list.rename(columns={'id': 'product_id'}, inplace=True)
        merged_df = pd.merge(train_df, unique_id_list, on='product_id')
        pivot_df = merged_df.pivot_table(index='order_id', columns='unique_id', aggfunc='size', fill_value=0)
        all_unique_ids = unique_id_list['unique_id'].unique()
        zeros_df = pd.DataFrame(0, index=pivot_df.index,
                                columns=[uid for uid in all_unique_ids if uid not in pivot_df.columns])
        pivot_df = pd.concat([pivot_df, zeros_df], axis=1)
        pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)
        pivot_df.reset_index(inplace=True)
        os.makedirs(f'{output_data_path}{user}')
        pivot_df.to_csv(f'{output_data_path}{user}/train.csv')


transform()