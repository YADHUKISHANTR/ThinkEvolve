import os
from dotenv import load_dotenv
from google import genai
import serpapi

load_dotenv()

# -----------------------------
# API CLIENTS
# -----------------------------

# Gemini
gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# SerpApi
serp = serpapi.Client(
    api_key=os.getenv("SERPAPI_KEY")
)


# -----------------------------
# GEMINI: GENERATE RESEARCH QUERIES
# -----------------------------

def generate_queries(idea):

    prompt = f"""
You are a web research query generator.

Your task is to turn the USER IDEA into exactly 3 highly targeted Google
search queries for product and market research.

USER IDEA:
{idea}

First understand:
- who the target users are
- what problem they have
- what the proposed solution does
- the important domain or use case

Then create these EXACTLY THREE searches:

SEARCH 1 — EXISTING SOLUTIONS
Find real products, apps, companies, platforms, or projects that solve the
same or a very similar problem for the same or similar users.

SEARCH 2 — USER PROBLEMS
Find real complaints, reviews, discussions, limitations, frustrations,
or missing features related to existing solutions for this specific problem.

SEARCH 3 — ALTERNATIVES AND GAPS
Find alternative ways users currently solve this problem and evidence about
limitations, unmet needs, or weaknesses in those alternatives.

QUERY REQUIREMENTS:

- Every query MUST contain important keywords from the USER IDEA.
- Make the queries specific to the actual problem and target users.
- Use natural Google search wording.
- Do NOT use generic queries such as "market trends", "market size",
  "industry analysis", or "future of".
- Do NOT search for how to build the product.
- Do NOT restrict searches to one website such as Reddit.
- Do NOT use "colleagues" unless the USER IDEA specifically concerns colleagues.
- Each query must have a different research purpose.
- Prefer queries likely to return real-world evidence.
- Keep each query concise.

Before returning the queries, mentally check:
1. Does Query 1 find existing competitors?
2. Does Query 2 find actual user problems?
3. Does Query 3 find alternatives and gaps?
4. Are all three clearly related to the USER IDEA?

Return ONLY the 3 queries.

One query per line.
No numbering.
No explanations.
"""

    response = gemini.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    queries = response.text.strip().split("\n")

    return [query.strip() for query in queries if query.strip()][:3]

# -----------------------------
# SERPAPI: SEARCH THE WEB
# -----------------------------

def search_web(query):
    try:
        results = serp.search({
            "engine": "google",
            "q": query
        })

        clean_results = []

        for result in results.get("organic_results", []):
            clean_results.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet")
            })

        return clean_results

    except Exception as e:
        print("Search failed:", e)
        return []


# -----------------------------
# GEMINI: ANALYZE RESEARCH
# -----------------------------

def analyze_results(idea, research_results):

    prompt = f"""
You are an expert product research analyst.

USER IDEA:
{idea}

WEB RESEARCH RESULTS:
{research_results}

Each research result contains a unique source_id.
Use those source_ids to identify the exact source supporting each finding.

Analyze the research and return the result as JSON.

Use exactly this structure:

{{
    "existing_solutions": [
        {{
            "name": "Name of solution",
            "description": "What it does and how it relates to the user's idea.",
            "source_id": 1
        }}
    ],

    "common_approaches": [
        {{
            "text": "Description of the common approach.",
            "source_id": 1
        }}
    ],

    "user_problems": [
        {{
            "text": "Specific user problem or complaint.",
            "source_id": 1
        }}
    ],

    "competition": {{
        "level": "Low / Moderate / High",
        "summary": "Short explanation of how crowded the space appears.",
        "source_id": 1
    }},

    "gaps_opportunities": [
        {{
            "text": "Gap or opportunity identified from the research.",
            "source_id": 1
        }}
    ],

    "idea_improvements": [
        "Specific improvement 1",
        "Specific improvement 2",
        "Specific improvement 3"
    ]
}}

IMPORTANT RULES:

- Every source_id MUST exactly match a source_id from the WEB RESEARCH RESULTS.
- Use the SINGLE most relevant source for each finding.
- Do NOT assign multiple source IDs to one finding.
- Do not invent source IDs.
- Do not invent companies, products, statistics, complaints, or facts.
- Base factual claims on the provided web research.
- If evidence is weak or unclear, say so.
- Only assign a source_id when the research actually supports the finding.
- The idea improvements can be your own analytical recommendations.
- Idea improvements do not require a source_id.
- Keep each item concise and useful.
- Do not treat your own assumptions as evidence.
- Return ONLY valid JSON.
- Do not use markdown.
"""

    try:
        response = gemini.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

    except Exception as e:
        print("Gemini query generation failed:", e)
        return []

    return response.text

