from google import genai
import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GEMINI_API_KEY")

model="gemini-2.0-flash"
client = genai.Client(api_key=API_KEY)

class AICaller:
    """a class that will call gemini's API to make tasks and task_lists"""

    @staticmethod
    def make_AI_tasklist(input_prompt:str) -> str:
        """
        Gets a json output from google gemini to make a new task list
        input:
            input_prompt: the prompt from the user to base the list on
        output:
            a string containing the json for the task_list
        """

        cur_time = datetime.datetime.now()
        prompt = f"""
        You are an assistant that makes lists of task for a user to meet goals and track schedules
        reply to the prompt with the needed task list in this json schema but output it as text
        (be very sure not to have ANY extra formating):
        [
        {{
            "title": "task1 title",
            "date": "suggested date for the task",
            "time": "suggested time for the task",
            "description": "description for the task",
            "priority": "integer (in a string) for priority 1=highest 5=lowest"
        }},
        {{
            "title": "task1 title",
            "date": "suggested date for the task",
            "time": "suggested time for the task",
            "description": "description for the task",
            "priority": "integer (in a string) for priority 1=highest 5=lowest"
        }}
        ]
        the current time is : {cur_time}

        user prompt:
        {input_prompt}
        """

        print("Waiting for AI response")
        response = client.models.generate_content(
        model=model,
        contents=prompt,)
        print("Response recieved")

        print(response.text)
        return response.text

    @staticmethod
    def make_AI_task(input_prompt:str) -> str:
        """
        Gets a json output from google gemini to make a new task
        input:
            input_prompt: the prompt from the user to base the task on
        output:
            a string containing the json for the task
        """

        cur_time = datetime.datetime.now()
        prompt = f"""
        You are an assistant that adds tasks to a users running list, which is in json
        what you reply will be appended to the file holding the tasks
        reply to the prompt with the needed task in this json schema but output it as text
        (be very sure not to have ANY extra formating):
        {{
            "title": "task1 title",
            "date": "suggested date for the task",
            "time": "suggested time for the task",
            "description": "description for the task",
            "priority": "integer (in a string) for priority 1=highest 5=lowest"
        }},
        
        
        the current time is : {cur_time}

        user prompt:
        {input_prompt}
        """

        print("Waiting for AI response")
        response = client.models.generate_content(
        model=model,
        contents=prompt,)
        print("Response recieved")

        print(response.text)
        return response.text



