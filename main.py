import streamlit as st
import os
import openai
from streamlit_chat import message
from PIL import Image
import time

txtInputQuestion = "userQuestion"
pageTitle = "Bhagvad Gita GPT"

openai.api_key = st.secrets["OPENAI_API_KEY"]

def clear_text(textInput):

    st.session_state[textInput] = ""

def generate_prompt(question):
    return """You are Bhagvad Gita Question and Answer Generator. You are a polite text generation model, to provide answers to questions about life and philosophy based on the teachings of the Bhagavad Gita.
The model should generate responses that are grounded in the principles and lessons of the Gita, and provide insightful and thoughtful answers to the questions asked.
The model should consider the following guidelines:
1. No answer exceeds 250 tokens.
2. For questions unrelated to Bhagvad Gita, remind user to stay on topic of Bhagvad Gita.
Question: {}
Answer:""".format(
        question
    )



def generate_response_davinci(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(question),
        temperature=0.6,
        max_tokens=2048
    )
    return response.choices[0].text

def generate_response_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": generate_prompt(question)}
        ]
        )
        return response['choices'][0]['message']['content']
    except RateLimitError as e:
        st.error("Rate limit reached. Please try again later.")
        for i in range(60):
            time.sleep(1) # Wait for 1 second
            st.warning(f"Retrying in {60-i} seconds...")
        return generate_response_chatgpt(question) # Retry the function

def get_text():
    input_text = st.text_input("Hello, ask me a question about life and philosophy.",placeholder="Type Your question here.", key=txtInputQuestion)
    return input_text

def page_setup(title, icon):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout='centered',
        initial_sidebar_state='auto',
        menu_items={
            'About': 'About your application: **This is Bhagvad Gita GPT, a simple ChatGPT use case demo to show how one can easily leverage openAI APIs to create intelligent conversational experiences related to a specific topic.**'
        }
    )
    st.sidebar.title('Creators :')
    st.sidebar.write("Abhishek Mishra")
    st.sidebar.markdown('Abhishek Mishra (https://github.com/abhishek-mishra-07)')
    st.sidebar.write("Shubhi Tiwari (https://github.com/tiwariShubhi)")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    icon = Image.open('gita.jpg')

    #setup page
    page_setup(pageTitle,icon)


    col1, col2 = st.columns(2)
    with col1:
        st.title("Bhagvad Gita GPT")
    with col2:
        st.image(icon)
    #st.write("test 1")

    user_input = get_text()

    print("get_text called.")
    if user_input:
        output = generate_response_chatgpt(user_input)
        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:

        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i),seed=10,avatar_style='avataaars')
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user',seed=200,avatar_style='avataaars')

