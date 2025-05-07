from agent_utils.prompt import parser
from state import NC_AgentResponse
from datetime import datetime

def save_report(raw_response):
    # 1. Try parsing the response
    try:
        structured_response = parser.parse(raw_response["output"])
    except Exception as e:
        print(f"Error parsing response: {e}")
        structured_response = None

    # 2. Print the JSON (optional)
    print(structured_response.model_dump_json(indent=4))

    # 3. Convert to dictionary
    if structured_response:
        data = structured_response.model_dump()

        # 4. Generate Markdown text
        md = f"# {data['topic']}\n\n"
        md += f"## Summary\n{data['summary']}\n\n"
        md += f"## User Profile Summary\n{data['user_profile_summary']}\n\n"

        md += "## Suitable Countries with Score\n"
        for item in data['suitable_countries_with_score']:
            md += f"- {item}\n"
        md += "\n"

        md += "## Suitable Universities with Score\n"
        for item in data['suitable_universities_with_score']:
            md += f"- {item}\n"
        md += "\n"

        md += "## Scholarship Opportunities\n"
        for item in data['scholarship_opportunities']:
            md += f"- {item}\n"
        md += "\n"

        md += "## University Details\n"
        for item in data['university_details']:
            md += f"- {item}\n"
        md += "\n"

        md += f"## Reasoning\n{data['reasoning']}\n\n"

        md += "## Pros\n"
        for item in data['pros']:
            md += f"- {item}\n"
        md += "\n"

        md += "## Cons\n"
        for item in data['cons']:
            md += f"- {item}\n"
        md += "\n"

        md += f"## Suggestions\n{data['suggestions']}\n\n"

        md += "## Sources\n"
        for item in data['sources']:
            md += f"- {item}\n"
        md += "\n"

        md += "## Tools Used\n"
        for item in data['tools_used']:
            md += f"- {item}\n"
        md += "\n"

        # 5. Write to file
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"report_{time}.md", "w", encoding="utf-8") as f:
            f.write(md)

        print(f"✅ Markdown file saved as report_{time}.md")
    else:
        print("❌ Could not generate markdown. Structured response is None.")

