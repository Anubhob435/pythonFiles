# Compiler Design - Assignment 2: Implementation of Lexical Analyzer using Lex Tool

## List of Experiments

### 1. Count Characters, Words, Keywords, Numbers, Spaces, and Lines
Write a Lex Program to count the number of characters, words, keyword, number, spaces, end of lines in a given input file.

#### Simple Answer:
```lex
%{
#include <stdio.h>
int chars = 0;
int words = 0;
int keywords = 0;
int numbers = 0;
int spaces = 0;
int lines = 0;

// Define keywords
int isKeyword(char* str) {
    return (!strcmp(str, "if") || !strcmp(str, "else") || !strcmp(str, "while") ||
            !strcmp(str, "for") || !strcmp(str, "int") || !strcmp(str, "float") ||
            !strcmp(str, "char") || !strcmp(str, "return") || !strcmp(str, "void"));
}
%}

%%
[0-9]+ { 
    numbers++; 
    chars += strlen(yytext); 
}
if|else|while|for|int|float|char|return|void {
    keywords++;
    chars += strlen(yytext);
    words++;
}
[a-zA-Z_][a-zA-Z0-9_]* {
    if(!isKeyword(yytext)) {
        chars += strlen(yytext);
        words++;
    }
}
[ \t] { 
    spaces++; 
    chars++; 
}
\n {
    lines++;
    chars++;
}
. { 
    chars++; 
}
%%

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
    }
    yylex();
    printf("Characters: %d\n", chars);
    printf("Words: %d\n", words);
    printf("Keywords: %d\n", keywords);
    printf("Numbers: %d\n", numbers);
    printf("Spaces: %d\n", spaces);
    printf("Lines: %d\n", lines);
    return 0;
}
```

### 2. Count Vowels and Consonants
Write a Lex Program to count the number of vowels and consonants in a given string.

#### Simple Answer:
```lex
%{
#include <stdio.h>
#include <ctype.h>
int vowels = 0;
int consonants = 0;
%}

%%
[aeiouAEIOU] { vowels++; }
[a-zA-Z] { consonants++; }
.|\n {}
%%

int main() {
    printf("Enter a string: ");
    yylex();
    printf("Vowels: %d\n", vowels);
    printf("Consonants: %d\n", consonants);
    return 0;
}
```

### 3. Count Positive/Negative Integers and Fractions
Write a Lex Program to count no of: a) +ve and –ve integers b) +ve and –ve fractions

#### Simple Answer:
```lex
%{
#include <stdio.h>
int positive_int = 0;
int negative_int = 0;
int positive_frac = 0;
int negative_frac = 0;
%}

%%
[0-9]+ { positive_int++; }
-[0-9]+ { negative_int++; }
[0-9]+\.[0-9]+ { positive_frac++; }
-[0-9]+\.[0-9]+ { negative_frac++; }
%%

int main() {
    printf("Enter numbers: ");
    yylex();
    printf("Positive integers: %d\n", positive_int);
    printf("Negative integers: %d\n", negative_int);
    printf("Positive fractions: %d\n", positive_frac);
    printf("Negative fractions: %d\n", negative_frac);
    return 0;
}
```

### 4. Count and Remove Comment Lines in C Program
Write a Lex Program to count the no of comment line in a given C program. Also eliminate them and copy that program into separate file.

#### Simple Answer:
```lex
%{
#include <stdio.h>
FILE *output;
int comment_lines = 0;
%}

%%
"//".* { 
    comment_lines++; 
    printf("Comment removed: %s\n", yytext); 
}
"/*"[^*]*"*"+([^/][^*]*"*"+)*"/" { 
    comment_lines++; 
    printf("Block comment removed\n"); 
}
.|\n { 
    fprintf(output, "%s", yytext); 
}
%%

int main() {
    output = fopen("output.c", "w");
    yylex();
    fclose(output);
    printf("Comment lines: %d\n", comment_lines);
    return 0;
}
```

### 5. Replace scanf and printf Statements
Write a Lex Program to count the no of 'scanf' and 'printf' statements in a C program. Replace them with 'readf' and 'writef' statements respectively

#### Simple Answer:
```lex
%{
#include <stdio.h>
int scanf_count = 0;
int printf_count = 0;
%}

%%
scanf { 
    scanf_count++; 
    printf("readf"); 
}
printf { 
    printf_count++; 
    printf("writef"); 
}
.|\n { 
    printf("%s", yytext); 
}
%%

int main() {
    yylex();
    printf("\nScanf count: %d\n", scanf_count);
    printf("Printf count: %d\n", printf_count);
    return 0;
}
```

### 6. Recognize Arithmetic Expression
Write a Lex Program to recognize a valid arithmetic expression and identify the identifiers and operators present. Print them separately.

#### Simple Answer:
```lex
%{
#include <stdio.h>
%}

%%
[a-zA-Z_][a-zA-Z0-9_]* { 
    printf("Identifier: %s\n", yytext); 
}
[+\-*/] { 
    printf("Operator: %s\n", yytext); 
}
[0-9]+ { 
    printf("Number: %s\n", yytext); 
}
[ \t]+ {}
\n { 
    return 0; 
}
%%

int main() {
    printf("Enter arithmetic expression: ");
    yylex();
    return 0;
}
```

### 7. Identify Simple or Compound Sentence
Write a Lex Program to recognize whether a given sentence is simple or compound.

#### Simple Answer:
```lex
%{
#include <stdio.h>
#include <string.h>
int conjunctions = 0;
%}

%%
and|but|or|so|yet|for|nor { 
    conjunctions++; 
}
\. {
    if(conjunctions > 0) {
        printf("Compound sentence\n");
    } else {
        printf("Simple sentence\n");
    }
    conjunctions = 0;
}
.|\n {}
%%

int main() {
    printf("Enter sentence: ");
    yylex();
    return 0;
}
```

### 8. Arithmetic Calculator Implementation
Write a Lex Program to implement arithmetic calculator.

#### Simple Answer:
```lex
%{
#include <stdio.h>
#include <stdlib.h>
double result = 0;
double current_num = 0;
char operation = '+';
%}

%%
[0-9]+ {
    current_num = atof(yytext);
    switch(operation) {
        case '+': result += current_num; break;
        case '-': result -= current_num; break;
        case '*': result *= current_num; break;
        case '/': if(current_num != 0) result /= current_num; break;
    }
}
"+" { operation = '+'; }
"-" { operation = '-'; }
"*" { operation = '*'; }
"/" { operation = '/'; }
"=" {
    printf("Result: %.2f\n", result);
    result = 0;
    operation = '+';
}
[ \t] {}
\n { return 0; }
%%

int main() {
    printf("Arithmetic Calculator (use '=' to evaluate): ");
    yylex();
    return 0;
}
```