from datetime import datetime
import os
from langchain_core.messages import AIMessage, HumanMessage



def save_report(response):
    output_dir = "./responses"

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file_path = os.path.join(output_dir, f"report_{dt_string}.md")

    # Write to file with UTF-8 encoding
    with open(file_path, "w", encoding="utf-8") as f:
        # f.write(response["messages"][-1].content)
        msgs = [m for m in response["messages"] if isinstance(m, AIMessage)]
        for msg in msgs:
            f.write(msg.content)  # Add double newline for separation
            
    # Print confirmation message
    print(f"Response saved to {file_path}")