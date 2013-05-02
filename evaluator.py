import math

#Associativity constants
ASSOC_LEFT = 1
ASSOC_RIGHT = 2


class Operator(object):
  """A class to hold the basic operator stuff
  Holds it's associativity, precedence, number of arguments it takes
  and the function used to evaluate it
  """
  def __init__(self,assoc,prec,args,func):
    """Gives the most recent docstring"""
    self.assoc = assoc
    self.prec = prec
    self.args = args
    self.func = func

#The operators
operator_plus = "+"
operator_minus = "-"
operator_div = "/"
operator_mult = "*"
operator_mod = "%"
operator_uminus = "_"
operator_left_paran = "("
operator_right_paran = ")"
operator_pow = "^"
operator_abs = "abs"
operator_sqrt = "sqrt"
#the metadata for the operators
operators = {
  operator_plus: Operator(ASSOC_LEFT,1,2,lambda x,y: x + y),
  operator_minus: Operator(ASSOC_LEFT,1,2,lambda x,y: x - y),
  operator_div: Operator(ASSOC_LEFT,2,2,lambda x,y: x/y),
  operator_mult: Operator(ASSOC_LEFT,2,2,lambda x,y: x*y),
  operator_mod: Operator(ASSOC_LEFT,2,2,lambda x,y: x%y),
  operator_uminus: Operator(ASSOC_RIGHT,10,1,lambda x: -x),
  operator_pow: Operator(ASSOC_LEFT,8,2,lambda x,y: x ** y),
  operator_abs: Operator(ASSOC_RIGHT,7,1,lambda x: -x if x < 0 else x),
  operator_sqrt: Operator(ASSOC_RIGHT,7,1,lambda x: math.sqrt(x)),
  operator_left_paran: None,
  operator_right_paran: None
}

#Parsing code
def prec(op):
  """Returns the precedence of the given operator"""
  return operators[op].prec

def assoc(op):
  """Returns the associativity of the given operator"""
  return operators[op].assoc

def is_op(c):
  """Checks if the token is an operator, but not left/right parentheses"""
  return operators.has_key(c) and not (is_left_paran(c) or is_right_paran(c))

def is_left_paran(c):
  """Checks if the given token is the token equivalent of left parentheses"""
  return c == operator_left_paran

def is_right_paran(c):
  """Checks if the given token is the token equivalent of right parentheses"""
  return c == operator_right_paran

def append_token(token,arr):
  """Appends the given token to the array, and returns an empty string"""
  if token != "":
    arr.append(token)
  return ""

def tokenize(expr):
  """Tokenizes the given expression"""
  tokens = []
  last_token = ""
  last_op = "START" #dummy op to mark start
  in_token = False
  for c in expr:
    if c == " ":
      in_token = False
      last_token = append_token(last_token,tokens)
    elif is_op(c) or is_right_paran(c) or is_left_paran(c):
      #deal with the now defunct token
      in_token = False
      last_token = append_token(last_token,tokens)
      #check tokenization of minus sign (unary operator sometimes)
      if last_op != "" and not is_right_paran(c):
        if c == operator_minus:
          c = '_'
        elif not is_left_paran(c):
          raise ValueError("Illegal use of binary operator %c" % c)
      last_op = c
      tokens.append(c)
    else:
      in_token = True
      last_token += c
      last_op = ""
    if not in_token and last_token != "":
      last_token = append_token(last_token,tokens)
  if in_token:
    append_token(last_token,tokens)
  return tokens

def to_rpn(expr):
  """Converts a fully tokenized expression into Reverse Polish Notation (Prefix Notation)"""
  ops = []
  results = []
  for token in tokenize(expr):
    if is_op(token):
      while len(ops) > 0 and is_op(ops[-1]) and \
        ( (assoc(token) == ASSOC_LEFT and prec(token) <= prec(ops[-1])) or \
         (assoc(token) == ASSOC_RIGHT and prec(token) < prec(ops[-1]))):
        results.append(ops.pop())
      ops.append(token)
    elif is_left_paran(token):
      ops.append(token)
    elif is_right_paran(token):
      while len(ops) > 0 and not is_left_paran(ops[-1]):
        results.append(ops.pop())
      if len(ops) == 0:
        raise ValueError("Mismatched parentheses")
      if is_left_paran(ops[-1]):
        ops.pop()
    else:
      results.append(token)
  while len(ops) > 0:
    if is_right_paran(ops[-1]) or is_left_paran(ops[-1]):
      raise ValueError("Mismatched parentheses")
    results.append(ops.pop())
  return results


#Execution code
def eval_exp(op,stack):
  """Runs the operator on the stack"""
  arg = []
  for i in range(operators[op].args):
    if len(stack) <= 0:
      raise ValueError('Invalid number of arguments')
    arg.append(stack.pop())
  arg.reverse()
  return operators[op].func(*arg)

def can_float(val):
  """Checks if the number can be parsed to float"""
  try:
    float(val)
    return True
  except ValueError:
    return False

def parse_rpn(tokens):
  """Runs the RPN expression"""
  result = []
  y = 0.0
  x = 0.0
  for token in tokens:
    if is_op(token):
      result.append(eval_exp(token,result))
    elif can_float(token):
      result.append(float(token))
    else:
      raise ValueError("Invalid Token")
  if len(result) != 1:
    raise ValueError("Invalid arguments")
  return result.pop()


if __name__=="__main__":
  import sys
  print parse_rpn(to_rpn(sys.argv[1]))

