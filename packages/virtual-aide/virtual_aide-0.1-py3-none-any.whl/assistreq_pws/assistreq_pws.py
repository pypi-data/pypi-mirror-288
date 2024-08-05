import os

def set_env_vars():
    groq_api = os.getenv('GROQ_API')
    gemini_api = os.getenv('GEMINI_API')

    if not groq_api or not gemini_api:
        print("Environment variables for API keys are not set. Setting them now...")

        os.environ['GROQ_API'] = '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'
        os.environ['GEMINI_API'] = 'AIzaSyBMwqk3feRnEYm1IvdqoNHQhgk2c5Y47QE'

        print("Environment variables set successfully. Please restart the script.")

if __name__ == "__main__":
    set_env_vars()
