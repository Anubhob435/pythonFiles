import subprocess
import sys
import os

# Test cases based on question5.txt and the ReduceExp problem
test_cases = [
    # Example 1 from question
    {
        "input": "x*(x+2+1)+1+1",
        "expected_output": "3",
        "description": "Form 1 factorization: (x+1)*(x+2)"
    },
    
    # Example 2 from question
    {
        "input": "2*x*y+4*x+y+2+y*y",
        "expected_output": "6",
        "description": "Form 2 factorization with remaining y*y term"
    },
    
    # Example 3 from question
    {
        "input": "10*5+6*3",
        "expected_output": "0",
        "description": "Constants only - evaluates to 68"
    },
    
    # Additional test cases for different forms
    
    # Form 1: a1*a2*x*x + (a1*b2 + a2*b1)*x + b1*b2
    {
        "input": "x*x+3*x+2",
        "expected_output": "3",
        "description": "Form 1: (x+1)*(x+2) - simple quadratic"
    },
    
    {
        "input": "2*x*x+5*x+3",
        "expected_output": "4",  # Actually requires 4 operations in standard form
        "description": "Form 1: Standard form is better than factored"
    },
    
    {
        "input": "6*x*x+7*x+2",
        "expected_output": "5", # Requires 5 operations in standard form
        "description": "Form 1: Standard form calculation"
    },
    
    # Form 2: a1*a2*x*y + a1*b2*x + a2*b1*y + b1*b2
    {
        "input": "x*y+2*x+3*y+6",
        "expected_output": "3",
        "description": "Form 2: (x+3)*(y+2)"
    },
    
    {
        "input": "2*x*y+4*x+y+2",
        "expected_output": "4",  # Standard form operations
        "description": "Form 2: Standard form calculation"
    },
    
    {
        "input": "3*x*y+6*x+2*y+4",
        "expected_output": "4",  # Standard form operations  
        "description": "Form 2: Standard form calculation"
    },
    
    # Form 3: a1*a2*x*x + a1*b2*x + a2*b1*x*y + b1*b2*y
    {
        "input": "x*x+2*x+x*y+2*y",
        "expected_output": "7",  # Standard form operations
        "description": "Form 3: Standard form calculation"
    },
    
    {
        "input": "2*x*x+3*x+2*x*y+3*y",
        "expected_output": "9",  # Standard form operations
        "description": "Form 3: Standard form calculation"
    },
    
    # Cases with no factorization possible
    {
        "input": "x*x+x*y+y*y",
        "expected_output": "5",  # Standard form: x*x + x*y + y*y = 3 multiplications + 2 additions
        "description": "No factorization possible"
    },
    
    {
        "input": "x+y+1",
        "expected_output": "2",
        "description": "Simple linear expression"
    },
    
    {
        "input": "2*x+3*y+4",
        "expected_output": "4",
        "description": "Linear with coefficients"
    },
    
    # Edge cases
    {
        "input": "x*x",
        "expected_output": "1",
        "description": "Single quadratic term"
    },
    
    {
        "input": "x",
        "expected_output": "0",
        "description": "Single variable"
    },
    
    {
        "input": "5",
        "expected_output": "0",
        "description": "Single constant"
    },
    
    {
        "input": "x*x+x",
        "expected_output": "2",
        "description": "x*(x+1)"
    },
    
    {
        "input": "y*y+y",
        "expected_output": "2",
        "description": "y*(y+1)"
    },
    
    # Complex expressions
    {
        "input": "x*x+4*x+4",
        "expected_output": "3",
        "description": "Perfect square: (x+2)*(x+2)"
    },
    
    {
        "input": "x*(y+1)+y+1",
        "expected_output": "3",
        "description": "(x+1)*(y+1)"
    },
    
    # Expressions with brackets
    {
        "input": "(x+1)*(x+2)",
        "expected_output": "3",
        "description": "Already factored form"
    },
    
    {
        "input": "x*(x+1)+2*(x+1)",
        "expected_output": "3",
        "description": "(x+2)*(x+1)"
    },
    
    # Additional edge cases
    {
        "input": "0*x+0*y+0",
        "expected_output": "0",
        "description": "All zero coefficients"
    },
    
    {
        "input": "x*y",
        "expected_output": "1",
        "description": "Single multiplication term"
    },
    
    {
        "input": "100*x*x+200*x+100",
        "expected_output": "3",
        "description": "Large coefficients that can be factored"
    },
    
    {
        "input": "-x*x-3*x-2",
        "expected_output": "3",
        "description": "Negative coefficients factorization"
    },
    
    {
        "input": "x*x-1",
        "expected_output": "2",
        "description": "Difference of squares potential"
    },
    
    {
        "input": "x*y+x+y+1",
        "expected_output": "3",
        "description": "Form 2: (x+1)*(y+1)"
    }
]

def run_test_case(test_data):
    test_input = test_data["input"]
    expected = test_data["expected_output"]
    description = test_data["description"]
    
    print(f"Test: {description}")
    print(f"Input: {test_input}")
    print(f"Expected: {expected}")
    
    try:
        # Run answer5.py as a subprocess and pass test_input as stdin
        result = subprocess.run(
            [sys.executable, "answer5.py"],
            input=test_input,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        actual_output = result.stdout.strip()
        print(f"Actual: {actual_output}")
        
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            print("FAILED ❌")
        elif actual_output == expected:
            print("PASSED ✅")
        else:
            print("FAILED ❌")
            
    except Exception as e:
        print(f"ERROR running test: {e}")
        print("FAILED ❌")
    
    print("-" * 60)

def main():
    print("Running test cases for ReduceExp (Question 5)")
    print("=" * 60)
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}/{total}:")
        try:
            result = subprocess.run(
                [sys.executable, "answer5.py"],
                input=test_case["input"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            actual = result.stdout.strip()
            expected = test_case["expected_output"]
            
            print(f"Input: {test_case['input']}")
            print(f"Expected: {expected}")
            print(f"Actual: {actual}")
            print(f"Description: {test_case['description']}")
            
            if result.returncode == 0 and actual == expected:
                print("PASSED ✅")
                passed += 1
            else:
                print("FAILED ❌")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                    
        except Exception as e:
            print(f"ERROR: {e}")
            print("FAILED ❌")
            
        print("-" * 60)
    
    print(f"\nSummary: {passed}/{total} tests passed")
    if passed == total:
        print("All tests passed! 🎉")
    else:
        print(f"{total - passed} tests failed. 😞")

if __name__ == "__main__":
    main()
