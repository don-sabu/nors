import math
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

items = pd.read_csv('dataset_processing/sample_data/Daily_Items.csv')
item_name = list(items['name'])
item_id = list(items['id'])

day1 = st.multiselect(
    'Products ordered in week 1',
    sorted(item_name))
day2 = st.multiselect(
    'Products ordered in week 2',
    sorted(item_name))
day3 = st.multiselect(
    'Products ordered in week 3',
    sorted(item_name))
day4 = st.multiselect(
    'Products ordered in week 4',
    sorted(item_name))
day5 = st.multiselect(
    'Products ordered in week 5',
    sorted(item_name))

loaded_model = tf.keras.models.load_model('training/ann_model')
single_order = []
whole_order = []
predicted_names = []

if st.button("Predict", type="primary"):
    if day1 == day2 == day3 == day4 == day5 == []:
        st.write('Select atleast one items on each day')
    else:
        st.write('predicting..')
        for day in [day1,day2,day3,day4,day5]:
            for item in item_name:
                if item in day:
                    single_order.append(1)
                else:
                    single_order.append(0)
            whole_order.append(single_order)
            single_order = []
        probability = [sum(x)/5 for x in zip(*whole_order)]
        print(probability)
        p = np.array(whole_order).flatten()
        pred_float = loaded_model.predict(p.reshape(1, -1))
        rounded_prediction = np.around(pred_float,3)

        print(rounded_prediction)

        pred = probability*rounded_prediction[0]
        prediction = (pred >0.1).astype(int)
        for i, val in enumerate(prediction):
            if val == 1:
                predicted_names.append(item_name[i])
        st.write(predicted_names)
        single_order = []
        whole_order = []
        predicted_names = []
