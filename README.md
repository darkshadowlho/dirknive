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

## For `size version`, the command is : 
```
python dirknive-size.py -i [source_folder] -o [destination_folder] -s [size split folder in MB unit]
```

### What if size of file more than size split folder ?
The file will be excluded to folder exclution

### What is good feature ?
It will resulted good notes inside splitted or exclution folder with size of the folder. 

### Added Option
```
-f [name_folder] => name of folder, the default value is base path of source folder 
-n [num_char_folder] => number of character after name of splitted or exclution folder. Default value is using my formula haha.
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `type version`, the command is : 
```
python dirknive-type.py -i [source_folder] -o [destination_folder]
```
### Added Option
```
--dont_keep_structure => if you want all file doesn't have root folder.
```

## For `custom type version`, the command is : 
```
python dirknive-custtype.py -i [source_folder] -o [destination_folder]
```
This version will split the folder based on custom arrangement on the json file, you can see at this [example](https://github.com/darkshadowlho/dirknive/blob/main/dirknive-custtype.json)
### Added Option
```
--json [path of your json file] => if you want to rename the json file.
--dont_keep_structure => if you want all file doesn't have root folder.
```






