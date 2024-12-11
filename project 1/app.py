from dotenv import load_dotenv
load_dotenv() 
import os
import streamlit as st
import psycopg2
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage, AIMessage


groq_api_key = os.getenv("GROQ_API_KEY")


def get_groq_response(question, prompt):
    llm = ChatGroq(
        model_name="llama-3.1-70b-versatile",  
        temperature=0,  
    )
    response = llm([SystemMessage(content=prompt[0]), HumanMessage(content=question)])
    return response.content 


def read_sql_query(sql, db_host, db_port, db_username, db_password, db_name):
    try:
      
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_username,
            password=db_password,
            dbname=db_name
        )
        cur = conn.cursor()

        
        cur.execute(sql)
        rows = cur.fetchall()

        
        conn.commit()
        conn.close()

     
        return rows
    
    except Exception as e:
        print("Error: ", e)
        return []


prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database is odoo17, and the schema is private_schema. There are two tables: 'sales' and 'customer'.
    
    The table 'sales' has the following columns: 
    sale_id, product_name, product_code, sale_date, sale_amount, quantity_sold, customer_id, customer_name, 
    customer_email, shipping_address, billing_address, country, region, city, postal_code, phone_number, 
    payment_method, payment_status, discount_applied, discount_amount, total_amount, tax_rate, tax_amount, 
    shipping_cost, order_status, product_category, product_supplier, sale_channel, warranty_period, sales_rep, notes.
    
    The table 'customer' has the following columns: 
    customer_id, customer_name, customer_email, phone_number, address, country, region, city, postal_code, membership_level, signup_date.
    
    For example:
    Example 1 - How many entries of the records are present? 
    The SQL command will be something like this: 
    SELECT COUNT(*) 
    FROM private_schema.sales;
    
    Example 2 - Show all the products.
    The SQL command will be something like this: 
    SELECT DISTINCT product_name 
    FROM private_schema.sales;

    Example 3 - Tell me the top 5 sales.
    The SQL command will be something like this: 
    SELECT * 
    FROM private_schema.sales 
    ORDER BY sale_amount DESC 
    LIMIT 5;

    Example 4 - Can you show me the sales information along with customer names?
    The SQL command will be something like this: 
    SELECT 
    sales.sale_id, 
    sales.product_name, 
    sales.sale_date, 
    sales.sale_amount, 
    sales.quantity_sold, 
    sales.customer_id, 
    sales.payment_method,
    customer.customer_name, 
    customer.customer_email
    FROM private_schema.sales AS sales
    JOIN private_schema.customer AS customer 
    ON sales.customer_id = customer.customer_id;
    
    Example 5 - Can you show me the total sales amount for each product?
    The SQL command will be something like this: 
    SELECT 
    product_name, 
    SUM(sale_amount) AS total_sales
    FROM private_schema.sales
    GROUP BY product_name;
    
    Example 6 - Show the sales information along with customer information for each sale.
    The SQL command will be something like this: 
    SELECT 
    sales.sale_id, 
    sales.product_name, 
    sales.sale_date, 
    sales.sale_amount, 
    sales.quantity_sold, 
    sales.payment_method,
    customer.customer_name, 
    customer.customer_email, 
    customer.phone_number, 
    customer.address, 
    customer.city, 
    customer.country
    FROM private_schema.sales AS sales
    JOIN private_schema.customer AS customer
    ON sales.customer_id = customer.customer_id;

    The SQL query should not have ``` at the beginning or end, and the word "SQL" should not appear in the output.
    """
]




st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Groq App To Retrieve SQL Data")


custom_css = """
    <style>
    .result-text {
        font-size: 20px;
        color: white;
        font-family: 'Arial', sans-serif;
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
"""


st.markdown(custom_css, unsafe_allow_html=True)


question = st.text_input("Input: ", key="input")


submit = st.button("Ask the question")


if submit:
   
    response = get_groq_response(question, prompt)
    print(f"Generated SQL Query: {response}")
    
  
    db_host = ''
    db_port = ''
    db_username = ''
    db_password = ''
    db_name = ''
    
    
    response_data = read_sql_query(response, db_host, db_port, db_username, db_password, db_name)
    
  
    if response_data:
        st.subheader("The Response is")
        for row in response_data:
            st.markdown(f'<p class="result-text">{row}</p>', unsafe_allow_html=True)  
    else:
        st.write("No data found or an error occurred.")
