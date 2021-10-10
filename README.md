# Dirknive
```
     ## ##           ##              ##                     
     ## ##           ## ###          ##                 
#######      ######  ## ##   ######       ##  ##  ######
####### ### ######   ###     ####### ###  ##  ### ### 
##   ## ### ###      ###     ##  ### ###  ##  ### ######
##   ## ### ###      ## ##   ##  ### ###  ##  ### ######
####### ### ###      ## ###  ##  ### ###  ######  ###
####### ##  ###      ## ###  ##  ##  ##    ####   ######
```

## For `size version`, the command is : :point_down:
```
python dirknive-size.py -i [source_folder] -o [destination_folder] -s [size split folder in MB unit]
```
### What is good feature ?
 - It will resulted good notes inside splitted or exclution folder with size of the folder. :kissing_heart::kissing_heart:
 - The progress can be monitored from terminal or CMD :open_mouth::open_mouth:
### What if size of file more than size split folder ?
The file will be excluded to folder exclution :joy::joy:
### Added Option
```
-f [name_folder] => name of folder, the default value is base path of source folder 
-n [num_char_folder] => number of character after name of splitted or exclution folder. Default value is using my formula haha.
--dont_write_txt => if you dont want to write text file that containing list operation and size of folder.
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `time version`, the command is : :point_down:
```
python dirknive-time.py -i [source_folder] -o [destination_folder] -t [type of time(day, weekday, month, year)]
```
This option will divide file based on the recent time file being modified. For detailed result of the split operation you can see at python documentation about [datetime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) :joy::kissing_heart:
### Added Option
```
-m [modified or created] => created time only work on windows since I am still don't know how to get created time on posix machine. 
--dont_write_txt => if you dont want to write text file that containing list operation and size of folder.
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `amount version`, the command is : :point_down:
```
python dirknive-amount.py -i [source_folder] -o [destination_folder] -a [number of file in one folder]
```
### Added Option
```
-f [name_folder] => name of folder, the default value is base path of source folder 
-n [num_char_folder] => number of character after name folder.
--dont_write_txt => if you dont want to write text file that containing list operation.
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `type version`, the command is : :point_down:
```
python dirknive-type.py -i [source_folder] -o [destination_folder]
```
### Added Option
```
--dont_write_txt => if you dont want to write text file that containing list operation.
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `custom type version`, the command is : :point_down:
```
python dirknive-custtype.py -i [source_folder] -o [destination_folder]
```
This version will split the folder based on custom arrangement on the json file, you can see at this [example](https://github.com/darkshadowlho/dirknive/blob/main/dirknive-custtype.json) :wink::wink:
### Added Option
```
--json [path of your json file] => if you want to rename the json file.
--dont_write_txt => if you dont want to write text file that containing list operation.
--dont_keep_structure => if you want all file doesn't have root folder.
```
