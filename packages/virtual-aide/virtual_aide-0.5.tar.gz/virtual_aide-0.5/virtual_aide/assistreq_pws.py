import os

def set_env_vars():
    groq_api = os.getenv('GROQ_API')
    gemini_api = os.getenv('GEMINI_API')
    model_name = os.getenv('MODEL_NAME')
    env_vars_set = True
    

    if not groq_api:
        os.environ['GROQ_API'] = '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'
        env_vars_set = False
    if not gemini_api:
        os.environ['GEMINI_API'] = 'AIzaSyBMwqk3feRnEYm1IvdqoNHQhgk2c5Y47QE'
        env_vars_set = False
    if not model_name:
        os.environ['MODEL_NAME'] = "aura-athena-en"
        env_vars_set = False

    if not env_vars_set:
        print("Environment variables set successfully. Restarting the script...")
    
    return model_name , groq_api , gemini_api


if __name__ == "__main__":
    set_env_vars()
