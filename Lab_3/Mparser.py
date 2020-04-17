import ply.yacc as yacc

from Lab_3 import scanner
from Lab_3.AST import *

tokens = scanner.tokens
reserved = scanner.reserved
literals = scanner.literals

precedence = (
    ("left", '*', '/'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("left", '+', '-'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = Program(p[1])


def p_instructions_opt_1(p):
    """instructions_opt : instructions"""
    p[0] = InstructionsOpt(p[1])


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = InstructionsOpt("empty")


def p_instructions_1(p):
    """instructions : instruction instructions"""
    p[0] = Instructions(p[1], p[2])


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = Instructions(p[1], "")


def p_instruction_1(p):
    """instruction : if_statement"""
    p[0] = Instruction(p[1], "")


def p_instruction_2(p):
    """instruction : assign ';'"""
    p[0] = Instruction(p[1], "")


def p_instruction_3(p):
    """instruction : loop"""
    p[0] = Instruction(p[1], "")


def p_instruction_4(p):
    """instruction : BREAK ';'"""
    p[0] = Instruction(p[1], "")


def p_instruction_5(p):
    """instruction : CONTINUE ';'"""
    p[0] = Instruction(p[1], "")


def p_instruction_6(p):
    """instruction : PRINT printable ';'"""
    p[0] = Instruction(p[1], p[2])


def p_instruction_7(p):
    """instruction : RETURN EXPRESSION ';'"""
    p[0] = Instruction(p[1], p[2])


def p_instruction_8(p):
    """instruction : '{' instructions '}'"""
    p[0] = Instruction(p[2], "")


def p_printable_1(p):
    """ printable : printable ',' EXPRESSION"""
    p[0] = Printable('printable', p[1], p[3])


def p_printable_2(p):
    """printable : EXPRESSION"""
    p[0] = Printable(p[1], "", "")


def p_loop_1(p):
    """loop : WHILE '(' condition ')' instruction"""
    p[0] = Loop('while_loop', p[3], p[5])


def p_loop_2(p):
    """loop : FOR array_range instruction"""
    p[0] = Loop('for_loop', p[2], p[3])


def p_array_range_1(p):
    """ array_range : ID '=' INTNUM ':' ID"""
    p[0] = ArrayRange(p[1], p[3], p[5])


def p_array_range_2(p):
    """ array_range : ID '=' ID ':' ID"""
    p[0] = ArrayRange(p[1], p[3], p[5])


def p_array_range_3(p):
    """ array_range : ID '=' ID ':' INTNUM"""
    p[0] = ArrayRange(p[1], p[3], p[5])


def p_array_range_4(p):
    """ array_range : ID '=' INTNUM ':' INTNUM"""
    p[0] = ArrayRange(p[1], p[3], p[5])


def p_if_statement_1(p):
    """if_statement : IF '(' condition ')' instruction"""
    p[0] = IfStatement(p[3], p[5], "")


def p_if_statement_2(p):
    """if_statement : IF '(' condition ')' instruction else_statement"""
    p[0] = IfStatement(p[3], p[5], p[6])


def p_else_statement(p):
    """else_statement : ELSE instruction """
    p[0] = ElseStatement(p[2])


def p_condition_1(p):
    """condition : EXPRESSION logical_operator EXPRESSION"""
    p[0] = BinExpr(p[1], p[2], p[3])


def p_condition_2(p):
    """condition : condition OR condition"""
    p[0] = BinExpr(p[1], p[2], p[3])


def p_condition_3(p):
    """condition : condition AND condition"""
    p[0] = BinExpr(p[1], p[2], p[3])


def p_logical_operator_1(p):
    """logical_operator : EQ"""
    p[0] = LogicalOperator(p[1])


def p_logical_operator_2(p):
    """logical_operator : '<'"""
    p[0] = LogicalOperator(p[1])


def p_logical_operator_3(p):
    """logical_operator : '>'"""
    p[0] = LogicalOperator(p[1])


def p_logical_operator_4(p):
    """logical_operator : GE"""
    p[0] = LogicalOperator(p[1])


def p_logical_operator_5(p):
    """logical_operator : LE"""
    p[0] = LogicalOperator(p[1])


def p_logical_operator_6(p):
    """logical_operator : NEQ"""
    p[0] = LogicalOperator(p[1])

def p_assign_1(p):
    """assign : ID '=' EXPRESSION"""
    p[0] = Assign(p[2], p[1], p[3])


def p_assign_2(p):
    """assign : ID ADDASSIGN string_expression"""
    p[0] = Assign(p[2], p[1], p[3])


def p_assign_3(p):
    """assign : ID DIVASSIGN operable_expression"""
    p[0] = Assign(p[2], p[1], p[3])


def p_assign_4(p):
    """assign : ID MULASSIGN operable_expression"""
    p[0] = Assign(p[2], p[1], p[3])


def p_assign_5(p):
    """assign : ID ADDASSIGN operable_expression"""
    p[0] = Assign(p[2], p[1], p[3])


def p_assign_6(p):
    """assign : array_part '=' EXPRESSION"""
    p[0] = Assign(p[2], p[1], p[3])


def p_introw_1(p):
    """introw : introw ',' INTNUM"""
    p[0] = Introw(p[1], p[3])


def p_introw_2(p):
    """introw : INTNUM"""
    p[0] = IntNum(p[1])


def p_expression_1(p):
    """EXPRESSION : operable_expression"""
    p[0] = p[1]


def p_expression_2(p):
    """EXPRESSION : string_expression"""
    p[0] = p[1]


def p_string_expression(p):
    """string_expression :  string_expression '+' string_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_string_expression_1(p):
    """string_expression : STRING"""
    p[0] = String(p[1])


def p_expression_3(p):
    """operable_expression : operable_expression '*' operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_expression_4(p):
    """operable_expression : operable_expression '/' operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_expression_5(p):
    """operable_expression : array_part"""
    p[0] = p[1]


def p_expression_5a(p):
    """array_part : ID '[' introw ']'"""
    p[0] = ArrayPart(p[1], p[3])


def p_expression_6(p):
    """operable_expression :'(' operable_expression ')'"""
    p[0] = p[2]


def p_expression_7(p):
    """operable_expression : '-' operable_expression"""
    p[0] = UnaryExpression("-", p[1])


def p_expression_8(p):
    """operable_expression : operable_expression '+' operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_expression_9(p):
    """operable_expression : operable_expression '-' operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_m_expression_1(p):
    """operable_expression : EYE '(' INTNUM ')' """
    p[0] = Eye(p[3])


def p_m_expression_2(p):
    """operable_expression : ZEROS '(' INTNUM ')' """
    p[0] = Zeros(p[3])


def p_m_expression_3(p):
    """operable_expression : ONES '(' INTNUM ')' """
    p[0] = Ones(p[3])


def p_m_expression_4(p):
    """operable_expression : EYE '(' ID ')'' """
    p[0] = Eye(p[3])


def p_m_expression_5(p):
    """operable_expression : ZEROS '(' ID ')' """
    p[0] = Zeros(p[3])


def p_m_expression_6(p):
    """operable_expression : ONES '(' ID ')' """
    p[0] = Ones(p[3])


def p_m_expression_7(p):
    """operable_expression : operable_expression DOTADD operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_m_expression_8(p):
    """operable_expression : operable_expression DOTSUB operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_m_expression_9(p):
    """operable_expression : operable_expression DOTMUL operable_expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_m_expression_10(p):
    """operable_expression : operable_expression DOTDIV operable_expression"""
    p[0] = BinExpr(p[2], p[1], p[3])


def p_m_expression_11(p):
    """operable_expression : operable_expression TRANSPOSE """
    p[0] = UnaryExpression('TRANSPOSE', p[1])


def p_create_matrix_1(p):
    """operable_expression : matrix """
    p[0] = Matrix(p[1])


def p_create_matrix_2(p):
    """operable_expression : FLOAT"""
    p[0] = FloatNum(p[1])


def p_create_matrix_3(p):
    """operable_expression : INTNUM"""
    p[0] = IntNum(p[1])


def p_create_matrix(p):
    """operable_expression : ID """
    p[0] = Variable(p[1])


def p_matrix(p):
    """matrix : '[' rows ']'"""
    p[0] = Matrix(p[2])


def p_rows_1(p):
    """rows : rows ';' row """
    p[0] = Rows(p[1], p[3])


def p_rows_2(p):
    """rows : row """
    p[0] = Rows("", p[1])


def p_row_1(p):
    """row : row ',' EXPRESSION"""
    p[0] = Row(p[1], p[3])


def p_row_2(p):
    """row :  EXPRESSION """
    p[0] = Row("", p[1])


parser = yacc.yacc()
