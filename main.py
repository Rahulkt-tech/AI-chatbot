from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

@tool
def calculator(a: float, b: float) ->str:
    """Adds two numbers and returns the result as a string."""
    return str(a + b)

def main():
    load_dotenv()  # ✅ loads OPENAI_API_KEY from .env

    model = ChatOpenAI(temperature=0)

    tools = [calculator]
    agent_executor = create_react_agent(model, tools)

    print("Welcome to the React Agent. Type 'exit' to quit.")
    print("You can ask questions or give commands.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Exiting the React Agent. Goodbye!")
            break

        print("\nAgent: ", end="")

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

        print()

if __name__ == "__main__":
    main()
