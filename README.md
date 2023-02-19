# LSD: Lindenmayer-System-Drawing
## Lenguaje de dominio específico para la visualización de Sistemas-L

LSD es un DSL :) que tiene como objetivo la visualización de Sistemas-L. Un Sistema-L o un sistema de Lindenmayer es una gramática formal (un conjunto de reglas y símbolos) principalmente utilizados para modelar el proceso de crecimiento de las plantas; puede modelar también la morfología de una variedad de organismos. Además pueden utilizarse para generar fractales autosimilares como los sistemas de función iterada. Los sistemas-L fueron introducidos y desarrollados en 1968 por el biólogo y botánico teórico húngaro Aristid Lindenmayer.

## Sintaxis del lenguaje
Lenguaje de tipado estático, no orientado a objetos.

### Tipos internos del lenguaje:

### Palabras reservadas:
 'canvas'     : 'TYPE',
    'draw'       : 'DRAW',
    'brush'      : 'TYPE',
    'lsys'       : 'TYPE',
    'axiom'      : 'AXIOM',
    'color'      : 'COLOR',
    'size'       : 'SIZE',
    'speed'      : 'SPEED',
    'high'       : 'HIGH',
    'width'      : 'WIDTH',
    'if'         : 'IF',
    'else'       : 'ELSE',
    'bool'       : 'TYPE',
    'true'       : 'BOOL',
    'false'      : 'BOOL',
    'int'        : 'TYPE',
    'string'     : 'TYPE',
    'add_rule'   : 'ADD_RULE',
    'repeat'     : 'REPEAT'
