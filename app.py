import streamlit as st
from multiapp import MultiApp
import person_dashboard, admin

# PAGES = {
#     "person_dashboard": person_dashboard
# }

# st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]
# page.app()

app = MultiApp()

# Add all your application here
app.add_app("User", person_dashboard.app)
app.add_app("Admin", admin.app)

# The main app
app.run()