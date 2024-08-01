import os
import os.path as osp


def find_files(directory, pattern=None, contains=None, onlyfirst=True):
    filepath_list = []
    filename_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if contains is not None and file.find(contains) == -1:
                continue
            ext = file[file.rfind(".") :].lower()
            if pattern is not None and not ext.endswith(pattern):
                continue
            filepath_list.append(os.path.join(root, file))
            filename_list.append(file)
        if onlyfirst:
            break
    print("total number of files: %d" % len(filepath_list))
    return filepath_list, filename_list


def get_files_path(input_file, pattern=None, contains=None, onlyfirst=True):
    if input_file and os.path.isfile(input_file):
        imgpath = osp.abspath(input_file)
        imgname = osp.basename(input_file)
        return [imgpath], [imgname]

    infer_dir = os.path.abspath(input_file)
    assert os.path.isdir(infer_dir), "{} is not a directory".format(infer_dir)
    img_paths, img_names = find_files(input_file, pattern, contains, onlyfirst)
    return img_paths, img_names
