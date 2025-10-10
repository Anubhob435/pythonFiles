import subprocess

# Test cases from question4.txt
test_cases = [
    # Test Case 1
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
    
    # Test Case 2
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
"""
]

expected_outputs = [
    "21",  # Expected output for test case 1
    "9"   # Expected output for test case 2
]

def run_test_case(test_input, case_number, expected_output):
    print(f"=== Test Case {case_number} ===")
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
        print("✅ PASS")
    else:
        print("❌ FAIL")
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    print("-" * 50)

# Run all test cases
for i, (test_input, expected_output) in enumerate(zip(test_cases, expected_outputs), 1):
    run_test_case(test_input, i, expected_output)

print("Test execution completed!")