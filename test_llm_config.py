#!/usr/bin/env python3
"""Test the new LLM configuration system."""

from northau.archs.main_sub import create_agent
from northau.archs.llm import LLMConfig


def test_llm_config_basic():
    """Test basic LLMConfig functionality."""
    print("Testing LLMConfig basic functionality")
    print("=" * 40)
    
    # Test LLMConfig creation
    config1 = LLMConfig(
        model="gpt-4",
        base_url="https://api.openai.com/v1",
        temperature=0.8,
        max_tokens=4096
    )
    
    print(f"Config 1: {config1}")
    print(f"OpenAI params: {config1.to_openai_params()}")
    print(f"Client kwargs: {config1.to_client_kwargs()}")
    
    # Test the example from the user
    config2 = LLMConfig(
        base_url="https://***REMOVED***/v1/",
        model="***REMOVED***",
        api_key="***REMOVED***",
        temperature=0.6,
        max_tokens=8192
    )
    
    print(f"\nConfig 2: {config2}")
    print(f"OpenAI params: {config2.to_openai_params()}")
    print(f"Client kwargs: {config2.to_client_kwargs()}")


def test_agent_with_llm_config():
    """Test agent creation with LLMConfig."""
    print("\nTesting Agent with LLMConfig")
    print("=" * 40)
    
    # Test with LLMConfig object
    llm_config = LLMConfig(
        model="gpt-4",
        base_url="https://api.openai.com/v1",
        temperature=0.7,
        max_tokens=4096
    )
    
    agent1 = create_agent(
        name="test_agent_1",
        llm_config=llm_config
    )
    
    print(f"Agent 1 LLM Config: {agent1.llm_config}")
    
    # Test with dictionary
    agent2 = create_agent(
        name="test_agent_2",
        llm_config={
            "model": "claude-3-sonnet",
            "base_url": "https://***REMOVED***/v1/",
            "api_key": "sk-test123",
            "temperature": 0.5,
            "max_tokens": 2048
        }
    )
    
    print(f"Agent 2 LLM Config: {agent2.llm_config}")
    
    # Test backward compatibility
    agent3 = create_agent(
        name="test_agent_3",
        model="gpt-3.5-turbo",
        model_base_url="https://api.openai.com/v1",
        temperature=0.9,
        max_tokens=1024
    )
    
    print(f"Agent 3 LLM Config (backward compat): {agent3.llm_config}")


def test_llm_config_extensibility():
    """Test extensibility with custom parameters."""
    print("\nTesting LLMConfig extensibility")
    print("=" * 40)
    
    # Test with custom parameters
    config = LLMConfig(
        model="custom-model",
        base_url="https://custom-api.com/v1",
        temperature=0.6,
        custom_param="custom_value",
        another_param=42,
        nested_config={"key": "value"}
    )
    
    print(f"Config with custom params: {config}")
    print(f"Custom param: {config.get_param('custom_param')}")
    print(f"Another param: {config.get_param('another_param')}")
    print(f"Non-existent param: {config.get_param('non_existent', 'default')}")
    
    # Test parameter updates
    config.set_param('temperature', 0.8)
    config.set_param('new_param', 'new_value')
    
    print(f"After updates: {config}")
    print(f"OpenAI params: {config.to_openai_params()}")


def main():
    """Run all tests."""
    try:
        test_llm_config_basic()
        test_agent_with_llm_config()
        test_llm_config_extensibility()
        
        print("\n" + "=" * 50)
        print("✓ All LLM configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)