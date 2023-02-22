# LSD: Lindenmayer-System-Drawing
## Lenguaje de dominio específico para la visualización de Sistemas-L

LSD es un DSL :) que tiene como objetivo la visualización de Sistemas-L. Un Sistema-L o un sistema de Lindenmayer es una gramática formal (un conjunto de reglas y símbolos) principalmente utilizados para modelar el proceso de crecimiento de las plantas; puede modelar también la morfología de una variedad de organismos. Además pueden utilizarse para generar fractales autosimilares como los sistemas de función iterada. Los sistemas-L fueron introducidos y desarrollados en 1968 por el biólogo y botánico teórico húngaro Aristid Lindenmayer.

## Sintaxis del lenguaje
Lenguaje de tipado estático, no orientado a objetos.

### Tipos internos del lenguaje:

`lsys` - representa un Sistema-L
`int` - representa un entero de 32 bits
`float` - representa un flotante
`string` - representa una cadena de caracteres (Siempre en mayúscula)
`brush` - representa una brocha para dibujar
`canvas` - representa un lienzo para dibujar
`color` - representa un color (en hexadecimal)
`bool` - true | false


### Palabras reservadas:
-`canvas`     
-`draw`     
-`brush`      
-`lsys`    
-`axiom`   
-`color`     
-`size`     
-`speed`      
-`high`       
-`width`      
-`if`         
-`else`      
-`bool`       
-`true`      
-`false`      
-`int`        
-`string`     
-`addRule`   
-`repeat` 

### Declaración de un Sistema-l

**Definición:**

```
lsys <nombre_del_sistema> {
    axiom: <caracter_representante>,
    <parte_derecha_de_la_regla> => <parte_izquierda_de_la_regla>,
    ...
    <parte_derecha_de_la_regla> => <parte_izquierda_de_la_regla>,
}

```
***Ejemplo:**

```
lsys leaf {
    axiom : A,
    F => >F<,
    A => F[+X]FB,
    B => F[-Y]FA,
    X => A,
    Y => B
};

```
#### Símbolos permitidos en la declaración de reglas

| Símbolo       | Acción asociada a la brocha |
| ------------- | ------------------------------------ |
| f             |  Se mueve hacia adelante pintando    |
| g             |  Se mueve hacia adelante sin pintar  |
| +             |  Girar a la izquierda el ángulo indicado  |
| -             |  Girar a la derecha el ángulo indicado  |
| [             |  Agrega a la pila el estado actual del dibujo (posición de la brocha y ángulo de rotación) |
| ]            |  Saca a la pila el último estado y lo toma como actual |
| #            |  Incrementa el grosor de la línea |
| !            |  Decrementa el grosor de la linea |
| >            |  Multiplica el largo de la línea por un factor |
| <            |  Divide el largo de la línea por un factor |
| &            |  Cambia el significado del + y el -|
| %            |  Aumenta el ángulo de giro |
| $            |  Decrementa el ángulo de giro |

### Cambiar el axioma de un Sistema-L ya defido

**Definición:**

```
change_axiom( <nombre_del_sistema>, <nuevo_axioma>);

```
**Ejemplo:**

```
change_axiom( leaf, AC );

```
### Agregar una regla a un Sistema-L ya defido

**Definición:**

```
add_rule( <nombre_del_sistema>, <parte_derecha_de_la_regla> => <parte_izquierda_de_la_regla> );

```
**Ejemplo:**

```
add_rule(leaf, C => FF );

```

### Declaración de brochas

**Definición:**

```
brush <nombre_de_la_brocha> {
    size: <int>,
    color: <color>,
    speed: <int>

}

*size* - Describe en ancho de la línea de la brocha
*speed* - Describe la velocidad con la que dibuja la brocha
```
**Ejemplo:**

```

brush small_blue {

    size: 1,
    color: #40e0d0,
    speed: 300

};

brush big_red {

    size: 5,
    color: #ff0000,
    speed: 300

};


```

### Declaración de lienzos

**Definición:**

```
canvas <nombre_de_la_brocha> {

    high: <int>,
    width: <int>,
    color: <color>

}
```
**Ejemplo:**

```
canvas soft_orange {

    high: 4000,
    width: 4000,
    color: #ffebcd
};

```

### Para dibujar Sistemas-L!

**Definición:**

```python
draw( <lsys>, <brush>, <canvas>, <largo_de_las_lineas>, <ángulo_de_giro>, <complejidad_del_sistema>)
```


