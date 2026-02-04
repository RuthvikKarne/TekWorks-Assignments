import mysql.connector
import streamlit as st
connector=mysql.connector
conn=connector.connect(host="localhost",user="root",password="Ruthvik2006",database='loginandreg')
cursor=conn.cursor()
print(conn.is_connected())
st.title("Login and Registration Page")
st.sidebar.title("menu")
choice=st.sidebar.radio("menu",["login","register"])
if choice=="register":
    st.subheader("create new account")
    firstname=st.text_input("enter first name")
    lastname=st.text_input("enter last name")
    username=st.text_input("enter user name")
    password=st.text_input("enter password name")
    if st.button("register"):
        st.success("register succesfull")
        sql="insert into login(firstname,lastname,username,password) values(%s,%s,%s,%s)"
        cursor.execute(sql,(firstname,lastname,username,password))
        conn.commit()
elif choice == "login":
    st.header("Login")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter password", type="password")
    col1, col2 = st.columns(2)
    if st.button("Login"):
        sql = "SELECT firstname, lastname FROM login WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        data = cursor.fetchone()
        if data:
            col1.header("First Name")
            col1.success(data[0])
            col2.header("Last Name")
            col2.success(data[1])
        else:
            st.error("Wrong username or password")

