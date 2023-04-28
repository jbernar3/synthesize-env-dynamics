
# words_and_lines = []

end_characters = ["#", "Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]
start_chars = ["Effect" , "Proposition", "Factor", "Action", "Constant", "Policy"]

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

# input lines
# output: "str_output", rest of lines not included in expression
def translate_one_line(line):
    return "<one-line-expr>"

def translate_expr(lines):
    if lines == []:
        "", []
    elif lines[0] == []:
        translate_expr(lines[1:])
    elif lines[0][0] == 'if':
        str_out, rst = translate_if_expr(lines)
        str_out + translate_expr(rst)
    return "Hello", []

def translate_if_expr(lines):
    lam_expr = ""
    if lines == [] or lines[0] == []:
        return "4", lines
    elif lines[0][0] == 'if':
        lam_expr += "(if "
        lam_expr += translate_one_line(lines[0][1:])
        out1, rst1 = translate_expr(lines[1:])
        lam_expr += " " + out1
        out2, rst2 = translate_expr(rst1)
        lam_expr += " " + out2
        return lam_expr + ")", rst2
    else:
        return "5", lines


get_lines_method()
print("Effect: ", diction["Effect"]["action_effect"])
print("---------------------------------")
out, lines = translate_if_expr(diction["Effect"]["action_effect"])
print(out)
# print("effects: ", diction["Effect"]["main"])
