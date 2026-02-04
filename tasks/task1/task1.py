import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ruthvik2006",   # change this
        database="student_db"
    )

# ---------------- CRUD FUNCTIONS ----------------
def add_student(name, age, subject, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, subject, marks) VALUES (%s,%s,%s,%s)",
        (name, age, subject, marks)
    )
    conn.commit()
    conn.close()

def get_students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def update_marks(student_id, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET marks=%s WHERE id=%s",
        (marks, student_id)
    )
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()

# ---------------- STREAMLIT UI ----------------
st.title("Student Performance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Update Marks", "Delete Student", "Analytics"]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", 0, 100)

    if st.button("Add"):
        add_student(name, age, subject, marks)
        st.success("Student added")

# ---------------- VIEW STUDENTS ----------------
elif menu == "View Students":
    df = get_students()
    df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    st.dataframe(df)

# ---------------- UPDATE MARKS ----------------
elif menu == "Update Marks":
    df = get_students()
    if not df.empty:
        student_id = st.selectbox("Student ID", df["id"])
        new_marks = st.number_input("New Marks", 0, 100)
        if st.button("Update"):
            update_marks(student_id, new_marks)
            st.success("Marks updated")

# ---------------- DELETE STUDENT ----------------
elif menu == "Delete Student":
    df = get_students()
    if not df.empty:
        student_id = st.selectbox("Student ID", df["id"])
        if st.button("Delete"):
            delete_student(student_id)
            st.warning("Student deleted")

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    df = get_students()

    if not df.empty:
        df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

        st.metric("Average Marks", round(df["marks"].mean(), 2))
        st.metric("Pass Percentage", round((df["Status"] == "Pass").mean() * 100, 2))

        top = df.loc[df["marks"].idxmax()]
        st.metric("Top Scorer", top["name"], top["marks"])

        # Bar Chart: Subject vs Average Marks
        st.subheader("Subject vs Average Marks")
        subject_avg = df.groupby("subject")["marks"].mean()
        fig1, ax1 = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

        # Pie Chart: Pass / Fail
        st.subheader("Pass / Fail Ratio")
        pf = df["Status"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(pf, labels=pf.index, autopct="%1.1f%%")
        st.pyplot(fig2)
