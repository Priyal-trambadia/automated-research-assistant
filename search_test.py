from ddgs import DDGS

query = "latest developments in Generative AI"

print("🔎 Searching DuckDuckGo...\n")

results = DDGS().text(
    query,
    max_results=5
)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Title:", result.get("title"))
    print("URL:", result.get("href"))
    print("Description:", result.get("body"))