
# words_and_lines = []

global_var_num = 0

end_characters = ["#", "Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]
start_chars = ["Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]
operators = ["==", "+", "-"]
#Convert file into list of lines of words
def get_lines_method():
    file_path = "rlang_examples/gridworld.rlang"
    lines = []
    
    with open(file_path, 'r') as f:
        for idx, line in enumerate(f):
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
            #print(line)
            counter = 1
            if(line[2:] != []): #for one line functions
                body.append(line[3:]) #not great 

            #keep adding to the body of the function if haven't reached another function
            while(idx+counter < len(lines) and lines[idx+counter][0] not in end_characters):
                #remove any comments in lines
                if("#" in lines[idx+counter]):
                    # print("# in there")
                    # print(lines[idx+counter])
                    index = lines[idx+counter].index('#')
                    # print("index: ", index)
                    body.append(lines[idx+counter][:index])
                else:
                    body.append(lines[idx+counter])
                counter += 1  
            # effects[line[1].strip(':')] = body 
            diction[line[0]][line[1].strip(':')] =body #Udpate dictionary

var_to_num = dict()

def translate_elt(elt):
    global global_var_num
    global var_to_num
    if elt.isnumeric():
        return elt
    elif elt in var_to_num:
        return "$" + var_to_num[elt]
    elif elt == "[":
        return "<list>"
    else:
        var_to_num[elt] = str(global_var_num)
        global_var_num += 1
        return "$" + var_to_num[elt]


# input lines
# output: "str_output", rest of lines not included in expression
def translate_one_line(line):
    global operators
    global global_var_num
    if (line[1] == "=="):
        return "(= " + translate_elt(line[0]) + " " + translate_elt(line[2]) + ")"
    elif (line[1] in operators):
        first = "$" + str(global_var_num)
        second = "$" + str(global_var_num + 1)
        global_var_num += 2
        return "(" + line[1] + " " + translate_elt(line[0]) + " " + translate_elt(line[2]) + ")"
    elif (line[1] == "->"):
        return translate_one_line(line[2:])
    return "<one-line>"

def translate_expr(lines):
    if lines == []:
        return "", []
    elif lines[0] == []:
        return translate_expr(lines[1:])
    elif lines[0][0] == 'if' or lines[0][0] == 'elif':
        str_out, rst = translate_if_expr(lines)
        str_out + translate_expr(rst), []
    return translate_one_line(lines[0]) + translate_expr(lines[1:]) , []

# def translate_elif_body(lines):
#     if lines == [] or lines[0] == [] or lines[0][0] == 'elif':
#         return ")", lines[1:]
#     else:
#         out, rst = translate_elif_body(lines[1:])
#         return translate_one_line(lines[0]) + " " + out, rst

# return array of translated one-liners and then rst (next elif or [])
def translate_if_clause_body(lines):
    if lines == [] or lines[0] == [] or lines[0][0] == 'elif':
       return "]", lines
    else:
        out, rst = translate_if_clause_body(lines[1:])
        return translate_one_line(lines[0]) + " " + out, rst
    
def translate_if_expr_helper(lines):
    lam_expr = ""
    if lines == [] or lines[0] == []:
        return "()", lines
    elif lines[0][0] == 'if' or lines[0][0] == 'elif':
        lam_expr += "(if" + " "
        lam_expr += translate_one_line(lines[0][1:]) + " "
        out, rst = translate_if_clause_body(lines[1:])
        lam_expr += "[" + out + " "
        out2, rst2 = translate_if_expr_helper(rst)
        lam_expr += out2 + ")"
        return lam_expr, rst2

# def translate_if_expr(lines):
#     lam_expr = ""
#     if lines == [] or lines[0] == []:
#         return "<error>", lines
#     elif lines[0][0] == 'if' or lines[0][0] == 'elif':
#         lam_expr += "(" + lines[0][0] + " "
#         lam_expr += translate_one_line(lines[0][1:])
#         out1, rst1 = translate_elif_body(lines[1:])
#         lam_expr += " " + out1
#         out2, rst2 = translate_elif_body(rst1)
#         lam_expr += " (" + out2
#         return lam_expr + ")", rst2
#     else:
#         return "5", lines


get_lines_method()
# print("Effect: ", diction["Effect"]["action_effect"])
# print("---------------------------------")
out, lines = translate_if_expr_helper(diction["Effect"]["action_effect"])
print(out)
# print("effects: ", diction["Effect"]["main"])
