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
    'INT'    : '_int'
}