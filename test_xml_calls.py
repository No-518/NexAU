#!/usr/bin/env python3
"""Test XML-based tool and sub-agent calls."""

from northau.archs.main_sub import create_agent
from northau.archs.tool import Tool
from northau.archs.tool.builtin.bash_tool import bash
from northau.archs.tool.builtin.file_tool import file_edit, file_search
from northau.archs.tool.builtin.web_tool import web_search, web_read


def test_xml_processing():
    """Test XML processing functionality."""
    print("Testing XML Processing")
    print("=" * 30)
    
    # Create tools
    bash_tool = Tool.from_yaml("tools/Bash.yaml", binding=bash)
    edit_tool = Tool.from_yaml("tools/Edit.yaml", binding=file_edit)
    
    # Create agent
    agent = create_agent(
        name="test_agent",
        tools=[bash_tool, edit_tool],
        sub_agents=[
            ("file_search", create_agent(tools=[Tool.from_yaml("tools/Grep.yaml", binding=file_search)]))
        ]
    )
    
    # Test system prompt building
    print("System prompt with capabilities:")
    print("-" * 40)
    system_prompt = agent._build_system_prompt_with_capabilities()
    print(system_prompt[:500] + "..." if len(system_prompt) > 500 else system_prompt)
    
    # Test XML tool processing
    print("\n\nTesting XML tool processing:")
    print("-" * 40)
    
    mock_response_with_tool = """I'll help you with that task.

<tool_use>
  <tool_name>Bash</tool_name>
  <parameters>
    <command>ls -la</command>
    <timeout>10</timeout>
  </parameters>
</tool_use>

This will list the files in the current directory."""
    
    processed = agent._process_xml_calls(mock_response_with_tool)
    print("Original response:")
    print(mock_response_with_tool)
    print("\nProcessed response:")
    print(processed)
    
    # Test XML sub-agent processing
    print("\n\nTesting XML sub-agent processing:")
    print("-" * 40)
    
    mock_response_with_sub_agent = """I'll delegate this task to the file search agent.

<sub-agent>
  <agent_name>file_search</agent_name>
  <message>find all Python files</message>
</sub-agent>

The search has been completed."""
    
    processed = agent._process_xml_calls(mock_response_with_sub_agent)
    print("Original response:")
    print(mock_response_with_sub_agent)
    print("\nProcessed response:")
    print(processed)


def main():
    """Test the XML-based functionality."""
    try:
        test_xml_processing()
        print("\n" + "=" * 50)
        print("✓ XML processing tests completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)