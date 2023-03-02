import streamlit as st
import os
import openai
from streamlit_chat import message
from PIL import Image

txtInputQuestion = "userQuestion"
pageTitle = "Bhagvad Gita GPT"

openai.api_key = st.secrets["OPENAI_API_KEY"]

def clear_text(textInput):

    st.session_state[textInput] = ""

def generate_prompt(question):
    return """Bhagavad Gita Question and Answer Generator

The goal of this text generation model is to provide answers to questions about life and philosophy based on the teachings of the Bhagavad Gita. The model should generate responses that are grounded in the principles and lessons of the Gita, and provide insightful and thoughtful answers to the questions asked.

When generating responses, the model should consider the following guidelines:

1. Emphasize the importance of dharma (duty) and the individual's role in fulfilling it
2. Discuss the concept of non-attachment and how it relates to finding purpose in life
3. Highlight the importance of self-reflection and the pursuit of self-realization
4. Address the concept of the cycle of birth and death and the ultimate goal of liberation
5. Discuss the balancing of action and detachment in daily life
6. If any question appears to be outside the context of Bhagvad Gita, ask the user to input questions related to Bhagvad Gita only.

The model should also aim to generate answers that are coherent, clear, and concise. The responses should be written in a manner that is easy to understand and engaging for the reader.

Example Question-Answer Pairs:
1. Question: What is the ultimate goal in life according to the Bhagavad Gita?
   Answer: The ultimate goal in life according to the Bhagavad Gita is self-realization and liberation from the cycle of birth and death. This can be achieved through fulfilling one's dharma, pursuing self-reflection, and practicing non-attachment.

2. Question: How does the Bhagavad Gita suggest balancing action and detachment in daily life?
   Answer: The Bhagavad Gita emphasizes the importance of balancing action and detachment in daily life. It teaches that one should perform their actions without attachment to the outcome and without expectation of reward. This allows one to fulfill their dharma while remaining detached from the results, promoting inner peace and equanimity.

3. Question: What is the significance of dharma in the Bhagavad Gita?
   Answer: Dharma holds a central place in the teachings of the Bhagavad Gita. It refers to an individual's duty, or the path that they are meant to follow in life. Fulfilling one's dharma is essential for finding purpose and meaning in life, and is also seen as a means of attaining self-realization and liberation. The Gita emphasizes that dharma should be pursued with dedication and commitment, while also recognizing the importance of detachment and non-attachment.

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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": generate_prompt(question)}
    ]
    )
    return response['choices'][0]['message']['content']

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
            'Get Help': 'https://streamlit.io/',
            'Report a bug': 'https://github.com',
            'About': 'About your application: **Hello world**'
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

