
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ANGLE ARROW AXIOM BREAK BRUSH CANVAS COL COLOR COMMA DIFFER DRAW ELSE END EQUAL EQUALEQUAL FALSE FLOAT GEQUAL GREATER ID IF INT LBRACE LCOR LEFT LEQUAL LESS LINE LPAREN LSYS MINUS MULTIPLY NILL NOT OR PLUS POP PUSH RBRACE RCOR RIGHT RPAREN RULE SIZE SPEED STRING TRUE TWOPOINTS TYPE WHILE\n    Program : InstructionList\n    \n    InstructionList : Instruction END InstructionList\n                   | Instruction END\n     Assignable : INT\n    Instruction : LSYS ID LBRACE Lsystem_body RBRACE\n    \n    \n    Instruction : ID EQUAL Assignable \n                | TYPE ID EQUAL Assignable\n    \n    Lsystem_body : AXIOM TWOPOINTS STRING COMMA Ls_rules\n                \n    \n    Ls_rules : STRING ARROW STRING COMMA Ls_rules\n             | STRING ARROW STRING\n    \n    Instruction : BRUSH ID LBRACE Brush_body RBRACE\n    \n    Brush_body : SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT    \n    '
    
_lr_action_items = {'LSYS':([0,8,],[4,4,]),'ID':([0,4,6,7,8,],[5,9,11,12,5,]),'TYPE':([0,8,],[6,6,]),'BRUSH':([0,8,],[7,7,]),'$end':([1,2,8,13,],[0,-1,-3,-2,]),'END':([3,15,16,21,24,26,],[8,-6,-4,-7,-5,-11,]),'EQUAL':([5,11,],[10,17,]),'LBRACE':([9,12,],[14,18,]),'INT':([10,17,27,43,],[16,16,29,44,]),'AXIOM':([14,],[20,]),'SIZE':([18,],[23,]),'RBRACE':([19,22,33,37,41,44,],[24,26,-8,-10,-9,-12,]),'TWOPOINTS':([20,23,34,42,],[25,27,36,43,]),'STRING':([25,30,35,39,],[28,32,37,32,]),'COMMA':([28,29,37,38,],[30,31,39,40,]),'COLOR':([31,],[34,]),'ARROW':([32,],[35,]),'COL':([36,],[38,]),'SPEED':([40,],[42,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Program':([0,],[1,]),'InstructionList':([0,8,],[2,13,]),'Instruction':([0,8,],[3,3,]),'Assignable':([10,17,],[15,21,]),'Lsystem_body':([14,],[19,]),'Brush_body':([18,],[22,]),'Ls_rules':([30,39,],[33,41,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> InstructionList','Program',1,'p_program','parser.py',46),
  ('InstructionList -> Instruction END InstructionList','InstructionList',3,'p_instruction_list','parser.py',52),
  ('InstructionList -> Instruction END','InstructionList',2,'p_instruction_list','parser.py',53),
  ('Assignable -> INT','Assignable',1,'p_assignable','parser.py',63),
  ('Instruction -> LSYS ID LBRACE Lsystem_body RBRACE','Instruction',5,'p_lsystem','parser.py',69),
  ('Instruction -> ID EQUAL Assignable','Instruction',3,'p_variables','parser.py',78),
  ('Instruction -> TYPE ID EQUAL Assignable','Instruction',4,'p_variables','parser.py',79),
  ('Lsystem_body -> AXIOM TWOPOINTS STRING COMMA Ls_rules','Lsystem_body',5,'p_lsystem_body','parser.py',90),
  ('Ls_rules -> STRING ARROW STRING COMMA Ls_rules','Ls_rules',5,'p_lsystem_rules','parser.py',97),
  ('Ls_rules -> STRING ARROW STRING','Ls_rules',3,'p_lsystem_rules','parser.py',98),
  ('Instruction -> BRUSH ID LBRACE Brush_body RBRACE','Instruction',5,'p_brush','parser.py',108),
  ('Brush_body -> SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT','Brush_body',11,'p_brush_body','parser.py',114),
]
