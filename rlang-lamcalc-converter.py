

def get_lines_method():
    file_path = "gridworld.rlang"
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

def find_end_of_effect():
    pass


# get_sentences()
get_lines_method()

