def main():
    import subprocess
    process = subprocess.Popen(["streamlit", "run", 'src/interactive_chatbot_demo/demo_introduction.py'])

    # Import and show your pages or sidebar router logic here
    # e.g., from .pages import demo_introduction; demo_introduction.show()

if __name__ == "__main__":
    main()
