import streamlit as st
import os

from handleOpenAI import handleOpenAI

api_key = os.getenv('OPENAPI_KEY')

st.title('Chat')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):

        response = handleOpenAI(api_key, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            if response.startswith('http'):
                st.image(response)
            else:
                st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
