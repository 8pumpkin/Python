import os


def rename(path):
    file_list = os.listdir(path)  # get filename in path
    for i in range(len(file_list)):
        file_path = "./file/" + file_list[i]
        file_name, file_type = os.path.splitext(file_path)  # get file type
        old_name = path + os.sep + file_list[i]
        new_name = path + os.sep + str(i) + file_type
        os.renames(old_name, new_name)  # file rename
        print("%s======>%s" % (old_name, new_name))


path = "./file"
rename(path)
