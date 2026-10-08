# ThinkEvolve

ThinkEvolve is an AI-powered research agent that helps users investigate, improve, and evolve startup or product ideas using real-world web evidence.

Instead of simply asking whether an idea already exists, ThinkEvolve researches how the problem is currently being solved, identifies common approaches and user problems, finds gaps and opportunities, and then helps the user develop a stronger second version of the idea.

## How It Works

User enters an idea
↓
AI understands the idea
↓
AI generates targeted research queries
↓
SerpApi searches the web
↓
AI analyzes the research evidence
↓
Existing solutions
Common approaches
User problems
Gaps & opportunities
Competition
↓
AI proposes Version 2
↓
User researches Version 2
↓
V1 vs V2 comparison

## Key Features

### AI-Powered Research

ThinkEvolve generates targeted search queries based on the user's idea and uses SerpApi to retrieve real-world web results.

### Evidence-Based Analysis

The research is organized into:

- Existing solutions
- Common approaches
- User problems
- Competition
- Gaps and opportunities

Findings are connected to the web sources used during the research.

### Idea Evolution

Rather than stopping at idea validation, ThinkEvolve uses the research to suggest a stronger Version 2 of the idea.
The user can then research the improved idea again.

### V1 vs V2 Comparison

ThinkEvolve compares the original and improved versions across:

- Differentiation
- Competitive position
- Opportunity
- Practicality

This turns startup research into an iterative process instead of a one-time validation check.

## SerpApi Usage

SerpApi is a core part of ThinkEvolve.

For each research cycle, the application:

1. Uses Gemini to understand the user's idea.
2. Generates three targeted research queries.
3. Sends those queries to SerpApi's Google Search API.
4. Collects relevant search results and snippets.
5. Passes the collected evidence to Gemini for analysis.
6. Uses the evidence to generate improvement suggestions.

SerpApi therefore provides the real-world web research layer that grounds the AI analysis in current web information.

## AI Usage

ThinkEvolve uses Google's Gemini API for:

- Generating research queries
- Analyzing collected web evidence
- Identifying gaps and opportunities
- Generating an improved Version 2 of the idea
- Comparing Version 1 and Version 2

Gemini is used for reasoning and analysis, while SerpApi provides the web search evidence.

## Tech Stack

- SerpApi
- Flask
- Google Gemini API
- Python
- HTML
- CSS
- JavaScript

## Project Structure

ThinkEvolve/
├── app.py
├── agent.py
├── requirements.txt
├── .gitignore
└── templates/
└── index.html

## Setup

1. Clone the repository

git clone https://github.com/YADHUKISHANTR/ThinkEvolve.git
cd ThinkEvolve

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Create environment variables

Create a .env file in the project root:

SERPAPI_KEY=your_serpapi_key
GEMINI_API_KEY=your_gemini_api_key

Do not commit the .env file to GitHub.

5. Run the application

python app.py

Open:

http://127.0.0.1:5000

## Example

Enter a product or startup idea such as:

A platform that helps college students find verified people travelling on the same route who can offer a spare seat.

ThinkEvolve researches existing solutions, approaches, user problems, competition, and gaps before suggesting ways to improve the idea.

## Hackathon

Built for the SerpApi India Hackathon 2026.

The project focuses on using AI agents and web search to turn startup idea research into an evidence-based iterative process.

## AI Disclosure

- **Google Gemini API:** Used in the ThinkEvolve application for generating research queries, analyzing SerpApi search results, improving ideas, and comparing Version 1 and Version 2.
- **ChatGPT:** Used during development as a coding assistant for generating, debugging, and improving parts of the project code and UI.
