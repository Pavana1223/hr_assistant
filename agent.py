import json
import os
from rapidfuzz import process, fuzz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICIES_DIR = os.path.join(BASE_DIR, "policies")

# ------------ LOAD KB FROM 3 JSON FILES ---------------- #

def load_json(file_name):
    """
    Load a JSON file from the policies folder.
    """
    file_path = os.path.join(POLICIES_DIR, file_name)
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_kb():
    """
    Loads all knowledge base files and merges them.
    """
    kb = []
    kb.extend(load_json("benefits.json"))
    kb.extend(load_json("leaves.json"))
    kb.extend(load_json("policies.json"))
    return kb


kb = load_kb()   # GLOBAL KB AVAILABLE TO ALL FUNCTIONS


# ------------ QUERY MATCHING FUNCTION ---------------- #

def find_best_match(query, top_n=2):
    """
    Finds best matching entries using fuzzy similarity.
    """

    if not kb:
        return []

    # Prepare searchable list
    search_strings = []
    index_map = {}

    for idx, entry in enumerate(kb):
        text = f"{entry['title']} {entry['text']}"
        search_strings.append(text)
        index_map[idx] = entry  # map index → original entry

    # Fuzzy match
    results = process.extract(
        query,
        search_strings,
        scorer=fuzz.WRatio,
        limit=top_n
    )

    # Results will be list of tuples: (matched_string, score, index)
    matches = []
    for match_text, score, index in results:
        entry = index_map[index]
        matches.append({
            "title": entry["title"],
            "text": entry["text"],
            "score": score
        })

    return matches


# ------------ MAIN ANSWERING FUNCTION ---------------- #

def answer_query(query):
    """
    Returns the best possible answer to a query.
    """

    matches = find_best_match(query)

    if not matches:
        return "Sorry, I don't have information on that."

    best = matches[0]

    if best["score"] < 40:     # too weak match
        return "I'm not fully sure. Could you please ask more clearly?"

    return best["text"]


# ------------ CLI ENTRY POINT ---------------- #

def cli():
    print("\nHR Assistant Agent Started!")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = answer_query(query)
        print("HR Assistant:", response)
        print()


if __name__ == "__main__":
    cli()