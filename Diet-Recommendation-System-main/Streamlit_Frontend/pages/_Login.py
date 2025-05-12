import streamlit as st
from auth.auth import authenticate_user, register_user, logout, is_authenticated, get_current_user
from auth.database import check_and_initialize_db
from streamlit_extras.switch_page_button import switch_page
import requests


# ✅ Ensure DB and table exist before anything else
check_and_initialize_db()


def show_login_page():
    menu = ["Login Page", "Register Page"]
    choice = st.sidebar.radio("Select an option", menu)
    st.title(choice)

    if not is_authenticated():
        # menu = ["Login Page", "Register Page"]
        # choice = st.sidebar.radio("Select an option", menu)

        if choice == "Login Page":
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                success, message = authenticate_user(email, password)
                if success:
                    st.success("Logged in successfully!")
                    switch_page("Hello")  # 👈 Go to Hello directly
                    # st.switch_page("Hello.py")  # 👈 Go to Hello directly
                    # switch_page("Hello.py")  # 👈 Go to Hello directly
                else:
                    st.error(message)

        elif choice == "Register Page":
            st.subheader("Register")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")

            if st.button("Register"):
                success, message = register_user(email, password)
                if success:
                    st.success(message)
                    st.info("Go to Login to sign in")
                else:
                    st.error(message)



def show_home_page():
    st.title("Welcome!")
    user_email = get_current_user()
    st.write(f"Logged in as: {user_email}")
    if st.button("Logout"):
        logout()
        st.success("Logged out.")
        st.rerun()


def main():
    if is_authenticated():
        show_home_page()
    else:
        show_login_page()


if __name__ == "__main__":
    main()
