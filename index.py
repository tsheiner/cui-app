

import streamlit as st

# Define pages
list_page = st.Page("list_page.py", title="List Items", icon="")
map_page = st.Page("map_page.py", title="Map Items", icon="")

# Set up navigation
pg = st.navigation([list_page, map_page])

# Set common page configuration if needed
st.set_page_config(page_title="My Multi-Page App", page_icon=":world_map:")

# Execute the current page
pg.run()

# Function to generate icon HTML
def get_icon(icon_name):
    return f'<i class="material-icons">{icon_name}</i>'

# Page with Material Icon
def main():
    # Add Material Icons CSS
    st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

    # Title with Icon
    st.markdown(f"<h1>{get_icon('home')} Home Page</h1>", unsafe_allow_html=True)
    st.write("This is the Home page with a Material Icon.")

    # Subtitle with Icon
    st.markdown(f"<h2>{get_icon('list')} List of Items</h2>", unsafe_allow_html=True)
    st.write("Here is a list of items.")