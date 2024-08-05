import os

def set_env_vars():
    groq_api = os.getenv('GROQ_API')
    gemini_api = os.getenv('GEMINI_API')
    model_name = os.getenv('MODEL_NAME')

    if not groq_api:
        os.environ['GROQ_API'] = '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'
        
    if not gemini_api:
        os.environ['GEMINI_API'] = 'AIzaSyBMwqk3feRnEYm1IvdqoNHQhgk2c5Y47QE'
        
    if not model_name:
        os.environ['MODEL_NAME'] = "aura-athena-en"
        
if __name__ == "__main__":
    set_env_vars()
