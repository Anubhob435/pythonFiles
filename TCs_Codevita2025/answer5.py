equation = input().strip().replace(' ', '')

# Extract coefficients by evaluating at strategic points
def get_coeffs(expr):
    try:
        safe_dict = {"__builtins__": {}}
        
        has_x = 'x' in expr
        has_y = 'y' in expr
        
        if not has_x and not has_y:
            val = eval(expr, safe_dict, {})
            return {'xx': 0, 'yy': 0, 'xy': 0, 'x': 0, 'y': 0, 'const': int(val)}
        
        # Evaluate at 6 points to solve for 6 unknowns
        points = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
        values = []
        for x_val, y_val in points:
            val = eval(expr, safe_dict, {'x': x_val, 'y': y_val})
            values.append(val)
        
        # Solve system manually
        c_0 = values[0]
        c_xx = (values[4] - 2*values[1] + c_0) / 2
        c_x = values[1] - c_0 - c_xx
        c_yy = (values[5] - 2*values[2] + c_0) / 2
        c_y = values[2] - c_0 - c_yy
        c_xy = values[3] - c_xx - c_yy - c_x - c_y - c_0
        
        return {
            'xx': int(round(c_xx)),
            'yy': int(round(c_yy)),
            'xy': int(round(c_xy)),
            'x': int(round(c_x)),
            'y': int(round(c_y)),
            'const': int(round(c_0))
        }
    except:
        return None

coeffs = get_coeffs(equation)

if coeffs is None:
    print(0)
else:
    def count_ops_standard(c):
        ops = 0
        terms = []
        
        for term_type in ['xx', 'yy', 'xy', 'x', 'y', 'const']:
            coeff = c[term_type]
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
    
    def count_factored_ops(a1, b1, a2, b2, is_same_variable=True, allow_perfect_square_opt=False):
        # Check if it's a perfect square: (a1*x + b1) == (a2*x + b2) with same variable
        if a1 == a2 and b1 == b2 and is_same_variable and allow_perfect_square_opt:
            # Perfect square case: only count the factor once, then squaring
            ops = 0
            terms = 0
            if a1 != 0:
                if abs(a1) != 1:
                    ops += 1
                terms += 1
            if b1 != 0:
                terms += 1
            if terms > 1:
                ops += 1
            ops += 1  # +1 for squaring operation
            return ops
        
        # Normal case: two different factors
        ops = 0
        terms1 = 0
        if a1 != 0:
            if abs(a1) != 1:
                ops += 1
            terms1 += 1
        if b1 != 0:
            terms1 += 1
        if terms1 > 1:
            ops += 1
        
        terms2 = 0
        if a2 != 0:
            if abs(a2) != 1:
                ops += 1
            terms2 += 1
        if b2 != 0:
            terms2 += 1
        if terms2 > 1:
            ops += 1
        
        if terms1 > 0 and terms2 > 0:
            ops += 1
        
        return ops
    
    min_ops = count_ops_standard(coeffs)
    
    # First try factoring out common factors
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    
    def try_factor_out_common(coeffs):
        nonzero_coeffs = [v for v in coeffs.values() if v != 0]
        if len(nonzero_coeffs) <= 1:
            return coeffs, 1
        
        common_factor = nonzero_coeffs[0]
        for coeff in nonzero_coeffs[1:]:
            common_factor = gcd(common_factor, coeff)
        
        if abs(common_factor) > 1:
            new_coeffs = {}
            for key, value in coeffs.items():
                new_coeffs[key] = value // common_factor if value != 0 else 0
            return new_coeffs, abs(common_factor)
        return coeffs, 1
    
    # Try factoring out common factors first
    factored_coeffs, common_factor = try_factor_out_common(coeffs)
    
    if common_factor > 1:
        # Calculate operations for factored version
        factored_ops = count_ops_standard(factored_coeffs)
        if common_factor != 1:
            factored_ops += 1  # multiplication by common factor
        min_ops = min(min_ops, factored_ops)
        
        # Also try further factorization on the reduced coefficients
        coeffs_to_use = factored_coeffs
    else:
        coeffs_to_use = coeffs
    
    # Form 1: (a1*x + b1)*(a2*x + b2)
    if coeffs_to_use['xy'] == 0 and coeffs_to_use['yy'] == 0 and coeffs_to_use['y'] == 0:
        A, B, C = coeffs_to_use['xx'], coeffs_to_use['x'], coeffs_to_use['const']
        if A != 0:
            for a1 in range(-100, 101):
                if a1 == 0 or A % a1 != 0:
                    continue
                a2 = A // a1
                if C != 0:
                    for b1 in range(-100, 101):
                        if b1 != 0 and C % b1 == 0:
                            b2 = C // b1
                            if a1 * b2 + a2 * b1 == B:
                                factored_ops = count_factored_ops(a1, b1, a2, b2, True, common_factor > 1)
                                if common_factor > 1:
                                    factored_ops += 1
                                min_ops = min(min_ops, factored_ops)
                elif C == 0 and B == 0:
                    factored_ops = count_factored_ops(a1, 0, a2, 0, True, common_factor > 1)
                    if common_factor > 1:
                        factored_ops += 1
                    min_ops = min(min_ops, factored_ops)
    
    # Form 2: (a1*x + b1)*(a2*y + b2) + remaining
    if coeffs_to_use['xx'] == 0:
        A_xy, B_x, C_y, D = coeffs_to_use['xy'], coeffs_to_use['x'], coeffs_to_use['y'], coeffs_to_use['const']
        if A_xy != 0 and D != 0:
            for a1 in range(-100, 101):
                if a1 == 0 or A_xy % a1 != 0:
                    continue
                a2 = A_xy // a1
                for b1 in range(-100, 101):
                    if b1 != 0 and D % b1 == 0:
                        b2 = D // b1
                        if a1 * b2 == B_x and a2 * b1 == C_y:
                            ops_factored = count_factored_ops(a1, b1, a2, b2, False, False)
                            remaining_ops = 0
                            if coeffs_to_use['yy'] != 0:
                                if abs(coeffs_to_use['yy']) != 1:
                                    remaining_ops += 1
                                remaining_ops += 2
                            if common_factor > 1:
                                ops_factored += 1
                            min_ops = min(min_ops, ops_factored + remaining_ops)
    
    # Form 3: (a1*x + b1*y)*(a2*x + b2)
    if coeffs_to_use['yy'] == 0:
        A_xx, B_x, C_xy, D_y, E = coeffs_to_use['xx'], coeffs_to_use['x'], coeffs_to_use['xy'], coeffs_to_use['y'], coeffs_to_use['const']
        if A_xx != 0 and D_y != 0:
            for a1 in range(-100, 101):
                if a1 == 0 or A_xx % a1 != 0:
                    continue
                a2 = A_xx // a1
                for b1 in range(-100, 101):
                    if b1 == 0 or D_y % b1 != 0:
                        continue
                    b2 = D_y // b1
                    if a1 * b2 == B_x and a2 * b1 == C_xy and b1 * b2 == E:
                        ops = 0
                        if abs(a1) != 1:
                            ops += 1
                        if abs(b1) != 1:
                            ops += 1
                        ops += 1
                        if abs(a2) != 1:
                            ops += 1
                        if b2 != 0:
                            ops += 1
                        ops += 1
                        if common_factor > 1:
                            ops += 1
                        min_ops = min(min_ops, ops)
    
    print(min_ops)
