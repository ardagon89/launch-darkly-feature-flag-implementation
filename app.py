import streamlit as st
from multiapp import MultiApp
import person_dashboard, admin

app = MultiApp()

# Add all your application here
app.add_app("User", person_dashboard.app)
app.add_app("Admin", admin.app)

# The main app
app.run()