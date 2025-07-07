import os
import streamlit as st
from interactive_chatbot_demo.intialize import initialize_if_empty

initialize_if_empty()     

st.set_page_config(
    page_title="Prompt Engineering Demo",
    page_icon="🤖",
)

st.title("🤖 Prompt Engineering Playground")

st.sidebar.success("👈 Select a demo page to begin")

st.markdown(
    """
Welcome to the **Prompt Engineering Playground**!  
This interactive app is designed to help you **explore, experiment, and evaluate** prompt-based behaviors of language models — without any fine-tuning involved.

---

### 🛠 What You Can Do Here

- 🔧 **Modify the Base Prompt**  
Play around with the core system message that guides the model’s behavior.

- 🧾 **Edit the Context (Restaurant Info & Menu)**  
Change the environment and see how the model adapts its response.

- 🎯 **Add Fewshot Examples**  
Inject custom examples to steer the model's behavior through few-shot learning.

- 🧪 **Run Test Cases**  
View how the model performs under various customer queries, including:
    - Normal ordering scenarios
    - Edge cases
    - Prompt injection attempts (and how well they’re handled)

- 💬 **Chat with the Assistant**  
Try out your configuration in real-time with a simulated chatbot interface.

---

### 🚫 No Fine-Tuning Required

This app demonstrates the **power of prompt engineering** alone — no model retraining, fine-tuning, or API-level customization needed.

---

### 🤓 For Developers & Researchers

Great for:
- Testing prompt robustness
- Understanding LLM limitations
- Designing resilient chatbot interfaces
- Evaluating few-shot effectiveness

---

👈 **Select a page from the sidebar** to begin your exploration.

---
🔗 **[View the Source Code on GitHub](https://github.com/arjiomega/interactive_chatbot_prompt_management)**  
Explore the full implementation, contribute, or dive deeper into the codebase.
"""
)