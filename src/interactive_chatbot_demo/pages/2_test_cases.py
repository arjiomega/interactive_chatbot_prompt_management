import json
import os
from pathlib import Path
import streamlit as st

import dotenv
dotenv.load_dotenv()

from interactive_chatbot_demo.intialize import initialize_if_empty
initialize_if_empty()     

st.set_page_config(
    page_title="Test Cases",
    page_icon="🤖",
)

st.header("Test Cases")

run_all_test_cases = st.button("Run All Test Cases")


def compile_menu(menu):
    compiled_string = ""
    
    for section_name, section_content in menu.items():
        
        section_string = "\n".join(f"{item['name']} ({item['price']})" for item in section_content)
        compiled_string += f"{section_name}:\n" 
        compiled_string += section_string + "\n\n"

    return compiled_string.strip()

class TestCase:
    def __init__(self, context, input, expected_output):
        self.context = context
        self.input = input
        self.expected_output = expected_output

    @classmethod
    def from_json_path(cls, json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
            return cls(
                context=data['context'],
                input=data['input'],
                expected_output=data['expected_output']
            )

    def _check_variables_similarity(self, base_prompt):
        base_prompt_variables = set(base_prompt.variables)
        expected_variables = {"restaurant_information", "menu"}

        if not base_prompt_variables.issubset(expected_variables):
            raise ValueError(
                f"Base prompt variables {base_prompt_variables} do not match expected variables {expected_variables}"
            )

    def compile_system_prompt(self, base_prompt):
        self._check_variables_similarity(base_prompt)

        restaurant_info = self.context['restaurant_information']
        menu = self.context['menu']

        return base_prompt.format(
            restaurant_information=f"Restaurant Name: {restaurant_info['restaurant_name']}\n"
                                   f"Location: {restaurant_info['location']}\n"
                                   f"Hours: {restaurant_info['hours']}",
            menu=compile_menu(menu)
        )


tab1, tab2 = st.tabs(["Simple Orders", "Prompt Injections"])

simple_order_test_cases_path = "evaluation/test_cases/simple_order_test_cases/"
simple_order_test_cases = os.listdir(simple_order_test_cases_path)

def compare_orders(pred_orders, expected_orders):
    if pred_orders == expected_orders:
        return True, "Exact match"

    pred_map = {(o['item'], o['price']): o['quantity'] for o in pred_orders}
    expected_map = {(o['item'], o['price']): o['quantity'] for o in expected_orders}

    missing = []
    wrong_quantity = []
    extra = []

    for key, expected_qty in expected_map.items():
        if key not in pred_map:
            missing.append({'item': key[0], 'price': key[1], 'quantity': expected_qty})
        elif pred_map[key] != expected_qty:
            wrong_quantity.append({
                'item': key[0],
                'price': key[1],
                'expected_quantity': expected_qty,
                'actual_quantity': pred_map[key]
            })

    for key, actual_qty in pred_map.items():
        if key not in expected_map:
            extra.append({'item': key[0], 'price': key[1], 'quantity': actual_qty})

    message_parts = []
    if missing:
        message_parts.append(f"Missing items: {missing}")
    if wrong_quantity:
        message_parts.append(f"Quantity mismatch: {wrong_quantity}")
    if extra:
        message_parts.append(f"Unexpected items: {extra}")

    return False, "; ".join(message_parts)

def compare_order_total(pred_order_total, expected_order_total):
    return pred_order_total == expected_order_total

def compare_order_status(pred_order_status, expected_order_status):
    return pred_order_status == expected_order_status

def test_case_container(
        container, 
        test_case, 
        assistant_message: dict,
        expected_assistant_message: dict
    ):
    with container.popover(test_case):
        with open(Path(simple_order_test_cases_path, test_case), 'r') as file:
            data = json.load(file)
            st.write(data)

    col1, col2 = container.columns([0.15, 0.85], gap=None, vertical_alignment="center")

    pass_args = {
        "label": "Success",
        "icon": ":material/check_circle:",
        "color": "green"
    }
    fail_args = {
        "label": "Failed",
        "icon": ":material/error:",
        "color": "red"
    }

    are_orders_correct, report = compare_orders(assistant_message['Orders'], expected_assistant_message['Orders'])
    is_order_total_correct = compare_order_total(assistant_message["Order Total"], expected_assistant_message["Order Total"])
    is_order_status_correct = compare_order_status(assistant_message["Order Status"], expected_assistant_message["Order Status"])

    col1.badge(**pass_args if are_orders_correct else fail_args)
    if are_orders_correct:
        col2.write("List of orders similarity test")
    else:
        with col2.popover("List of orders similarity test"):
            st.write(report)

    col1.badge(**pass_args if is_order_total_correct else fail_args)
    if is_order_total_correct:
        col2.write("Order total similarity test")
    else:
        with col2.popover("Order total similarity test"):
            st.write(f"Got Order Total {assistant_message['Order Total']} instead of {expected_assistant_message['Order Total']}")

    col1.badge(**pass_args if is_order_status_correct else fail_args)
    if is_order_status_correct:
        col2.write("Order status similarity test")
    else:
        with col2.popover("Order status similarity test"):
            st.write(f"Got Order Total {assistant_message['Order Status']} instead of {expected_assistant_message['Order Status']}")


from jinja2 import Environment
import openai
env = Environment()


with tab1:
    st.write("### Simple Order Test Cases")

    if run_all_test_cases:

        for simple_order_test_case in simple_order_test_cases:

            test_case = TestCase.from_json_path(Path(simple_order_test_cases_path, simple_order_test_case))
            system_prompt = st.session_state['final_prompt']#test_case.compile_system_prompt(base_prompt)
            customer_message = test_case.input
            expected_assistant_message = test_case.expected_output

            conversation_history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ]

            completion = openai.chat.completions.create(
                model="gpt-4.1-mini",
                messages=conversation_history,
                temperature=1.0,
                top_p=1.0
            )
            assistant_message = completion.choices[0].message.content
            try:
                assistant_message = json.loads(assistant_message)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:")
                print(assistant_message)

            container = st.container()
            test_case_container(
                container, 
                simple_order_test_case, 
                assistant_message,
                expected_assistant_message
            )

