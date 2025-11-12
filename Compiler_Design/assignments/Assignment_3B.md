# Compiler Design - Assignment 3B: YACC Specification for Syntactic Categories

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
    char* keywords[] = {"int", "char", "float", "double", "if", "else", "while", "for", "return", "void", NULL};
    for(int i = 0; keywords[i] != NULL; i++) {
        if(strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}
%}

alpha [a-zA-Z]
digit [0-9]
identifier {alpha}({alpha}|{digit}|_)*

%%
{identifier} {
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
extern int yylex();
void yyerror(char *s);
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

stmt: expr { printf("Valid expression\n"); }
    ;

expr: expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '(' expr ')'
    | NUMBER
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Invalid expression: %s\n", s);
}

int main() {
    printf("Enter arithmetic expression: ");
    yyparse();
    return 0;
}
```

### 3. Recognize Nested IF Statements
Write a YACC Program to recognize nested IF control statements and display the levels of nesting.

#### Simple Answer:
```yacc
%{
#include <stdio.h>
#include <stdlib.h>

int nesting_level = 0;

extern int yylex();
void yyerror(char *s);
%}

%token IF THEN ELSE ID '(' ')'
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE
%%

stmt: matched_stmt
    | unmatched_stmt
    ;

matched_stmt: IF '(' ID ')' matched_stmt ELSE matched_stmt { 
                printf("IF-ELSE at nesting level %d\n", nesting_level); 
              }
            | other_statement
            ;

unmatched_stmt: IF '(' ID ')' stmt { 
                  nesting_level++;
                  printf("IF at nesting level %d\n", nesting_level); 
                }
              | IF '(' ID ')' matched_stmt ELSE unmatched_stmt { 
                  printf("Mixed IF-ELSE at nesting level %d\n", nesting_level); 
                }
              ;

other_statement: ID '=' ID ';'
               | '{' stmt_list '}'
               ;

stmt_list: stmt
         | stmt_list stmt
         ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Parse error: %s\n", s);
}

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
extern int yylex();
void yyerror(char *s);
%}

%token NUMBER ID
%left '+' '-'
%left '*' '/'
%%

stmt: expr { printf("Syntax is correct\n"); }
    ;

expr: expr '+' term
    | expr '-' term
    | term
    ;

term: term '*' factor
    | term '/' factor
    | factor
    ;

factor: '(' expr ')'
      | NUMBER
      | ID
      ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Syntax error: %s\n", s);
}

int main() {
    printf("Enter expression to check: ");
    yyparse();
    return 0;
}
```

### 5. Evaluate Arithmetic Expression
Write a YACC Program to evaluate an arithmetic expression involving operating +, -, * and /

#### Simple Answer:
```yacc
%{
#include <stdio.h>
extern int yylex();
void yyerror(char *s);
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

stmt: expr { printf("Result: %d\n", $1); }
    ;

expr: expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { 
        if($3 != 0) 
            $$ = $1 / $3; 
        else {
            printf("Error: Division by zero\n");
            $$ = 0;
        }
      }
    | '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Evaluation error: %s\n", s);
}

int main() {
    printf("Enter arithmetic expression to evaluate: ");
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
#include <ctype.h>
extern int yylex();
void yyerror(char *s);
%}

%token LETTER DIGIT
%union {
    char value[100];
}
%token <value> ID
%%

variable: ID { 
    printf("Valid variable: %s\n", $1); 
}
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Invalid variable: %s\n", s);
}

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
#include <string.h>

int a_count = 0, b_count = 0;
%}

%token A B
%%

start: S { 
    if((a_count == 1 && b_count == 1) ||  // 'ab'
       (a_count == 3 && b_count == 1) ||  // 'aaab' 
       (a_count == 1 && b_count == 3) ||  // 'abbb'
       (a_count == 1 && b_count == 0)) {  // 'a'
        printf("Valid string pattern recognized\n");
    } else {
        printf("Invalid pattern\n");
    }
}
    ;

S: A_sequence B_sequence
    | A_only
    ;

A_sequence: A_sequence A { a_count++; }
    | A { a_count = 1; }
    ;

B_sequence: B_sequence B { b_count++; }
    | B { b_count = 1; }
    ;

A_only: A { a_count = 1; b_count = 0; }
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
int n_count = 0;
%}

%token A B
%%

start: A_sequence B
    {
        if(n_count >= 10) {
            printf("Valid: grammar a^n b where n >= 10\n");
        } else {
            printf("Invalid: grammar a^n b where n must be >= 10, got n = %d\n", n_count);
        }
    }
    ;

A_sequence: A_sequence A 
    { n_count++; }
    | A 
    { n_count = 1; }
    ;

%%

int main() {
    printf("Enter string in format a...ab (at least 10 a's): ");
    yyparse();
    return 0;
}
```

### 9. Arithmetic Calculator Implementation
Write a YACC Program to implement arithmetic calculator.

#### Simple Answer:
```yacc
%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
void yyerror(char *s);
%}

%token NUMBER
%left '+' '-'
%left '*' '/'
%%

lines: lines line
     | /* empty */
     ;

line: expr '\n' { printf("= %d\n", $1); }
    | '\n' { }
    | error '\n' { yyerrok; }
    ;

expr: expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { 
        if($3 != 0) 
            $$ = $1 / $3; 
        else {
            printf("Error: Division by zero\n");
            $$ = 0;
        }
      }
    | '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Calculator (type expressions followed by Enter):\n");
    yyparse();
    return 0;
}
```