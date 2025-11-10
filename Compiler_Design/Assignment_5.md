# Compiler Design - Assignment 5: Compiler Backend and Storage Allocation

## PROJECT

### 1. Stack Storage Allocation Strategies
Write a C program to implement Stack storage allocation strategies.

#### Simple Answer:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STACK_SIZE 1000
#define MAX_SCOPE_LEVELS 100

typedef struct {
    char name[50];
    int value;
    int size;
    int offset;
} Variable;

typedef struct {
    Variable variables[100];
    int var_count;
    int base_address;
} ActivationRecord;

ActivationRecord stack[MAX_SCOPE_LEVELS];
int stack_top = -1;

void init() {
    stack_top = -1;
}

void push_scope() {
    stack_top++;
    stack[stack_top].var_count = 0;
    if (stack_top == 0) {
        stack[stack_top].base_address = 0;
    } else {
        stack[stack_top].base_address = stack[stack_top-1].base_address + 
                                       (sizeof(int) * stack[stack_top-1].var_count);
    }
    printf("Entering scope level %d\n", stack_top);
}

void pop_scope() {
    if (stack_top >= 0) {
        printf("Exiting scope level %d\n", stack_top);
        stack_top--;
    }
}

void add_variable(char* name, int size) {
    if (stack_top >= 0) {
        strcpy(stack[stack_top].variables[stack[stack_top].var_count].name, name);
        stack[stack_top].variables[stack[stack_top].var_count].size = size;
        stack[stack_top].variables[stack[stack_top].var_count].value = 0;
        stack[stack_top].variables[stack[stack_top].var_count].offset = 
            stack[stack_top].base_address + (stack[stack_top].var_count * sizeof(int));
        stack[stack_top].var_count++;
        printf("Added variable '%s' at offset %d in scope %d\n", 
               name, stack[stack_top].variables[stack[stack_top].var_count-1].offset, stack_top);
    }
}

int find_variable(char* name, int* scope_level, int* offset) {
    for (int i = stack_top; i >= 0; i--) {
        for (int j = 0; j < stack[i].var_count; j++) {
            if (strcmp(stack[i].variables[j].name, name) == 0) {
                *scope_level = i;
                *offset = stack[i].variables[j].offset;
                return j;
            }
        }
    }
    return -1;
}

void set_variable_value(char* name, int value) {
    int scope_level, offset, var_idx;
    var_idx = find_variable(name, &scope_level, &offset);
    if (var_idx != -1) {
        stack[scope_level].variables[var_idx].value = value;
        printf("Set variable '%s' to %d\n", name, value);
    } else {
        printf("Variable '%s' not found\n", name);
    }
}

int get_variable_value(char* name) {
    int scope_level, offset, var_idx;
    var_idx = find_variable(name, &scope_level, &offset);
    if (var_idx != -1) {
        return stack[scope_level].variables[var_idx].value;
    } else {
        printf("Variable '%s' not found\n", name);
        return -1;
    }
}

void display_stack() {
    printf("\nCurrent Stack State:\n");
    for (int i = 0; i <= stack_top; i++) {
        printf("Scope Level %d (Base Address: %d):\n", i, stack[i].base_address);
        for (int j = 0; j < stack[i].var_count; j++) {
            printf("  %s: offset=%d, value=%d\n", 
                   stack[i].variables[j].name, 
                   stack[i].variables[j].offset, 
                   stack[i].variables[j].value);
        }
    }
}

