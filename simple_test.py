#!/usr/bin/env python3
"""Simple test of XML processing without tool execution."""

from northau.archs.main_sub import create_agent


def main():
    """Simple test."""
    print("Testing XML Processing")
    print("=" * 30)
    
    # Create simple agent without tools that might hang
    agent = create_agent(name="test_agent")
    
    # Test system prompt building
    print("System prompt:")
    system_prompt = agent._build_system_prompt_with_capabilities()
    print(system_prompt)
    
    # Test XML parsing without execution
    print("\nTesting XML parsing:")
    
    test_xml = '''<tool_name>TestTool</tool_name>
    <parameters>
        <param1>value1</param1>
        <param2>value2</param2>
    </parameters>'''
    
    try:
        result = agent._execute_tool_from_xml(test_xml)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error (no TestTool): {e}")
    
    print("\n✓ Basic XML processing test completed!")


if __name__ == "__main__":
    main()