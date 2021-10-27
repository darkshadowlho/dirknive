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

## Function to get the name of splitted folder
def get_nmdst(nm,src):
    if (nm):
        return nm
    else:
        return os.path.basename(src)

## Function to get number of char
def get_numchar(n_char,n_list):
    if (n_char):
        return '%0.'+str(n_char)+'d'
    else:
        return '%0.'+str(len(str(len(n_list))))+'d'

## Function to write txt
def write_txtamt(dst_pth,dst_nm,opr_lst):
    fp = open(dst_pth+'/'+dst_nm+'/'+dst_nm+'.txt', 'w', encoding='utf-8')
    fp.write('Operation in folder '+dst_nm+' is :')
    for i in opr_lst:
        fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
    fp.close()

## Function to return the amount series or not
def det_as(amt, amtss):
    if (amt == None) and (amtss == None):
        print('Add amount with -a or amount series with -as')
    elif (amt) and (amtss):
        print('Choose between amount or size amount series dont choose both')
    else:
        if (amtss):
            amt = list(map(lambda s: int(s), amtss.split(',')))
        return amt

## Function to return the amount series
def det_amtss(num,lst):
    if type(lst) != list:
        inc = -(-num//lst)
    else:
        tot = sum(lst)
        mult = (-(-num//tot))-1
        num = num - (mult*tot)
        sm_lst = [sum([lst[x] for x in range(len(lst)-i-1)]) for i in range(len(lst))]
        add = 0
        for i in range(len(sm_lst)):
            if num > sm_lst[i]:
                add = len(sm_lst)-i
                break
        inc = (mult*len(lst))+add
    return inc

'''
=============================
Main function
=============================
'''

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on amount of file')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--amount','-a',type=int,default=None,help='Amount of file in one folder')
    parser.add_argument('--amount_series','-as',type=str,default=None,help='Series of amount file in one folder if you doesnt want monotone amount')
    parser.add_argument('--name','-f',type=str,default=None,help='Name of the split folder')
    parser.add_argument('--amount_char','-n',type=int,default=None,help='Amount of number character that used when renaming folder on the behind')
    parser.add_argument('--dont_write_txt',default=False,action='store_true',help='Dont write txt file contained operation')
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
            num = det_amtss(amt,lim)
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
    ## Print progress
    print('Progress :\n')
    colorama.init()
    for key in listtype['split_list']:
        last_file = listtype['split_list'][key][-1].replace('\\','/')
        if not opt.dont_write_txt:
            temp_ext_dir = []
        for ev_file in listtype['split_list'][key]:
            ev_file = ev_file.replace('\\','/')
            ## Print the progress
            prt_prg(ev_file,prog_now,prog_total) 
            ## Determine name folder
            numdir_name = get_nmdst(opt.name,opt.input)+get_numchar(opt.amount_char,listtype['split_list']) % (key)
            ## Determine target path
            target_path = opt.output+'/'+numdir_name+get_bpath(ev_file,opt.dont_keep_structure,opt.input)
            copy_good(ev_file, target_path)
            prog_now += 1
            if not opt.dont_write_txt:
                temp_ext_dir.append(add_inner(ev_file, target_path))
            if (ev_file == last_file):
                ## Printing progress for one category of extension
                print_middle('%d %s' % (prog_now,' file already transferred'), get_upchar(ev_file))
                ## Writing to text files
                if not opt.dont_write_txt:
                    write_txtamt(opt.output,numdir_name,temp_ext_dir)
            ## Clearing after print progress
            clr_prg(get_upchar(ev_file))
    ## Ending and thank you
    print_end()

## Main Function
def split_est_dir():
    opt.input = opt.input.replace('\\','/')
    opt.output = opt.output.replace('\\','/')
    if not os.path.isdir(opt.output):
        os.makedirs(opt.output)
    amt = det_as(opt.amount, opt.amount_series)
    ## if src_dir isn't directory, folder split doesn't work
    if not os.path.isdir (opt.input):
        print('I am sorry, dirknive amount only work on directory')
    elif amt != None:
        listam_file = list_file(opt.input,0,amt,0)
        split_dir(listam_file)
        

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
------------------- Amount Version ----------------------- \n")
    opt = get_args()
    split_est_dir()
