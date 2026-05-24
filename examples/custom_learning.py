# Example: Custom Learning Tasks
from agent_learning import LearningAgent

def example_custom_learning():
    """Run agent learning on custom tasks."""
    agent = LearningAgent(name="custom-learner")

    # Custom task
    result = agent.solve("Find the shortest path in a graph with 100 nodes", max_rounds=5)

    # Reflect
    agent.reflect()

    print(f"Best strategy: {result['best_strategy']}")
    print(f"Performance trend: {agent.performance_trend()}")

if __name__ == "__main__":
    example_custom_learning()
