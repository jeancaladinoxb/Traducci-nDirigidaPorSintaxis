## Proyecto Traducción Dirigida por Sintaxis

Para el siguiente proyecto se desarrolló un traductor básico dirigido por sintaxis que permite el desarrollo de operaciones aritméticas básicas como sumas, resta, multiplicación y división. Se consideró la implementación de un esquema de traducción dirigido por la sintaxis, en donde se implementó una gramática independiente del contexto. El proyecto se desarrolló en fases tales como: Diseño de la gramática, definición de atributos, el cálculo de conjuntos de primeros, segundos y producción, la generación de un AST decorado, tabla de símbolos como lo propone la definición dirigida por la sintaxis, el uso de la gramática de atributos y por último el esquema de traducción dirigido por sintaxis.

## Fase 1 Gramática 

Para la gramática de este proyecto de operaciones aritméticas, se consideró la siguiente:

E -> E + T | E - T | T

T -> T * F | T / F | F

F -> (E) | num 


Donde se consideró que E es una expresión que representa las sumas y restas, T es un término para multiplicaciones y divisiones, F representará el factor de números u operaciones en paréntesis y num será un número como token terminal. A su vez es de considerar que esta gramática permite el respeto a la precedencia de operaciones.

## Fase 2 Atributos

Para la fase de atributos se implementaron los siguientes con respecto a la gramáticas establecida con anterioridad:

E.val: Para la evaluación de operaciones de suma y resta.

T.val: Para la evaluación de operaciones de multiplicación y división.

Num.val: Para el valor léxico del número leído.

## Fase 3 Conjunto de Primeros, Segundos y preducción 

Los conjuntos de primeros, segundos y de predicción generados para la gramática base se consideraron tales como:

Primeros:

F -> {'(', num }

T -> {'(', num }

E -> {'(', num }

Segundos: 

E -> {')', $}

T -> {'+', '-', ')', $}

F -> {'*', '/', '+', '-', ')', $}

Predicción:

E → E + T	{ (, num }

E → E - T	{ (, num }

E → T	{ (, num }

T → T * F	{ (, num }

T → T / F	{ (, num }

T → F	{ (, num }

F → ( E )	{ ( }

F → num	{ num }