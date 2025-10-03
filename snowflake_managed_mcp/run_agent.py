from example_mcp_crew.crew import create_crew
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    user_question = input("Ask your data question: ")
    crew = create_crew()
    result = crew.kickoff(inputs={"message": user_question})
    print("\nAnswer:\n", result)
