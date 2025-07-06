from pathlib import Path
import streamlit as st
from jinja2 import Environment
env = Environment()

BASE_PROMPT_PATH = Path("prompts/base_prompt.txt")

def compile_menu(menu):
    compiled_string = ""
    
    for section_name, section_content in menu.items():
        
        section_string = "\n".join(f"{item['name']} ({item['price']})" for item in section_content)
        compiled_string += f"{section_name}:\n" 
        compiled_string += section_string + "\n\n"

    return compiled_string.strip()

def initialize_if_empty():

    # For base prompt
    if 'base_prompt' not in st.session_state:
        st.session_state['base_prompt'] = Path(BASE_PROMPT_PATH).read_text(encoding="utf-8")

    # For restaurant information
    if 'restaurant_information' not in st.session_state:
        restaurant_information_fn = lambda restaurant_name, location, hours: (
            f"Restaurant Name: {restaurant_name}\n"
            f"Location: {location}\n"
            f"Hours: {hours}"
        )
        restaurant_name = "Silog Express"
        location = "Barangay Uno, Pasay, Manila, Philippines"
        hours = "8AM to 9PM"
        st.session_state['restaurant_information'] = restaurant_information_fn(
            restaurant_name, location, hours
        )

    # For menu
    if 'menu' not in st.session_state:
        menu_dict = {
            "Drinks": [
                {"name": "Iced Tea", "price": "₱50"},
                {"name": "Soda", "price": "₱40"},
                {"name": "Bottled Water", "price": "₱30"}
            ],
            "Meals": [
                {"name": "Tapsilog", "price": "₱150"},
                {"name": "Longsilog", "price": "₱140"},
                {"name": "Tocilog", "price": "₱145"},
                {"name": "Bangsilog", "price": "₱155"},
                {"name": "Chicksilog", "price": "₱160"},
                {"name": "Liempo Silog", "price": "₱170"}
            ],
        }
        st.session_state['menu'] = compile_menu(menu_dict)

    # For fewshot examples
    if 'sample_dict' not in st.session_state:
        st.session_state['sample_dict'] = {}

    if 'compiled_samples' not in st.session_state:
        st.session_state['compiled_samples'] = "<EMPTY EXAMPLES>"

    # For Final Prompt
    if 'final_prompt' not in st.session_state:
        base_prompt = env.from_string(st.session_state['base_prompt'])
        
        st.session_state['final_prompt'] = base_prompt.render(
            restaurant_information=st.session_state['restaurant_information'],
            menu=st.session_state['menu'],
            fewshot_examples=st.session_state["compiled_samples"]
        )

    # For chatbot
    