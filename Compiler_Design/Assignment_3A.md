# Compiler Design - Assignment 3: YACC Specification for Syntactic Categories

## Topics
Generate YACC specification for a few syntactic categories:
- Program to recognize a valid arithmetic expression that uses operator +, – , * and /.
- Program to recognize a valid variable which starts with a letter followed by any number of letters or digits.
- Implementation of Calculator using LEX and YACC

## List of Experiments

### 1. Count Identifiers in Input File
Write a Lex Program to recognize and count the number of identifiers in a given input file.

#### Simple Answer:
```lex
%{
#include <stdio.h>
#include <string.h>
int count = 0;
int isKeyword(char* str) {
    return (!strcmp(str, "if") || !strcmp(str, "else") || !strcmp(str, "while") ||
            !strcmp(str, "for") || !strcmp(str, "int") || !strcmp(str, "float") ||
            !strcmp(str, "char") || !strcmp(str, "return") || !strcmp(str, "void"));
}
%}

%%
[a-zA-Z_][a-zA-Z0-9_]* {
    if(!isKeyword(yytext)) {
        count++;
        printf("Identifier found: %s\n", yytext);
    }
}
.|\n {}
%%

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
    }
    yylex();
    printf("Total identifiers: %d\n", count);
    return 0;
}
```

### 2. Test Arithmetic Expression Validity
Write a YACC Program to test the validity of a simple expression involving operators +, -, * and /

#### Simple Answer:
```yacc
%{
#include <stdio.h>
int valid = 1;
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

expr: expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | NUMBER
    ;

%%

int main() {
    printf("Enter arithmetic expression: ");
    if(yyparse()) {
        printf("Invalid expression\n");
    } else {
        printf("Valid expression\n");
    }
    return 0;
}
```

### 3. Recognize Nested IF Statements
Write a YACC Program to recognize nested IF control statements and display the levels of nesting.

#### Simple Answer:
```yacc
%{
#include <stdio.h>
int level = 0;
%}

%token IF THEN ELSE ID
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE
%%

stmt: IF '(' ID ')' stmt %prec LOWER_THAN_ELSE
    {
        printf("IF at level %d\n", level);
    }
    | IF '(' ID ')' stmt ELSE stmt
    {
        printf("IF-ELSE at level %d\n", level);
    }
    | stmt
    ;

%%

int main() {
    printf("Enter nested IF statements: ");
    yyparse();
    return 0;
}
```

### 4. Check Syntax of Expression
Write a YACC Program to check the syntax of a simple expression involving operators +, -, * and /

#### Simple Answer:
```yacc
%{
#include <stdio.h>
%}

%token NUMBER ID
%left '+' '-'
%left '*' '/'
%%

expr: expr '+' expr { printf("Addition\n"); }
    | expr '-' expr { printf("Subtraction\n"); }
    | expr '*' expr { printf("Multiplication\n"); }
    | expr '/' expr { printf("Division\n"); }
    | '(' expr ')' { printf("Parentheses\n"); }
    | NUMBER
    | ID
    ;

%%

int main() {
    printf("Enter expression to check syntax: ");
    if(yyparse()) {
        printf("Syntax Error\n");
    } else {
        printf("Syntax OK\n");
    }
    return 0;
}
```

### 5. Evaluate Arithmetic Expression
Write a YACC Program to evaluate an arithmetic expression involving operating +, -, * and /

#### Simple Answer:
```yacc
%{
#include <stdio.h>
int yylex(void);
void yyerror(char *s);
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

expr: expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { 
        if($3 != 0) 
            $$ = $1 / $3; 
        else {
            printf("Division by zero error\n");
            $$ = 0;
        }
      }
    | '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    ;

%%

int main() {
    printf("Enter arithmetic expression: ");
    yyparse();
    return 0;
}
```

### 6. Recognize Valid Variable
Write a YACC Program to recognize a valid variable, which starts with a letter, followed by any number of letters or digits.

#### Simple Answer:
```yacc
%{
#include <stdio.h>
%}

%token ID
%%

variable: ID { 
    printf("Valid variable: %s\n", yytext); 
}
    ;

%%

int main() {
    printf("Enter variable name: ");
    yyparse();
    return 0;
}
```

### 7. Recognize String Patterns
Write a YACC Program to recognize strings 'aaab', 'abbb', 'ab' and 'a' using grammar (an b n , n>=0)

#### Simple Answer:
```yacc
%{
#include <stdio.h>
%}

%token A B
%%

string: S { printf("Valid string pattern recognized\n"); }
    ;

S: A S B
    | A B
    | A
    | /* empty */
    ;

%%

int main() {
    printf("Enter string to check pattern: ");
    yyparse();
    return 0;
}
```

### 8. Recognize Grammar an b
Write a YACC Program to recognize the grammar (an b, n>=10)

#### Simple Answer:
```yacc
%{
#include <stdio.h>
int count = 0;
%}

%token A B
%%

start: a_sequence B
    ;

a_sequence: a_sequence A { count++; }
    | A { count = 1; }
    ;

%%

int main() {
    printf("Enter string with a's followed by b: ");
    yyparse();
    if(count >= 10) {
        printf("Valid: contains at least 10 a's followed by b\n");
    } else {
        printf("Invalid: needs at least 10 a's before b, got %d\n", count);
    }
    return 0;
}
```

### 9. Arithmetic Calculator Implementation
Write a YACC Program to implement arithmetic calculator.

#### Simple Answer:
```yacc
%{
#include <stdio.h>
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

calc: calc expr '\n' { printf("= %d\n", $2); }
    | /* empty */
    ;

expr: expr '+' term { $$ = $1 + $3; }
    | expr '-' term { $$ = $1 - $3; }
    | term { $$ = $1; }
    ;

term: term '*' factor { $$ = $1 * $3; }
    | term '/' factor { 
        if($3 != 0) 
            $$ = $1 / $3; 
        else {
            printf("Division by zero\n");
            $$ = 0;
        }
      }
    | factor { $$ = $1; }
    ;

factor: '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    ;

%%

int main() {
    printf("Calculator (enter expressions ending with newline):\n");
    yyparse();
    return 0;
}
```