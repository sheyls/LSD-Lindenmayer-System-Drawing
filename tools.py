Operator={

    '(+)' : lambda x,y : x+y,
    '(-)' : lambda x,y : x-y,
    '(*)' : lambda x,y : x*y,
    '(/)' : lambda x,y : x/y,

}

Bool_Operator={
    '==' : lambda x,y : x==y,
    '(>)' : lambda x,y : x>y,
    '(<)' : lambda x,y : x<y,
    '>=' : lambda x,y : x>=y,
    '<=' : lambda x,y : x<=y,
    '!=' : lambda x,y : x!=y,
}

Token_to_types={
    'STRING' : 'string',
    'INT'    : 'int',
    'CANVAS' : 'canvas',
    'BRUSH' : 'brush',
    'LSYS' : 'lsys',
    'FLOAT'  : 'float',
    'COL'   : 'color'
}

def update_errs(errors, new_errs):
    if new_errs != None and new_errs != []:
        errors.append(new_errs)
