from pathlib import Path
import collections
import shutil
import os
import sys

file_list = []
interesting_files = []

def program()->None:
    "main program that combines every search options and shows process"
    while True:
        file_name = input()
        pathway = Path(file_name[2:])
        if file_name[:2] == 'D ' and pathway.is_dir() == True:
            directory_caller(pathway)
            sorting_lst_and_print(file_list)
            narrow_search()

        elif file_name[:2] == 'R ' and pathway.is_dir() == True:
            recursive(pathway)
            sorting_lst_and_print(file_list)
            narrow_search()

        else:
            print("ERROR")
            program()
    return

def narrow_search()-> None:
    "narrowing the search with the specific orders and characteristics"
    while True:
        command = input()
        command_two = command[:2]
#A        
        if command == 'A':
            for file in file_list:
                str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
#N                
        elif command_two == 'N ':
            for file in file_list:
                if str(Path(command[2:])) == str(Path(file).name):
                    str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
#E            
        elif command_two == 'E ':
            for file in file_list:
                if str(Path(command[2:])) in str(Path(file).suffix) or str(Path(command[2:])) == str(Path(file).suffix):
                    str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
#T
        elif command_two =='T ':
            for file in file_list:
                if 'txt' in str(Path(file).suffix):
                    f = (Path(file)).open('r')                   
                    for text in f.readlines():
                        if str(Path(command[2:])) in text:
                            str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
#<
        elif command_two =='< ' and int(command[2:])>=0:
            for file in file_list:
                file_size = os.path.getsize(Path(file))
                if int(command[2:]) > file_size:
                    str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
#>                        
        elif command_two =='> ' and int(command[2:])>=0:
            for file in file_list:
                file_size = os.path.getsize(Path(file))
                if int(command[2:]) < file_size:
                    str_path_to_list(Path(file), interesting_files)
            sorting_lst_and_print(interesting_files)
            if len(interesting_files) == 0:
                end_program(interesting_files)
            else:
                action()
            
        else:
            print("ERROR")
            
    return None

def action()->None:
    "perform actions on files which are considered interesting in narrow_search()"
    while True:
        command = input()
#F
        if command=='F':
            for file in sorting_lst(interesting_files):
                if str(Path(file).suffix) == '.txt':
                    f = (Path(file)).open('r')
                    print(f.readline().strip())
                else:
                    print('NOT TEXT')
            sys.exit(0)
#D
        elif command=='D':
            for file in sorting_lst(interesting_files):
                shutil.copyfile(file, file + '.dup')
            sys.exit(0)
#T                
        elif command=='T':
            for file in sorting_lst(interesting_files):
                with open(file,'a'):
                    os.utime(file,None)
            sys.exit(0)
        else:
            print('ERROR')

###supplement functions
            
def path_to_str(path:"path") -> str:
    "turns path into the string"
    str_path = str(path)
    return str_path

def str_path_to_list(path:str, lst:[]) ->None:
    "place strings into a list"
    lst.append(path_to_str(path))
    return None

def file_length(file:tuple) -> int:
    "gets the length of the path"
    return file[1]

def sorting_lst_and_print(lst:[]) -> None:
    "sorts and prints the paths"
    file_tuple = []
    b2 = []
    lst.sort()
    for file in lst:
        file_tuple.append((file, len(str(Path(file).parent))))
    file_tuple.sort(key =file_length)
    for file in file_tuple:
        b2.append(file[0])
    for file in b2:
        print(file)
    return

def sorting_lst(lst:[]) -> "lst":
    "only sorts the paths"
    file_tuple = []
    b2 = []
    lst.sort()
    for file in lst:
        file_tuple.append((file, len(str(Path(file).parent))))
    file_tuple.sort(key =file_length)
    for file in file_tuple:
        b2.append(file[0])
    return b2

def directory_caller(directory: str) -> None:
    "calls the directory out"
    folder = Path(directory)
    for file in folder.iterdir():
        if file.is_file():
            str_path_to_list(file, file_list)

def recursive(directory: str) -> None:
    "makes the program become recursive"
    folder = Path(directory)
    Pathlist = list(folder.iterdir())
    for path in Pathlist:
        if path.is_dir():
            recursive(path)
        elif path.is_file():
            str_path_to_list(path, file_list)
            continue
        
    
def end_program(lst:[])->None:
    'end the program'
    if len(lst) == 0:
        sys.exit(0)
    else:
        pass

if __name__=='__main__':
    program()
