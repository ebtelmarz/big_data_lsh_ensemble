import os
import platform
import config


def check_if_dataset_exists(dataset_filename):
    fn = dataset_filename
    result = os.path.exists(config.DATA_DIR + fn)
    if result:
        return result

    return result


def check_if_dataset_filename_is_valid(dataset_filename):
    if dataset_filename in config.DATASETS_REFERENCES.keys():
        return True
    print(dataset_filename + ' is not a valid reference. Check config.DATASET_REFERENCES')

    return False


def download_dataset(dataset_filename):
    if platform.system() == 'Windows':
        os.chdir(config.DATA_DIR)
        print('Using curl to download dataset ' + dataset_filename)
        os.system('curl ' + config.DATASETS_REFERENCES[dataset_filename] + ' --output ' + dataset_filename)
        os.chdir('..')

    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.chdir(config.DATA_DIR)
        print('Using wget to download dataset ' + dataset_filename)
        os.system('wget ' + config.DATASETS_REFERENCES[dataset_filename])
        os.chdir('..')

    if check_if_dataset_exists(dataset_filename):
        return dataset_filename
    return None


def extract_dataset(dataset_filename):
    decompressed_dataset_filename = dataset_filename[:len(dataset_filename) - 3]  # remove .gz

    print('Extracting data...')

    os.chdir(config.DATA_DIR)
    os.system('gzip -d ' + dataset_filename)
    os.chdir('..')

    print('Dataset \'' + decompressed_dataset_filename + '\' extracted to folder: ' + config.DATA_DIR)

    return decompressed_dataset_filename


def download_dataset_if_needed(dataset_filename):
    decompressed_dataset_filename = dataset_filename[:len(dataset_filename) - 3]
    if not check_if_dataset_exists(decompressed_dataset_filename) and check_if_dataset_filename_is_valid(dataset_filename):
        print('Dataset ' + dataset_filename + " wasn't downloaded, i'll try to download it right now...")

        if download_dataset(dataset_filename) == dataset_filename:
            return extract_dataset(dataset_filename)

    if check_if_dataset_exists(decompressed_dataset_filename):
        return decompressed_dataset_filename

    return None


def choose_dataset(dataset, key):
    index = 0
    choices = {}
    print('\nAVAILABLE DATASETS FOR ' + key + ' EXECUTION: \n')
    for line in dataset.keys():
        print('[' + str(index) + '] ' + line[:len(line) - 7])
        choices.update({str(index): line})
        index += 1
    print('\n')
    os.system('./prepare_dataset/bash_scripts/choose_dataset.sh > tmp.txt')
    print('\n')
    res1 = open('tmp.txt').readlines()[0].replace('\n', '')
    dataset_filename = choices[res1]

    return dataset_filename


def clean_data_dir():
    files = os.listdir(config.DATA_DIR)
    for file in files:
        os.system('rm ' + os.path.join(config.DATA_DIR, file))


def main():
    clean_data_dir()
    os.system('./prepare_dataset/bash_scripts/choose_environment.sh > tmp.txt')
    try:
        input_value = open('tmp.txt').readlines()[0].replace('\n', '')
    except IndexError:
        input_value = open('tmp.txt').readlines()
    os.remove('tmp.txt')

    if not (input_value == 'l' or input_value == 'L' or input_value == 'C' or input_value == 'c'):
        print("Program exited with error code, please choose a valid execution environment: 'C' or 'L'")
    elif input_value == 'L' or input_value == 'l':
        key = 'LOCAL'
        dataset_filename = choose_dataset(config.DATASETS_REFERENCES_LOCAL, key)
        download_dataset_if_needed(dataset_filename)
    elif input_value == 'C' or input_value == 'c':
        key = 'CLUSTER'
        dataset_filename = choose_dataset(config.DATASETS_REFERENCES_CLUSTER, key)
        download_dataset_if_needed(dataset_filename)

    os.remove('tmp.txt')


if __name__ == '__main__':
    main()
