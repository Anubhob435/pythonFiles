import subprocess

# Test cases from questions.txt
test_cases = [
    """8
Diesel 1
Alloy 4
Battery 5
Alloy 1
Car 5
Zirconium 7
Vinyl 3
Wine 1
6
""",
    """4
Can 5
Alloy 4
Battery 5
Alloy 1
3
"""
]

def run_test_case(test_input):
    # Run answer1.py as a subprocess and pass test_input as stdin
    result = subprocess.run(
        ["python", "answer1.py"],
        input=test_input,
        capture_output=True,
        text=True
    )
    print("Input:\n", test_input)
    print("Output:\n", result.stdout)
    print("-" * 40)

for case in test_cases:
    run_test_case(case)