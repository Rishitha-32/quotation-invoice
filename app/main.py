import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quotation & Invoice Generator", page_icon="💼", layout="centered")

st.title("Quotation & Invoice Generator")
st.write("Fill out the details below to create a quotation or invoice.")


st.header("Company Information")
company_name = st.text_input("Company Name")
client_name = st.text_input("Client Name")
invoice_type = st.selectbox("Type", ["Quotation", "Invoice"])


st.header(" Items")
items = []
num_items = st.number_input("Number of items", min_value=1, step=1)

for i in range(int(num_items)):
    st.subheader(f"Item {i+1}")
    item_name = st.text_input(f"Item Name {i+1}", key=f"name_{i}")
    quantity = st.number_input(f"Quantity {i+1}", min_value=1, key=f"qty_{i}")
    price = st.number_input(f"Unit Price {i+1}", min_value=0.0, key=f"price_{i}")
    items.append({"Item": item_name, "Qty": quantity, "Price": price, "Total": quantity * price})


if st.button("Generate Summary"):
    df = pd.DataFrame(items)
    total_amount = df["Total"].sum()

    st.write(f"### {invoice_type} Summary for {client_name}")
    st.dataframe(df)
    st.subheader(f"Total Amount: ₹{total_amount:.2f}")
