import os
from multiprocessing import Pool
from process_tools import full_process_text
from tqdm import tqdm

if __name__ == '__main__':
    directory = 'D:\\Work\\projects\\pycharm\\txts'
    file_paths = os.listdir(directory)[:10]

    # for file in file_paths:
    #     full_process_text(file)

    with Pool(processes=4) as pool:
        pool.map(full_process_text, file_paths)

# dir = 'D:\\Work\\projects\\pycharm\\txts'
# print(os.listdir(dir))


