import re

# words_and_lines = []
number_pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
global_var_num = 0

end_characters = ["#", "Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]
start_chars = ["Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]
operators = {"==": "eq?", "+": "+", "-": "-", "!=": "neq?"}
#Convert file into list of lines of words
def get_lines_method():
    file_path = "rlang_examples/gridworld.rlang"
    lines = []
    
    with open(file_path, 'r') as f:
        for _, line in enumerate(f):
            words = line.split()
            if(words): #only add lines if non-empty
                lines.append(words)

    # print("Parsed file into lines and words: ")
    # print(lines)
    effects = {}
    make_dictionary(lines, effects)
    #print(effects)


diction ={"Effect" : {}, "Factor": {}, "Constant": {}, "Proposition" : {}, "Action": {}, "Policy": {}}
#Creates mappings from name of effect to the body of the effect
def make_dictionary(lines, effects):
#    body = []
   for idx, line in enumerate(lines):
        if(line[0] in start_chars):
            body = []
            counter = 1
            if(line[2:] != []): #for one line functions
                body.append(line[3:]) #not great 

            #keep adding to the body of the function if haven't reached another function
            while(idx+counter < len(lines) and lines[idx+counter][0] not in end_characters):
                #remove any comments in lines
                if("#" in lines[idx+counter]):
                    index = lines[idx+counter].index('#')
                    body.append(lines[idx+counter][:index])
                else:
                    body.append(lines[idx+counter])
                counter += 1  
            diction[line[0]][line[1].strip(':')] =body #Udpate dictionary

var_to_num = dict()

def translate_list(line):
    if line == []:
        return "", []
    elif ']' in line[0]:
        line[0] = line[0].replace(']', '')
        return translate_elt(line)
    elif '[' in line[0]:
        line[0] = line[0].replace('[', '')
        line[0] = line[0].replace(',', '')
        out, rst = translate_elt(line)
        out2, rst2 = translate_list(rst)
        return "(" + out + " " + out2 + ")", rst2
    else:
        line[0] = line[0].replace(',', '')
        out, rst = translate_elt(line)
        out2, rst2 = translate_list(rst)
        return out + " " + out2, rst2

def translate_elt(line):
    global global_var_num
    global var_to_num
    global number_pattern
    elt = re.sub(r'[:,()]+', '', line[0])
    elt = elt.replace('(', '')
    elt = elt.replace(')', '')
    if bool(re.match(number_pattern, elt)):
        return elt, line[1:]
    elif elt in var_to_num:
        return "$" + var_to_num[elt], line[1:] 
    elif elt[0] == "[":
        return translate_list(line)
    else:
        var_to_num[elt] = str(global_var_num)
        global_var_num += 1
        return "$" + var_to_num[elt], line[1:]


# input lines
# output: "str_output", rest of lines not included in expression
def translate_one_line(line):
    global operators
    global global_var_num
    if (len(line) == 1):
        return translate_elt(line)
    if (line[0][0] == '('):
        first_expr = line
        first_expr[0] = first_expr[0].replace('(', '')
        out, rst = translate_one_line(line)
        if rst[0] == "and":
            next_expr = rst[1:]
            next_expr[0] = next_expr[0].replace('(', '')
            out2, rst2 = translate_one_line(next_expr)
            return "(and " + out + " " + out2 + ")", rst2
        return out, rst
    elif (line[1] == "->"):
        out, rst = translate_elt(line)
        out2, rst2 = translate_one_line(rst[1:])
        return out2, rst2
    elif (line[1] in operators):
        out, rst = translate_elt(line)
        out2, rst2 = translate_elt(rst[1:])
        return "(" + operators[rst[0]] + " " + out + " " + out2 + ")", rst2
    elif (line[1] == "->"):
        return translate_one_line(line[2:])
    return "<parse-error:one-line>"

def translate_expr(lines):
    if lines == []:
        return "", []
    elif lines[0] == []:
        return translate_expr(lines[1:])
    elif lines[0][0] == 'if' or lines[0][0] == 'elif':
        str_out, rst = translate_if_expr(lines, True)
        str_out + translate_expr(rst), []
    return translate_one_line(lines[0])[0] + translate_expr(lines[1:]) , []

# return array of translated one-liners and then rst (next elif or [])
def translate_if_clause_body(lines, outputList):
    if lines == [] or lines[0] == [] or lines[0][0] == 'elif' or lines[0][0] == 'else:':
       return "empty", lines
    elif lines[0][1] == '->' and lines[0][2] == 'if': # handle nested if statement
        lines[0] = lines[0][2:]
        out, rst = translate_if_expr(lines, False)
        out2, rst2 = translate_if_clause_body(rst, outputList)
        if outputList:
            return "(cons " + out + " " + out2 + ")", rst2
        return out + " " + out2, rst2
        # return "(cons " + out + " " + out2 + ")", rst2 if outputList else out + " " + out2, rst2
    else:
        out, rst = translate_if_clause_body(lines[1:], outputList)
        if outputList:
            return "(cons " + translate_one_line(lines[0])[0] + " " + out + ")", rst
        return translate_one_line(lines[0])[0] + " ", rst
    
# Translates an if expression from Rlang to Lamda calculus
#   lines - an array of lines; each being an array of whitespace-separated
#           elements from the original rlang file
#   outputClauseList - if set to True, each if/elif/else clause will be outputted
#                      as a list of values using con expressions. Else, the clause
#                      will be outputted as the value its expression(s) represents
def translate_if_expr(lines, outputClauseList):
    lam_expr = ""
    if lines == [] or lines[0] == []:
        return "()", lines
    elif lines[0][0] == 'else:':
        out, rst = translate_one_line(lines[1])
        return out, lines[2:]
    elif lines[0][0] == 'if' or lines[0][0] == 'elif':
        lam_expr += "(if" + " "
        lam_expr += translate_one_line(lines[0][1:])[0] + " "
        out, rst = translate_if_clause_body(lines[1:], outputClauseList)
        lam_expr += "" + out + " "
        out2, rst2 = translate_if_expr(rst, True)
        lam_expr += out2 + ")"
        return lam_expr, rst2


get_lines_method()
# print("Effect: ", diction["Effect"]["action_effect"])
# print("---------------------------------")
out, lines = translate_if_expr(diction["Effect"]["action_effect"], True)
print(out)
# print("effects: ", diction["Effect"]["main"])
