def main():
    import subprocess
    process = subprocess.Popen(["streamlit", "run", 'src/interactive_chatbot_demo/demo_introduction.py'])

if __name__ == "__main__":
    main()
