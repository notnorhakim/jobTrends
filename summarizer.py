import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key from the environment variable
api_key = os.environ.get("API_KEY")

if not api_key:
    print("API key is missing. Please set it in the .env file.")
    exit()

openai.api_key = api_key


def summarize(prompt):
    """Summarize job listings into requirements and skills."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": (
                        "Categorize the following information from the job listings into two parts: requirements and skills. "
                        "Extract details related to degrees, certifications, experience under requirements. "
                        "Look for technical skills such as programming languages, tools, and software under skills. "
                        "Provide a concise summary in bullet points for each category. "
                        "If a section doesn't have relevant information, leave it empty."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"


def sort_by_trend(prompt):
    """Sort job listings requirements and skills by trend."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data-driven assistant."},
                {
                    "role": "user",
                    "content": (
                        "You will receive summarized listings of different jobs in 2 categories: requirements and skills. "
                        "Sort both skills and requirements from the most in-demand to the least. "
                        "Provide two lists of the top 10 most in-demand skills and requirements, with no extra formatting."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    while True:
        text = input("\nEnter the text to summarize (type 'exit' to quit): ")
        if text.lower() in ["exit", "quit"]:
            break
        
        summary = summarize(text)
        print("\n📄 Summary:\n", summary)

        trend = sort_by_trend(text)
        print("\n📊 Trending Skills/Requirements:\n", trend)
