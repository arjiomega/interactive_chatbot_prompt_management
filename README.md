# 🤖 Prompt Engineering Playground

An interactive Streamlit demo for exploring and evaluating **prompt-based behaviors** of language models — no fine-tuning required.

---

## 🚀 Overview

This playground empowers you to:

- 🛠 **Modify the Base Prompt**  
  Tweak the core system message that shapes the model’s behavior.

- 🧾 **Edit Context (Restaurant Info & Menu)**  
  Change environment data and observe how it influences responses.

- 🎯 **Add Few-shot Examples**  
  Guide the model with your own examples to steer its behavior.

- 🧪 **Run Test Cases**  
  Evaluate the model across:
  - Normal order flows
  - Edge cases
  - Prompt-injection attacks

- 💬 **Chat with the Assistant**  
  Engage in live conversation using your configured prompt & context.

---

## 🔧 Features

- **No fine-tuning needed** — everything is demoed with prompt engineering alone.
- Supports **prompt robustness testing**, including adversarial inputs.
- Great for **researchers, developers**, and anyone interested in LLM limitations and prompt design.
- Completely **open-source** — ideal for learning or building prototypes.

---

## 📦 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/prompt-engineering-playground.git
   cd prompt-engineering-playground
   ```

2. **Install locally**
    ```bash
    pip install -e .
    ```

3. **Configure your API key**
    ```bash
    OPENAI_API_KEY=sk-...
    ```

4. **Run the app**
    ```bash
    streamlit-start
    ```