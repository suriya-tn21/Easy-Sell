import streamlit as st
from PIL import Image
import Pages

def change_page(page):
    st.session_state['page'] = page

if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  

st.set_page_config(layout = "wide")
logo = Image.open("Images/easy-shop.png")
st.image(logo, width = 125)

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col1:
    st.button("Home", on_click = change_page, args = ('Home',))
with col2:
    st.button("Products", on_click = change_page, args = ('Products',))
with col3:
    st.button("About", on_click = change_page, args = ('About',))
with col4:
    st.button("Account", on_click = change_page, args = ('Account',))

if st.session_state['logged_in']:
    with col5:
        st.button("➕", on_click=change_page, args=('Add Product',))
    with col6:
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.success("You have been signed out.")
            st.rerun()  # Refresh the page to reflect the logged-out state

else:
    with col5:
        st.write("")  # Keep the layout consistent


# Page content based on selected page
if st.session_state['page'] == 'Home':
    Pages.Home_page()
elif st.session_state['page'] == 'Products':
    Pages.All_products_page()
elif st.session_state['page'] == 'About':
    Pages.About_page()
elif st.session_state['page'] == 'Account':
    Pages.Account_page()
elif st.session_state['page'] == 'Add Product':
    Pages.Add_Product_page()
elif st.session_state['page'] == 'Edit Profile':
    Pages.Edit_Profile_page()
elif st.session_state['page'] == 'Product Details':
    Pages.Product_details_page()
