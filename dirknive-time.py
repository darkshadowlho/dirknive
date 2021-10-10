import os
from datetime import datetime
import argparse
import colorama

## Function to check link of folder or files
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

## Function to classify based on time
def get_date(fl, mod, tm):
    mod_lst = {'modified' : 'st_mtime', 'created' : 'st_ctime'}
    tm_lst = {'year' : '%Y','month' : '%B','weekday': '%A','day' : '%d'}
    if (mod in mod_lst) and (tm in tm_lst):
        mod_tm = mod_lst[mod]
        tmn = tm_lst[tm]
        time_dt = datetime.fromtimestamp(getattr(os.stat(fl),mod_tm))
        return time_dt.strftime(tmn)
    else:
        print('Check input again, error in mode or kind of time')

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on extension of file')
    parser.add_argument('--input','-i',type=str,default='.',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='.',help='Destination for the split folder')
    parser.add_argument('--mode','-m',type=str,default='modified',choices=['created','modified'],help='Mode for get type of time')
    parser.add_argument('--type','-t',type=str,default='year',choices=['year','month','weekday','day'],help='Mode for time format (year, month, weekday, or day)')
    parser.add_argument('--dont_write_txt',default=False,action='store_true',help='Dont write txt file contained operation')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Function to classify based on the date
def lstdatefl(pth_dir,mod,tm,np):
    lst_tm = {}
    amt = 0
    np += 1
    for inner in os.listdir(pth_dir):
        inr_chk = os.path.join(pth_dir, inner)
        ## Condition for file
        if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
            amt += 1
            ctgy = get_date(inr_chk,mod,tm)
            if ctgy not in lst_tm:
                lst_tm[ctgy] = []
            lst_tm[ctgy].append(inr_chk)
        elif not is_nt_link(inr_chk):
            lsttm = lstdatefl(inr_chk,mod,tm,np)
            for key in lsttm:
                if key not in lst_tm:
                    lst_tm[key] = []
                for fl in lsttm[key]:
                    amt += 1
                    lst_tm[key].append(fl)
    ## Useful without count total list
    if np != 1:
        return lst_tm
    else:
        return{'amt' : amt, 'split_lst' : lst_tm}

## Function split dir that work on time version
def split_dir(listtime):
    ## initiation progress
    prog_now = 0
    prog_total = listtime['amt']
    ## Print progress
    print('Progress :\n')
    colorama.init()
    for key in listtime['split_lst']:
        last_file = listtime['split_lst'][key][-1].replace('\\','/')
        if not opt.dont_write_txt:
            temp_ext_dir = []
        for ev_file in listtime['split_lst'][key]:
            ev_file = ev_file.replace('\\','/')
            ## Print progress
            prt_prg(ev_file,prog_now,prog_total)
            ## if parser is set, it will remove the folder structure
            back_path = get_bpath(ev_file,opt.dont_keep_structure,opt.input)
            target_path = opt.output+'/'+key+back_path
            copy_good(ev_file, target_path)
            prog_now += 1
            if not opt.dont_write_txt:
                temp_ext_dir.append(add_inner(ev_file, target_path))
            if (ev_file == last_file):
                ## Printing progress for one category of extension
                print_middle('All file that '+opt.mode+' on '+key+' already transferred.', get_upchar(ev_file))
                ## Writing to text files
                if not opt.dont_write_txt:
                    fp = open(opt.output+'/'+key+'/'+key+'.txt', 'w', encoding='utf-8')
                    fp.write('Operation in file that '+opt.mode+' on '+key+' is :')
                    for i in temp_ext_dir:
                        fp.write('\n\n'+i['src_path']+' is transferred to '+i['dest_path'])
                    fp.close()
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
    ## if src_dir isn't directory, folder split doesn't work
    if os.path.isdir (opt.input):
        listfiletime = lstdatefl(opt.input,opt.mode,opt.type,0)
        split_dir(listfiletime)
    else:
        print('I am sorry, dirknive time only work on directory')

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
------------------- Time Version ------------------------- \n")
    opt = get_args()
    split_est_dir()
                 
            
