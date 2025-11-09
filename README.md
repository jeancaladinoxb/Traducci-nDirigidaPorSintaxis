## Proyecto Traducción Dirigida por Sintaxis

Para el siguiente proyecto se desarrolló un traductor básico dirigido por sintaxis que permite el desarrollo de operaciones aritméticas básicas como sumas, resta, multiplicación y división. Se consideró la implementación de un esquema de traducción dirigido por la sintaxis, en donde se implementó una gramática independiente del contexto. El proyecto se desarrolló en fases tales como: Diseño de la gramática, definición de atributos, el cálculo de conjuntos de primeros, segundos y producción, la generación de un AST decorado, tabla de símbolos como lo propone la definición dirigida por la sintaxis, el uso de la gramática de atributos y por último el esquema de traducción dirigido por sintaxis.

## Fase 1 Gramática 

Para la gramática de este proyecto de operaciones aritméticas, se consideró la siguiente:

E -> E + T | E - T | T

T -> T * F | T / F | F

F -> (E) | num 

En adición se consideró la siguiente derivación para una gramática de tipo LL(1)

E  → T E'

E' → + T E' | - T E' | ε

T  → F T'

T' → * F T' | / F T' | ε

F  → (E) | num

Donde se consideró que E es una expresión que representa las sumas y restas, T es un término para multiplicaciones y divisiones, F representará el factor de números u operaciones en paréntesis y num será un número como token terminal. A su vez es de considerar que esta gramática permite el respeto a la precedencia de operaciones.

## Fase 2 Atributos

Para la fase de atributos se implementaron los siguientes con respecto a la gramáticas establecida con anterioridad:

E	.val	Valor total de la expresión

E'	.inh, .val	Valor acumulado de sumas/restas

T	.val	Valor de un término (multiplicaciones/divisiones)

T'	.inh, .val	Valor acumulado de productos/divisiones

F	.val	Valor de un número o subexpresión (E)

## Fase 3 Conjunto de Primeros, Segundos y preducción 

Los conjuntos de primeros, segundos y de predicción generados para la gramática base se consideraron tales como:

Primeros:

E  ->	{ (, num }

E' ->	{ +, -, ε }

T  ->	{ (, num }

T' ->	{ *, /, ε }

F  ->	{ (, num }

Segundos: 

E  ->	{ ), $ }

E' ->	{ ), $ }

T  ->	{ +, -, ), $ }

T' ->	{ +, -, ), $ }

F  ->	{ *, /, +, -, ), $ }

Predicción:

E -> T E'	{ (, num }

E' -> + T E'	{ + }

E' -> - T E'	{ - }

E' -> ε	{ ), $ }

T -> F T'	{ (, num }

T' -> * F T'	{ * }

T' -> / F T'	{ / }

T' -> ε	{ +, -, ), $ }

