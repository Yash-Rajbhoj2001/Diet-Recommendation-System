import streamlit as st
from auth.auth import is_authenticated, logout
from streamlit_extras.switch_page_button import switch_page

# This MUST be the only set_page_config in your entire app
# and must be the first Streamlit command
st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon="🍏",
    layout="wide"
)

def main():
    if not is_authenticated():
        # Redirect to login page if not authenticated
        switch_page("Login")
        # st.switch_page("pages/Login.py")
        # switch_page("pages/Login.py")
        # return

    st.write("# Welcome to Diet Recommendation System! 👋")
    
    with st.sidebar:
        if is_authenticated():
            st.write(f"Logged in as {st.session_state.get('user_email', 'User')}")
            if st.button("Logout"):
                logout()
                st.success("Logged out successfully.")
                st.rerun()
                
    
    st.sidebar.success("Select a Recommendation Page.")
    st.markdown("""
        A diet recommendation web application using content-based approach
        with Scikit-Learn, FastAPI and Streamlit.
        [GitHub Repo](https://github.com/Yash-Rajbhoj2001/Diet-Recommendation-System.git)
    """)

if __name__ == "__main__":
    main()  