int main() {
    init();
    
    push_scope();  // Global scope
    add_variable("x", sizeof(int));
    add_variable("y", sizeof(int));
    
    push_scope();  // Local scope
    add_variable("a", sizeof(int));
    add_variable("b", sizeof(int));
    
    set_variable_value("x", 10);
    set_variable_value("y", 20);
    set_variable_value("a", 30);
    set_variable_value("b", 40);
    
    display_stack();
    
    printf("\nValue of x: %d\n", get_variable_value("x"));
    printf("Value of a: %d\n", get_variable_value("a"));
    
    pop_scope();  // Exit local scope
    printf("\nAfter exiting local scope:\n");
    display_stack();
    
    return 0;
}
```

### 2. DAG Implementation
Write a C program to implement DAG (Directed Acyclic Graph).

#### Simple Answer:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NODES 100

typedef struct DAGNode {
    int id;
    char label[20];
    int type;  // 0 for leaf, 1 for operator
    struct DAGNode* left;
    struct DAGNode* right;
} DAGNode;

DAGNode* nodes[MAX_NODES];
int node_count = 0;

DAGNode* create_node(char* label, int type) {
    DAGNode* new_node = (DAGNode*)malloc(sizeof(DAGNode));
    new_node->id = node_count;
    strcpy(new_node->label, label);
    new_node->type = type;
    new_node->left = NULL;
    new_node->right = NULL;
    nodes[node_count] = new_node;
    node_count++;
    return new_node;
}

void print_dag_recursive(DAGNode* node, int visited[]) {
    if (node == NULL || visited[node->id]) return;
    
    visited[node->id] = 1;
    
    if (node->left) print_dag_recursive(node->left, visited);
    if (node->right) print_dag_recursive(node->right, visited);
    
    if (node->type == 1) { // operator
        char left_label[20] = "NULL", right_label[20] = "NULL";
        if (node->left) strcpy(left_label, node->left->label);
        if (node->right) strcpy(right_label, node->right->label);
        printf("Node %d: %s [%s %s %s]\n", node->id, node->label, left_label, node->label, right_label);
    } else { // leaf
        printf("Node %d: %s [leaf]\n", node->id, node->label);
    }
}

void print_dag(DAGNode* root) {
    int visited[MAX_NODES] = {0};
    printf("DAG Structure:\n");
    print_dag_recursive(root, visited);
}

// Check if two nodes are equivalent (for DAG optimization)
int nodes_equal(DAGNode* a, DAGNode* b) {
    if (a == NULL && b == NULL) return 1;
    if (a == NULL || b == NULL) return 0;
    return (strcmp(a->label, b->label) == 0 && a->type == b->type);
}

// Find existing node that matches the given parameters
DAGNode* find_existing_node(char* label, int type, DAGNode* left, DAGNode* right) {
    for (int i = 0; i < node_count; i++) {
        if (nodes[i] && strcmp(nodes[i]->label, label) == 0 && 
            nodes[i]->type == type && nodes_equal(nodes[i]->left, left) && 
            nodes_equal(nodes[i]->right, right)) {
            return nodes[i];
        }
    }
    return NULL;
}

// Build example DAG for expression: a + b * c + a
int main() {
    // Create leaf nodes
    DAGNode* a1 = create_node("a", 0);  // variable 'a'
    DAGNode* b = create_node("b", 0);   // variable 'b'
    DAGNode* c = create_node("c", 0);   // variable 'c'
    
    // Create operator nodes with DAG optimization (reusing 'a')
    DAGNode* mult_node = create_node("*", 1);
    mult_node->left = b;
    mult_node->right = c;
    
    DAGNode* add_node1 = create_node("+", 1);
    add_node1->left = a1;
    add_node1->right = mult_node;
    
    DAGNode* add_node2 = create_node("+", 1);
    add_node2->left = add_node1;
    add_node2->right = a1;  // Reuse the same 'a' node (DAG property)
    
    print_dag(add_node2);
    
    printf("\nDAG Nodes created: %d\n", node_count);
    return 0;
}
```

### 3. 8086 Assembly Code Generation
Implement the back end of the compiler which takes the three address code and produces the 8086 assembly language instructions that can be assembled and run using a 8086 assembler. The target assembly instructions can be simple move, add, sub, jump. Also simple addressing modes are used.

#### Simple Answer:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_CODE 100
#define MAX_VAR 100

typedef struct {
    char result[20];
    char arg1[20];
    char arg2[20];
    char op[10];
} TAC;

