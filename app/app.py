import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Quotation & Invoice Generator", page_icon="")

st.title(" Quotation & Invoice Generator")


st.subheader("Client & Quotation Details")
client_name = st.text_input("Client Name")
quotation_date = st.date_input("Date", date.today())


st.subheader("Add Items")
num_items = st.number_input("Number of Items", min_value=1, max_value=20, value=1)

items = []
for i in range(int(num_items)):
    st.write(f"### Item {i+1}")
    desc = st.text_input(f"Description {i+1}")
    qty = st.number_input(f"Quantity {i+1}", min_value=1, value=1, key=f"qty{i}")
    price = st.number_input(f"Price per unit {i+1}", min_value=0.0, value=0.0, key=f"price{i}")
    total = qty * price
    items.append({"Description": desc, "Quantity": qty, "Price": price, "Total": total})


if st.button("Generate Summary"):
    df = pd.DataFrame(items)
    st.table(df)

    subtotal = sum([item["Total"] for item in items])
    gst = subtotal * 0.18  # 18% GST
    grand_total = subtotal + gst

    st.write(f"###  Subtotal: ₹{subtotal:.2f}")
    st.write(f"###  GST (18%): ₹{gst:.2f}")
    st.success(f"### Grand Total: ₹{grand_total:.2f}")

    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Quotation Invoice")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Client Name: {client_name}")
    c.drawString(50, 750, f"Date: {quotation_date}")

    y = 720
    c.drawString(50, y, "Description")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(370, y, "Total")
    y -= 20

    for item in items:
        c.drawString(50, y, item["Description"])
        c.drawString(250, y, str(item["Quantity"]))
        c.drawString(300, y, f"₹{item['Price']:.2f}")
        c.drawString(370, y, f"₹{item['Total']:.2f}")
        y -= 20

    c.drawString(50, y-10, f"Subtotal: ₹{subtotal:.2f}")
    c.drawString(50, y-30, f"GST (18%): ₹{gst:.2f}")
    c.drawString(50, y-50, f"Grand Total: ₹{grand_total:.2f}")
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    st.download_button(
        label=" Download Quotation as PDF",
        data=pdf_bytes,
        file_name=f"quotation_{client_name}.pdf",
        mime="application/pdf"
    )
