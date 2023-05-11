import re

lamcalc_input = []
binary_operators = {"(+": "+", "(eq?": "==", "(-": "-"}
number_pattern = r'^[-+]?[0-9]*\.?[0-9]+$'

def read_words_method():
    file_path = "lamcalc_examples/gridworld.txt"
    global lamcalc_input
    lamcalc_input = []
    
    with open(file_path, 'r') as f:
        for _, line in enumerate(f):
            words = line.split()
            if(words): #only add lines if non-empty
                lamcalc_input = lamcalc_input + words

def get_expr_body(input, num_open):
    if input == []:
        if num_open > 0: ValueError('expression body not closed off properly')
        else: return [], []
    elif '(' == input[0][0]:
        num_occur = input[0].count("(")
        num_occur_close = input[0].count(")")
        out, rst = get_expr_body(input[1:], num_open+(num_occur-num_occur_close))
        return [input[0]] + out, rst
    elif ')' in input[0]:
        num_occur = input[0].count(")")
        if num_open - num_occur  == 0:
            return [input[0]], input[1:]
        out, rst = get_expr_body(input[1:], num_open- num_occur)
        return [input[0]] + out, rst
    else:
        out, rst = get_expr_body(input[1:], num_open)
        return [input[0]] + out, rst
    
def translate_cons_helper(input):
    if input[0].startswith('empty)'):
        return ']'
    elif input[0] == '(cons':
        out, rst2 = translate_expr(input[1:])
        out2 = translate_cons_helper(rst2)
        if out2 == ']':
            return out + ']'
        return out + ', ' + out2
    else:
        ValueError('not a cons expression')
    
    
def translate_expr(input):
    global binary_operators
    rlang_out = ''
    if (input == [] or input[0].startswith('()')):
        return rlang_out, input[1:]
    elif (input[0][0] == '$'):
        return input[0].replace('$', 'var').replace(')', ''), input[1:]
    elif (input[0].startswith('empty)')):
        return rlang_out + ']', input[1:]
    elif bool(re.match(number_pattern, input[0].replace(')', ''))):
        return rlang_out + input[0].replace(')', ''), input[1:]
    elif (input[0] == '(index'):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        out2, rst3 = translate_expr(rst2)
        return out2 + '[' + out + ']', rst
    elif (input[0] == '(incr'):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        return out + ' + 1', rst
    elif (input[0] == '(decr'):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        return out + ' - 1', rst
    elif (input[0] == '(if'):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        rlang_out += 'if ' + out + ':' + '\n'
        out2, rst3 = translate_expr(rst2)
        rlang_out += out2 + '\n'
        out3, rst4 = translate_expr(rst3)
        if (out3 == ''): return rlang_out, rst
        rlang_out += 'else:\n' + out3
        if (rst4 != []): ValueError("if not properly closed")
        return rlang_out, rst
    elif (input[0] == '(cons'):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        rest_of_list = translate_cons_helper(rst2)
        if rest_of_list == ']':
            return '[' + out + ']', rst
        return '[' + out + ', ' + rest_of_list, rst
    elif (input[0] in binary_operators):
        body, rst = get_expr_body(input, 0)
        out, rst2 = translate_expr(body[1:])
        rlang_out += out + " " + binary_operators[body[0]] + " "
        out2, rst3 = translate_expr(rst2)
        rlang_out += out2
        return rlang_out, rst
    else:
        return "<parse-error>", []



read_words_method()
print(translate_expr(lamcalc_input)[0])