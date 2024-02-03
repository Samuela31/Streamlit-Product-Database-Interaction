import psycopg2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Database connection
conn = psycopg2.connect(
    database="records_db",
    user="postgres",
    password="1234",
    host="localhost",  
    port="5432"         
)

# Create a cursor object
cursor = conn.cursor()

# Create 'products' table if it doesn't exist
create_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id text PRIMARY KEY,
        name text,
        cost numeric,
        rating integer CHECK (rating >= 1 AND rating <= 5)
    )
"""
cursor.execute(create_table_sql)
conn.commit()

# Streamlit app
st.title("Product Database Interaction")

st.header("Insert Product")
id = st.text_input("Enter Product ID:")
name = st.text_input("Enter Product Name:")
cost = st.number_input("Enter Product Cost:")
rating = st.number_input("Enter Product Rating (1 to 5):", min_value=1, max_value=5)

if st.button("Insert Product"):
    cursor.execute("INSERT INTO products (id, name, cost, rating) VALUES (%s, %s, %s, %s)", (id, name, cost, rating))
    conn.commit()
    st.success(f"Product inserted: ID - {id}, Name - {name}, Cost - {cost}, Rating - {rating}")

st.header("Update Product")
update_id = st.text_input("Enter ID of Product to Update:")
new_name = st.text_input("Enter New Name:")
new_cost = st.number_input("Enter New Cost:")
new_rating = st.number_input("Enter New Rating (1 to 5):", min_value=1, max_value=5)

if st.button("Update Product"):
    cursor.execute("UPDATE products SET name = %s, cost = %s, rating = %s WHERE id = %s", (new_name, new_cost, new_rating, update_id))
    conn.commit()
    if cursor.rowcount == 0:
        st.warning(f"No product found with ID - {update_id}")
    else:
        st.success(f"Product updated: ID - {update_id}, New Name - {new_name}, New Cost - {new_cost}, New Rating - {new_rating}")

st.header("Delete Product")
delete_id = st.text_input("Enter ID of Product to Delete:")

if st.button("Delete Product"):
    cursor.execute("DELETE FROM products WHERE id = %s", (delete_id,))
    conn.commit()
    if cursor.rowcount == 0:
        st.warning(f"No product found with ID - {delete_id}")
    else:
        st.success(f"Product deleted: ID - {delete_id}")

# Display the table of products
st.header("Products Table")
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()

if products:
    # Define column headings
    col_headings = ["ID", "Name", "Cost", "Rating"]

    # Combine column headings with the data
    products_with_headings = [col_headings] + products

    st.table(products_with_headings)

    # Data Visualization
    df = pd.DataFrame(products, columns=["ID", "Name", "Cost", "Rating"])
    
    # Bar Chart for Cost
    st.subheader("Cost Distribution")
    plt.bar(df["Name"], df["Cost"])
    plt.xlabel("Product Name")
    plt.ylabel("Cost")
    st.pyplot(plt)
    
    # Scatter Plot for Rating
    st.subheader("Rating Distribution")

    # Clear the current figure
    plt.clf()

    plt.scatter(df["Name"], df["Rating"])
    plt.xlabel("Product Name")
    plt.ylabel("Rating")
    st.pyplot(plt)

else:
    st.warning("No products found in the table.")        

# Close database connections
cursor.close()
conn.close()
