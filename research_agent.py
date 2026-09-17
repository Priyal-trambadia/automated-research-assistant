import os
from dotenv import load_dotenv
from google import genai
from ddgs import DDGS

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)


def search_web(query):
    """Search DuckDuckGo and return results."""

    print("\n🔎 Searching DuckDuckGo...")

    results = DDGS().text(
        query,
        max_results=5
    )

    return results


def generate_answer(question, search_results):
    """Use Gemini to create an answer from search results."""

    # Convert search results into text
    research_data = ""

    for i, result in enumerate(search_results, start=1):
        research_data += f"""
Result {i}:
Title: {result.get("title")}
URL: {result.get("href")}
Description: {result.get("body")}
"""

    prompt = f"""
You are an AI research assistant.

User question:
{question}

Here are search results from DuckDuckGo:

{research_data}

Using these search results, provide a clear and useful answer.

Instructions:
- Explain in simple language.
- Use the search results as your information source.
- Mention important recent information.
- If the search results are not enough, clearly say so.
- Do not invent facts.
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text


print("🤖 Automated Research Assistant")
print("Type 'exit' to stop.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Agent: Goodbye!")
        break

    try:

        # Step 1: Search the web
        results = search_web(question)

        # Step 2: Ask Gemini to analyze results
        answer = generate_answer(question, results)

        # Step 3: Show final answer
        print("\n📝 Research Answer:\n")
        print(answer)

    except Exception as e:
        print("\n❌ Error:", e)