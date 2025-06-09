import streamlit as st
import pandas as pd
from sqlalchemy import text
import datetime
from datetime import datetime

#I need to code a check to stop them from logging in multiple times the same day

def main():
    # Establish connection to database
    conn = st.connection("neon", type="sql")

    #Get the day's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    with conn.session as session:
        code_query_result = session.execute(text(f"SELECT daily_code FROM passwords"))
        daily_code = code_query_result.fetchone()
        daily_code = daily_code[0]
    


    st.header('Prof. Hauptfeld\'s Class Log')
    
    with st.form('Login Form'):
        fname = st.text_input('First Name')
        fname = fname.lower()
        lname = st.text_input('Last Name')
        lname = lname.lower()
        submitted_code = str(st.text_input('Today\'s Code')).lower()
        submitted = st.form_submit_button("Log in")

        if submitted:
            if submitted_code == daily_code:
                #This adds the names and date to my Neon database
                with conn.session as session:
                    session.execute(text("INSERT INTO student (fname, lname, date) VALUES (:fname, :lname, :date) ON CONFLICT (fname, lname, date) DO NOTHING"),
                                    {"fname": fname, "lname": lname, "date": today_date})
                    session.commit()
                st.write('Successfully logged in as ', fname, ' ', lname, ' for ', today_date, '.')

                #This gets the student's attendance record as a cursor object in a singleton tuple
                with conn.session as session:
                    result = session.execute(text("SELECT CONCAT(fname, ' ', lname) AS student, date FROM student WHERE fname = :fname AND lname = :lname"),
                                            {"fname": fname, "lname": lname}), 
                
                # Extract the CursorResult from the tuple and convert to dataframe to display past attendance
                cursor_result = result[0]  # Get the actual CursorResult object from the tuple
                rows = cursor_result.fetchall()  # Get all rows as tuples
                column_headers = cursor_result.keys()   # Get column names
                student_attendance_record = pd.DataFrame(rows, columns=column_headers)  # Create DataFrame
                st.subheader("Attendance Record")
                st.write(f"📋 Showing {len(student_attendance_record)} records")
                st.dataframe(student_attendance_record, hide_index=True)
            else:
                st.subheader(':red[Incorrect code]')



main()