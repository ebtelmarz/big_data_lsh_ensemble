import os
import config
import random


def generate_query_file(query_file):
    os.system('touch ' + query_file)
    os.system('chmod 777 ' + query_file)


def get_random_query_index(filename):
    os.system('wc -l ' + os.path.join(config.DATA_DIR, filename) + ' > tmp.txt')

    opened = open('tmp.txt').readlines()
    first_line = opened[0].replace('\n', '')
    lines = first_line.split()[0]
    range = int(lines)

    query_index = random.randrange(range + 1)
    os.remove('tmp.txt')

    return query_index


def main():
    print('\nSelecting random query from dataset...')

    i = 0
    filename = os.listdir(config.DATA_DIR)[0]
    file = open(os.path.join(config.DATA_DIR, filename))
    query_file = config.QUERY_FILE

    generate_query_file(query_file)
    query_index = get_random_query_index(filename)

    for line in file:
        i += 1
        if i == query_index:
            os.system('echo \'' + line + '\' > ' + query_file)
            break

    print('Query selected and written to file \'' + query_file + '\'')


if __name__ == '__main__':
    main()
