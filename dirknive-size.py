import os
import shutil
import colorama
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

## Function to check size from path
def chk_size(path):
    try:
        with os.scandir(path) as it:
            return sum(chk_size(entry) for entry in it if not is_nt_link(entry))
    except NotADirectoryError:
        if not is_nt_link(path):
            return os.stat(path).st_size/(1024**2)

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

## Function to make txt in split folder only
def write_temp(dst_dir, name, list_opr, size_dir):
    fps = open(dst_dir+'/'+name+'/'+name+'.txt', 'w', encoding='utf-8')
    fps.write('Operation in '+name+' :')
    for i in list_opr:
        fps.write('\n\n'+i['src_path']+' is transfered to '+i['dest_path'])
    fps.write('\n\nThe Folder Size is '+'%.3f%s' % (size_dir,' MB'))
    fps.close()

## Function to copy file if the destination directory isn't exist
def copy_good(src_path, dst_path, upchar):
    back_dst_path = dst_path.replace('/'+os.path.basename(dst_path),'')
    if not os.path.isdir(back_dst_path):
        os.makedirs(back_dst_path, exist_ok=True)
    if os.path.isfile(src_path) and not os.path.isfile(dst_path):
        shutil.copy(src_path,back_dst_path)
    else:
        print_middle('Sorry, the source file is doesnt exist or destination file already copied', upchar)

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on size limit')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--size_limit','-s',type=int,default=5120,help='The size of the split folder in MB unit')
    parser.add_argument('--name','-f',type=str,default=None,help='Name of the split folder')
    parser.add_argument('--amount_char','-n',type=int,default=None,help='Amount of number character that used when renaming folder on the behind')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function to classify based on size
def listszfile(pth_dir,sz_lim,tot_sz,chk_sz,s_n,e_n,np):
    ## initiation for dict and track num of loop function
    lst_sz = {}
    np += 1
    for inner in os.listdir(pth_dir):
        inr_chk = os.path.join(pth_dir, inner)
        ## Condition for file
        if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
            f_sz = round(chk_size(inr_chk),4)
            tot_sz += f_sz
            ## Check if size of file more than size limit
            if (f_sz >= sz_lim):
                e_ns = '%s%d'%('e',e_n)
                ## Append to list
                lst_sz[e_ns] = []
                lst_sz[e_ns].append([f_sz,inr_chk])
                e_n += 1
            else:
                ## Check for the first file that make sum more than size limit
                if (chk_sz + f_sz >= sz_lim):
                    chk_sz = f_sz
                    s_n += 1
                else:
                    chk_sz += f_sz
                s_ns = '%s%d'%('s',s_n)
                ## Append to list
                if s_ns not in lst_sz:
                    lst_sz[s_ns] = []
                lst_sz[s_ns].append([f_sz,inr_chk])
        elif not is_nt_link(inr_chk):
            subfl_lst = listszfile(inr_chk,sz_lim,tot_sz,chk_sz,s_n,e_n,np)
            for b_fdr in subfl_lst:
                ## Rewrite program for file more than size limit
                if b_fdr[0]=='e':
                    e_n += 1
                    lst_sz[b_fdr] = []
                    lst_sz[b_fdr].append(subfl_lst[b_fdr][0])
                    tot_sz += subfl_lst[b_fdr][0][0]
                else:
                    ## Rewrite program for another file
                    for fl_data in subfl_lst[b_fdr]:
                        tot_sz += fl_data[0]
                        ## Checking for first file that make sum more than size limit
                        if (chk_sz + fl_data[0] >= sz_lim):
                            chk_sz = fl_data[0]
                            s_n += 1
                        else:
                            chk_sz += fl_data[0]
                        ## You can move up this below code to up because it don't need key again 
                        if b_fdr not in lst_sz:
                            lst_sz[b_fdr] = []
                        lst_sz[b_fdr].append(fl_data)
    ## Useful without creating function to count total size
    if np != 1:
        return lst_sz
    else:
        return {'tot_sz' : round(tot_sz,4), 'split_list' : lst_sz}

## Function split dir that work on amount and size version
def split_dir(listtype):
    ## initiation progress
    prog_now = 0
    prog_total = listtype['tot_sz']
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
        last_file = listtype['split_list'][key][-1][1].replace('\\','/')
        temp_ext_dir = []
        split_sum = 0
        for ev_file in listtype['split_list'][key]:
            ev_file[1] = ev_file[1].replace('\\','/')
            ## Progress initiation
            col = shutil.get_terminal_size().columns
            sentence = 'Transferring '+ev_file[1]
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
                back_path = '/'+os.path.basename(ev_file[1])
            else :
                back_path = ev_file[1].replace(opt.input, '').replace('\\','/')
            ## Determine split folder name exclution or split
            if key[0]=='e':
                dirsz_name = name_dest_dir+'_exclution'+num_dir % (int(key[1:]))
            else:
                dirsz_name = name_dest_dir+'_split'+num_dir % (int(key[1:]))
            target_path = opt.output+'/'+dirsz_name+back_path
            copy_good(ev_file[1], target_path, up_char)
            temp_ext_dir.append(add_inner(ev_file[1], target_path))
            prog_now += ev_file[0]
            split_sum += ev_file[0]
            if (ev_file[1] == last_file):
                ## Printing progress for one category of extension
                print_middle('The sum size until '+dirsz_name+' %s %.3f %s [%.2f%%]' % ('is',prog_now,'MB',prog_now/prog_total*100), up_char)
                ## Writing to text files
                fp = open(opt.output+'/'+dirsz_name+'/'+dirsz_name+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in folder '+dirsz_name+' is :')
                for i in temp_ext_dir:
                    fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                fp.write('%s %.3f %s' % ('\n\nThe Folder Size is ',split_sum,'MB'))
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
        listsz_file = listszfile(opt.input,opt.size_limit,0,0,1,1,0)
        split_dir(listsz_file)
    else:
        print('I am sorry, dirknive-size only work on directory')

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
------------------- Size Version ------------------------- \n\
Progress : \n")
    opt = get_args()
    split_est_dir(opt)

