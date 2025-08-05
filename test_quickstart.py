#!/usr/bin/env python3
"""Test the quick start example from the specification."""

import os
from northau.archs.main_sub import create_agent
from northau.archs.tool import Tool
from northau.archs.tool.builtin.bash_tool import bash
from northau.archs.tool.builtin.file_tool import file_edit, file_search
from northau.archs.tool.builtin.web_tool import web_search, web_read
from northau.archs.llm import LLMConfig


def main():
    """Test the quick start example."""
    print("Testing Northau Framework Quick Start Example")
    print("=" * 50)
    
    try:
        # Create tools
        print("Creating tools...")
        bash_tool = Tool.from_yaml("tools/Bash.yaml", binding=bash)
        edit_tool = Tool.from_yaml("tools/Edit.yaml", binding=file_edit)
        file_search_tool = Tool.from_yaml("tools/Grep.yaml", binding=file_search)
        web_search_tool = Tool.from_yaml("tools/WebSearch.yaml", binding=web_search)
        web_read_tool = Tool.from_yaml("tools/WebRead.yaml", binding=web_read)
        print("✓ Tools created successfully")
        
        # Create sub-agents
        llm_config = LLMConfig(
                model=os.getenv("LLM_MODEL"),
                base_url=os.getenv("LLM_BASE_URL"),
                api_key=os.getenv("LLM_API_KEY")
        )
        print("\nCreating sub-agents...")
        # file_search_agent = create_agent(
        #     name="file_search_agent",
        #     tools=[file_search_tool],
        #     llm_config=llm_config,
        #     system_prompt="You are a file search agent. You are given a message and you need to search for the files that match the message."
        # )
        
        deep_research_agent = create_agent(
            name="deep_research_agent",
            tools=[web_search_tool, web_read_tool],
            llm_config=llm_config,
            system_prompt="You are a deep research agent. You are given a message and you need to search for the information that matches the message. Use the web_search and web_read tools to get the information. Wait for the web_read tool to finish before you continue your response."
        )
        print("✓ Sub-agents created successfully")
        
        # Create main agent
        print("\nCreating main agent...")
        main_agent = create_agent(
            name="main_agent",
            tools=[bash_tool, edit_tool, file_search_tool],
            sub_agents=[
                # ("file_search", file_search_agent),
                ("deep_research", deep_research_agent)
            ],
            llm_config=llm_config,
            system_prompt="You are a main agent. You are given a message and you need to delegate the task to the appropriate sub-agent. Use the file_search and deep_research sub-agents to get the information. Wait for the sub-agents to finish before you continue your response."
        )
        print("✓ Main agent created successfully")
        
        # Test the agent
        print("\nTesting agent functionality...")
        test_message = "find all Python files in the current directory"
        
        print(f"\nUser: {test_message}")
        print("\nAgent Response:")
        print("-" * 30)
        
        response = main_agent.run(test_message)
        print(response)
        
        print("\n" + "=" * 50)
        print("✓ Quick start example completed successfully!")
        
        # Test delegation
        print("\nTesting delegation with web research...")
        web_message = "research the latest Python frameworks"
        print(f"\nUser: {web_message}")
        print("\nAgent Response:")
        print("-" * 30)
        
        response = main_agent.run(web_message)
        print(response)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)