import os
from app.prompts import *
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

#change classname to some sort of teacher
class IndianCuisineExpertChat(Command):
    def __init__(self):
        super().__init__()
        #change this to some sort of teacher
        self.name = "foods"
        #change this to explain what the agent(teacher does)
        self.description = "Interact with a Indian Cuisine Expert AI to learn about different foods from India."
        self.history = []
        load_dotenv()
        API_KEY = os.getenv('OPENAI_API_KEY')
        # you can try GPT4 but it costs a lot more money than the default 3.5
        # self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-4-0125-preview")  # Initialize once and reuse
        self.llm = ChatOpenAI(openai_api_key=API_KEY)  # Initialize once and reuse

    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text) + text.count(' ')

    def interact_with_ai(self, user_input, character_name):
        # Generate a more conversational and focused prompt
        prompt_text = prompt1
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used

    def execute(self, *args, **kwargs):
        #change these bottom two lines
        character_name = kwargs.get("character_name", "Indian Cuisine Expert")
        print(f"Welcome to the Indian Cuisine Expert Chat! Let's talk about Indian Foods! Ask a question to get started.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Thank you for using the Indian Cuisine Expert Chat. Goodbye!")
                break

            self.history.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Indian Cuisine Expert: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.history.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")