TAC code[MAX_CODE];
char variables[MAX_VAR][20];
int var_count = 0;
int code_count = 0;

int is_variable(char* name) {
    if (name[0] >= '0' && name[0] <= '9') return 0;  // It's a constant
    if (strcmp(name, "0") == 0) return 0;  // Special case for 0
    return 1;  // It's a variable
}

void add_variable(char* name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(variables[i], name) == 0) {
            return;  // Already exists
        }
    }
    strcpy(variables[var_count], name);
    var_count++;
}

void parse_tac_line(char* line) {
    // Simple parser for three address code
    // Format: result = arg1 op arg2  OR  result = arg1
    char temp[200];
    strcpy(temp, line);
    
    // Find '='
    char* pos = strchr(temp, '=');
    if (!pos) return;
    
    *pos = '\0';
    char* result = temp;
    char* rest = pos + 1;
    
    // Trim whitespace
    while (*result == ' ' || *result == '\t') result++;
    char* result_end = result + strlen(result) - 1;
    while (result_end > result && (*result_end == ' ' || *result_end == '\t')) result_end--;
    *(result_end + 1) = '\0';
    
    // Process the right side
    char* operand1 = rest;
    while (*operand1 == ' ' || *operand1 == '\t') operand1++;
    
    // Look for operators
    char* op_pos = NULL;
    if ((op_pos = strstr(operand1, " + ")) != NULL) {
        strcpy(code[code_count].op, "+");
        *op_pos = '\0';
        char* operand2 = op_pos + 3;
        
        strcpy(code[code_count].result, result);
        strcpy(code[code_count].arg1, operand1);
        while (*operand2 == ' ' || *operand2 == '\t') operand2++;
        char* end = operand2 + strlen(operand2) - 1;
        while (end > operand2 && (*end == ' ' || *end == '\t')) end--;
        *(end + 1) = '\0';
        strcpy(code[code_count].arg2, operand2);
    }
    else if ((op_pos = strstr(operand1, " - ")) != NULL) {
        strcpy(code[code_count].op, "-");
        *op_pos = '\0';
        char* operand2 = op_pos + 3;
        
        strcpy(code[code_count].result, result);
        strcpy(code[code_count].arg1, operand1);
        while (*operand2 == ' ' || *operand2 == '\t') operand2++;
        char* end = operand2 + strlen(operand2) - 1;
        while (end > operand2 && (*end == ' ' || *end == '\t')) end--;
        *(end + 1) = '\0';
        strcpy(code[code_count].arg2, operand2);
    }
    else if ((op_pos = strstr(operand1, " * ")) != NULL) {
        strcpy(code[code_count].op, "*");
        *op_pos = '\0';
        char* operand2 = op_pos + 3;
        
        strcpy(code[code_count].result, result);
        strcpy(code[code_count].arg1, operand1);
        while (*operand2 == ' ' || *operand2 == '\t') operand2++;
        char* end = operand2 + strlen(operand2) - 1;
        while (end > operand2 && (*end == ' ' || *end == '\t')) end--;
        *(end + 1) = '\0';
        strcpy(code[code_count].arg2, operand2);
    }
    else if ((op_pos = strstr(operand1, " / ")) != NULL) {
        strcpy(code[code_count].op, "/");
        *op_pos = '\0';
        char* operand2 = op_pos + 3;
        
        strcpy(code[code_count].result, result);
        strcpy(code[code_count].arg1, operand1);
        while (*operand2 == ' ' || *operand2 == '\t') operand2++;
        char* end = operand2 + strlen(operand2) - 1;
        while (end > operand2 && (*end == ' ' || *end == '\t')) end--;
        *(end + 1) = '\0';
        strcpy(code[code_count].arg2, operand2);
    }
    else {
        // Assignment: result = arg1
        strcpy(code[code_count].result, result);
        strcpy(code[code_count].arg1, operand1);
        strcpy(code[code_count].arg2, "");
        strcpy(code[code_count].op, "=");
        
        while (*operand1 == ' ' || *operand1 == '\t') operand1++;
        char* end = operand1 + strlen(operand1) - 1;
        while (end > operand1 && (*end == ' ' || *end == '\t')) end--;
        *(end + 1) = '\0';
    }
    
    // Add variables to the list
    if (is_variable(code[code_count].result)) add_variable(code[code_count].result);
    if (is_variable(code[code_count].arg1)) add_variable(code[code_count].arg1);
    if (is_variable(code[code_count].arg2)) add_variable(code[code_count].arg2);
    
    code_count++;
}

