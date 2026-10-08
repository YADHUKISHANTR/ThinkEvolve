import json

from flask import Flask, request, render_template

from agent import (
    generate_queries,
    search_web,
    analyze_results,
    improve_idea,
    compare_ideas
)


app = Flask(__name__)


def research_idea(idea):

    queries = generate_queries(idea)

    all_results = []

    for query in queries:

        results = search_web(query)

        for result in results[:5]:

            result["query"] = query
            result["source_id"] = len(all_results) + 1

            all_results.append(result)

    if not all_results:
        return None, []

    analysis_text = analyze_results(
        idea,
        all_results
    )

    try:

        analysis = json.loads(analysis_text)

    except json.JSONDecodeError:

        analysis = {
            "error": "The AI returned an invalid research result."
        }

    return analysis, all_results


@app.route("/", methods=["GET", "POST"])
def home():

    analysis = None
    sources = []

    idea = ""

    improved_idea = None

    v2_analysis = None
    v2_sources = []
    v2_idea = ""
    comparison = None

    if request.method == "POST":

        action = request.form.get("action", "research")

        # --------------------------------
        # RESEARCH ORIGINAL IDEA
        # --------------------------------

        if action == "research":

            idea = request.form.get("idea", "").strip()

            if idea:

                analysis, sources = research_idea(idea)

                if analysis and "error" not in analysis:

                    improved_text = improve_idea(
                        idea,
                        analysis,
                        sources
                    )

                    try:

                        improved_idea = json.loads(
                            improved_text
                        )

                    except json.JSONDecodeError:

                        improved_idea = None

        # --------------------------------
        # RESEARCH VERSION 2
        # --------------------------------

        elif action == "research_v2":

            idea = request.form.get("original_idea", "").strip()

            v2_idea = request.form.get("version2", "").strip()

            # Reconstruct the original analysis
            # from the hidden form data

            original_analysis = request.form.get(
                "original_analysis",
                ""
            )

            original_sources = request.form.get(
                "original_sources",
                ""
            )

            if original_analysis:

                try:

                    analysis = json.loads(
                        original_analysis
                    )

                except json.JSONDecodeError:

                    analysis = None

            if original_sources:

                try:

                    sources = json.loads(
                        original_sources
                    )

                except json.JSONDecodeError:

                    sources = []

            if v2_idea:

                v2_analysis, v2_sources = research_idea(
                    v2_idea
                )

                if (
                    analysis
                    and "error" not in analysis
                    and v2_analysis
                    and "error" not in v2_analysis
                ):

                    comparison_text = compare_ideas(
                        idea,
                        analysis,
                        v2_idea,
                        v2_analysis
                    )

                    try:

                        comparison = json.loads(
                            comparison_text
                        )

                    except json.JSONDecodeError:

                        comparison = None

    return render_template(
    "index.html",

    analysis=analysis,
    sources=sources,

    idea=idea,

    improved_idea=improved_idea,

    v2_analysis=v2_analysis,
    v2_sources=v2_sources,
    v2_idea=v2_idea,

    comparison=comparison
)


if __name__ == "__main__":
    app.run(debug=True)