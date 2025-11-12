# Compiler Design - Assignment 1: Lexical Analyzer

Develop a lexical analyzer to recognize a few patterns in C. (Ex. identifiers, constants, comments, operators etc.)

## List of Experiments

### 1. Valid Identifier Checker
Write a C program to check if a user given string is a valid identifier or not?

#### Simple Answer:
```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int isValidIdentifier(char *str) {
    if (str[0] != '_' && !isalpha(str[0])) 
        return 0;  // First character must be letter or underscore

    for (int i = 1; i < strlen(str); i++) {
        if (str[i] != '_' && !isalnum(str[i])) 
            return 0;  // Subsequent characters must be alphanumeric or underscore
    }
    
    return 1;  // Valid identifier
}

int main() {
    char str[100];
    printf("Enter an identifier: ");
    scanf("%s", str);
    
    if (isValidIdentifier(str))
        printf("%s is a valid identifier.\n", str);
    else
        printf("%s is not a valid identifier.\n", str);
    
    return 0;
}
```

### 2. Valid Comment Checker
Write a C program to check if a user given C program statement is a valid Comment or not?

#### Simple Answer:
```c
#include <stdio.h>
#include <string.h>

int isValidComment(char *str) {
    int len = strlen(str);
    
    // Check for single-line comment: starts with //
    if (len >= 2 && str[0] == '/' && str[1] == '/') {
        return 1;
    }
    
    // Check for multi-line comment: starts with /* and ends with */
    if (len >= 4 && str[0] == '/' && str[1] == '*' && 
        str[len-2] == '*' && str[len-1] == '/') {
        return 1;
    }
    
    return 0;  // Not a valid comment
}

int main() {
    char str[1000];
    printf("Enter a comment: ");
    fgets(str, sizeof(str), stdin);
    
    if (isValidComment(str))
        printf("Valid comment.\n");
    else
        printf("Not a valid comment.\n");
    
    return 0;
}
```

### 3. Remove Comments from File
Write a C program to read a program written in a file and remove all comments. After removing all comments, rewrite the program in a separate file.

#### Simple Answer:
```c
#include <stdio.h>
#include <string.h>

void removeComments(FILE *input, FILE *output) {
    char ch, next_ch;
    int in_single_line_comment = 0;
    int in_multi_line_comment = 0;
    
    while ((ch = fgetc(input)) != EOF) {
        if (in_single_line_comment) {
            if (ch == '\n') {
                in_single_line_comment = 0;
                fputc(ch, output);
            }
        } else if (in_multi_line_comment) {
            if (ch == '*' && (next_ch = fgetc(input)) == '/') {
                in_multi_line_comment = 0;
            } else {
                ungetc(next_ch, input);
            }
        } else {
            if (ch == '/' && (next_ch = fgetc(input)) == '/') {
                in_single_line_comment = 1;
                ungetc(next_ch, input);
            } else if (ch == '/' && next_ch == '*') {
                in_multi_line_comment = 1;
            } else {
                ungetc(next_ch, input);
                fputc(ch, output);
            }
        }
    }
}

int main() {
    FILE *input = fopen("input.c", "r");
    FILE *output = fopen("output.c", "w");
    
    if (input == NULL || output == NULL) {
        printf("Error opening files.\n");
        return 1;
    }
    
    removeComments(input, output);
    
    fclose(input);
    fclose(output);
    
    printf("Comments removed successfully.\n");
    return 0;
}
```

### 4. Infix to Postfix Converter
Write a C program to convert an infix statement into a postfix statement.

#### Simple Answer:
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char stack[100];
int top = -1;

void push(char x) {
    stack[++top] = x;
}

char pop() {
    if(top == -1) return -1;
    else return stack[top--];
}

int priority(char x) {
    if(x == '(') return 0;
    if(x == '+' || x == '-') return 1;
    if(x == '*' || x == '/') return 2;
    return 0;
}

int main() {
    char exp[100];
    char *e, x;
    printf("Enter the expression: ");
    scanf("%s", exp);
    e = exp;
    
    printf("\nPostfix: ");
    while(*e != '\0') {
        if(isalnum(*e))
            printf("%c", *e);
        else if(*e == '(')
            push(*e);
        else if(*e == ')') {
            while((x = pop()) != '(')
                printf("%c", x);
        }
        else {
            while(priority(stack[top]) >= priority(*e))
                printf("%c", pop());
            push(*e);
        }
        e++;
    }
    
    while(top != -1) {
        printf("%c", pop());
    }
    return 0;
}
```

### 5. Arithmetic Expression Evaluator
Write a C program to evaluate an arithmetic expression which is given as a string. Consider the input has no parentheses and contains the following operators only: +, -, *, /

#### Simple Answer:
```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Function to perform operations
double applyOp(double a, double b, char op) {
    switch(op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
    }
    return 0;
}

double evaluate(char* tokens) {
    double values[100];  // Stack for numbers
    char ops[100];       // Stack for operators
    int valTop = -1, opTop = -1;
    
    for (int i = 0; i < strlen(tokens); i++) {
        if (tokens[i] == ' ') continue;
        
        else if (isdigit(tokens[i])) {
            double val = 0;
            while (i < strlen(tokens) && isdigit(tokens[i])) {
                val = (val * 10) + (tokens[i] - '0');
                i++;
            }
            values[++valTop] = val;
            i--;  // Adjust for the extra increment in for loop
        }
        
        else {
            while (opTop != -1 && priority(ops[opTop]) >= priority(tokens[i])) {
                double val2 = values[valTop--];
                double val1 = values[valTop--];
                char op = ops[opTop--];
                values[++valTop] = applyOp(val1, val2, op);
            }
            ops[++opTop] = tokens[i];
        }
    }
    
    while (opTop != -1) {
        double val2 = values[valTop--];
        double val1 = values[valTop--];
        char op = ops[opTop--];
        values[++valTop] = applyOp(val1, val2, op);
    }
    
    return values[valTop];
}

int main() {
    char expression[100];
    printf("Enter arithmetic expression (e.g., 2+3*4): ");
    scanf("%s", expression);
    
    double result = evaluate(expression);
    printf("Result: %.2f\n", result);
    
    return 0;
}
```