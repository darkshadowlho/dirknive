import os
import colorama
import argparse

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

'''
=============================
Basic function
=============================
'''

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

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

'''
=============================
Random function
=============================
'''

def write_txttp(dst_pth,dst_nm,opr_lst):
    fp = open(dst_pth+'/'+dst_nm+'/'+dst_nm+'.txt', 'w', encoding='utf-8')
    fp.write('Operation in folder that contain file with extension '+dst_nm+' is :')
    for i in opr_lst:
        fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
    fp.close()

'''
=============================
Main function
=============================
'''

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on extension of file')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--dont_write_txt',default=False,action='store_true',help='Dont write txt file contained operation')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function to classify based on extension
def list_type(pth_dir,np):
    ## initiation list and count total file
    np += 1
    lst_file = {}
    amt = 0
    for inner in os.listdir(pth_dir):
        inr_chk = os.path.join(pth_dir,inner)
        if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
            ## Operation for file
            amt += 1
            extension = inner.split('.')[-1].upper()
            ## Check if file doesn't have extension will be added to Other
            if inner.split('.')[-1] == inner:
                if ("OTHER" not in lst_file):
                    lst_file["OTHER"]=[]
                lst_file["OTHER"].append(inr_chk)
            else:
                if extension not in lst_file:
                    lst_file[extension] = []
                lst_file[extension].append(inr_chk)
        elif not is_nt_link(inr_chk):
            list_file = list_type(inr_chk,np)
            ## Rewrite the function file in the folder
            for nm_file in list_file:
                if nm_file not in lst_file:
                    lst_file[nm_file]=[]
                ## Append file to list
                for nmn in list_file[nm_file]:
                    amt += 1
                    lst_file[nm_file].append(nmn)
    ## Useful without make function to count total
    if np != 1:
        return lst_file
    else:
        return {'amt' : amt, 'split_list' : lst_file}

## Function split dir that work on type and custom type version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = listtype['amt']
    ## Print progress
    print('Progress :\n')
    colorama.init()
    for key in listtype['split_list']:
        last_file = listtype['split_list'][key][-1].replace('\\','/')
        if not opt.dont_write_txt:
            temp_ext_dir = []
        for ev_file in listtype['split_list'][key]:
            ev_file = ev_file.replace('\\','/')
            ## Print progress initiation
            prt_prg(ev_file,prog_now,prog_total)
            ## Determine target path 
            target_path = opt.output+'/'+key+get_bpath(ev_file,opt.dont_keep_structure,opt.input)
            copy_good(ev_file, target_path)
            prog_now += 1
            if not opt.dont_write_txt:
                temp_ext_dir.append(add_inner(ev_file, target_path))
            if (ev_file == last_file):
                ## Printing progress for one category of extension
                print_middle('All file with '+key+' extension already transferred', get_upchar(ev_file))
                ## Writing to text files
                if not opt.dont_write_txt:
                    write_txttp(opt.output,key,temp_ext_dir)
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
        listfiletype = list_type(opt.input,0)
        split_dir(listfiletype)
    else:
        print('I am sorry, dirknive type only work on directory')

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
------------------- Type Version ------------------------- \n")
    opt = get_args()
    split_est_dir()
        

