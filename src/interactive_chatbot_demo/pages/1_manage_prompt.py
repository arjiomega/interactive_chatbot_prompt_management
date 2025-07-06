import os
import streamlit as st
from interactive_chatbot_demo.intialize import initialize_if_empty

initialize_if_empty()            

st.set_page_config(
    page_title="Manage Prompt",
    page_icon="👋",
)

st.header("Manage Prompt")


base_prompt_tab, context_tab, fewshot_tabs, final_prompt_tab = st.tabs(["Base Prompt", "Context", "Fewshot Examples", "Final Prompt"])

from jinja2 import Environment
env = Environment()

with base_prompt_tab:
    st.header("Base Prompt")
    raw_template_list = st.session_state['base_prompt'].split("---")

    prompt_intro_area, context_area, fewshot_area = raw_template_list[:3]
    rest_of_prompt_area = raw_template_list[-1]

    top_area_of_prompt = prompt_intro_area + "---" + context_area + "---" + fewshot_area + "---"

    st.code(top_area_of_prompt, language="text")

    base_prompt_input = st.text_area("modifiable part of base prompt:", rest_of_prompt_area, height=1000)
    st.session_state['base_prompt'] = top_area_of_prompt+base_prompt_input



with context_tab:
    st.header("Context")

    st.session_state['restaurant_information'] = st.text_area(
        "Restaurant Information: ", st.session_state['restaurant_information']
    )
    st.session_state['menu'] = st.text_area("Menu: ", st.session_state['menu'], height=300)

if 'sample_dict' not in st.session_state:
    st.session_state['sample_dict'] = {}

with fewshot_tabs:
    st.header("Fewshot Examples")


    with st.form("my_form"):
        st.write("Inside the form")
        
        restaurant_info_fs = st.text_area("restaurant_information", st.session_state['restaurant_information'])
        menu_fs = st.text_area("menu", st.session_state['menu'], height=300)
        customer_message_fs = st.text_area("customer_message", "I would like to order Tapsilog and a bottle of water, please.")

        st.write("##### Expected Response:")

        st.write("Follow the structure...")

        expected_response_fs = st.text_area("Expected Response:", (
            "{\n"
            "    \"Orders\": [\n"
            "        { \"item\": \"Tapsilog\", \"price\": \"₱150\", \"quantity\": 1 },\n"
            "        { \"item\": \"Bottled Water\", \"price\": \"₱30\", \"quantity\": 1 }\n"
            "    ],\n"
            "    \"Order Total\": \"₱180\",\n"
            "    \"Order Status\": \"Pending\",\n"
            "    \"Response\": \"Thanks for your order! Would you like to add anything else before we proceed?\"\n"
            "}"
        ),
        height=250)

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.success("Form submitted successfully!")
        current_example_count = len(st.session_state['sample_dict'])
        st.session_state['sample_dict'][current_example_count] = {
            "restaurant_information": restaurant_info_fs,
            "menu": menu_fs,
            "customer_message": customer_message_fs,
            "expected_response": expected_response_fs
        }


    compiled_examples = ""

    for example_idx, example in st.session_state['sample_dict'].items():

        compiled_examples += f"### Example {example_idx+1}\n"
        compiled_examples += f"{example['restaurant_information']}\n"
        compiled_examples += f"{example['menu']}\n"
        compiled_examples += f"{example['customer_message']}\n"
        compiled_examples += f"{example['expected_response']}\n"
        compiled_examples += "\n"

        col1, col2 = st.columns([0.80, 0.20], vertical_alignment="top")
        with col1.expander(f"Example {example_idx+1}"):
            st.write("Restaurant Information:")
            st.code(example["restaurant_information"], language="text")
            st.write("Menu:")
            st.code(example["menu"], language="text")
            st.write("Customer Message:")
            st.code(example["customer_message"], language="text")
            st.write("Expected Response:")
            st.code(example["expected_response"], language="json")

        col2.button("Remove", key=f"remove_example_{example_idx}", on_click=lambda: st.session_state['sample_dict'].pop(example_idx, None), type="primary")

    if compiled_examples:
        st.session_state["compiled_samples"] = compiled_examples
        st.code(st.session_state["compiled_samples"], language="text")

with final_prompt_tab:
    st.header("Final Prompt")
    base_prompt = env.from_string(st.session_state['base_prompt'])
    st.session_state['final_prompt'] = base_prompt.render(
        restaurant_information=st.session_state['restaurant_information'],
        menu=st.session_state['menu'],
        fewshot_examples=st.session_state["compiled_samples"]
    )
    st.code(st.session_state['final_prompt'], language="text")