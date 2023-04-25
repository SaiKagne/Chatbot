import nltk
from nltk.chat.util import Chat, reflections
import streamlit as st
import time
import json

st.set_page_config(page_title="Student Queries Chatbot", page_icon="🤖")

with open("users.json", "r") as f:
    users = json.load(f)

def add_user(new_user,new_password):
    users.update({new_user: new_password})
    with open("users.json", "w") as f:
        json.dump(users, f)

# Load the pairs from a JSON file
with open("pairs.json", "r") as f:
    pairs = json.load(f)

# Define a function to update the pairs and save them to the file
def update_pairs(question, answer):
    pairs.append([question, [answer]])
    with open("pairs.json", "w") as f:
        json.dump(pairs, f)

# Create the Chatbot
chatbot = Chat(pairs, reflections)

def main():
    # Create a Streamlit SessionState object to keep track of the login status and username
    session_state = st.session_state
    if "logged_in" not in session_state:
        session_state.logged_in = False
    if "username" not in session_state:
        session_state.username = ""

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #F5F5F5;
            }
            .stButton button {
                background-color: #00BFFF;
                color: black;
                font-weight: bold;
            }
            .stTextInput input[type="text"], .stTextInput input[type="password"] {
                background-color: #FFFFFF;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the login form if the user is not logged in
    if not session_state.logged_in:
        st.write("")
        st.write("")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("")
        with col2:
            st.write("")
            username = st.text_input(f"**Username:**")
            password = st.text_input(f"**Password:**", type="password")
            st.write('---')
            but1, but2 = st.columns(2)
            if but2.button('Sign Up'):
                add_user(username,password)
                st.success("Credentials Successfully Updated!")
            if but1.button("Log in"):
                if username in users and password == users[username]:
                    session_state.logged_in = True
                    session_state.username = username
                    st.success(f"Logged in as {username}.")
                else:
                    st.error("Invalid username or password.")
    # If the user is logged in, display the appropriate page based on their username
    else:
        if session_state.username != 'admin':
            st.markdown("""
                 <h1 style='background-color: #9A2827; padding: 10px; border-radius: 10px; color: white; text-align: center;'>
                 🤖 Student Queries Chatbot</h1>
             """, unsafe_allow_html=True)

            st.write('---')

                # Create a two-column layout
            col1, col2 = st.columns(2)

                # Initialize the conversation history
            if 'conversation' not in st.session_state:
                st.session_state.conversation = []

                # Get the user's input
            st.write('---')
            user_input = st.text_input("Ask Your Question:")

                # Respond to the user's input
            if user_input:
                with st.spinner("Searching..."):
                    time.sleep(1)
                    bot_response = chatbot.respond(user_input)

                if bot_response:
                    # Add the conversation to the history
                    st.session_state.conversation.append(('👤', user_input))
                    st.session_state.conversation.append(('🤖', bot_response))

                    # Display the conversation history
                    for speaker, message in st.session_state.conversation:
                        if speaker == '👤':
                            col2.write(f"<div style='background-color: #d1d1d1; padding: 10px; border-radius: 10px; margin: 5px; display: inline-block;'>{speaker}: {message}</div>", unsafe_allow_html=True)
                        elif speaker == '🤖':
                            col1.write(f"<div style='background-color: #90ee90; padding: 10px; border-radius: 10px; margin: 5px; display: inline-block;'>{speaker}: {message}</div>", unsafe_allow_html=True)
                else:
                    st.error(u'\U0001F916' + ": Sorry, I don't have any knowledge about your question.")

        elif session_state.username == "admin":
            st.markdown("""
                 <h1 style='background-color: #9A2827; padding: 10px; border-radius: 10px; color: white; text-align: center;'>
                 👤 Welcome! Admin Interface</h1>
             """, unsafe_allow_html=True)

            st.write('---')
            question = st.text_input("Enter New Question:")
            answer = st.text_input("Enter New Question's Response:")
            st.write('---')

            if st.button("Update Database"):
                update_pairs(question, answer)
                st.success("Data Successfully Updated!")

if __name__ == "__main__":

    main()
