%{
	#include <stdio.h>
%}
%token Number Plus Minus Multiply Divide Left Right
%left Plus Minus
%left Multiply Divide
%left UMinus
%start input
%%

input: input stat '\n' | /* Empty */ ;
stat: expr {printf("Result: %d\n\n", $1);} | /* Empty */ ;
expr: Left expr Right {$$ = $2;}
| expr Plus expr {$$ = $1 + $3; printf("%d Plus %d = %d\n", $1, $3, $1 + $3);}
| expr Minus expr {$$ = $1 - $3; printf("%d Minus %d = %d\n", $1, $3, $1 - $3);}
| expr Multiply expr {$$ = $1 * $3; printf("%d Multiply %d = %d\n", $1, $3, $1 * $3);}
| expr Divide expr {$$ = $1 / $3; printf("%d Divide %d = %d\n", $1, $3, $1 / $3);}
| Minus expr %prec UMinus {$$ = - $2;}
| Number {$$ = $1;}
;

%%
int main(){
	yyparse();
	return 0;
}

int yyerror(char *msg){
	printf("Error: %s\n", msg);
}