RLANG_EXPR_TYPES = [
    'Factor',
    'Constant',
    'Proposition',
    'import',
    'Action',
    'Policy'
]

def get_lines_method():
    file_path = "rlang_examples/gridworld.rlang"
    lines = []
    
    with open(file_path, 'r') as f:
        for line in f:
            # if(printline[0])
            # print(line[0])
            words = line.split()
            if(words):
                if(words[0] == 'Effect'):
                    print("effect")
            # print(words[0])
            lines.append(words)
            # print("Current line: ", )

        
    # print(lines)

def get_expr_body(line):
    line_split = line.split()
    if line_split == [] or line_split[0] == '#' or line_split[0] == '':
        return []
    elif line_split[0] in RLANG_EXPR_TYPES:
        return []
    else:
        return [line_split[0]] + get_expr_body(line_split[1:])

# get_sentences()
get_lines_method()

