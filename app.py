import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType
import os

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("To-Do List Generator📝")
st.markdown("Welcome! Effortlessly organize your tasks with our intuitive to-do list generator. Simply provide the main project name and a few subtasks, and we'll create a clear and actionable list for you.")
st.markdown("            1) Mention your Task Name. ")
st.markdown("            2) Mention your Subtasks.")
st.markdown("            2) Mention any additional notes or comments.")
input = st.text_input(" Please enter the above details:",placeholder=f"""Type here""")

open_ai_text_completion_model = OpenAIModel(
    api_key=st.secrets["apikey"],
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def generation(input):
    generator_agent = Agent(
        role="Expert TO-DO LIST ORGANIZER",
        prompt_persona=f"Your task is to CREATE a COMPREHENSIVE to-do list based on the DETAILS provided by the user, including TASK NAME, SUBTASKS, and any additional NOTES.")
    prompt = f"""
You are an Expert TO-DO LIST ORGANIZER. Your task is to CREATE a COMPREHENSIVE to-do list based on the DETAILS provided by the user, including TASK NAME, SUBTASKS, and any additional NOTES.

Here's how you should approach this:

1.IDENTIFY all information from the user regarding the main TASK NAME they wish to accomplish. ANALYZE further details on any SUBTASKS associated with the main task, ensuring you have a clear understanding of each step involved. IDENTIFY if there are any NOTES or additional pieces of information that could be relevant or helpful in completing the tasks and subtasks.

2. ORGANIZE these details into a STRUCTURED to-do list format, prioritizing tasks as necessary and grouping related subtasks under their respective main tasks.

3. PRESENT the to-do list in an ORDERLY and ACCESSIBLE manner, allowing for easy tracking of progress and updates.

You MUST maintain clarity and precision throughout this process to ensure that every item on the to-do list is actionable and understandable.

 """

    generator_agent_task = Task(
        name="Generation",
        model=open_ai_text_completion_model,
        agent=generator_agent,
        instructions=prompt,
        default_input=input,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
    ).execute()

    return generator_agent_task 
   
if st.button("Generate!"):
    solution = generation(input)
    st.markdown(solution)

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata Agent . For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)