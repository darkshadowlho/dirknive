import os
import sys
import json
import shutil
import colorama
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

## Function to turn extension to custom type
def turn_type(ext,json_pth):
    reslt = 'Other'
    json_file = open(json_pth)
    ref_type = json.load(json_file)
    for ctg in ref_type:
        if ext.lower() in ref_type[ctg]:
            reslt = ctg
    return(reslt)

## Function to classify file based on arrangemet
def cust_type(pth_dir, json_pth):
    def cust_inner(path_dir):
        lst_file = {}
        for inner in os.listdir(path_dir):
            inr_chk = os.path.join(path_dir,inner)
            if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
                end_file = inner.split('.')[-1]
                category = turn_type(end_file,json_pth)
                if category not in lst_file:
                    lst_file[category] = []
                lst_file[category].append(inr_chk)
            elif not is_nt_link(inr_chk):
                list_file = cust_inner(inr_chk)
                for ctgy in list_file:
                    if ctgy not in lst_file:
                        lst_file[ctgy]=[]
                    for in_file in list_file[ctgy]:
                        lst_file[ctgy].append(in_file)
        return lst_file
    if os.path.isfile(json_pth):
        return cust_inner(pth_dir)
    else:
        print('JSON file doesnt exist')

## Function to count list of file
def count_type(reslt):
    tot = 0
    for typ in reslt:
        for item in reslt[typ]:
            tot +=1
    return tot

## Function to make the list of operation
def add_inner(src, dest):
    return {'src_path' : src, 'dest_path' : dest}

## Function to be able print in the middle of process
def print_middle(str_test, upchar):
    co = shutil.get_terminal_size().columns
    sys.stdout.write('\r'+'\033[A'*upchar+' '*co+'\033[A')
    print(str_test)
    sys.stdout.write('\n'*upchar)
    sys.stdout.flush()

## Function to copy file if the destination directory isn't exist
def copy_good(src_path, dst_path, upchar):
    back_dst_path = dst_path.replace('/'+os.path.basename(dst_path),'')
    if not os.path.isdir(back_dst_path):
        os.makedirs(back_dst_path, exist_ok=True)
    if os.path.isfile(src_path)and not os.path.isfile(dst_path):
        shutil.copy(src_path,back_dst_path)
    else:
        print_middle('Sorry, the source file is doesnt exist or destination file already copied', upchar)

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on size limit')
    parser.add_argument('--input','-i',type=str,default='',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='',help='Destination for the split folder')
    parser.add_argument('--json',type=str,default='dirknive-custtype.json',help='Path for json file it can be changed if you want')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function split dir that work on type and custom type version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = count_type(listtype)
    colorama.init()
    for extension in listtype:
        last_file = listtype[extension][-1].replace('\\','/')
        temp_ext_dir = []
        for ev_file in listtype[extension]:
            ev_file = ev_file.replace('\\','/')
            ## Progress initiation
            col = shutil.get_terminal_size().columns
            sentence = 'Transferring '+ev_file
            ## Counting the upchar
            up_char = int(-(-len(sentence)//col))
            if (len(sentence)%col == 0):
                up_char += 1
            ## Count the progress
            prog = prog_now/prog_total*40
            print(sentence)
            sys.stdout.write("[%-40s] %.2f%%" % ('='*int(prog), 2.5*prog))
            sys.stdout.flush()
            ## if parser is set, it will remove the folder structure
            if opt.dont_keep_structure:
                back_path = '/'+os.path.basename(ev_file)
            else :
                back_path = ev_file.replace(opt.input, '').replace('\\','/')
            target_path = opt.output+'/'+extension+back_path
            copy_good(ev_file, target_path, up_char)
            temp_ext_dir.append(add_inner(ev_file, target_path))
            prog_now += 1
            if (ev_file == last_file):
                ## Printing progress for one category of extension
                print_middle('All file in '+extension+' category already transferred', up_char)
                ## Writing to text files
                fp = open(opt.output+'/'+extension+'/'+extension+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in category '+extension+' is :')
                for i in temp_ext_dir:
                    fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                fp.close()
            ## Clearing after print progress
            sys.stdout.write('\r')
            for j in range(up_char+1):
                sys.stdout.write(' '*col+'\033[A'*2)
            sys.stdout.flush()
            print()
    print('Operation is done, Thanks for using Dirknive')
    sys.stdout.write("[%-40s] %d%%" % ('='*40, 100))

## Main Function
def split_est_dir(opt):
    opt.input = opt.input.replace('\\','/')
    opt.output = opt.output.replace('\\','/')
    if not os.path.isdir(opt.output):
        os.makedirs(opt.output)
    ## if src_dir isn't directory, folder split doesn't work
    if os.path.isdir (opt.input):
        listcusttype = cust_type(opt.input,opt.json)
        if (listcusttype != None):
            split_dir(listcusttype)
    else:
        print('I am sorry, dirknive custom type only work on directory')

## Execute main function
if __name__ == '__main__':
    print ("==========================================================\n\
     ## ##           ##              ##                    \n\
     ## ##           ## ###          ##                    \n\
#######      ######  ## ##   ######       ##  ##  ######   \n\
####### ### ######   ###     ####### ###  ##  ### ###      \n\
##   ## ### ###      ###     ##  ### ###  ##  ### ######   \n\
##   ## ### ###      ## ##   ##  ### ###  ##  ### ######   \n\
####### ### ###      ## ###  ##  ### ###  ######  ###      \n\
####### ##  ###      ## ###  ##  ##  ##    ####   ######   \n\
========================================================== \n\
---------------- Custom Type Version --------------------- \n\
Progress : \n")
    opt = get_args()
    split_est_dir(opt)
