#!/usr/bin/env python3
"""Test model_base_url parameter."""

from northau.archs.main_sub import create_agent


def main():
    """Test model_base_url parameter."""
    print("Testing model_base_url parameter")
    print("=" * 40)
    
    # Test with default OpenAI URL
    agent1 = create_agent(
        name="test_agent_1",
        model="gpt-4",
        model_base_url="https://api.openai.com/v1"
    )
    
    print(f"Agent 1 - Model: {agent1.model}")
    print(f"Agent 1 - Base URL: {agent1.model_base_url}")
    print(f"Agent 1 - OpenAI Client: {'Initialized' if agent1.openai_client else 'Not initialized'}")
    
    # Test with custom URL (like Ollama, local LM Studio, etc.)
    agent2 = create_agent(
        name="test_agent_2", 
        model="llama2",
        model_base_url="http://localhost:11434/v1"
    )
    
    print(f"\nAgent 2 - Model: {agent2.model}")
    print(f"Agent 2 - Base URL: {agent2.model_base_url}")
    print(f"Agent 2 - OpenAI Client: {'Initialized' if agent2.openai_client else 'Not initialized'}")
    
    # Test without base URL (default)
    agent3 = create_agent(
        name="test_agent_3",
        model="gpt-3.5-turbo"
    )
    
    print(f"\nAgent 3 - Model: {agent3.model}")
    print(f"Agent 3 - Base URL: {agent3.model_base_url}")
    print(f"Agent 3 - OpenAI Client: {'Initialized' if agent3.openai_client else 'Not initialized'}")
    
    print("\n✓ model_base_url parameter test completed!")


if __name__ == "__main__":
    main()