void generate_8086_code() {
    printf("8086 Assembly Code:\n");
    printf("DATA SEGMENT\n");
    for (int i = 0; i < var_count; i++) {
        printf("    %s DW ?\n", variables[i]);
    }
    printf("DATA ENDS\n\n");
    
    printf("CODE SEGMENT\n");
    printf("ASSUME CS:CODE, DS:DATA\n");
    printf("START:\n");
    printf("    MOV AX, DATA\n");
    printf("    MOV DS, AX\n\n");
    
    for (int i = 0; i < code_count; i++) {
        if (strcmp(code[i].op, "=") == 0) {
            // Assignment: result = arg1
            if (is_variable(code[i].arg1)) {
                printf("    MOV AX, %s\n", code[i].arg1);
                printf("    MOV %s, AX\n", code[i].result);
            } else {
                // Constant assignment
                printf("    MOV AX, %s\n", code[i].arg1);
                printf("    MOV %s, AX\n", code[i].result);
            }
        }
        else if (strcmp(code[i].op, "+") == 0) {
            // Addition: result = arg1 + arg2
            printf("    MOV AX, %s\n", code[i].arg1);
            printf("    ADD AX, %s\n", code[i].arg2);
            printf("    MOV %s, AX\n", code[i].result);
        }
        else if (strcmp(code[i].op, "-") == 0) {
            // Subtraction: result = arg1 - arg2
            printf("    MOV AX, %s\n", code[i].arg1);
            printf("    SUB AX, %s\n", code[i].arg2);
            printf("    MOV %s, AX\n", code[i].result);
        }
        else if (strcmp(code[i].op, "*") == 0) {
            // Multiplication: result = arg1 * arg2
            printf("    MOV AX, %s\n", code[i].arg1);
            printf("    MOV BX, %s\n", code[i].arg2);
            printf("    IMUL BX\n");  // AX = AX * BX
            printf("    MOV %s, AX\n", code[i].result);
        }
        else if (strcmp(code[i].op, "/") == 0) {
            // Division: result = arg1 / arg2
            printf("    MOV AX, %s\n", code[i].arg1);
            printf("    MOV BX, %s\n", code[i].arg2);
            printf("    CWD\n");        // Sign extend AX to DX:AX
            printf("    IDIV BX\n");    // DX:AX / BX, result in AX, remainder in DX
            printf("    MOV %s, AX\n", code[i].result);
        }
    }
    
    printf("\n    MOV AH, 4CH\n");
    printf("    INT 21H\n");
    printf("CODE ENDS\n");
    printf("END START\n");
}

int main() {
    // Sample three address code
    parse_tac_line("t1 = a + b");
    parse_tac_line("t2 = c * d");
    parse_tac_line("t3 = t1 - t2");
    parse_tac_line("result = t3");
    
    printf("Three Address Code:\n");
    for (int i = 0; i < code_count; i++) {
        if (strcmp(code[i].op, "=") == 0 && strlen(code[i].arg2) == 0) {
            printf("    %s = %s\n", code[i].result, code[i].arg1);
        } else if (strcmp(code[i].op, "=") == 0) {
            printf("    %s = %s %s %s\n", code[i].result, code[i].arg1, code[i].op, code[i].arg2);
        } else {
            printf("    %s = %s %s %s\n", code[i].result, code[i].arg1, code[i].op, code[i].arg2);
        }
    }
    printf("\n");
    
    generate_8086_code();
    
    return 0;
}
```