import os
import shutil
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

## Function to make txt in split folder only
def write_temp(dst_dir, name, list_opr, size_dir):
    fps = open(dst_dir+'\\'+name+'\\'+name+'.txt', 'w', encoding='utf-8')
    opr_list = add_ndir(name, list_opr)
    fps.write('Operation in '+opr_list['name']+' :')
    for i in opr_list['contents']:
        fps.write('\n\n'+i['src_path']+' is transfered to '+i['dest_path'])
    fps.write('\n\nThe Folder Size is '+'%.3f%s' % (size_dir,' MB'))
    fps.close()

## Function to copy file if the destination directory isn't exist
def copy_good(src_path, dst_path):
    back_dst_path = dst_path.replace('\\'+os.path.basename(dst_path),'')
    if not os.path.isdir(back_dst_path):
        os.makedirs(back_dst_path, exist_ok=True)
    if os.path.isfile(src_path):
        shutil.copy(src_path,back_dst_path)
    else:
        print('Sorry, the file is doesnt exist anymore')

## Function to read the arguments
def get_args():
    parser = argparse.ArgumentParser('Part of Dir Knive that have function to divide directory based on size limit')
    parser.add_argument('--input','-i',type=str,default='',help='Source directory of the split folder')
    parser.add_argument('--output','-o',type=str,default='',help='Destination for the split folder')
    parser.add_argument('--size_limit','-s',type=int,default=5120,help='The size of the split folder in MB unit')
    parser.add_argument('--name','-f',type=str,default=None,help='Name of the split folder')
    parser.add_argument('--amount_char','-n',type=int,default=None,help='Amount of number character that used when renaming folder on the behind')
    parser.add_argument('--dont_keep_structure',default=False,action='store_true',help='Argument to keep the folder structure when doing the operation')
    args = parser.parse_args()
    return args

## Main Function
def split_est_dir(opt):
    if not os.path.isdir(opt.output):
        os.makedirs(opt.output)
    ## Making name of the split folder
    if opt.name:
        name_dest_dir = opt.name
    else:
        name_dest_dir = os.path.basename(opt.output)
    ## if src_dir isn't directory, folder split doesn't work
    if os.path.isdir (opt.input):
        ## Store the size of directory input
        src_size = chk_size(opt.input)
        ## Estimate the number of '0' when renaming folder.
        if opt.amount_char:
            num_dir = '%0.'+str(opt.amount_char)+'d'
        else:
            num_dir = '%0.'+str(len(str(int(-(-(src_size)//opt.size_limit)))))+'d'
        ## Initiation place to store operation within size limit
        temp_split_dir = []
        ## initiation number for [split] and [exclude]
        split_num = 1
        size_split_dir = 0
        excl_num = 1
        size_total = 0
        ## store last file to new variable
        last_src_dir = listing_file(opt.input)[-1]
        for ev_file in listing_file(opt.input):
            ## if parser is set, it will remove the folder structure
            if opt.dont_keep_structure:
                back_path = '\\'+os.path.basename(ev_file)
            else:
                back_path = ev_file.replace(opt.input, '')
            ## Settings for file that have size more than size limit
            if chk_size(ev_file) >= opt.size_limit:
                content = []
                name_excl = name_dest_dir+'_exclution'+num_dir % (excl_num)
                target_path = opt.output+'\\'+name_excl+back_path
                copy_good(ev_file,target_path)
                ## counting size total
                size_total += chk_size(ev_file)
                print('The sum size until '+name_excl+' is '+'%.3f%s' % (size_total,' MB')+' [{:>.2%}]'.format(size_total/src_size))
                ## Writing Text Files
                fp = open(opt.output+'\\'+name_excl+'\\'+name_excl+'.txt', 'w', encoding='utf-8')
                fp.write('Operation in '+name_excl+' :\n\n'+ev_file+' is transferred to '+target_path)
                fp.write('\n\nThe Folder Size is '+'%.3f%s' % (chk_size(ev_file),' MB'))
                fp.close()
                excl_num += 1
            else:
                ## For the first file that make sum more than size limit
                if (size_split_dir + chk_size(ev_file) >= opt.size_limit):
                    ## Counting Size Total
                    size_total += size_split_dir
                    print('The sum size until '+name_split+' is '+'%.3f%s' % (size_total,' MB')+' [{:>.2%}]'.format(size_total/src_size))
                    ## Writing to text file
                    write_temp(opt.output, name_split,temp_split_dir,size_split_dir)
                    ## initiate the beginning again
                    size_split_dir = chk_size(ev_file)
                    split_num += 1
                    temp_split_dir = []
                else:
                    size_split_dir += chk_size(ev_file)
                name_split = name_dest_dir+'_split'+num_dir % (split_num)
                target_path = opt.output+'\\'+name_split+back_path
                copy_good(ev_file,target_path)
                temp_split_dir.append(add_inner(ev_file, target_path))
                ## For the last file but the sum still lower than size limit
                if (ev_file==last_src_dir):
                    ## Counting Size Total
                    size_total += size_split_dir
                    print('The sum size until '+name_split+' is '+'%.3f%s' % (size_total,' MB')+' [{:>.2%}]'.format(size_total/src_size))
                    ## Writing to text files
                    write_temp(opt.output, name_split,temp_split_dir,size_split_dir)
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
------------------- Size Version -------------------------")
    opt = get_args()
    split_est_dir(opt)

