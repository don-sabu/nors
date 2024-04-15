import pandas as pd
import streamlit as st

items = pd.read_csv('dataset_processing/sample_data/Daily_Items.csv')
item_name = list(items['name'])
item_id = list(items['id'])

day1 = st.multiselect(
    'Products ordered in day 1',
    sorted(item_name))
day2 = st.multiselect(
    'Products ordered in day 2',
    sorted(item_name))
day3 = st.multiselect(
    'Products ordered in day 3',
    sorted(item_name))
day4 = st.multiselect(
    'Products ordered in day 4',
    sorted(item_name))
day5 = st.multiselect(
    'Products ordered in day 5',
    sorted(item_name))

if st.button("Predict", type="primary"):
    if day1 == day2 == day3 == day4 == day5 == []:
        st.write('Select atleast one items on each day')
    else:
        st.write('good')
