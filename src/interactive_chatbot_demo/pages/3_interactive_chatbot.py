import json
import streamlit as st
import os
import dotenv 
from openai import OpenAI

from interactive_chatbot_demo.intialize import initialize_if_empty
initialize_if_empty()     

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", None))

st.set_page_config(page_title="Interactive Chatbot Demo", page_icon="🤖")

st.title("Interactive Chatbot Demo")

# Initialize chat history
if "messages" not in st.session_state:
    # initialize system prompt
    st.session_state.messages = [
            {
                "role": "system",
                "content": st.session_state["final_prompt"],
            }
        ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != "system":
            st.markdown(message["content"])
     
# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="gpt-4.1-mini",
    ).choices[0].message.content

    print(response)
    print("RESPONSE TYPE:", type(response))

    assistant_message = json.loads(response)
    print(assistant_message)
    assistant_response = assistant_message.get("Response", "")

    st.header(f'Order Status: {assistant_message.get("Order Status", "")}')
    st.dataframe(assistant_message.get("Orders", ""))

    if assistant_message.get("Order Status", "") == "Confirmed":
        st.balloons()

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
