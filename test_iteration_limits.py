#!/usr/bin/env python3
"""Test iteration limiting functionality."""

from northau.archs.main_sub import create_agent
from northau.archs.tool import Tool
from northau.archs.tool.builtin.bash_tool import bash


def test_iteration_hints():
    """Test iteration hint generation."""
    print("Testing Iteration Hints")
    print("=" * 30)
    
    # Create agent
    agent = create_agent(
        name="test_agent",
        tools=[Tool.from_yaml("tools/Bash.yaml", binding=bash)]
    )
    
    # Test different iteration scenarios
    test_cases = [
        (1, 10, 9),  # Early iteration
        (5, 10, 5),  # Mid iteration
        (8, 10, 2),  # Near end
        (10, 10, 0), # Last iteration
    ]
    
    for current, max_iter, remaining in test_cases:
        hint = agent._build_iteration_hint(current, max_iter, remaining)
        print(f"\nIteration {current}/{max_iter} (remaining: {remaining}):")
        print(f"Hint: {hint}")
    
    print("\n" + "=" * 50)
    
    # Test XML processing with iteration hints
    print("Testing XML Processing with Iteration Context")
    print("=" * 50)
    
    # Mock a response that would typically trigger multiple iterations
    mock_response = """I need to run multiple commands.

<tool_use>
  <tool_name>Bash</tool_name>
  <parameters>
    <command>echo "First command"</command>
  </parameters>
</tool_use>

Now I'll run another command."""
    
    # Simulate different iteration states
    for iteration in [1, 5, 9, 10]:
        print(f"\n--- Simulating iteration {iteration}/10 ---")
        remaining = 10 - iteration
        hint = agent._build_iteration_hint(iteration, 10, remaining)
        processed = agent._process_xml_calls(mock_response)
        
        # Show how the hint would be added
        print(f"Iteration hint: {hint}")
        print(f"Tool result would be followed by: {hint}")


def main():
    """Test the iteration limiting functionality."""
    try:
        test_iteration_hints()
        print("\n" + "=" * 50)
        print("✓ Iteration limiting tests completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)