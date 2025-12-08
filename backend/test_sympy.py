
from sympy import solve, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def solve_equation(equation_str):
    transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))
    
    if "=" in equation_str:
        lhs_str, rhs_str = equation_str.split("=")
        lhs = parse_expr(lhs_str, transformations=transformations)
        rhs = parse_expr(rhs_str, transformations=transformations)
        expr = lhs - rhs
    else:
        expr = parse_expr(equation_str, transformations=transformations)
    
    # Find symbols in the expression
    symbols = expr.free_symbols
    
    if not symbols:
        return "No variables found"
        
    # Solve for the variables
    solution = solve(expr)
    return str(solution)

print(f"x^2 + 2x - 10 -> {solve_equation('x^2 + 2x - 10')}")
print(f"x + 1 = 2 -> {solve_equation('x + 1 = 2')}")
print(f"2x = 10 -> {solve_equation('2x = 10')}")
