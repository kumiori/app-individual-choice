import streamlit as st
import random
from streamlit_extras.row import row

# Define the lists of numbers and words
numbers = [1, 2, 3, 4, 5]
words = ["apple", "banana", "cherry", "date", "elderberry"]
words = ["🍎", "🍌", "🍒", "📅", "🫐"]

# Initialize session_state variables
if 'selected_number' not in st.session_state:
    st.session_state["selected_number"] = None

if 'selected_word' not in st.session_state:
    st.session_state["selected_word"] = None


# Shuffle the lists

# Get the correct association
correct_association = {num: word for num, word in zip(numbers, words)}

def commit_to_state(data_type, value):
    if data_type == "word":
        st.session_state["selected_word"] = value
    elif data_type == "number":
        st.session_state["selected_number"] = value


# Main Streamlit app
def main():
    st.title("Match the Number with the Word!")
    st.write("Match the number with the corresponding word.")

    col1, col2, col3 = st.columns([1, 9, 1])
    # Display the correct association
    st.write("Correct Association:")
    for num, word in correct_association.items():
        st.write(f"{num}: {word}")

    random.shuffle(words)
    random.shuffle(numbers)

    # Create buttons for each number-word pair

    if st.session_state["selected_number"] is None:
        icon_row = row(5)
        for num in numbers:
            if icon_row.button(
                str(num),
                key = f"button_{num}",
                use_container_width=True,
                on_click = commit_to_state, args = ["number", num]):
                st.session_state["selected_number"] = num
                if st.session_state["selected_word"] is not None:
                    check_answer()
    else:
        col1.markdown(
            f"# {st.session_state['selected_number']}",
            unsafe_allow_html=True,
        )

    if st.session_state["selected_word"] is None:
        icon_row = row(5)
        for word in words:
            if icon_row.button(
                word,
                key = f"button_{word}",
                use_container_width=True,
                on_click = commit_to_state, args = ["word", word]):
                st.session_state["selected_word"] = word
                if st.session_state["selected_number"] is not None:
                    check_answer()
    else:
        col3.markdown(
            f"# {st.session_state['selected_word']}",
            unsafe_allow_html=True,
        )
    
    if st.session_state["selected_number"] is not None and st.session_state["selected_word"] is not None:
        if st.button("Check Answer"):
            check_answer()
    col2.divider()
    st.json(st.session_state, expanded=False)
    
def clear_session_state():
    st.session_state["selected_number"] = None
    st.session_state["selected_word"] = None

def check_answer():
    selected_number = st.session_state["selected_number"]
    selected_word = st.session_state["selected_word"]
    correct_word = correct_association[selected_number]
    if selected_word == correct_word:
        st.success("Correct!")
    else:
        st.error("Incorrect. Try again.")

if __name__ == "__main__":
    
    # Add a button to clear session state
    if st.button("Clear Session State"):
        clear_session_state()
        st.write("Session state cleared.")
    
    main()