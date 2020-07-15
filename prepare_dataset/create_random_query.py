import os
import sys
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


def generate_query_file(query_file):
    os.system('touch ' + query_file)
    os.system('chmod 777 ' + query_file)


def get_random_query_line(filename):
    os.system('wc -l ' + os.path.join(config.DATA_DIR, filename) + ' > tmp.txt')

    opened = open('tmp.txt').readlines()
    file = open(os.path.join(config.DATA_DIR, filename)).readlines()
    first_line = opened[0].replace('\n', '')
    lines = first_line.split()[0]
    range = int(lines)

    query_index = random.randrange(range + 1)
    """
    line_values = file[query_index].split()[1]
    
    values = line_values.split(',')
    values_string = '\'' + str(values[0]) + '\''

    for element in values:
        values_string += ', \'' + str(element) + '\''

    line = str(0) + '\t' + '[' + values_string + ']'
    """

    line = file[query_index]
    os.remove('tmp.txt')

    return line


def main():
    print('\nSelecting random query from dataset...')

    filename = os.listdir(config.DATA_DIR)[0]
    query_file = config.QUERY_FILE

    generate_query_file(query_file)
    line = get_random_query_line(filename)

    open('data/query.txt', 'w').write(line)

    print('Query selected and written to file \'' + query_file + '\'')


if __name__ == '__main__':
    main()
