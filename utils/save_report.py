from datetime import datetime
import os

def save_report(response):
    output_dir = "D:\\NextCountry\\responses"

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file_path = os.path.join(output_dir, f"report_{dt_string}.md")

    # Write to file with UTF-8 encoding
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response["messages"][-1].content)
        
    print(f"Response saved to {file_path}")