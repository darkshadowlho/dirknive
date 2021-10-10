import os
import json
import colorama
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

'''
=============================
Printing Function
=============================
'''

## Function to get up_char
def get_upchar(fl):
    co = os.get_terminal_size().columns
    stc = 'Transferring '+fl
    ## Counting the upchar
    up_char = int(-(-len(stc)//co))
    '''if (len(stc)%co == 0):
        up_char += 1'''
    return up_char

## Print progress transferring
def prt_prg(fl,g_now,g_tot):
    stc = 'Transferring '+fl
    ## Count the progress
    prog = g_now/g_tot*40
    print(stc)
    print("[%-40s] %.2f%%" % ('='*int(prog), 2.5*prog),end='\t',flush=True)
    if os.name == 'nt':
        print()

## Function to be able print in the middle of progress
def print_middle(str_test,upchar):
    co = os.get_terminal_size().columns
    upchradd = 3 if os.name=='nt' else 1
    print('\033[A'*(upchar+upchradd))
    print(' '*co+'\033[A')
    print(str_test)
    upchrdwn = -1 if os.name=='nt' else 1
    print('\n'*(upchar-upchrdwn))

## Function to clear after print progress
def clr_prg(up_chr):
    co = os.get_terminal_size().columns
    initadd = 2 if os.name == 'nt' else 1 
    print('\033[A'*initadd)
    upchradd = 2 if os.name=='nt' else 1
    for j in range(up_chr+upchradd):
        print(' '*co+'\033[A'*2)
    print()

## Function to print the ending
def print_end():
    print('Operation is done, Thanks for using Dirknive')
    up_end = 1 if os.name == 'nt' else 0
    print("[%-40s] %d%%" % ('='*40, 100)+'\033[A'*up_end)

'''
=============================
End of print function
=============================
'''

## Function to get back path
def get_bpath(fl,strct,src):
    if (strct):
       back_path = '/'+os.path.basename(fl)
    else:
        back_path = fl.replace(src, '').replace('\\','/')
    return back_path

## Function to make the list of operation
def add_inner(src, dest):
    return {'src_path' : src, 'dest_path' : dest}

## Function to copy file if the destination directory isn't exist
def copy_good(src_path, dst_path):
    upchar = get_upchar(src_path)
    back_dst_path = dst_path.replace('/'+os.path.basename(dst_path),'')
    if not os.path.isdir(back_dst_path):
        os.makedirs(back_dst_path, exist_ok=True)
    if os.path.isfile(src_path) and not os.path.isfile(dst_path):
        if os.name == 'nt':
            src_path = src_path.replace('/','\\')
            back_dst_path = back_dst_path.replace('/','\\')
            os.system('%s "%s" "%s"' %('copy /z',src_path,back_dst_path))
        elif os.name == 'posix':
            os.system('%s "%s" "%s"' %('cp -p',src_path,back_dst_path))
        else:
            print_middle('I am sorry the printing maybe will be messed up', upchar)
    else:
        print_middle('Sorry, the source file is doesnt exist or destination file already copied', upchar)

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

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on custom category of extension')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--json',type=str,default='dirknive-custtype.json',help='Path for json file it can be changed if you want')
    parser.add_argument('--dont_write_txt',default=False,action='store_true',help='Dont write txt file contained operation')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function to classify file based on arrangemet
def cust_type(pth_dir, json_pth):
    ## initiation for loop function
    np = 0
    def cust_inner(path_dir, np):
        ## initiation inner function
        np += 1
        amt = 0
        lst_file = {}
        for inner in os.listdir(path_dir):
            inr_chk = os.path.join(path_dir,inner)
            if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
                ## Classify based on category
                amt += 1
                end_file = inner.split('.')[-1]
                category = turn_type(end_file,json_pth)
                ## Append file to list
                if category not in lst_file:
                    lst_file[category] = []
                lst_file[category].append(inr_chk)
            elif not is_nt_link(inr_chk):
                list_file = cust_inner(inr_chk,np)
                ## Rewrite function for file in the folder
                for ctgy in list_file:
                    if ctgy not in lst_file:
                        lst_file[ctgy]=[]
                    ## Append file to the list
                    for in_file in list_file[ctgy]:
                        amt += 1
                        lst_file[ctgy].append(in_file)
        ## Useful without function to count total
        if np != 1:
            return lst_file
        else:
            return {'amt' : amt, 'split_list' : lst_file}
    ## Check if JSON file is valid or not
    if is_json(json_pth):
        return cust_inner(pth_dir,np)
    else:
        print('Error when parsing JSON file or doesnt exist')

## Function split dir that work on type and custom type version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = listtype['amt']
    ## Print progress
    print('Progress : \n')
    colorama.init()
    for key in listtype['split_list']:
        last_file = listtype['split_list'][key][-1].replace('\\','/')
        if not opt.dont_write_txt:
            temp_ext_dir = []
        for ev_file in listtype['split_list'][key]:
            ev_file = ev_file.replace('\\','/')
            ## Print Progress initiation
            prt_prg(ev_file,prog_now,prog_total)
            ## if parser is set, it will remove the folder structure
            back_path = get_bpath(ev_file,opt.dont_keep_structure,opt.input)
            target_path = opt.output+'/'+key+back_path
            copy_good(ev_file, target_path)
            prog_now += 1
            if not opt.dont_write_txt:
                temp_ext_dir.append(add_inner(ev_file, target_path))
            if (ev_file == last_file):
                ## Printing progress for one custom type category
                print_middle('All file in '+key+' category already transferred', get_upchar(ev_file))
                ## Writing to text files
                if not opt.dont_write_txt:
                    fp = open(opt.output+'/'+key+'/'+key+'.txt', 'w', encoding='utf-8')
                    fp.write('Operation in category '+key+' is :')
                    for i in temp_ext_dir:
                        fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                    fp.close()
            ## Clearing after print progress
            clr_prg(get_upchar(ev_file))
    ## ending and thank you
    print_end()

## Main Function
def split_est_dir():
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
---------------- Custom Type Version --------------------- \n")
    opt = get_args()
    split_est_dir()
