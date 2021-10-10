import os
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

## Function to check size from path
def chk_size(path):
    try:
        with os.scandir(path) as it:
            return sum(chk_size(entry) for entry in it if not is_nt_link(entry))
    except NotADirectoryError:
        if not is_nt_link(path):
            return os.stat(path).st_size/(1024**2)

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

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on size limit')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--size_limit','-s',type=int,default=5120,help='The size of the split folder in MB unit')
    parser.add_argument('--name','-f',type=str,default=None,help='Name of the split folder')
    parser.add_argument('--amount_char','-n',type=int,default=None,help='Amount of number character that used when renaming folder on the behind')
    parser.add_argument('--dont_write_txt',default=False,action='store_true',help='Dont write txt file contained operation')
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
    ## Print progress started
    print('Progress :\n')
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
        ## Check option for dont_write_txt
        if not opt.dont_write_txt:
            temp_ext_dir = []
            split_sum = 0
        for ev_file in listtype['split_list'][key]:
            ev_file[1] = ev_file[1].replace('\\','/')
            ## Print Progress
            prt_prg(ev_file[1],prog_now,prog_total)
            ## if parser is set, it will remove the folder structure
            back_path = get_bpath(ev_file[1],opt.dont_keep_structure,opt.input)
            ## Determine split folder name exclution or split
            if key[0]=='e':
                dirsz_name = name_dest_dir+'_exclution'+num_dir % (int(key[1:]))
            else:
                dirsz_name = name_dest_dir+'_split'+num_dir % (int(key[1:]))
            target_path = opt.output+'/'+dirsz_name+back_path
            copy_good(ev_file[1], target_path)
            prog_now += ev_file[0]
            if not opt.dont_write_txt:
                temp_ext_dir.append(add_inner(ev_file[1], target_path))
                split_sum += ev_file[0]
            if (ev_file[1] == last_file):
                ## Printing progress for one category of extension
                print_middle('The sum size until '+dirsz_name+' %s %.3f %s [%.2f%%]' % ('is',prog_now,'MB',prog_now/prog_total*100), get_upchar(ev_file[1]))
                ## Writing to text files
                if not opt.dont_write_txt:
                    fp = open(opt.output+'/'+dirsz_name+'/'+dirsz_name+'.txt', 'w', encoding='utf-8')
                    fp.write('Operation in folder '+dirsz_name+' is :')
                    for i in temp_ext_dir:
                        fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                    fp.write('%s %.3f %s' % ('\n\nThe Folder Size is ',split_sum,'MB'))
                    fp.close()
            ## Clearing after print progress
            clr_prg(get_upchar(ev_file[1]))
    ## Ending and thank You
    print_end()

## Main Function
def split_est_dir():
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
------------------- Size Version ------------------------- \n")
    opt = get_args()
    split_est_dir()

