import os
from dotenv import load_dotenv
from google import genai
from ddgs import DDGS


# ==========================================
# 1. LOAD GEMINI API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

client = genai.Client(api_key=api_key)


# ==========================================
# 2. DECIDE WHETHER WEB SEARCH IS NEEDED
# ==========================================

def should_search(question):
    """Decide whether the question needs web search."""

    question_lower = question.lower().strip()

    # --------------------------------------
    # Questions that need current information
    # --------------------------------------

    search_keywords = [
        "latest",
        "recent",
        "today",
        "this week",
        "this month",
        "current",
        "news",
        "update",
        "updates",
        "new release",
        "released",
        "price",
        "prices",
        "2026",
        "yesterday",
        "tomorrow",
        "this year"
    ]

    # Check for current-information keywords
    for keyword in search_keywords:

        if keyword in question_lower:
            return "SEARCH"


    # --------------------------------------
    # General educational questions
    # --------------------------------------

    no_search_patterns = [
        "what is",
        "what are",
        "who is",
        "who are",
        "what does",
        "what do",
        "explain",
        "define",
        "meaning of",
        "difference between",
        "how does",
        "how do",
        "why is",
        "why are"
    ]

    # These questions normally don't need web search
    for pattern in no_search_patterns:

        if question_lower.startswith(pattern):
            return "NO_SEARCH"


    # --------------------------------------
    # If unclear, ask Gemini
    # --------------------------------------

    prompt = f"""
You are a search decision system.

User question:
{question}

Decide whether this question requires CURRENT information from the internet.

Return ONLY one of these two words:

SEARCH

or

NO_SEARCH

Rules:

SEARCH:
- Current information is required.
- Latest news or updates are requested.
- Information may have changed recently.
- Current prices, releases, events, or versions are requested.

NO_SEARCH:
- General knowledge.
- Educational explanations.
- Basic programming concepts.
- Definitions.
- Concepts that do not require current information.

Do not return anything except SEARCH or NO_SEARCH.
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    decision = response.output_text.strip().upper()

    # --------------------------------------
    # IMPORTANT:
    # Exact comparison
    # --------------------------------------

    if decision == "SEARCH":
        return "SEARCH"

    return "NO_SEARCH"


# ==========================================
# 3. SEARCH DUCKDUCKGO
# ==========================================

def search_web(query):
    """Search the web using DuckDuckGo."""

    print("\n🔎 Searching DuckDuckGo...")

    results = DDGS().text(
        query,
        max_results=5
    )

    return list(results)


# ==========================================
# 4. REMOVE DUPLICATE SOURCES
# ==========================================

def clean_results(results):
    """Remove duplicate URLs."""

    unique_results = []
    seen_urls = set()

    for result in results:

        url = result.get("href")

        if url and url not in seen_urls:

            seen_urls.add(url)

            unique_results.append(result)

    return unique_results


# ==========================================
# 5. PREPARE RESEARCH DATA
# ==========================================

def prepare_research_data(results):
    """Convert search results into clean text."""

    research_data = ""

    for i, result in enumerate(results, start=1):

        title = result.get(
            "title",
            "No title"
        )

        url = result.get(
            "href",
            "No URL"
        )

        description = result.get(
            "body",
            "No description"
        )

        research_data += f"""
SOURCE {i}

Title: {title}

URL: {url}

Description:
{description}

--------------------------------
"""

    return research_data


# ==========================================
# 6. GENERATE FINAL ANSWER
# ==========================================

def generate_answer(question, search_results=None):
    """Generate the final answer using Gemini."""

    # --------------------------------------
    # SEARCH MODE
    # --------------------------------------

    if search_results:

        research_data = prepare_research_data(
            search_results
        )

        prompt = f"""
You are an AI research assistant.

User question:
{question}

Web research results:

{research_data}

Use the research results to answer the user's question.

Instructions:

1. Explain the answer clearly.
2. Use simple language.
3. Use information from the provided sources.
4. Do not invent facts.
5. Do not invent sources.
6. If information is insufficient, clearly say so.
7. Add [Source 1], [Source 2], etc. after important claims.
8. Keep the answer organized and easy to understand.
"""

    # --------------------------------------
    # NO SEARCH MODE
    # --------------------------------------

    else:

        prompt = f"""
You are a helpful AI assistant.

User question:
{question}

Answer the question directly.

Instructions:
- Use simple language.
- Explain clearly.
- Give examples when useful.
- Do not unnecessarily mention web research.
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text


# ==========================================
# 7. DISPLAY SOURCES
# ==========================================

def display_sources(results):
    """Display source titles and URLs."""

    if not results:
        return

    print("\n📚 Sources:\n")

    for i, result in enumerate(results, start=1):

        title = result.get(
            "title",
            "Unknown source"
        )

        url = result.get(
            "href",
            "No URL"
        )

        print(f"{i}. {title}")
        print(f"   {url}")
        print()


# ==========================================
# 8. MAIN PROGRAM
# ==========================================

print("🤖 Smart Automated Research Assistant")
print("Type 'exit' to stop.")


while True:

    question = input("\nYou: ")

    # --------------------------------------
    # Exit
    # --------------------------------------

    if question.lower().strip() == "exit":

        print("Agent: Goodbye!")

        break


    # --------------------------------------
    # Empty question
    # --------------------------------------

    if not question.strip():

        print("⚠️ Please enter a question.")

        continue


    try:

        # ----------------------------------
        # STEP 1: DECIDE
        # ----------------------------------

        decision = should_search(question)

        print(
            f"\n🤖 Agent Decision: {decision}"
        )


        # ----------------------------------
        # STEP 2: SEARCH
        # ----------------------------------

        if decision == "SEARCH":

            results = search_web(question)

            results = clean_results(results)


            # ------------------------------
            # STEP 3: GENERATE ANSWER
            # ------------------------------

            answer = generate_answer(
                question,
                results
            )


            # ------------------------------
            # STEP 4: SHOW ANSWER
            # ------------------------------

            print("\n📝 Final Answer:\n")

            print(answer)


            # ------------------------------
            # STEP 5: SHOW SOURCES
            # ------------------------------

            display_sources(results)


        # ----------------------------------
        # NO SEARCH
        # ----------------------------------

        else:

            answer = generate_answer(
                question
            )

            print("\n📝 Final Answer:\n")

            print(answer)


    except Exception as e:

        print("\n❌ Error:", e)