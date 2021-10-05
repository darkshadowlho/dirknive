import os
import sys
import shutil
import argparse

## Function to check path is link or not in windows
def is_nt_link(pth_dir):
    return True if (os.path.abspath(pth_dir) != os.path.realpath(pth_dir)) else False

## Function to make list of file from path
def listing_file(pth_dir):
    try :
        content =[]
        for inner in os.listdir(pth_dir):
            inr_chk = os.path.join(pth_dir, inner)
            if os.path.isfile(inr_chk) and not is_nt_link(inr_chk):
                content.append(inr_chk)
            elif not is_nt_link(inr_chk):
                list_file = listing_file(inr_chk)
                for nm_file in list_file:
                    content.append(nm_file)
        return content
    except NotADirectoryError:
        if not is_nt_link(path):
            return [pth_dir]

## Function to make the list of operation
def add_inner(src, dest):
    return {'src_path' : src, 'dest_path' : dest}

def add_ndir(pth_dir, inner):
    return {'name' : pth_dir, 'contents' : inner}

## Function to copy file if the destination directory isn't exist
def copy_good(src_path, dst_path):
    back_dst_path = dst_path.replace('/'+os.path.basename(dst_path),'')
    if not os.path.isdir(back_dst_path):
        os.makedirs(back_dst_path, exist_ok=True)
    if os.path.isfile(src_path)and not os.path.isfile(dst_path):
        shutil.copy(src_path,back_dst_path)
    else:
        print('Sorry, the source file is doesnt exist or destination file already copied')

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on size limit')
    parser.add_argument('--input','-i',type=str,default='',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='',help='Destination for the split folder')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Main Function
def split_est_dir(opt):
    opt.input = opt.input.replace('\\','/')
    opt.output = opt.output.replace('\\','/')
    if not os.path.isdir(opt.output):
        os.makedirs(opt.output)
    ## if src_dir isn't directory, folder split doesn't work
    if os.path.isdir (opt.input):
        ev_file = listing_file(opt.input)
        for n in range(0,len(ev_file)):
            ev_file[n] = ev_file[n].replace('\\','/')
            ## print the progress
            prog = (n+1)/len(ev_file)*40
            sys.stdout.write('\r')
            sys.stdout.write("[%-40s] %.2f%%" % ('='*int(prog), 2.5*prog))
            sys.stdout.flush()
            ## main function
            if opt.dont_keep_structure:
                back_path = '/'+os.path.basename(ev_file[n])
            else:
                back_path = ev_file[n].replace(opt.input, '').replace('\\','/')
            fldr_name = ev_file[n].split('.')[-1].upper()
            target_path = opt.output+'/'+fldr_name+back_path
            copy_good(ev_file[n], target_path) ## opt.output+'/'+fldr_name+'/'+
            if not os.path.isfile(opt.output+'/'+fldr_name+'/'+fldr_name+'.txt'):
                fp = open(opt.output+'/'+fldr_name+'/'+fldr_name+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in '+fldr_name+' :\n\n')
                fp.write(ev_file[n]+' is transfered to '+target_path+'\n\n')
                fp.close()
            else:
                fp = open(opt.output+'/'+fldr_name+'/'+fldr_name+'.txt', 'a', encoding='utf-8')
                fp.write(ev_file[n]+' is transfered to '+target_path+'\n\n')
                fp.close()
    else:
        print('I am sorry, dirknive-type only work on directory')

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
------------------- Type Version ------------------------- \n\
Progress : \n")
    opt = get_args()
    split_est_dir(opt)
        

