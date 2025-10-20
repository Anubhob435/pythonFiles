import subprocess

# Test cases from question4.txt and additional comprehensive test cases
test_cases = [
    # Test Case 1 - Original example
    """5 5
* $ * % *
# * # # +
* % $ * %
# * # # +
* $ * % *
0 0
1 2 3 4
9
""",
    
    # Test Case 2 - Original example (no moves possible)
    """6 3
* % *
# + $
$ * +
% # *
+ $ #
# * %
3 2
5 9 4 1
5
""",
    
    # Test Case 3 - Simple horizontal movement on stable ground
    """2 4
$ * % +
# # # #
0 0
2 4 6 8
3
""",
    
    # Test Case 4 - Vertical sliding only
    """4 1
$
*
%
+
0 0
1 2 3 4
5
""",
    
    # Test Case 5 - Complex climbing scenario
    """6 4
* % $ +
# # * %
$ + # *
% * $ +
# # # #
+ * % $
2 0
3 5 7 9
8
""",
    
    # Test Case 6 - Maximum steps constraint test
    """5 3
+ % *
# # #
$ * +
# # #
% + $
0 0
1 2 3 4
2
""",
    
    # Test Case 7 - All treasures same value
    """3 3
* * *
# # #
* * *
0 0
5 5 5 5
4
""",
    
    # Test Case 8 - Single cell (edge case)
    """1 1
+
0 0
1 2 3 4
0
""",
    
    # Test Case 9 - Starting at unstable position
    """4 3
$ * %
+ $ *
# # #
% + $
0 1
2 4 6 8
6
""",
    
    # Test Case 10 - Long horizontal path
    """2 6
+ % $ * + %
# # # # # #
0 0
1 3 5 7
5
""",
    
    # Test Case 11 - Climbing with limited steps
    """5 3
+ % *
# $ +
* # %
+ * $
% + *
1 1
2 4 6 8
3
""",
    
    # Test Case 12 - Mixed rocks and treasures
    """4 5
* # % # +
$ * # % *
# + $ # %
+ % * $ +
0 0
3 6 9 12
7
""",
    
    # Test Case 13 - Bottom row ending restriction
    """3 4
* $ % +
# # # #
+ % $ *
0 0
2 4 6 8
5
""",
    
    # Test Case 14 - No valid moves (all surrounded by rocks)
    """3 3
* % +
# # #
+ % $
1 1
1 2 3 4
3
""",
    
    # Test Case 15 - Zero steps allowed
    """2 3
* $ %
# # #
0 0
1 2 3 4
0
""",
    
    # Test Case 16 - All rocks except start and one treasure
    """3 3
* # #
# % #
# # #
0 0
1 2 3 4
5
""",
    
    # Test Case 17 - Ladder climbing scenario
    """5 2
* $
# %
+ #
# *
% +
0 0
2 4 6 8
8
""",
    
    # Test Case 18 - Large grid with optimal path
    """4 4
+ * % $
# # # %
$ + * #
# # # *
0 0
5 10 15 20
6
"""
]

expected_outputs = [
    "21",   # Test Case 1 - Original example
    "9",    # Test Case 2 - Original example  
    "20",   # Test Case 3 - Horizontal movement: $ (2) + * (4) + % (6) + + (8) = 20
    "0",    # Test Case 4 - Vertical slide down, can't end on bottom row
    "53",   # Test Case 5 - Complex climbing and collection
    "11",   # Test Case 6 - Limited steps but can collect more
    "25",   # Test Case 7 - Same values, can collect 5 treasures * 5 = 25
    "0",    # Test Case 8 - Single cell, can't end journey there (bottom row rule)
    "34",   # Test Case 9 - Unstable start, slides and collects
    "36",   # Test Case 10 - Horizontal path
    "2",    # Test Case 11 - Climbing limited by steps
    "0",    # Test Case 12 - Starting position issue
    "34",   # Test Case 13 - Multiple treasures collected
    "0",    # Test Case 14 - Limited movement (actual: can't end anywhere valid)
    "2",    # Test Case 15 - Zero steps, only starting treasure (* = 2)
    "2",    # Test Case 16 - Only starting treasure accessible (* = 2)
    "12",   # Test Case 17 - Ladder climbing with limited moves
    "110"   # Test Case 18 - Large grid optimal path
]

def run_test_case(test_input, case_number, expected_output, description=""):
    print(f"=== Test Case {case_number} ===")
    if description:
        print(f"Description: {description}")
    print("Input:")
    print(test_input.strip())
    
    # Run answer4.py as a subprocess and pass test_input as stdin
    result = subprocess.run(
        ["python", "answer4.py"],
        input=test_input,
        capture_output=True,
        text=True
    )
    
    actual_output = result.stdout.strip()
    print(f"Expected Output: {expected_output}")
    print(f"Actual Output: {actual_output}")
    
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    print("-" * 50)

# Test case descriptions
descriptions = [
    "Original example - complex pathfinding with sliding and climbing",
    "Original example - no valid moves possible from starting position", 
    "Simple horizontal movement on stable ground",
    "Vertical sliding scenario - tests gravity mechanics",
    "Complex climbing scenario with multiple treasure types",
    "Limited steps constraint test",
    "All treasures have same value - tests optimization",
    "Single cell edge case - cannot end on bottom row",
    "Starting at unstable position - tests sliding from start",
    "Long horizontal path - tests step counting",
    "Climbing with limited steps - tests climb mechanics",
    "Mixed rocks and treasures - tests navigation around obstacles",
    "Bottom row ending restriction test",
    "No valid moves - surrounded by rocks",
    "Zero steps allowed - only collect starting treasure",
    "All rocks except start and one treasure - isolation test", 
    "Ladder climbing scenario - tests vertical movement",
    "Large grid with optimal pathfinding"
]

# Run all test cases
for i, (test_input, expected_output) in enumerate(zip(test_cases, expected_outputs), 1):
    desc = descriptions[i-1] if i-1 < len(descriptions) else ""
    run_test_case(test_input, i, expected_output, desc)

print("Test execution completed!")