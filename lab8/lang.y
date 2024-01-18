%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%token IDENTIFIER INT_CONST STRING_CONST CHAR_CONST BOOL_CONST
%token READ PRINT RETURN IF ELSE FOR WHILE
%token INT STRING CHAR BOOL
%token VAR COLON SEMICOLON COMMA LSQUARE RSQUARE LPAREN RPAREN
%token TRUE FALSE
%token EQUAL PLUS MINUS TIMES DIVIDE MOD LT GT LE GE EQ NE AND OR NOT
%token TAB

%union {
    char* string_val;
    int int_val;
}

%token <string_val> STRING_CONSTANT
%token <int_val> INT_CONSTANT

%type <string_val> identifier const string_constant
%type <int_val> expression

%%

program: statement_list

statement_list: statement
              | statement_list statement

statement: declaration_stmt
         | input_stmt
         | output_stmt
         | return_stmt
         | assign_stmt
         | if_stmt
         | for_stmt
         | while_stmt

declaration_stmt: VAR identifiers_list COLON type SEMICOLON { /* Semantic action for declaration statement */ }

identifiers_list: identifier
               | identifier COMMA identifiers_list
               | identifier LSQUARE RSQUARE
               | identifier LSQUARE RSQUARE COMMA identifiers_list

type: INT
    | STRING
    | CHAR
    | BOOL

input_stmt: READ LPAREN identifier RPAREN SEMICOLON { /* Semantic action for input statement */ }

output_stmt: PRINT LPAREN identifier RPAREN SEMICOLON { /* Semantic action for output statement */ }

return_stmt: RETURN identifier SEMICOLON { /* Semantic action for return statement */ }
           | RETURN TRUE SEMICOLON { /* Semantic action for returning true */ }
           | RETURN FALSE SEMICOLON { /* Semantic action for returning false */ }
           | RETURN const SEMICOLON { /* Semantic action for returning a constant */ }

assign_stmt: identifier EQUAL expression SEMICOLON { /* Semantic action for assignment statement */ }

const: INT_CONSTANT { /* Semantic action for integer constant */ }
     | STRING_CONSTANT { /* Semantic action for string constant */ }
     | CHAR_CONST { /* Semantic action for character constant */ }
     | TRUE { /* Semantic action for true */ }
     | FALSE { /* Semantic action for false */ }

expression: identifier { /* Semantic action for identifier in expression */ }
          | const { /* Semantic action for constant in expression */ }
          | expression op expression { /* Semantic action for binary operation in expression */ }
          | op expression { /* Semantic action for unary operation in expression */ }
          | LPAREN expression RPAREN { /* Semantic action for parenthesized expression */ }

op: PLUS | MINUS | TIMES | DIVIDE | MOD | LT | GT | LE | GE | EQ | NE | AND | OR | NOT { /* Semantic action for operators */ }

block: TAB statement
     | TAB statement_list

if_stmt: IF LPAREN expression RPAREN COLON block %prec LOWER_THAN_ELSE { /* Semantic action for if statement */ }
       | IF LPAREN expression RPAREN COLON block ELSE COLON block { /* Semantic action for if-else statement */ }

for_stmt: FOR LPAREN assign_stmt SEMICOLON expression SEMICOLON assign_stmt RPAREN COLON block { /* Semantic action for for statement */ }

while_stmt: WHILE LPAREN expression RPAREN COLON block { /* Semantic action for while statement */ }

%%

int main() {
    yyparse();
    return 0;
}

int yyerror(const char *msg) {
    fprintf(stderr, "Error: %s\n", msg);
    return 1;
}
