import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ruthvik2006",   # change this
        database="school_db"
    )

st.title("Student Attendance & Marks Portal")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Student",
        "Mark Attendance",
        "Add Marks",
        "View Attendance",
        "Reports"
    ]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    st.subheader("Add Student")

    with st.form("add_student"):
        roll = st.number_input("Roll No", min_value=1)
        name = st.text_input("Name")
        class_name = st.selectbox("Class", ["10A", "10B", "11A", "11B"])
        submit = st.form_submit_button("Add Student")

        if submit:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (roll_no, name, class) VALUES (%s,%s,%s)",
                (roll, name, class_name)
            )
            conn.commit()
            conn.close()
            st.success("Student added successfully")

# ---------------- MARK ATTENDANCE ----------------
elif menu == "Mark Attendance":
    st.subheader("Mark Daily Attendance")

    conn = get_conn()
    students = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if students.empty:
        st.error("No students available")
    else:
        student = st.selectbox(
            "Select Student",
            students["id"],
            format_func=lambda x: students[students["id"] == x]["name"].values[0]
        )

        status = st.radio("Attendance Status", ["Present", "Absent"])

        if st.button("Mark Attendance"):
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s,%s,%s)",
                (student, date.today(), status)
            )
            conn.commit()
            conn.close()
            st.success("Attendance marked")

# ---------------- ADD MARKS ----------------
elif menu == "Add Marks":
    st.subheader("Add Subject-wise Marks")

    conn = get_conn()
    students = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if students.empty:
        st.error("No students available")
    else:
        student = st.selectbox(
            "Select Student",
            students["id"],
            format_func=lambda x: students[students["id"] == x]["name"].values[0]
        )

        subject = st.selectbox("Subject", ["Maths", "Science", "English"])
        marks = st.number_input("Marks", 0, 100)

        if st.button("Add Marks"):
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s)",
                (student, subject, marks)
            )
            conn.commit()
            conn.close()
            st.success("Marks added")

# ---------------- VIEW ATTENDANCE ----------------
elif menu == "View Attendance":
    st.subheader("Attendance History")

    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.roll_no, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        ORDER BY a.date DESC
    """, conn)
    conn.close()

    st.dataframe(df)

# ---------------- REPORTS ----------------
elif menu == "Reports":
    st.subheader("Student Report")

    conn = get_conn()
    students = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if students.empty:
        st.error("No students available")
    else:
        student = st.selectbox(
            "Select Student",
            students["id"],
            format_func=lambda x: students[students["id"] == x]["name"].values[0]
        )

        conn = get_conn()

        attendance = pd.read_sql(
            f"SELECT status FROM attendance WHERE student_id={student}",
            conn
        )

        marks = pd.read_sql(
            f"SELECT subject, marks FROM marks WHERE student_id={student}",
            conn
        )

        conn.close()

        # Attendance %
        if not attendance.empty:
            att_percent = round((attendance["status"] == "Present").mean() * 100, 2)
            st.metric("Attendance Percentage", att_percent)
        else:
            st.info("No attendance records")

        # Marks & Result
        if not marks.empty:
            avg_marks = marks["marks"].mean()
            result = "Pass" if avg_marks >= 40 else "Fail"
            st.metric("Average Marks", round(avg_marks, 2))
            st.metric("Result", result)
            st.dataframe(marks)
        else:
            st.info("No marks records")
