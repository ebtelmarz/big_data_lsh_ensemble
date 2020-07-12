import os


def get_threshold():
    try:
        threshold = open('prepare_dataset/tmp.txt').readlines()[0].replace('\n', '')
    except IndexError:
        threshold = open('prepare_dataset/tmp.txt').readlines()

    #os.remove('prepare_dataset/tmp.txt')

    return {
        'threshold': float(threshold),
        'num_permutations': 128,
        'num_partitions': 32
    }


def main():
    print('\n')
    os.system('./prepare_dataset/bash_scripts/choose_threshold.sh > prepare_dataset/tmp.txt')
    try:
        res = open('prepare_dataset/tmp.txt').readlines()[0].replace('\n', '')
    except IndexError:
        res = open('prepare_dataset/tmp.txt').readlines()

    if res == 'no':
        print('Program exited with error code, please choose a valid threshold value in range [0,1]')


if __name__ == '__main__':
    main()
