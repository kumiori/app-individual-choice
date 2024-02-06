import streamlit as st
from lib.presentation import PagedContainer

def main():
    st.title("Paged Container Example")

    # creates an current_page element in session_state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    
    items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10"]

    paged_container = PagedContainer(items)
    st.write(f'session {st.session_state}')

    col1, _, col2 = st.columns([2, .1, 2])
    with col2:
        if st.button("Next"):
            st.session_state["current_page"] = min(st.session_state.current_page + 1, paged_container.get_total_pages() - 1)
    with col1:
        if st.button("Prev"):
            st.session_state["current_page"] = max(st.session_state.current_page - 1, 0)

    paged_container.display_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
