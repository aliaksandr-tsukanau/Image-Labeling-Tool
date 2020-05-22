import os


def get_img_paths(dir, extensions=('.jpg', '.png', '.jpeg')):
    '''
    :param dir: folder with files
    :param extensions: tuple with file endings. e.g. ('.jpg', '.png'). Files with these endings will be added to img_paths
    :return: list of all filenames
    '''

    img_paths = []

    for filename in os.listdir(dir):
        if filename.lower().endswith(extensions):
            img_paths.append(os.path.join(dir, filename))

    return img_paths


def make_folder(directory):
    """
    Make folder if it doesn't already exist
    :param directory: The folder destination path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)