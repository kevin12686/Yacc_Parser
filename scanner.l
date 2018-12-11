%{
	#include "y.tab.h"
%}
%option noyywrap
%%
[0-9]+	{yylval = atoi(yytext);	return(Number);}
"+" {return Plus;}
"-" {return Minus;}
"*" {return Multiply;}
"/" {return Divide;}
"(" {return Left;}
")" {return Right;}
"\n" {return '\n';}
. {}
%%