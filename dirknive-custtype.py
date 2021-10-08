import os
import json
import shutil
import colorama
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

## Function to check JSON file
def is_json(s):
    try:
        s = s.replace('\\','/')
        json.load(open(s))
        return True
    except FileNotFoundError or ValueError:
        return False

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
    np = 0
    def cust_inner(path_dir, np):
        np += 1
        amt = 0
        lst_file = {}
        for inner in os.listdir(path_dir):
            inr_chk = os.path.join(path_dir,inner)
            if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
                amt += 1
                end_file = inner.split('.')[-1]
                category = turn_type(end_file,json_pth)
                if category not in lst_file:
                    lst_file[category] = []
                lst_file[category].append(inr_chk)
            elif not is_nt_link(inr_chk):
                list_file = cust_inner(inr_chk,np)
                for ctgy in list_file:
                    if ctgy not in lst_file:
                        lst_file[ctgy]=[]
                    for in_file in list_file[ctgy]:
                        amt += 1
                        lst_file[ctgy].append(in_file)
        if np != 1:
            return lst_file
        else:
            return {'amt' : amt, 'split_list' : lst_file}
    if is_json(json_pth):
        return cust_inner(pth_dir,np)
    else:
        print('Error when parsing JSON file or doesnt exist')

## Function to make the list of operation
def add_inner(src, dest):
    return {'src_path' : src, 'dest_path' : dest}

## Function to be able print in the middle of process
def print_middle(str_test,upchar):
    co = shutil.get_terminal_size().columns
    print('\033[A'*(upchar+1))
    print(' '*co+'\033[A',end='')
    print(str_test)
    print('\n'*(upchar-1))

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
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--json',type=str,default='dirknive-custtype.json',help='Path for json file it can be changed if you want')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function split dir that work on type and custom type version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = listtype['amt']
    colorama.init()
    for key in listtype['split_list']:
        last_file = listtype['split_list'][key][-1].replace('\\','/')
        temp_ext_dir = []
        for ev_file in listtype['split_list'][key]:
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
            print("[%-40s] %.2f%%" % ('='*int(prog), 2.5*prog),end='\t')
            ## if parser is set, it will remove the folder structure
            if opt.dont_keep_structure:
                back_path = '/'+os.path.basename(ev_file)
            else :
                back_path = ev_file.replace(opt.input, '').replace('\\','/')
            target_path = opt.output+'/'+key+back_path
            copy_good(ev_file, target_path, up_char)
            temp_ext_dir.append(add_inner(ev_file, target_path))
            prog_now += 1
            if (ev_file == last_file):
                ## Printing progress for one custom type category
                print_middle('All file in '+key+' category already transferred', up_char)
                ## Writing to text files
                fp = open(opt.output+'/'+key+'/'+key+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in category '+key+' is :')
                for i in temp_ext_dir:
                    fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                fp.close()
            ## Clearing after print progress
            print('\033[A')
            for j in range(up_char+1):
                print(' '*col+'\033[A'*3)
            print()
    print('Operation is done, Thanks for using Dirknive')
    print("[%-40s] %d%%\033[A" % ('='*40, 100))

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
