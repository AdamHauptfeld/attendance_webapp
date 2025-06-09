import streamlit as st
import datetime
import secrets
import string
from datetime import datetime
from sqlalchemy import text

conn = st.connection("neon", type="sql")
admin_pw = st.secrets['admin_password']

today_date = '2025-06-08'

def admin_login():
    given_pw = st.text_input('Enter admin password: ')
    if given_pw == admin_pw:
        return 5
    else:
        return False


def set_daily_code():
    with st.form('Login Form'):
            daily_code = st.text_input('Enter Code')
            daily_code = daily_code.lower()
            submitted = st.form_submit_button("Submit")

            if submitted:
                with conn.session as session:
                    session.execute(text("""
                                INSERT INTO passwords (daily_code, date) 
                                VALUES (:daily_code, :date)
                                ON CONFLICT (date) 
                                DO UPDATE SET daily_code = :daily_code
                            """), {"daily_code": daily_code, "date": today_date})
                    session.commit()
                st.write('Code submitted: ', daily_code)
                


def main():
    chex = admin_login()
    if chex == 5:
        set_daily_code()
    else:
        pass

main()