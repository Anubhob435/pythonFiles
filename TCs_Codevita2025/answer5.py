from sympy import symbols, expand, sympify
from sympy.parsing.sympy_parser import parse_expr

def solution():
    equation = input().strip()
    
    x, y = symbols('x y')
    
    # Parse and expand the expression
    try:
        expr = parse_expr(equation, transformations='all')
        expr = expand(expr)
    except:
        equation = equation.replace(' ', '')
        expr = sympify(equation)
        expr = expand(expr)
    
    # Extract coefficients for each term type
    coeffs = {'xx': 0, 'xy': 0, 'yy': 0, 'x': 0, 'y': 0, 'const': 0}
    
    coeffs['xx'] = int(expr.coeff(x**2) if expr.coeff(x**2) is not None else 0)
    coeffs['yy'] = int(expr.coeff(y**2) if expr.coeff(y**2) is not None else 0)
    coeffs['xy'] = int(expr.coeff(x*y) if expr.coeff(x*y) is not None else 0)
    
    expr_temp = expr - coeffs['xx']*x**2 - coeffs['yy']*y**2 - coeffs['xy']*x*y
    coeffs['x'] = int(expr_temp.coeff(x) if expr_temp.coeff(x) is not None else 0)
    
    expr_temp = expr_temp - coeffs['x']*x
    coeffs['y'] = int(expr_temp.coeff(y) if expr_temp.coeff(y) is not None else 0)
    
    coeffs['const'] = int(expr_temp - coeffs['y']*y)
    
    # Count operations in standard form
    def count_ops_standard(c):
        ops = 0
        terms = []
        
        for term_type, coeff in [('xx', c['xx']), ('yy', c['yy']), ('xy', c['xy']), 
                                   ('x', c['x']), ('y', c['y']), ('const', c['const'])]:
            if coeff != 0:
                if term_type in ['xx', 'yy', 'xy']:
                    if abs(coeff) != 1:
                        ops += 1
                    ops += 1
                elif term_type in ['x', 'y']:
                    if abs(coeff) != 1:
                        ops += 1
                terms.append(1)
        
        if len(terms) > 1:
            ops += len(terms) - 1
        
        return ops
    
    def count_factored_ops(a1, b1, a2, b2):
        ops = 0
        
        # First bracket
        terms1 = 0
        if a1 != 0:
            if abs(a1) != 1:
                ops += 1
            terms1 += 1
        if b1 != 0:
            terms1 += 1
        if terms1 > 1:
            ops += 1
        
        # Second bracket
        terms2 = 0
        if a2 != 0:
            if abs(a2) != 1:
                ops += 1
            terms2 += 1
        if b2 != 0:
            terms2 += 1
        if terms2 > 1:
            ops += 1
        
        # Multiply brackets
        if terms1 > 0 and terms2 > 0:
            ops += 1
        
        return ops
    
    min_ops = count_ops_standard(coeffs)
    
    # Form 1: (a1*x + b1)*(a2*x + b2)
    if coeffs['xy'] == 0 and coeffs['yy'] == 0 and coeffs['y'] == 0:
        A, B, C = coeffs['xx'], coeffs['x'], coeffs['const']
        if A != 0:
            for a1 in range(-100, 101):
                if a1 == 0:
                    continue
                if A % a1 == 0:
                    a2 = A // a1
                    if C != 0:
                        for b1 in range(-100, 101):
                            if b1 != 0 and C % b1 == 0:
                                b2 = C // b1
                                if a1 * b2 + a2 * b1 == B:
                                    min_ops = min(min_ops, count_factored_ops(a1, b1, a2, b2))
                    elif C == 0 and B == 0:
                        min_ops = min(min_ops, count_factored_ops(a1, 0, a2, 0))
    
    # Form 2: (a1*x + b1)*(a2*y + b2) + remaining
    if coeffs['xx'] == 0:
        A_xy, B_x, C_y, D = coeffs['xy'], coeffs['x'], coeffs['y'], coeffs['const']
        
        if A_xy != 0 and D != 0:
            for a1 in range(-100, 101):
                if a1 == 0:
                    continue
                if A_xy % a1 == 0:
                    a2 = A_xy // a1
                    for b1 in range(-100, 101):
                        if b1 != 0 and D % b1 == 0:
                            b2 = D // b1
                            if a1 * b2 == B_x and a2 * b1 == C_y:
                                ops_factored = count_factored_ops(a1, b1, a2, b2)
                                remaining_ops = 0
                                if coeffs['yy'] != 0:
                                    if abs(coeffs['yy']) != 1:
                                        remaining_ops += 1
                                    remaining_ops += 2  # y*y + addition
                                
                                min_ops = min(min_ops, ops_factored + remaining_ops)
    
    # Form 3: (a1*x + b1*y)*(a2*x + b2)
    if coeffs['yy'] == 0:
        A_xx, B_x, C_xy, D_y, E = coeffs['xx'], coeffs['x'], coeffs['xy'], coeffs['y'], coeffs['const']
        
        if A_xx != 0 and D_y != 0:
            for a1 in range(-100, 101):
                if a1 == 0:
                    continue
                if A_xx % a1 == 0:
                    a2 = A_xx // a1
                    for b1 in range(-100, 101):
                        if b1 == 0:
                            continue
                        if D_y % b1 == 0:
                            b2 = D_y // b1
                            if a1 * b2 == B_x and a2 * b1 == C_xy and b1 * b2 == E:
                                ops = 0
                                # First bracket: a1*x + b1*y
                                if abs(a1) != 1:
                                    ops += 1
                                if abs(b1) != 1:
                                    ops += 1
                                ops += 1
                                
                                # Second bracket: a2*x + b2
                                if abs(a2) != 1:
                                    ops += 1
                                if b2 != 0:
                                    ops += 1
                                
                                ops += 1  # Multiply brackets
                                
                                min_ops = min(min_ops, ops)
    
    print(min_ops)

solution()
