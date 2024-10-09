import streamlit as st
from PIL import Image
import io
import User
import Product
import datetime

image1 = Image.open("Images/image1.png")

def Home_page():
    col1, col2 = st.columns(2)
    with col1:
        st.header("Give Your Workout A New Style!")
        st.write("Success isn't always about greatness. It's about consistency. Consistent hard work gains success. Greatness will come.")
    with col2:
        st.image(image1)

    st.subheader("Products")
    products = Product.fetch_products()
    cols = st.columns(4)  
    for i, product in enumerate(products[:4]):  # Display up to 4 products
        with cols[i % 4]:  
            if product[0]: 
                image = Image.open(io.BytesIO(product[0]))
                st.image(image, use_column_width=True)
            else:
                st.write("No image available")
            
            st.subheader(product[5])  # Assuming the 6th item is the product name
            st.write(f"Rs. {product[6]}")  # Assuming the 7th item is the price
            if st.button("Details", key=f"details_{i}"):
                    st.session_state.selected_product = product
                    st.session_state.page = 'Product Details'
                    st.rerun()

def All_products_page():
    st.title("All Products")
    st.session_state.search_query = st.text_input("Search for products", value=st.session_state.search_query)
    sort_option = st.selectbox("Sort by", ("Default Sorting", "Sort by price", "Sort by popularity", "Sort by rating", "Sort by sale"))
    
    st.write("---")
    products = Product.fetch_products()

    if products:
        cols = st.columns(4)  
        for i, product in enumerate(products[:4]):  # Display up to 4 products
            with cols[i % 4]:  
                if product[0]: 
                    image = Image.open(io.BytesIO(product[0]))
                    st.image(image, use_column_width=True)
                else:
                    st.write("No image available")
                
                st.subheader(product[5])
                st.write(f"Rs. {product[6]}")
                if st.button("Details", key=f"details_{i}"):
                    st.session_state.selected_product = product
                    st.session_state.page = 'Product Details'
                    st.rerun()

    else:
        # If there are no products, display a message
        st.write("No products available at the moment.")

def Product_details_page():
    st.title("Product Details")
    if 'selected_product' in st.session_state:
        product = st.session_state.selected_product
        
        image_container = st.container()
        with image_container:
            cols = st.columns(5)
            for i, img_data in enumerate(product[:5]):  # First 5 elements are image data
                if img_data:
                    image = Image.open(io.BytesIO(img_data))
                    resized_image = Product.resize_image(image)
                    with cols[i]:
                        st.image(resized_image, use_column_width=True)
                else:
                    with cols[i]:
                        st.write("No image")
        
        # Display other product details
        st.write(f"**{product[5]}**")  # Product name
        st.write(f"Price: {product[6]}")  # Product price
        st.write(f"Description: {product[7]}")  # Product description
        st.write(f"Contact: {product[8]}")  # Product contact info
    else:
        st.write("No product selected.")

def About_page():
    st.title("About Us")
    st.write("Easy Shop is your one-stop destination for a wide range of products.")

def Account_page():
    # Check if the user is logged in and show the profile page if true
    if st.session_state.get("logged_in"):
        show_profile_page(st.session_state.username)
    else:
        # Otherwise, show the login and registration tabs
        st.title("Sign in | Sign up")
        login_tab, register_tab, reset_tab = st.tabs(["Login", "Register", "Reset Password"])

        with login_tab:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                if User.sign_in(login_username, login_password):
                    st.success("Logged in successfully")
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.rerun()  # This refreshes the page to switch to the profile view
                else:
                    st.error("Login failed. Check your credentials.")

        with register_tab:
            st.subheader("Sign Up")
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            reg_email = st.text_input("Email", key="reg_email")
            reg_phone = st.text_input("Phone Number", key="reg_phone")
            reg_dob = st.date_input("Date of Birth", key="reg_dob")
            reg_profile_pic = st.file_uploader("Profile Picture", type=["png", "jpg", "jpeg"], key="reg_profile_pic")
            reg_bio = st.text_area("Biography", key="reg_bio")

            if st.button("Sign up"):
                if reg_password == reg_confirm_password:
                    result = User.sign_up(reg_username, reg_password, reg_email, reg_phone, reg_dob, reg_profile_pic, reg_bio)
                    st.success(result)
                else:
                    st.error("Passwords do not match.")

        with reset_tab:
            st.subheader("Reset Password")
        
