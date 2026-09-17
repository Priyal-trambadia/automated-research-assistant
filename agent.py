import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

print("🤖 My First AI Agent")
print("Type 'exit' to stop.")

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Agent: Goodbye!")
        break

    try:
        # Use the new Interactions API
        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=question
        )

        print("\nAgent:", response.output_text)

    except Exception as e:
        print("\n❌ Error:", e)















# import os
# from dotenv import load_dotenv
# from google import genai

# # Load environment variables
# load_dotenv()

# # Get Gemini API key
# api_key = os.getenv("GEMINI_API_KEY")

# # Check API key
# if not api_key:
#     print("❌ GEMINI_API_KEY not found in .env file")
#     exit()

# # Create Gemini client
# client = genai.Client(api_key=api_key)

# print("🤖 My First AI Agent")
# print("Type 'exit' to stop.")

# while True:
#     question = input("\nYou: ")

#     if question.lower() == "exit":
#         print("Agent: Goodbye!")
#         break

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=question
#     )

#     print("\nAgent:", response.text)








# import os
# from crewai import Agent, Task, Crew, Process
# from langchain_community.tools import DuckDuckGoSearchRun

# # 1. SET UP YOUR API KEY
# # Replace 'your-api-key-here' with your actual OpenAI key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

# # 2. DEFINE THE TOOL
# # This allows the agent to search the internet
# search_tool = DuckDuckGoSearchRun()

# # 3. CREATE THE AGENT
# # An agent is defined by its Role, its Goal, and its Backstory
# researcher = Agent(
#     role='Senior Research Analyst',
#     goal='Uncover cutting-edge developments in {topic}',
#     backstory="""You are an expert researcher. You are skilled at 
#     finding the most relevant information and summarizing it 
#     concisely for busy professionals.""",
#     tools=[search_tool],
#     verbose=True, # This lets you see the agent's "thoughts" in the terminal
#     allow_delegation=False
# )

# # 4. DEFINE THE TASK
# # A task is a specific assignment for the agent
# research_task = Task(
#     description="""Search the internet to find the latest news and 
#     breakthroughs regarding {topic}. Provide a detailed summary 
#     of the top 3 most important findings.""",
#     expected_output="A 3-paragraph summary report formatted in Markdown.",
#     agent=researcher
# )

# # 5. ASSEMBLE THE CREW
# # The Crew is what actually executes the work
# my_first_crew = Crew(
#     agents=[researcher],
#     tasks=[research_task],
#     process=Process.sequential # Tasks are done one after another
# )

# # 6. KICKOFF THE PROCESS
# print("### Starting the Research Agent ###")
# result = my_first_crew.kickoff(inputs={'topic': 'SpaceX Starship progress 2024'})

# print("\n\n########################")
# print("## FINAL REPORT ##")
# print("########################\n")
# print(result)
