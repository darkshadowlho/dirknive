import os
import shutil
import colorama
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

## Function to be able print in the middle of process
def print_middle(str_test,upchar):
    co = shutil.get_terminal_size().columns
    print('\033[A'*(upchar+1))
    print(' '*co+'\033[A',end='')
    print(str_test)
    print('\n'*(upchar-1))

## Function to make the list of operation
def add_inner(src, dest):
    return {'src_path' : src, 'dest_path' : dest}

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
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on amount of file')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--amount_file','-a',type=int,default=10,help='Amount of file in one folder')
    parser.add_argument('--name','-f',type=str,default=None,help='Name of the split folder')
    parser.add_argument('--amount_char','-n',type=int,default=None,help='Amount of number character that used when renaming folder on the behind')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function to classify based on sort by os listdir and number
def list_file(path_dir,amt,lim,np):
    ## initiation for list and loop function detection
    np += 1
    lst_file = {}
    for inner in os.listdir(path_dir):
        inr_chk = os.path.join(path_dir,inner)
        if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
            ## Count the category based on formula
            amt += 1
            num = int(-(-amt//lim))
            ## Append file to list
            if num not in lst_file:
                lst_file[num] = []
            lst_file[num].append(inr_chk)
        elif not is_nt_link(inr_chk):
            ck_file = list_file(inr_chk,amt,lim,np)
            ## Rewrite the function for file in the folder
            for nm in ck_file:
                if nm not in lst_file:
                    lst_file[nm] = []
                ## Append file to list
                for fl in ck_file[nm]:
                    amt += 1
                    lst_file[nm].append(fl)
    ## Useful without count total function
    if np != 1:
        return lst_file
    else:
        return {'amt' : amt, 'split_list' : lst_file}

## Function split dir that work on amount and size version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = listtype['amt']
    colorama.init()
    ## Determine the name of the splitted folder
    if opt.name:
        name_dest_dir = opt.name
    else:
        name_dest_dir = os.path.basename(opt.input)
    ## Estimate the number of 0 after name of the folder
    if opt.amount_char:
        num_dir = '%0.'+str(opt.amount_char)+'d'
    else:
        num_dir = '%0.'+str(len(str(len(listtype['split_list']))))+'d'
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
            numdir_name = name_dest_dir+num_dir % (key)
            target_path = opt.output+'/'+numdir_name+back_path
            copy_good(ev_file, target_path, up_char)
            temp_ext_dir.append(add_inner(ev_file, target_path))
            prog_now += 1
            if (ev_file == last_file):
                ## Printing progress for one category of extension
                print_middle('%d %s' % (prog_now,' file already transferred'), up_char)
                ## Writing to text files
                fp = open(opt.output+'/'+numdir_name+'/'+numdir_name+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in folder '+numdir_name+' is :')
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
        listam_file = list_file(opt.input,0,opt.amount_file,0)
        split_dir(listam_file)
    else:
        print('I am sorry, dirknive amount only work on directory')

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
------------------- Amount Version ------------------------- \n\
Progress : \n")
    opt = get_args()
    split_est_dir(opt)
        