def show_profile_page(username):
    st.title(f"Welcome, {username}!")
    st.divider()
    user_details = User.fetch_user_details(username)

    if user_details:
        col1, col2 = st.columns([1, 3])

        with col1:
            if user_details['profile_pic']:
                profile_image = Image.open(io.BytesIO(user_details['profile_pic']))
                resized_image = profile_image.resize((256, 256))
                st.image(resized_image, use_column_width=True)
            else:
                st.write("No profile picture available.")
        
        with col2:
            st.subheader("Profile Information")
            st.write(f"**Username:** {user_details['username']}")
            st.write(f"**Email:** {user_details['email']}")
            st.write(f"**Phone Number:** {user_details['phone']}")
            st.write(f"**Date of Birth:** {user_details['dob']}")
            
            st.subheader("Biography")
            st.write(user_details['bio'])

        st.divider()
        st.subheader("Account Actions")
        if st.button("Edit Profile"):
            st.session_state['page'] = 'Edit Profile'
            st.rerun()
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.success("You have been signed out.")
            st.rerun()  

    else:
        st.error("Failed to fetch profile details.")

def Add_Product_page():
    if not st.session_state.get('logged_in'):
        st.error("You must be logged in to add a product.")
        st.write("Please go to the Account page to sign in or create an account.")
        return
    
    st.title("Add Product")
    st.write("Please fill in the details below to add your product:")
    
    # Allow up to 5 images to be uploaded
    product_images = [st.file_uploader(f"Choose image {i+1} (optional)", type=["png", "jpg", "jpeg"]) for i in range(5)]
    
    product_name = st.text_input("Product Name")
    product_price = st.text_input("Price")
    product_description = st.text_area("Description")
    
    if st.button("Submit"):
        if product_name and product_price and product_description:
            # Convert uploaded files to PIL images
            images = [Image.open(image) if image else None for image in product_images]
            
            Product.add_product(images, product_name, product_price, product_description, st.session_state.username, User.get_email(st.session_state.username))
            st.success("Product added successfully!")
        else:
            st.error("Please fill in all required fields.")

def Edit_Profile_page():
    username = st.session_state.get('username')    
    user_details = User.fetch_user_details(username)
    
    if user_details:
        st.title(f"Edit Profile: {username}")
        st.markdown("---")
        
        new_email = st.text_input("Email", value=user_details['email'])
        new_phone = st.text_input("Phone Number", value=user_details['phone'])

        # Convert the date string to a datetime.date object
        try:
            current_dob = datetime.datetime.strptime(user_details['dob'], '%Y-%m-%d').date()
        except (ValueError, TypeError):
            current_dob = datetime.date.today()  # Use today's date as a fallback

        new_dob = st.date_input("Date of Birth", value=current_dob)
        new_profile_pic = st.file_uploader("Update Profile Picture (optional)", type=["png", "jpg", "jpeg"])
        new_bio = st.text_area("Biography", value=user_details['bio'])
        
        if st.button("Save Changes"):
            User.update_profile(username, new_email, new_phone, new_dob, new_profile_pic, new_bio)
            st.success("Profile updated successfully!")
            st.session_state['page'] = 'Account'  # Return to the Account page after saving
            st.rerun()
        
        if st.button("Cancel"):
            st.session_state['page'] = 'Account'  # Return to the Account page without saving
            st.rerun()
            
    else:
        st.error("Failed to fetch user details.")

