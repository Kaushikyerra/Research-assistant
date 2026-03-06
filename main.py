from agent_graph import app
from langchain_core.messages import HumanMessage

def main():
    print("Starting Scientific Agent...")
    
    # specialized problem input
    user_input = "How can we optimize battery life in extreme cold temperatures?"
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "research_data": "",
        "hypothesis": "",
        "critique": ""
    }
    
    # Run the graph
    final_hypothesis = ""
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"Finished Node: {key}")
            if "hypothesis" in value:
                final_hypothesis = value["hypothesis"]
            # print(f"Output: {value}")
            print("-" * 20)

    print("Agent execution finished.\n")
    print("=" * 60)
    print("FINAL STRUCTURED OUTPUT")
    print("=" * 60)
    print(final_hypothesis)

if __name__ == "__main__":
    main()
