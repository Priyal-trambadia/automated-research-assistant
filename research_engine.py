import os
from dotenv import load_dotenv
from google import genai
from ddgs import DDGS


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ==========================================
# DECIDE WHETHER SEARCH IS NEEDED
# ==========================================

def should_search(question):

    question_lower = question.lower().strip()

    # Current information keywords
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

    for keyword in search_keywords:

        if keyword in question_lower:
            return "SEARCH"


    # General educational questions
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

    for pattern in no_search_patterns:

        if question_lower.startswith(pattern):
            return "NO_SEARCH"


    # Ask Gemini for unclear questions
    prompt = f"""
You are a search decision system.

User question:
{question}

Decide whether this question requires CURRENT information from the internet.

Return ONLY:

SEARCH

or

NO_SEARCH

Use SEARCH when:
- Current information is required.
- Latest information is requested.
- News or updates are requested.
- Information may have changed recently.

Use NO_SEARCH for:
- General knowledge.
- Educational explanations.
- Basic programming concepts.
- Definitions.
- Concepts that do not require current information.
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    decision = response.output_text.strip().upper()

    if decision == "SEARCH":
        return "SEARCH"

    return "NO_SEARCH"


# ==========================================
# WEB SEARCH
# ==========================================

def search_web(query):

    results = DDGS().text(
        query,
        max_results=5
    )

    return list(results)


# ==========================================
# REMOVE DUPLICATES
# ==========================================

def clean_results(results):

    unique_results = []
    seen_urls = set()

    for result in results:

        url = result.get("href")

        if url and url not in seen_urls:

            seen_urls.add(url)
            unique_results.append(result)

    return unique_results


# ==========================================
# PREPARE RESEARCH DATA
# ==========================================

def prepare_research_data(results):

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
# GENERATE ANSWER
# ==========================================

def generate_answer(question, search_results=None):

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

Answer the user's question using the research results.

Rules:

1. Explain clearly.
2. Use simple language.
3. Use the provided sources.
4. Do not invent facts.
5. Do not invent sources.
6. If information is insufficient, say so.
7. Add [Source 1], [Source 2], etc. after important claims.
"""

    else:

        prompt = f"""
You are a helpful AI assistant.

User question:
{question}

Answer directly.

Use simple and clear language.
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text


# ==========================================
# MAIN RESEARCH FUNCTION
# ==========================================

def research_question(question):

    # Step 1
    decision = should_search(question)

    # Step 2
    if decision == "SEARCH":

        results = search_web(question)

        results = clean_results(results)

        # Step 3
        answer = generate_answer(
            question,
            results
        )

        return {
            "decision": decision,
            "answer": answer,
            "sources": results
        }

    else:

        answer = generate_answer(question)

        return {
            "decision": decision,
            "answer": answer,
            "sources": []
        }