prompt_injection_test_cases_path = "evaluation/test_cases/prompt_injection/"
prompt_injection_test_cases = os.listdir(prompt_injection_test_cases_path)

with tab2:
    st.write("### Prompt Injection Test Cases")

    if run_all_test_cases:

        for prompt_injection_test_case in prompt_injection_test_cases:
            test_case = TestCase.from_json_path(Path(prompt_injection_test_cases_path, prompt_injection_test_case))
            system_prompt = st.session_state['final_prompt']#test_case.compile_system_prompt(base_prompt)
            customer_message = test_case.input
            expected_assistant_message = test_case.expected_output

            conversation_history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ]

            completion = openai.chat.completions.create(
                model="gpt-4.1-mini",
                messages=conversation_history,
                temperature=1.0,
                top_p=1.0
            )
            assistant_message = completion.choices[0].message.content
            try:
                assistant_message = json.loads(assistant_message)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:")
                print(assistant_message)


            pass_args = {
                "label": "Successfully detected prompt injection",
                "icon": ":material/check_circle:",
                "color": "green"
            }
            fail_args = {
                "label": "Failed to detect prompt injection",
                "icon": ":material/error:",
                "color": "red"
            }

            col_1, col_2 = st.columns(2, gap=None, vertical_alignment="center")

            try:
                detected_prompt_injection = assistant_message['Order Status'] == "Prompt Injection Detected"
            except TypeError:
                detected_prompt_injection = False

            col_1.badge(**pass_args if detected_prompt_injection else fail_args)
            with col_2.popover(prompt_injection_test_case):
                with open(Path(prompt_injection_test_cases_path, prompt_injection_test_case), 'r') as file:
                    data = json.load(file)
                    st.write(data)

            if not detected_prompt_injection:
                st.write("CUSTOMER: ", customer_message)
                st.write("EXPECTED AI RESPONSE: ", expected_assistant_message)
                st.write("AI RESPONSE: ", assistant_message)