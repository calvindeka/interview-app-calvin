#!/usr/bin/env python3
"""Simple Flask API exposing a stub equation solver."""

from __future__ import annotations

import os
from flask import Flask, jsonify, request
from sympy import solve as sympy_solve
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response):  # type: ignore[override]
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @app.get("/solve")
    def solve():
        equation = (request.args.get("equation") or "").strip()
        if not equation:
            return jsonify({"error": "Missing 'equation' query parameter"}), 400
        
        try:
            transformations = (
                standard_transformations
                + (implicit_multiplication_application, convert_xor)
            )
            
            if "=" in equation:
                lhs_str, rhs_str = equation.split("=")
                lhs = parse_expr(lhs_str, transformations=transformations)
                rhs = parse_expr(rhs_str, transformations=transformations)
                expr = lhs - rhs
            else:
                expr = parse_expr(equation, transformations=transformations)
            
            # Find symbols in the expression
            symbols = expr.free_symbols
            
            if not symbols:
                # If no symbols, evaluate the expression
                return jsonify({"result": str(expr)})
                
            # Solve for the variables
            solution = sympy_solve(expr)
            return jsonify({"result": str(solution)})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "Equation API. Try /solve?equation=1+1"})

    return app


def run() -> None:
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
