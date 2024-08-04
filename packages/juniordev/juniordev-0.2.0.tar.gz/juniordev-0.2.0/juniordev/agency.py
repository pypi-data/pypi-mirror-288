from agency_swarm import Agency, set_openai_key
from .CEO import CEO
from .Copywriter import Copywriter
from .WebDeveloper import WebDeveloper
from .Designer import Designer
import os

# Prompt the user for the OpenAI API key
def get_openai_key():
    return input("Please enter your OpenAI API key: ")

# Set the API key
set_openai_key(get_openai_key())

ceo = CEO()
designer = Designer()
web_developer = WebDeveloper()
copywriter = Copywriter()

agency = Agency([ceo, designer, web_developer,
                 [ceo, designer],
                 [designer, web_developer],
                 [designer, copywriter]],
                shared_instructions='./agency_manifesto.md')



def rundemo():
    agency.run_demo()

if __name__ == '__main__':
    # agency.demo_gradio(height=400)
    agency.run_demo()