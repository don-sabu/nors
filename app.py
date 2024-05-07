import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="NORS",
    layout="wide")
st.title("Next Order Recommendation System")

model = tf.keras.models.load_model('training/ann_model')


class Products:
    products_data = pd.read_csv('dataset_processing/sample_data/Daily_Items.csv')
    products = products_data.set_index('id')['name'].to_dict()

    suggestions = None
    item_names = list(products_data['name'])

    def __init__(self, user_id):
        self.user_purchase_data = None
        self.user_id = user_id
        self.orders = [0] * 20
        self.last_five_rows = None

    def last_five_orders(self):
        if len(self.user_purchase_data) >= 5:
            self.last_five_rows = self.user_purchase_data.tail(5).values.tolist()

    def load_user_purchase_data(self):
        if self.user_id is not None or self.user_id != "":
            try:
                self.user_purchase_data = pd.read_csv(f'cache/{self.user_id}.csv')
                self.last_five_orders()
                self.make_suggestions()
            except FileNotFoundError:
                columns = [str(i) for i in range(1, 21)]
                user_purchase_data = pd.DataFrame(columns=columns)
                user_purchase_data.to_csv(f'cache/{self.user_id}.csv', index=False)

    def append_order(self, products):
        self.user_purchase_data.loc[len(self.user_purchase_data.index)] = products
        self.user_purchase_data.to_csv(f'cache/{self.user_id}.csv', index=False)
        self.last_five_orders()
        self.make_suggestions()

    def make_suggestions(self):
        if self.last_five_rows is not None:
            probability = [sum(x) / 5 for x in zip(*self.last_five_rows)]
            print(probability)
            p = np.array(self.last_five_rows).flatten()
            pred_float = model.predict(p.reshape(1, -1))
            rounded_prediction = np.around(pred_float, 3)

            print(rounded_prediction)

            pred = probability * rounded_prediction[0]
            self.suggestions = (pred > 0.1).astype(int)
            print(self.suggestions)


userid = None
products = Products(userid)

sample_image_url = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTU3KisAtQ0WwwUVh9CRbByRi3r5l3G9-9SwDySA8y-MA&s",
                    "https://www.jiomart.com/images/product/original/491695705/fortune-maida-refined-wheat-flour-500-g-product-images-o491695705-p590040929-0-202306091505.jpg?im=Resize=(1000,1000)",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX162ENc-omb8zqTMQbS-r_gM2E_kdvhYiKAn-tyZhaA&s",
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/1200px-Tomato_je.jpg",
                    "https://images.immediate.co.uk/production/volatile/sites/30/2017/01/Bunch-of-bananas-67e91d5.jpg?quality=90&resize=440,400",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcP6XM0U-qVvgjkDvS407aOCTQKmVabZWhQfDkQ0SR4Q&s",
                    "https://www.bigbasket.com/media/uploads/p/xl/40248005-2_1-amul-buffalo-milk-uht-treated-calcium-rich-no-preservatives.jpg",
                    "https://www.bigbasket.com/media/uploads/p/l/40281258_1-milky-mist-greek-yogurt-natural-high-protein-no-added-sugar.jpg",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmnbJkb_PoRWq2flcWdCf2nP--YF5joP7IfslRb-E5Mw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUQ0qM3pCPViJo8D9h98o4KfSJL980oEVQrME0-q8Ylg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6EB2saqlZvlqp3D_VhRj43lLSSE27lljCJDQH5x1P6A&s",
                    "https://5.imimg.com/data5/BU/TM/MY-60738954/fresh-salmon-fish-500x500.jpg",
                    "https://images-cdn.ubuy.co.in/650fba357845e21c616bd7b8-kirkland-signature-extra-fancy-mixed.jpg",
                    "https://m.media-amazon.com/images/I/71kOsITKSkL._AC_UF1000,1000_QL80_.jpg",
                    "https://www.tatanutrikorner.com/cdn/shop/products/61kPDKZHGRL._SX679.jpg?v=1709816226",
                    "https://m.media-amazon.com/images/I/61AZt0aOGoL._AC_UF894,1000_QL80_.jpg",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJV4q9dGUWsMLkzTFmy6V42PNwxhkol2UEyW61an1hUA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvIeI0offkLfFvq31WJX_OJDK2USLwrQ_07Z6BdRTtnQ&s",
                    "https://www.bigbasket.com/media/uploads/p/l/10000459_13-bb-royal-refined-sugar-sulphurless.jpg",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCYsP_i4SakA8lnLT5KqHdmq6ofYDFziXlOSC6jpUSOA&s"]
if 'purchase_counts' not in st.session_state:
    st.session_state.purchase_counts = [0] * len(products.item_names)
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = []

if products.suggestions is None:
    st.session_state.suggestion = []
else:
    st.session_state.suggestion = products.suggestions

suggestion_section, product_section, cart_section = st.columns([0.25, 0.45, 0.3], gap="large")
with st.sidebar:
    products.user_id = st.text_input("Username")
    products.load_user_purchase_data()
    if st.button("Reset"):
        st.rerun()

with suggestion_section:
    st.header("Suggestions")
    st.session_state.suggestion = products.suggestions if products.suggestions is not None else []

    for index, count in enumerate(st.session_state.suggestion):
        if count == 1:
            if st.button(f"Buy {products.item_names[index]}"):
                st.session_state.purchase_counts[index] = 1
                st.session_state.cart.append(products.item_names[index])

with product_section:
    st.header("Products")
    col_count = 3  # number of products per row
    rows = (len(products.item_names) + col_count - 1) // col_count  # Calculate needed rows

    for i in range(rows):
        cols = st.columns(col_count)
        for j in range(col_count):
            index = i * col_count + j
            if index < len(products.item_names):
                with cols[j]:
                    with st.container():
                        print(index)
                        st.image(sample_image_url[index], width=100)  # Display the product image
                        st.write(products.item_names[index])  # Display the product name
                        if st.button(f"Buy", key=f"buy_{index}"):
                            st.write(f"{products.item_names[index]} is added to cart.")
                            st.session_state.purchase_counts[index] = 1
                            st.session_state.cart.append(products.item_names[index])

with cart_section:
    st.header("Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        for item in set(st.session_state.cart):
            st.write(f"{item}")

        if st.button("Checkout", type='primary'):
            if products.user_id is None or products.user_id == "":
                st.error("Update username")
            else:
                products.append_order(st.session_state.purchase_counts)
                st.session_state.cart.clear()
                st.session_state.purchase_counts = [0] * len(products.item_names)
                if products.suggestions is not None:
                    st.session_state.suggestion = products.suggestions
