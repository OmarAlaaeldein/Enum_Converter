import os
import random
class Finder:
    def __init__(self,path=os.getcwd()):
        list_of_enumfiles = []
        dic_of_enumfiles = {}
        self.list_of_enumfiles=list_of_enumfiles
        self.dic_of_enumfiles=dic_of_enumfiles
        self.path=path
    def Recursive_files_Traversal(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(('.c', '.cpp', '.h', '.hpp')) and Finder.Enum_Detector(os.path.join(root, file)):
                    self.list_of_enumfiles.append(os.path.join(root, file))
        print('Converting...', *self.list_of_enumfiles, sep='\n')
    def Files_list(self):
        return self.list_of_enumfiles
    def Files_dicts(self):
        return self.dic_of_enumfiles
    @staticmethod
    def Enum_Detector(file_path):
        with open(file_path, 'r') as file:
            for i in file.readlines():
                if i.startswith('enum') or (i.startswith('typedef') and 'enum' in i):
                    return True
class Creator(Finder):
    def __init__(self):
        super().__init__()
    def Content_Extractor(self):
        for i in self.Files_list():
            self.Files_dics()[i] = Creator.Enum_Extractor(i)
    @staticmethod
    def Make_Dir(name='enums'):
        try:
            os.makedirs(name)  # create directory
        except:
            pass
    @staticmethod
    def randomize():
        a, b = 'abcdefghijklmnopqrstuvwxyz', ''
        b = ''
        for i in range(7):
            b += random.choice(a)
        return b
    @staticmethod
    def Enum_Extractor(path):
        s = []
        with open(path, 'r') as enums:
            x = enums.readlines()
            for i in range(len(x)):
                c = 1
                enumcounter = 0
                t=True
                if x[i].startswith('enum') or (x[i].startswith('typedef') and 'enum' in x[i]):
                    stuff = x[i].split()
                    if stuff[0] == 'typedef':
                        stuff.remove('enum')
                    if len(stuff) > 1:
                        if len(stuff[1]) < 3:
                            stuff[1] = "{}{}{}:\n".format(Creator.randomize(),'(Enum)',stuff[1])
                            t = False
                    stuff[0] = 'class'
                    if t:
                        stuff[-1] = stuff[-1] + '(Enum):\n'
                    x[i] = ' '.join(stuff)
                    x[i]=x[i].replace('{','')
                    s.append(x[i])
                    while ';' not in x[i + c]:
                        x[i + c] = Factory.Comment(x[i+c])
                    #   x[i + c] = x[i + c].replace('{', '')
                    #   x[i + c] = x[i + c].replace('}', '')
                    #   x[i + c] = x[i + c].replace('/*', '#')
                    #   x[i + c] = x[i + c].replace('///< ', '#')
                        if '=' not in x[i + c]:
                            x[i+c]=x[i+c].replace(',','={}'.format(enumcounter))
                            try:
                                if '=' not in x[i + 1+c]:
                                    x[i+c+1]=x[i+c+1].replace(',','={}'.format(enumcounter+1))
                            except:
                                pass
                        enumcounter += 1
                        s.append(x[i + c])
                        c += 1
                        i
        return s
    def Execute_Creation(self):
        Creator.Make_Dir()
        self.Content_Extractor()
class Writer(Creator,Finder):
    def Write_files(self):
        for i, j in self.Files_dics().items():
            og=i
            i = i.split('\\')[-1] + '.py'
            path = r'enums\{}'.format(i)
            with open(path, 'w') as create:
                create.write('from enum import Enum \n#  Original path is: {}\n'.format(og))
                create.writelines(j)
class Factory: # Factory Pattern design Implemented
    @staticmethod
    def Comment(line):
        if '/*' in line:
            return line.replace('/*', '#')
        if '///<' in line:
            return line.replace('///< ', '#')
        elif '{' in line:
            return line.replace('{', '')
        elif '}' in line:
            return line.replace('}','')
        else:
            return line
def Driver():
    a=Writer()
    a.Recursive_files_Traversal()
    a.Execute_Creation()
    a.Write_files()
Driver()