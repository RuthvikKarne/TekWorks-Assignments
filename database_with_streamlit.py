import streamlit as st
import mysql.connector
connector=mysql.connector
conn=connector.connect(host="localhost",user="root",password="Ruthvik2006",database="student_db")
cursor=conn.cursor()

st.sidebar.title("Menu")
choice = st.sidebar.radio(
    "Menu",
    ["entire data", "insert single data", "update data", "delete data", "view with condition"]
)
st.title("database connection")
if choice == "entire data":
    cursor.execute("select * from students")
    data=cursor.fetchall()
    st.table(data)
elif choice == "insert single data":
    st.subheader("insert data")
    id=st.text_input("enter id")
    name=st.text_input("enter ur name")
    age=st.text_input("enter age")
    if st.button("submit"):
        sql="insert into students (id,name,age) values (%s,%s,%s)"
        value=(id,name,age)
        cursor.execute(sql,value)
        conn.commit()
        st.success("data inserted successfully")
elif choice == "delete data":
    st.subheader("Delete data")
    sql="delete from students where id = %s"
    id=st.text_input("Enter the id to delete")
    if(st.button("delete")):
        cursor.execute(sql,(id,))
        conn.commit()
        st.success("Data deleted successfully")
elif choice == "update data":
    st.subheader("update data")

    id = st.text_input("enter the id to update")
    option = st.radio("name or age", ("name", "age", "both"))
    if option == "name":
        new_name = st.text_input("enter the name to be updated")
        if st.button("update name"):
            sql = "update students set name=%s where id=%s"
            cursor.execute(sql, (new_name, id))
            conn.commit()
            st.success("name updated successfully ✅")
    elif option == "age":
        new_age = st.number_input("Enter the age to be updated", min_value=1, step=1)

        if st.button("update age"):
            sql = "update students set age=%s where id=%s"
            cursor.execute(sql, (new_age, id))
            conn.commit()
            st.success("age updated successfully ✅")
    elif option == "both":
        new_name = st.text_input("enter name")
        new_age = st.number_input("enter age", min_value=1, step=1)

        if st.button("update name and age"):
            sql = "update students set name=%s, age=%s where id=%s"
            cursor.execute(sql, (new_name, new_age, id))
            conn.commit()
            st.success("data updated successfully ✅")

elif choice == "view with condition":
    st.subheader("view with condition")
    option=st.radio("filter by",("name","age"))
    if option=="name":
        a=st.text_input("enter name")
        sql="select * from students where name=%s"
        if st.button("submit"):
            cursor.execute(sql,(a,))
            data = cursor.fetchall()
            st.table(data)
    if option=="age":
        a=st.number_input("enter age",min_value=1,step=1)
        sql="select * from students where age=%s"
        if st.button("submit"):
            cursor.execute(sql,(a,))
            data = cursor.fetchall()
            st.table(data)        
        

        
