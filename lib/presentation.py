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
