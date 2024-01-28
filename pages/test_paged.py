import streamlit as st

class PagedContainer:
    def __init__(self, items, items_per_page=3, show_pagination = True):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 0
        self.show_pagination = show_pagination

    def display_page(self, page):
        # start_idx = self.current_page * self.items_per_page
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_items = self.items[start_idx:end_idx]

        for item in page_items:
            st.write(item)
        
        if self.show_pagination:
            st.write(f"Page {page + 1}/{self.get_total_pages()}")

    def get_total_pages(self):
        return (len(self.items) + self.items_per_page - 1) // self.items_per_page

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
