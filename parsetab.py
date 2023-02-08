
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD_RULE AND ANGLE ARROW AXIOM BREAK BRUSH CANVAS COL COLOR COMMA DIFFER DRAW ELSE END EQUAL EQUALEQUAL FALSE FLOAT GEQUAL GREATER HIGH ID IF INT LBRACE LCOR LEFT LEQUAL LESS LINE LPAREN LSYS MINUS MULTIPLY NILL NOT OR PLUS POP PUSH RBRACE RCOR RIGHT RPAREN RULE SIZE SPEED STRING TRUE TWOPOINTS TYPE TYPE WHILE WIDTH\n    Program : InstructionList\n    \n    InstructionList : Instruction END InstructionList\n                   | Instruction END\n     Assignable : INT\n    Instruction : LSYS ID LBRACE Lsystem_body RBRACE\n    \n    \n    Instruction : ID EQUAL Assignable \n                | TYPE ID EQUAL Assignable\n    \n    Lsystem_body : AXIOM TWOPOINTS STRING COMMA Ls_rules\n                \n    \n    Ls_rules : STRING ARROW STRING COMMA Ls_rules\n             | STRING ARROW STRING\n    Instruction : ADD_RULE LPAREN ID COMMA STRING COMMA STRING RPAREN\n    Instruction : BRUSH ID LBRACE Brush_body RBRACE\n    \n    Brush_body : SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT    \n    \n    Instruction : CANVAS ID LBRACE Canvas_body RBRACE\n    \n    Canvas_body : HIGH TWOPOINTS INT COMMA WIDTH TWOPOINTS INT COMMA COLOR TWOPOINTS COL    \n    \n    Instruction : DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA INT RPAREN\n    '
    
_lr_action_items = {'LSYS':([0,11,],[4,4,]),'ID':([0,4,6,8,9,11,15,18,36,49,],[5,12,14,16,17,5,24,27,44,54,]),'TYPE':([0,11,],[6,6,]),'ADD_RULE':([0,11,],[7,7,]),'BRUSH':([0,11,],[8,8,]),'CANVAS':([0,11,],[9,9,]),'DRAW':([0,11,],[10,10,]),'$end':([1,2,11,19,],[0,-1,-3,-2,]),'END':([3,21,22,30,37,40,42,57,76,],[11,-6,-4,-7,-5,-12,-14,-11,-16,]),'EQUAL':([5,14,],[13,23,]),'LPAREN':([7,10,],[15,18,]),'LBRACE':([12,16,17,],[20,25,26,]),'INT':([13,23,41,43,60,63,68,77,],[22,22,47,48,64,67,72,79,]),'AXIOM':([20,],[29,]),'COMMA':([24,27,39,44,45,47,48,54,64,65,66,67,],[31,36,46,49,50,52,53,60,68,69,70,71,]),'SIZE':([25,],[33,]),'HIGH':([26,],[35,]),'RBRACE':([28,32,34,56,65,73,79,80,],[37,40,42,-8,-10,-9,-13,-15,]),'TWOPOINTS':([29,33,35,58,59,74,75,],[38,41,43,62,63,77,78,]),'STRING':([31,38,46,50,61,69,],[39,45,51,55,65,55,]),'RPAREN':([51,72,],[57,76,]),'COLOR':([52,71,],[58,75,]),'WIDTH':([53,],[59,]),'ARROW':([55,],[61,]),'COL':([62,78,],[66,80,]),'SPEED':([70,],[74,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Program':([0,],[1,]),'InstructionList':([0,11,],[2,19,]),'Instruction':([0,11,],[3,3,]),'Assignable':([13,23,],[21,30,]),'Lsystem_body':([20,],[28,]),'Brush_body':([25,],[32,]),'Canvas_body':([26,],[34,]),'Ls_rules':([50,69,],[56,73,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> InstructionList','Program',1,'p_program','parser_1.py',50),
  ('InstructionList -> Instruction END InstructionList','InstructionList',3,'p_instruction_list','parser_1.py',56),
  ('InstructionList -> Instruction END','InstructionList',2,'p_instruction_list','parser_1.py',57),
  ('Assignable -> INT','Assignable',1,'p_assignable','parser_1.py',70),
  ('Instruction -> LSYS ID LBRACE Lsystem_body RBRACE','Instruction',5,'p_lsystem','parser_1.py',76),
  ('Instruction -> ID EQUAL Assignable','Instruction',3,'p_variables','parser_1.py',85),
  ('Instruction -> TYPE ID EQUAL Assignable','Instruction',4,'p_variables','parser_1.py',86),
  ('Lsystem_body -> AXIOM TWOPOINTS STRING COMMA Ls_rules','Lsystem_body',5,'p_lsystem_body','parser_1.py',97),
  ('Ls_rules -> STRING ARROW STRING COMMA Ls_rules','Ls_rules',5,'p_lsystem_rules','parser_1.py',104),
  ('Ls_rules -> STRING ARROW STRING','Ls_rules',3,'p_lsystem_rules','parser_1.py',105),
  ('Instruction -> ADD_RULE LPAREN ID COMMA STRING COMMA STRING RPAREN','Instruction',8,'p_add_rule','parser_1.py',114),
  ('Instruction -> BRUSH ID LBRACE Brush_body RBRACE','Instruction',5,'p_brush','parser_1.py',120),
  ('Brush_body -> SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT','Brush_body',11,'p_brush_body','parser_1.py',126),
  ('Instruction -> CANVAS ID LBRACE Canvas_body RBRACE','Instruction',5,'p_canvas','parser_1.py',132),
  ('Canvas_body -> HIGH TWOPOINTS INT COMMA WIDTH TWOPOINTS INT COMMA COLOR TWOPOINTS COL','Canvas_body',11,'p_canvas_body','parser_1.py',138),
  ('Instruction -> DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA INT RPAREN','Instruction',12,'p_draw','parser_1.py',144),
]
