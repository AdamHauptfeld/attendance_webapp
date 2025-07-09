import streamlit as st
import pandas as pd
from sqlalchemy import text
import datetime
from datetime import datetime

#I need to code a check to stop them from logging in multiple times the same day

def main():
    # Establish connection to database
    # conn = st.connection("neon", type="sql")

    #Get the day's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Get the daily code from the passwords database
    # with conn.session as session:
        code_query_result = session.execute(text(f"SELECT daily_code FROM passwords"))
        daily_code = code_query_result.fetchone()
        daily_code = daily_code[0]
        session.close()

    # This gets the class names to populate the select box
    # with conn.session as session:
        class_name_results = session.execute(text("SELECT class_name FROM class"))
        class_names = [row[0] for row in class_name_results.fetchall()]
        session.close()
    

    


    st.header('Class Login Webapp')
    
    with st.form('Login Form'):
        first_name = st.text_input('First Name')
        first_name = first_name.strip().lower()
        last_name = st.text_input('Last Name')
        last_name = last_name.strip().lower()
        class_name = st.selectbox('Your Class', class_names, placeholder = 'Select')
        submitted_code = str(st.text_input('Today\'s Code')).lower()
        submitted_code = submitted_code.strip()
        submitted = st.form_submit_button("Log in")

        if submitted:
            if submitted_code == daily_code:
                #This adds the names and date to my Neon database
                with conn.session as session:
                    session.execute(text("INSERT INTO student (first_name, last_name) VALUES (:first_name, :last_name) ON CONFLICT (first_name, last_name) DO NOTHING"),
                                    {"first_name": first_name, "last_name": last_name,})
                    session.execute(text("INSERT INTO attendance (student_id, class_id, date_id) SELECT"
                                            "(SELECT student_id FROM student WHERE first_name = :first_name AND last_name = :last_name),"
                                            "(SELECT class_id FROM class WHERE class_name = :class_name),"
                                            "(SELECT date_id FROM date WHERE class_date = :date)"
                                            "ON CONFLICT (student_id, class_id, date_id) DO NOTHING"),
                                    {"first_name": first_name, "last_name": last_name, "date": today_date, "class_name": class_name})
                    session.commit()
                    session.close()
                st.write('Successfully logged in as ', first_name, ' ', last_name, ' for ', today_date, '.')

                #This gets the student's attendance record as a cursor object in a singleton tuple
                with conn.session as session:
                    result = session.execute(text("SELECT CONCAT(student.first_name, ' ', student.last_name) as name, date.class_date as date, class.class_name as class "
                                                    "FROM attendance "
                                                    "JOIN student ON attendance.student_id = student.student_id "
                                                    "JOIN class ON attendance.class_id = class.class_id "
                                                    "JOIN date ON attendance.date_id = date.date_id "
                                                    "WHERE student.first_name = :first_name AND student.last_name = :last_name"),
                                            {"first_name": first_name, "last_name": last_name})


                    student_attendance_record = pd.DataFrame(result.fetchall(), columns=result.keys())
                    session.close()
                st.subheader("Attendance Record")
                st.write(f"Showing {len(student_attendance_record)} records")
                st.dataframe(student_attendance_record, hide_index=True)
            else:
                st.subheader(':red[Incorrect code]')

    conn._instance.dispose()

main()
