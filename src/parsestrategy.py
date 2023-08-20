# D-double S-stand H-hit P-split R-surrender

valid_options = ['D', 'S', 'H', 'P', 'R']

# a function that parses csv input and stores it in a dictionary
def parse_strategy_table(filename, dict):
    lines = []
    try:
        with open('files/' + filename, 'r') as file:
            for line in file:
                line = line.strip()
                lines.append(line)
    except FileNotFoundError:
        raise Exception(f"File '{filename}' not found.")
    except IOError:
        raise Exception(f"Error reading file '{filename}'.")
    
    dict['hard'] = read_table(lines, '---HARD', dict['hard'] if 'hard' in dict else {})
    dict['soft'] = read_table(lines, '---SOFT', dict['soft'] if 'soft' in dict else {})
    dict['pairs'] = read_table(lines, '---PAIRS', dict['pairs'] if 'pairs' in dict else {})

def read_table(lines, table, dict):
    if (lines.index(table) == -1):
        return dict
    dealer_cards = lines[lines.index(table) + 1].split(',')
    for line in lines[lines.index(table) + 2:]:
        if line.startswith('---'):
            break
        values = line.split(',')
        for i in range(1, len(values)):
            if values[i] not in valid_options:
                raise ValueError(f"Invalid option '{values[i]}' found in strategy file.")
            dict[(dealer_cards[i], values[0])] = values[i]
    return dict