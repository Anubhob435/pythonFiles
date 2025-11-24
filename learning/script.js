document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // Shared Logic (Mobile Menu)
    // ==========================================
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // ==========================================
    // Recursion Page Logic
    // ==========================================
    const qaContainer = document.getElementById('qa-container');
    if (qaContainer) {
        const theoryQuestions = [
            {
                q: "What is a base case and why is it essential?",
                a: "The base case is the condition that stops the recursion. It's the simplest form of the problem that can be solved directly. It is essential because, without it, the function would call itself indefinitely, leading to a stack overflow error."
            },
            {
                q: "What are the advantages of recursion?",
                a: "Recursion can lead to shorter, more elegant, and easier-to-read code for problems that are naturally recursive (like tree traversals or the Fibonacci sequence). It breaks down complex problems into simpler, manageable sub-problems."
            },
            {
                q: "What are the disadvantages of recursion?",
                a: "Recursion can be less efficient than iteration due to the overhead of function calls and return. It consumes more memory because each function call is added to the call stack. If the recursion is too deep, it can cause a stack overflow."
            },
            {
                q: "What are the types of recursion?",
                a: "<strong>Direct Recursion:</strong> A function calls itself.<br><strong>Indirect Recursion:</strong> A function (A) calls another function (B), which in turn calls the first function (A).<br><strong>Tail Recursion:</strong> The recursive call is the very last operation in the function. This can be optimized by compilers to be as efficient as iteration.<br><strong>Non-Tail Recursion:</strong> The recursive call is not the last operation (e.g., `n * factorial(n-1)` requires a multiplication after the call)."
            }
        ];

        theoryQuestions.forEach((item, index) => {
            const qaId = `qa-${index}`;
            const qaBlock = document.createElement('div');
            qaBlock.innerHTML = `
                <button class="question-btn" data-answer-id="${qaId}">
                    <span>${item.q}</span>
                    <svg class="w-5 h-5 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </button>
                <div id="${qaId}" class="answer-panel hidden">
                    <p class="text-[var(--text-light)]">${item.a}</p>
                </div>
            `;
            qaContainer.appendChild(qaBlock);
        });

        qaContainer.addEventListener('click', (e) => {
            const btn = e.target.closest('.question-btn');
            if (btn) {
                const answerId = btn.dataset.answerId;
                const answerPanel = document.getElementById(answerId);
                const icon = btn.querySelector('svg');

                answerPanel.classList.toggle('hidden');
                icon.classList.toggle('rotate-180');
            }
        });
    }

    const problemSelector = document.getElementById('problem-selector');
    if (problemSelector) {
        const problems = {
            factorial: {
                title: "Factorial of a Number",
                statement: "Write a recursive function to find the factorial of a non-negative integer 'n' (n!).",
                code: `public int factorial(int n) {
    // Base Case
    if (n == 0 || n == 1) {
        return 1;
    }
    // Recursive Case
    return n * factorial(n - 1);
}`,
                explanation: "The base case is when n is 0 or 1, which returns 1. The recursive step multiplies n by the factorial of (n-1). Each call reduces n, moving closer to the base case.",
                runner: {
                    inputs: [{ id: 'n', label: 'Enter n:', type: 'number', default: 5 }],
                    logic: (inputs) => {
                        const n = parseInt(inputs.n, 10);
                        if (isNaN(n) || n < 0) return "Error: n must be a non-negative integer.";
                        function fact(num) {
                            if (num === 0 || num === 1) return 1;
                            if (num > 20) return "Result too large to display.";
                            return num * fact(num - 1);
                        }
                        return `factorial(${n}) = ${fact(n)}`;
                    }
                }
            },
            fibonacci: {
                title: "N-th Fibonacci Number",
                statement: "Write a recursive function to find the n-th term of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8...).",
                code: `public int fibonacci(int n) {
    // Base Cases
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    // Recursive Case
    return fibonacci(n - 1) + fibonacci(n - 2);
}`,
                explanation: "There are two base cases: n=0 (returns 0) and n=1 (returns 1). The recursive step calculates the n-th term by summing the (n-1)th and (n-2)th terms.",
                runner: {
                    inputs: [{ id: 'n', label: 'Enter n:', type: 'number', default: 6 }],
                    logic: (inputs) => {
                        const n = parseInt(inputs.n, 10);
                        if (isNaN(n) || n < 0) return "Error: n must be a non-negative integer.";
                        if (n > 30) return "Error: n > 30 is too slow for this simple recursive version.";
                        function fib(num) {
                            if (num <= 0) return 0;
                            if (num === 1) return 1;
                            return fib(num - 1) + fib(num - 2);
                        }
                        return `fibonacci(${n}) = ${fib(n)}`;
                    }
                }
            },
            gcd: {
                title: "Greatest Common Divisor (GCD)",
                statement: "Write a recursive function to find the GCD (or HCF) of two numbers using the Euclidean algorithm.",
                code: `public int gcd(int a, int b) {
    // Base Case
    if (b == 0) {
        return a;
    }
    // Recursive Case
    return gcd(b, a % b);
}`,
                explanation: "The base case is when the second number 'b' becomes 0. At this point, the first number 'a' is the GCD. The recursive step calls gcd with 'b' as the new 'a' and the remainder of 'a / b' as the new 'b'.",
                runner: {
                    inputs: [
                        { id: 'a', label: 'Enter a:', type: 'number', default: 54 },
                        { id: 'b', label: 'Enter b:', type: 'number', default: 24 }
                    ],
                    logic: (inputs) => {
                        const a = parseInt(inputs.a, 10);
                        const b = parseInt(inputs.b, 10);
                        if (isNaN(a) || isNaN(b)) return "Error: Both inputs must be integers.";
                        function findGcd(x, y) {
                            if (y === 0) return x;
                            return findGcd(y, x % y);
                        }
                        return `gcd(${a}, ${b}) = ${findGcd(Math.abs(a), Math.abs(b))}`;
                    }
                }
            },
            palindrome: {
                title: "String Palindrome Check",
                statement: "Write a recursive function that returns true if a string is a palindrome (reads the same forwards and backwards) and false otherwise.",
                code: `public boolean isPalindrome(String s) {
    s = s.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
    return check(s, 0, s.length() - 1);
}

private boolean check(String s, int start, int end) {
    // Base Case 1
    if (start >= end) {
        return true;
    }
    // Base Case 2
    if (s.charAt(start) != s.charAt(end)) {
        return false;
    }
    // Recursive Case
    return check(s, start + 1, end - 1);
}`,
                explanation: "First, the string is cleaned. The helper function 'check' has two base cases: if the start/end pointers cross, it's a palindrome (true). If the characters at start and end don't match, it's not (false). The recursive step calls 'check' with the pointers moved one step inwards.",
                runner: {
                    inputs: [{ id: 's', label: 'Enter string:', type: 'text', default: 'A man, a plan, a canal: Panama' }],
                    logic: (inputs) => {
                        let s = inputs.s || "";
                        s = s.replaceAll(/[^a-zA-Z0-9]/g, "").toLowerCase();
                        function check(str, start, end) {
                            if (start >= end) return true;
                            if (str.charAt(start) !== str.charAt(end)) return false;
                            return check(str, start + 1, end - 1);
                        }
                        const result = check(s, 0, s.length - 1);
                        return `Is "${inputs.s}" a palindrome? ${result}`;
                    }
                }
            },
            sumOfDigits: {
                title: "Sum of Digits",
                statement: "Write a recursive function to find the sum of the digits of a number.",
                code: `public int sumOfDigits(int n) {
    n = Math.abs(n);
    // Base Case
    if (n == 0) {
        return 0;
    }
    // Recursive Case
    return (n % 10) + sumOfDigits(n / 10);
}`,
                explanation: "The base case is when the number 'n' becomes 0, at which point the sum is 0. The recursive step adds the last digit (n % 10) to the sum of the remaining digits (n / 10).",
                runner: {
                    inputs: [{ id: 'n', label: 'Enter number:', type: 'number', default: 12345 }],
                    logic: (inputs) => {
                        const n = parseInt(inputs.n, 10);
                        if (isNaN(n)) return "Error: Input must be an integer.";
                        function sum(num) {
                            num = Math.abs(num);
                            if (num === 0) return 0;
                            return (num % 10) + sum(Math.floor(num / 10));
                        }
                        return `Sum of digits for ${n} = ${sum(n)}`;
                    }
                }
            }
        };

        const titleEl = document.getElementById('problem-title');
        const statementEl = document.getElementById('problem-statement');
        const codeEl = document.getElementById('problem-code');
        const explanationEl = document.getElementById('problem-explanation');
        const runnerEl = document.getElementById('problem-runner');
        let activeBtn = null;

        function loadProblem(key) {
            const data = problems[key];
            if (!data) return;

            titleEl.textContent = data.title;
            statementEl.textContent = data.statement;
            codeEl.textContent = data.code;
            explanationEl.textContent = data.explanation;

            runnerEl.innerHTML = '';
            const inputs = {};

            data.runner.inputs.forEach(input => {
                const label = document.createElement('label');
                label.className = 'block text-sm font-medium text-[var(--text-light)] mb-1';
                label.setAttribute('for', input.id);
                label.textContent = input.label;

                const inputEl = document.createElement('input');
                inputEl.className = 'block w-full px-3 py-2 border border-[var(--border-color)] rounded-md shadow-sm focus:outline-none focus:ring-[var(--primary)] focus:border-[var(--primary)] sm:text-sm';
                inputEl.type = input.type;
                inputEl.id = input.id;
                inputEl.value = input.default;

                runnerEl.appendChild(label);
                runnerEl.appendChild(inputEl);
                inputs[input.id] = inputEl;
            });

            const runBtn = document.createElement('button');
            runBtn.className = 'btn-secondary mt-4';
            runBtn.textContent = 'Run';

            const resultEl = document.createElement('div');
            resultEl.className = 'mt-4 p-4 bg-gray-100 rounded-md text-[var(--text-main)] font-medium';
            resultEl.style.display = 'none';

            runBtn.addEventListener('click', () => {
                const inputValues = {};
                for (const id in inputs) {
                    inputValues[id] = inputs[id].value;
                }
                const result = data.runner.logic(inputValues);
                resultEl.textContent = result;
                resultEl.style.display = 'block';
            });

            runnerEl.appendChild(runBtn);
            runnerEl.appendChild(resultEl);
        }

        Object.keys(problems).forEach((key, index) => {
            const btn = document.createElement('button');
            btn.className = 'btn-selector w-full text-left';
            btn.textContent = problems[key].title;
            btn.dataset.problemKey = key;
            btn.addEventListener('click', () => {
                loadProblem(key);
                if (activeBtn) {
                    activeBtn.classList.remove('bg-[var(--primary)]', 'text-white');
                }
                btn.classList.add('bg-[var(--primary)]', 'text-white');
                activeBtn = btn;
            });
            problemSelector.appendChild(btn);

            if (index === 0) {
                btn.click();
            }
        });
    }

    const stackBtn = document.getElementById('run-stack-anim');
    if (stackBtn) {
        const stackVisual = document.getElementById('stack-visual');
        const stackExplanation = document.getElementById('stack-explanation');

        stackBtn.addEventListener('click', () => {
            stackBtn.disabled = true;
            stackVisual.innerHTML = '';
            stackExplanation.textContent = 'Animation started...';

            const steps = [
                { delay: 500, visual: 'factorial(3)', text: 'Call factorial(3). 3 is not 0 or 1. Must call factorial(2).' },
                { delay: 1000, visual: 'factorial(2)', text: 'Call factorial(2). 2 is not 0 or 1. Must call factorial(1).' },
                { delay: 1000, visual: 'factorial(1)', text: 'Call factorial(1). Base case reached! Return 1.' },
                { delay: 1500, visual: 'pop', text: 'factorial(1) returns 1. factorial(2) can now compute: 2 * 1 = 2. Return 2.' },
                { delay: 1500, visual: 'pop', text: 'factorial(2) returns 2. factorial(3) can now compute: 3 * 2 = 6. Return 6.' },
                { delay: 1500, visual: 'pop', text: 'factorial(3) returns 6. Final result is 6. Stack is empty.' },
                { delay: 1000, visual: 'clear', text: 'Click the button to run the animation again.' }
            ];

            let chain = Promise.resolve();

            steps.forEach(step => {
                chain = chain.then(() => new Promise(resolve => {
                    setTimeout(() => {
                        if (step.visual === 'pop') {
                            stackVisual.removeChild(stackVisual.lastChild);
                        } else if (step.visual === 'clear') {
                            stackVisual.innerHTML = '';
                            stackBtn.disabled = false;
                        } else {
                            const item = document.createElement('div');
                            item.className = 'stack-item';
                            item.textContent = step.visual;
                            stackVisual.appendChild(item);
                        }
                        stackExplanation.textContent = step.text;
                        resolve();
                    }, step.delay);
                }));
            });
        });
    }

    // ==========================================
    // File Handling Page Logic
    // ==========================================
    const tabs = document.querySelectorAll('.nav-tab');
    if (tabs.length > 0) {
        const pages = document.querySelectorAll('.page-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                const targetId = e.currentTarget.getAttribute('data-target');

                pages.forEach(page => {
                    page.style.display = 'none';
                });

                tabs.forEach(t => {
                    t.classList.remove('tab-active');
                });

                document.getElementById(targetId).style.display = 'block';
                e.currentTarget.classList.add('tab-active');
            });
        });

        const mainContent = document.querySelector('main');
        mainContent.addEventListener('click', (e) => {
            const toggleButton = e.target.classList.contains('toggle-btn') ? e.target : null;
            const accordionButton = e.target.closest('.toggle-accordion');

            if (toggleButton) {
                e.preventDefault();
                const answerContent = toggleButton.nextElementSibling;
                const isHidden = answerContent.style.display === 'none' || getComputedStyle(answerContent).display === 'none';

                answerContent.style.display = isHidden ? 'block' : 'none';
                toggleButton.textContent = isHidden ? 'Hide Answer' : 'Show Answer';
            }

            if (accordionButton) {
                e.preventDefault();
                const answerContent = accordionButton.nextElementSibling;
                const isHidden = answerContent.style.display === 'none' || getComputedStyle(answerContent).display === 'none';

                answerContent.style.display = isHidden ? 'block' : 'none';
                if (isHidden) {
                    accordionButton.classList.add('accordion-open');
                } else {
                    accordionButton.classList.remove('accordion-open');
                }
            }
        });
    }

});
