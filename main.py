# streamlit run main.py

import streamlit as st

login_page = st.Page(
    page='views/login.py',
    title = 'Login Page',
    default = True
)

admin_page = st.Page(
    page='views/admin.py',
    title = 'Admin Page'
)


pg = st.navigation(pages=[login_page, admin_page], expanded=False)

pg.run()