F -> (E)	{ ( }

F -> num	{ num }

## Fase 4 (Árbol decorado)

Para la creación del árbol se decidió la derivación de la gramática para un analizador de tipo LL(1), quedando de la siguiente forma:

E  → T E'

E' → + T E' | - T E' | ε

T  → F T'

T' → * F T' | / F T' | ε

F  → (E) | num

En la siguiente imagen se puede observar el árbol decorado para la siguiente operación ejemplo: 10 - 2 * (3 + 1)

![Arbol](Imagenes/arbol.png)

## Fase 5 Tabla de símbolos

El sistema por consola creará una tabla de símbolos de acuerdo a las operaciones formadas o ingresadas a través de un txt y se verá de la siguiente manera:

Tabla de Símbolos:

  resultado_1 -> tipo: float, valor: 11.0

  resultado_2 -> tipo: float, valor: 21.0

  resultado_3 -> tipo: float, valor: 8.0

  resultado_4 -> tipo: float, valor: 2.0

## Fase 6 Gramática de atributos 


E → T E'
    { E'.inh = T.val
      E.val  = E'.val }

E' → + T E1'
    { E1'.inh = E'.inh + T.val
      E'.val  = E1'.val }

T → F T'
    { T'.inh = F.val
      T.val  = T'.val }

F → num
    { F.val = num.lexema }

## Fase 7 ETDS

Producción      Acciones Semánticas

`E → T E'`    `{ E'.inh := T.val; E.val := E'.val }`   
         
`E' → + T E'`  `{ E1'.inh := E'.inh + T.val; E'.val := E1'.val }`

`E' → - T E'`  `{ E1'.inh := E'.inh - T.val; E'.val := E1'.val }`
 
`E' → ε`       `{ E'.val := E'.inh }` 
                            
`T → F T'`     `{ T'.inh := F.val; T.val := T'.val }`  
           
`T' → * F T'`  `{ T1'.inh := T'.inh * F.val; T'.val := T1'.val }` 

`T' → / F T'`  `{ T1'.inh := T'.inh / F.val; T'.val := T1'.val }` 

`T' → ε`       `{ T'.val := T'.inh }`     
                        
`F → (E)`      `{ F.val := E.val }`   
                            
`F → num`      `{ F.val := num.valor }` 

## Pasos para ejecutar el código

Pasos para ejecutar el proyecto del traductor dirigido por la sintaxis desde consola o terminal

1. Verificar que Python esté instalado

   * Abre la terminal o consola.
   * Escribe:
     python --version
     Si aparece una versión 3.x.x, significa que Python está instalado correctamente.
   * Si no aparece, debes descargarlo desde [https://www.python.org/downloads/](https://www.python.org/downloads/) e instalarlo.

2. Crear una carpeta para el proyecto

   * Crea una carpeta en el escritorio o en cualquier ubicación, por ejemplo:
     TraductorSintaxis
   * Dentro de esa carpeta guarda dos archivos:
     a) El archivo del código Python (por ejemplo traductor_sintaxis.py).
     b) Un archivo de texto llamado expresiones.txt.

3. Preparar el archivo expresiones.txt

   * En este archivo se colocan las expresiones aritméticas que el programa debe analizar, una por línea.
   * Ejemplo de contenido:
     3 + 4 * 2
     (2 + 5) * 3
     8 / 4 + 6
     10 - 2 * (3 + 1)

4. Instalar las librerías necesarias

   * Abre la terminal en la carpeta del proyecto.
   * Ejecuta los siguientes comandos:
     pip install graphviz
     pip install networkx
     pip install matplotlib
   * Si usas Windows, puede ser necesario instalar también el programa Graphviz desde
     [https://graphviz.org/download/](https://graphviz.org/download/)
     Durante la instalación, asegúrate de marcar la opción “Add Graphviz to the system PATH”.

5. Verificar que Graphviz funcione

   * En la consola escribe:
     dot -V
     Si muestra una versión, la instalación está correcta.

6. Ejecutar el programa

   * En la terminal, estando dentro de la carpeta del proyecto, escribe:
     python traductor_sintaxis.py
   * El programa leerá las expresiones del archivo expresiones.txt, analizará cada una, generará el árbol decorado y mostrará los resultados en consola.
   * Por cada expresión, se abrirá automáticamente una ventana con el árbol decorado generado por Graphviz.
   * También se guardarán las imágenes de los árboles en la misma carpeta del proyecto con nombres del tipo arbol_xxxxx.png.

7. Revisar la salida en consola

   * Se mostrará el resultado de cada expresión evaluada.
   * Al final se imprimirá la tabla de símbolos con los resultados acumulados de cada operación.

8. Archivos generados

   * arbol_XXXXX.png: imágenes de los árboles decorados de cada expresión.
   * tabla_simbolos.txt (si activas la opción de guardado en el código): archivo con la tabla de símbolos.

9. Para ejecutar nuevamente con otras expresiones

   * Modifica el contenido de expresiones.txt.
   * Guarda los cambios y vuelve a ejecutar:
     python traductor_sintaxis.py

                          


