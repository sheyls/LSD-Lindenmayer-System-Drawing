def apply_rules(curve, right, left):
    """ 
    Apply derivation rules to a string that belogs to the gramatic alphabet 
    (consult README)
    """
    curve = curve.replace(right.lower(),left)  
    return curve.lower()