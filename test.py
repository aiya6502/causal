import streamlit as st

# Initialize session state
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Define the first page
def page1():
    st.title("Page 1")
    
    # Create a selectbox on the first page
    selected_option = st.selectbox("Select an option", ["Option A", "Option B", "Option C"], index=None)
    
    # Store the selected option in session state
    st.session_state.selected_option = selected_option

# Define the second page
def page2():
    st.title("Page 2")
    
    # Display the selected option from session state
    st.write(f"You selected: {st.session_state.selected_option}")

# Create a navigation menu
page = st.sidebar.selectbox("Select a page", ["Page 1", "Page 2"])

# Display the selected page
if page == "Page 1":
    page1()
elif page == "Page 2":
    page2()