def improve_idea(idea, analysis, sources):

    prompt = f"""
You are helping a startup founder improve an idea based on web research.

ORIGINAL IDEA:
{idea}

RESEARCH ANALYSIS:
{analysis}

WEB SOURCES:
{sources}

Create a stronger Version 2 of the original idea.

The improved idea should:
- Keep the core problem and intent of the original idea.
- Address important problems discovered in the research.
- Use identified gaps or opportunities.
- Be meaningfully more differentiated.
- Remain realistic and buildable.
- Do not invent facts that are not supported by the research.

Return ONLY valid JSON in exactly this structure:

{{
    "version_2": "A clear description of the improved idea",
    "changes": [
        "Specific change made",
        "Specific change made"
    ],
    "why_better": [
        "Why this change improves the idea",
        "Why this change improves the idea"
    ]
}}
"""

    try:
        response = gemini.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini Version 2 generation failed:", e)
        return None
# -----------------------------
# MAIN PROGRAM
# -----------------------------

if __name__ == "__main__":

    idea = """
    An app that connects college students who travel along the same route
    so they can share rides and reduce transportation costs.
    """

    # Step 1: Generate research queries
    queries = generate_queries(idea)

    print("\n" + "=" * 60)
    print("GENERATED RESEARCH QUERIES")
    print("=" * 60)

    for query in queries:
        print("-", query)

    # Step 2: Search the web
    print("\n" + "=" * 60)
    print("SEARCHING WEB")
    print("=" * 60)

    all_results = []

    for query in queries:

        print("\nSEARCH:", query)

        results = search_web(query)

        if not results:
            print("No results returned.")

        for result in results[:5]:
            print(result)

        all_results.extend(results[:5])

    # Step 3: Analyze results
    print("\n" + "=" * 60)
    print("ANALYZING RESEARCH")
    print("=" * 60)

    if all_results:

        analysis = analyze_results(
            idea,
            all_results
        )

        print("\n" + analysis)

    else:

        print("No research results available for analysis.")

def compare_ideas(
    original_idea,
    original_analysis,
    version2_idea,
    version2_analysis
):

    prompt = f"""
You are an expert startup/product strategist.

VERSION 1 IDEA:
{original_idea}

VERSION 1 RESEARCH:
{original_analysis}

VERSION 2 IDEA:
{version2_idea}

VERSION 2 RESEARCH:
{version2_analysis}

Compare Version 1 and Version 2 based ONLY on the provided research.

Return ONLY valid JSON using exactly this structure:

{{
    "differentiation": {{
        "score": 1,
        "summary": "Short explanation."
    }},

    "competition": {{
        "score": 1,
        "summary": "Short explanation."
    }},

    "opportunity": {{
        "score": 1,
        "summary": "Short explanation."
    }},

    "practicality": {{
        "score": 1,
        "summary": "Short explanation."
    }},

    "overall": {{
        "winner": "Version 1 or Version 2",
        "summary": "Short explanation of which version is stronger and why."
    }},

    "key_change": "The single most important difference between Version 1 and Version 2."
}}

SCORING:

Use scores from 1 to 10.

For DIFFERENTIATION:
Higher = more distinct from existing solutions.

For COMPETITION:
Higher = better position / less direct competition.

For OPPORTUNITY:
Higher = stronger opportunity based on identified gaps.

For PRACTICALITY:
Higher = easier and more realistic to build and operate.

IMPORTANT:

- Do not invent market facts.
- Do not claim success is guaranteed.
- Base the comparison on the supplied research.
- Version 2 should not automatically win.
- If Version 1 is stronger in an area, give Version 1 the advantage.
- Return ONLY valid JSON.
"""

    response = gemini.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return response.text