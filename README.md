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

```
draw( <lsys>, <brush>, <canvas>, <int>, <float>, <int>)
```
**Ejemplo:**

```
draw(leaf, small_blue, soft_orange, 5, 35, 5);

```

