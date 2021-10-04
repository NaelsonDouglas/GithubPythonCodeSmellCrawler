def update_file(path, new_content):
    f = open(path, 'a')
    f.write(new_content)
    f.close()



def update_file(path, new_content):
    with open(path, 'a') as f:
        f.write(new_content)