**Ejemplo:**

```python
draw(leaf, small_blue, soft_orange, 5, 35, 5);

```

### Operaciones sobre tipos

| Símbolo       | Significado |
| ------------- | --------------- |
|   (+)         |  Suma estándar   |
|   (-)         |  Resta estándar |
|   (<)         |  Menor que |
|   (>)         |  Mayor que |
|   >=          |  Mayor igual|
|   <=          |  Menor igual |
|   ==          |  Igual |
|   !=          |  Distinto |

Todas las operaciones están definidas sobre los tipos int y float.
Los operadores de igualdad y desigualdad también están definidos para `strings` y `bool`.

### Asignación y Creación de variables
 
 ```
int a = 5;

draw(leaf, small_blue, soft_orange, a, 35, a);

a = 6;

repeat a {
    draw(leaf, small_blue, soft_orange, 7, 35, 5);
};
---------------------------------------------

bool b = true;

if (b) {
    draw(leaf, mibrocha, micanvas, 5 ,45, 8);
    b = false;
};

----------------------------------------------

string c = FF+;

if (c == FF+) {
    draw(leaf, mibrocha, micanvas, 5 ,45, 8);
};

----------------------------------------------

col white = #ffffff;

brush mibrocha {

    size: 1,
    color: white,
    speed: 500

};

 ```

### Condicionales:


**Ejemplo:**

``` python
if (a == 6) {
    draw(leaf, small_blue, soft_orange, a ,45, a)
};

if ( a (+) 1 == 7 ) {
    draw(leaf, small_blue, soft_orange, 5 ,45, 8);
} else { draw(star, big_red, soft_orange, 7 ,45, 3); };

```

### Ciclos:

**Definición:**

``` python
repeat <int> {
    <instructions>;
};

```

**Ejemplo:**

``` python
int a = 5;

repeat a{

    draw(quedratic_gosper, mibrocha, micanvas, a ,22.5 , a);
    a = a (+) 1
};

```
### Ejecución del programa:

Para la ejecución del programa, se recorre el AST y se evalúa cada nodo. Se empleó el *patrón visitor* para visistar los nodos del AST y ejecutar el código correspondiente a su funcionamiento en el lenguaje de programación Python, principalmente apoyado en el módulo `Turtle`. 
## Arquitectura del Compilador 
### Lexer:

Para el análisis léxico se utilizó el módulo ``lex`` de la biblioteca ``ply`` de Python. 
Se definieron las palabras reservadas del lenguaje y las expresiones regulares para reconocer los tokens. Para el trabajo con expresiones regulares se utiliza la biblioteca ``re``. 
Se utilizó el caracter ``#`` para indicar el comentario y el caracter ``;`` para indicar el fin de una instrucción.

### Parser:

Para el proceso de parsing se utilizó el módulo ``yacc`` de la biblioteca ``ply`` de Python y se definieron las reglas semánticas para indicar el comportamiento semántico del lenguaje y la construcción del árbol de sintaxis abtracta (AST). Yacc usa un parser LALR. Cada regla de la grámatica se especifica como una función de ``Python`` donde el docstring de la función indica la regla gramatical que corresponde. En el archivo ``parsing.out`` se muestra cómo queda la gramática y el autómata LALR correspondiente.

### Verificación semántica:

Para la fase de verificación semántica se empleó el patrón visitor para visistar los nodos del AST y realizar el chequeo de tipo correspondiente, y otras verificaciones de tipo semántico. Todos los errores semánticos que pueda tener el archivo, son encontrados y mostrados juntos al final.

A continuación algunas reglas semánticas del lenguaje:
- En la declaración o asignación de una variable, el tipo debe coincidir con el tipo estático con el que se nombró la variable.
- La asignación o llamado a una variable solo puede hacerse sobre variables previamente definidas
- Dos variables no pueden tener el mismo nombre.
- En el llamado a una función deben pasarse todos los argumentos de esta en el mismo orden en que se definieron los parámetros en la declaración.
- La condición de una instrucción ``if`` debe ser de tipo ``bool``
- La operación ``==`` está definida para operandos del mismo tipo. `

## Para correr la aplicacion 

En la carpeta *scripts* hay varios ejemplos de funconamiento del lenguage. Para ejecutar un archivo que no esté en la carpeta *scripts* se debe ponerle la extensión ``.lsystem`` y ponerlo en esta carpeta.

Ejecutar ``main.py`` e introducir el nombre del script que se desea ejecutar.


