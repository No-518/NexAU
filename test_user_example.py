#!/usr/bin/env python3
"""Test the exact configuration from the user's request."""

from northau.archs.main_sub import create_agent
from northau.archs.llm import LLMConfig


def test_user_example():
    """Test the exact configuration requested by the user."""
    print("Testing user's exact configuration")
    print("=" * 50)
    
    # Create the exact configuration from user's request
    llm_config = LLMConfig(
        base_url="https://***REMOVED***/v1/",
        model="***REMOVED***",
        api_key="***REMOVED***",
        temperature=0.6,
        max_tokens=8192
    )
    
    print("LLM Configuration:")
    print(f"  Model: {llm_config.model}")
    print(f"  Base URL: {llm_config.base_url}")
    print(f"  API Key: {llm_config.api_key}")
    print(f"  Temperature: {llm_config.temperature}")
    print(f"  Max Tokens: {llm_config.max_tokens}")
    
    # Create agent with this configuration
    agent = create_agent(
        name="user_example_agent",
        llm_config=llm_config
    )
    
    print(f"\nAgent created successfully:")
    print(f"  Name: {agent.name}")
    print(f"  LLM Config: {agent.llm_config}")
    print(f"  OpenAI Client: {'Initialized' if agent.openai_client else 'Not initialized'}")
    
    # Test parameter conversion
    print(f"\nOpenAI API Parameters:")
    api_params = llm_config.to_openai_params()
    for key, value in api_params.items():
        print(f"  {key}: {value}")
    
    print(f"\nClient Initialization Parameters:")
    client_kwargs = llm_config.to_client_kwargs()
    for key, value in client_kwargs.items():
        print(f"  {key}: {value}")
    
    # Test using dictionary method
    print(f"\n" + "=" * 30)
    print("Testing dictionary method:")
    
    agent2 = create_agent(
        name="user_example_agent_2",
        llm_config={
            "base_url": "https://***REMOVED***/v1/",
            "model": "***REMOVED***",
            "api_key": "***REMOVED***",
            "temperature": 0.6,
            "max_tokens": 8192
        }
    )
    
    print(f"Agent 2 LLM Config: {agent2.llm_config}")
    
    # Test backward compatibility method
    print(f"\n" + "=" * 30)
    print("Testing backward compatibility:")
    
    agent3 = create_agent(
        name="user_example_agent_3",
        model="***REMOVED***",
        model_base_url="https://***REMOVED***/v1/",
        api_key="***REMOVED***",
        temperature=0.6,
        max_tokens=8192
    )
    
    print(f"Agent 3 LLM Config: {agent3.llm_config}")


def main():
    """Run the test."""
    try:
        test_user_example()
        print("\n" + "=" * 50)
        print("✓ User example configuration test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)