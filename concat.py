import os

root_path = 'D:\\Desktop\\busyluo'
save_path = 'D:\\Desktop\\busyluo_concat'

def process_lecture(lec_path, lec_name, save_sec_path):
    print(lec_path, lec_name, save_sec_path)
    files = os.listdir(lec_path)
    
    sources = '+'.join(files)
    dest = os.path.join(save_sec_path, lec_name) + '.ts'
    dest = "\"" + dest + "\""
    cmd = 'copy /b ' + sources + ' ' + dest
    os.chdir(lec_path)
    #print(cmd)
    os.system(cmd)

for sec in os.listdir(root_path):
    sec_path = os.path.join(root_path, sec)
    if os.path.isfile(sec_path):
        continue
    print(sec)

    concat_sec_path = os.path.join(save_path, sec)
    if not os.path.exists(concat_sec_path):
        os.mkdir(concat_sec_path)

    for lec in os.listdir(sec_path):
        lec_path = os.path.join(sec_path, lec)
        if os.path.isfile(lec_path):
            continue
        print(lec)
        process_lecture(lec_path, lec, concat_sec_path)
    

