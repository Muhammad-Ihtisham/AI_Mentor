from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain_ollama import ChatOllama
# from langchain_community.chat_models import ChatDeepSeek
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

if "generated" not in st.session_state:
    st.session_state['generated'] = []

if "past" not in st.session_state:
    st.session_state['past'] = []

if "entered_prompt" not in st.session_state:
    st.session_state['entered_prompt'] = ""

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""



# set streamlit page configuration
st.set_page_config(page_title="chatbot")
st.title("AI Mentor")



# inititlize the llm model 

chat = ChatOllama(
    temperature = 0.5,
    model = "deepseek-r1:1.5b"   
)

def build_message_list():
    """Build a list of messages including system,Human and AI messages """

    zipped_messages = [SystemMessage(
        content ="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        your name is AI Mentor.you are an AI technical expert for Artificial Intelligence.
        1.Greet the user politely ask your name and ask how you can assist them
        2.provide information and relevent responses to questions about Artificial Intelligence, machine learning, deep learning, natural language processing, computer vision and related topics.
        3.you must avoid discussing sensitive, offensive or harmful content.Refrain from engaging in any form of discrimination,harassment or inappropriate behaviour.
        4.if teh user asks about the topic urelated to AI, politely steer the conversations or infform them that topic is outside the scope of this conversation.
        5.Be patient and considerate when responding to user queries and provide clear explaination.
        6.if the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
        7.Do not generate the long paragraphs in response.Maximum words should be 100.

        Remember, your primary goal is to assist and educate students in the field of AI.<|eot_id|> """

    
    )]

# zip together the past and generated responses 
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(content=f"<|start_header_id|>user<|end_header_id|>\n\n{human_msg}<|eot_id|>"))

    


        if ai_msg is not None:
            zipped_messages.append(AIMessage(content=f"<|start_header_id|>assistant<|end_header_id|>\n\n{ai_msg}<|eot_id|>"))

    return zipped_messages


def generate_response():
    """Generate AI responses using the """
    zipped_messages = build_message_list()
    ai_response = chat.invoke(zipped_messages)

    return ai_response.content


def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input

    st.session_state.prompt_input = ""


st.text_input('student', key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    user_query = st.session_state.entered_prompt

    st.session_state['past'].append(user_query)

    output = generate_response()

    st.session_state.generated.append(output)


# Disply the chat history

if st.session_state['generated']:
    for i in range (len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))

        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')









