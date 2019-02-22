import sys

class NotFound(Exception):
    pass

class NoArgValue(Exception):
    pass

helpstring ="""python main.py [options] [type] file
[options]
-h: prints this chunck of text.
-f: Uses custom file for morse code. Must be formatted with char,code. Defaults to morsesheet.csv.
-w: Character used to signify a space between words. Defaults to |.
-c: Character used to signify a new character. Defaults to a space.

[type]
-m: Converts Morsecode to English.
-e: Converts English to Morse.
"""

class Node:
    def __init__(self, parent, index, key, value):
        self.parent = parent
        self.index = index
        self.left=None
        self.right=None
        self.key = key
        self.value = value
    def __str__(self):
        return str([self.parent, self.index, self.left, self.right, self.key, self.value])
        
class BTS:
    def __init__(self):
        self.rootkey=0
        self.morselist=[Node('-1',0,' ',' ')]

    def __str__(self):
        testlist=[]
        for item in self.morselist:
            testlist.append(item.__str__())
        return str(testlist)
    
    def append(self, key, value):
        parentkey=self.rootkey
        side=None
        
        for test in range(len(key)):
            if key[test] == '.':
                if self.morselist[parentkey].left == None:
                    self.morselist.append(Node(parentkey,len(self.morselist),key,value))
                    self.morselist[parentkey].left=len(self.morselist)-1
                else:
                    parentkey=self.morselist[parentkey].left
            else:
                if self.morselist[parentkey].right == None:
                    self.morselist.append(Node(parentkey,len(self.morselist),key,value))
                    self.morselist[parentkey].right=len(self.morselist)-1
                else:
                    parentkey=self.morselist[parentkey].right
                    
    def search(self, key):
        parentkey = self.rootkey
        for k in range(len(key)):
            if parentkey == None:
                raise NotFound
            
            if key[k] == '.':
                parentkey = self.morselist[parentkey].left
            else:
                parentkey = self.morselist[parentkey].right
            
            if self.morselist[parentkey].key == key:
                return self.morselist[parentkey].value
        

def sortlist(list):
    newindex=-1
    for i in range(1,len(list)):
        for previous in range(i-1,-1,-1):
            if len(list[previous][0]) > len(list[i][0]):
                newindex=previous
                
        if newindex != -1:
            inserttuple=list[i]
            del list[i]
            list.insert(newindex,inserttuple)
            newindex=-1
    return list
        
        
def getsortedmorselist(file):
    """Convert csv file into list of tuples. tuple(morsecode, character)
    Pass list onto sortlist()
    return sortedlist
    """
    morselist=[]
    for line in file:
        linelist=line.split(",")
        morselist.append((linelist[1][:len(linelist[1])-1],linelist[0]))

    morselist = sortlist(morselist)

    if morselist[0][0] == '':
        del morselist[0]

    return morselist

def createmorsetree(file):
    """Calls getsortedmorselist in order to get a list of (Morse code,English letter) tuples. Each tuple is added as a node to a BST object. new BST object is returned after. 
    """
    file = open(file)
    morselist = getsortedmorselist(file)
    file.close()
    morsetree = BTS()
    
    for i in range(0,len(morselist)):
        morsetree.append(morselist[i][0],morselist[i][1])
        
    return morsetree;

def morsetoword(list, tree):
    """Converts a list of morse character to an English string.
    """
    englishword=[] #Characters are added to this list after they have been decrypted
    for char in list:
        if char != '':
            englishword.append(tree.search(char))
            
    return ''.join(englishword)
            
def converttoenglish(cspace, wspace, file, morsesheet):
    mbst=createmorsetree(file=morsesheet)
    englishstring=[]
    
    file = open(file)
    for line in file:
        wordlist=line.split(wspace)
        if '\n' in wordlist:
            del wordlist[wordlist.index('\n')]
        
        englishsent=[]
        for word in wordlist:
            characterlist=word.split(cspace)
            
            englishsent.append(morsetoword(characterlist,mbst)) #Adds the word that was decrypted to a list containing all words in the current line.
            englishsent.append(' ')
            
        englishstring.append(''.join(englishsent))
        englishsent=[]
        
    return englishstring
        
def converttomorse(cspace, wspace, file, morsesheet):
    pass

def getargvalue(list,arg):
    argindex=list.index(arg)
    if argindex == len(list)-1:
        raise NoArgValue
    return list[argindex+1]

def invalidarg():
    print('Invalid argument')
    exit()

if __name__ == '__main__':
    arglist=sys.argv[1:]
    morsesheet='morsesheet.csv'
    encodedtype=''
    wspace='/'
    cspace=' '
    
    validargs=['-f','-w','-c','-m','-e']
    argdict={}
    if '-h' in arglist:
        print(helpstring)
        exit()
    for arg in arglist:
        if arg[0] == '-':
            try:
                if arg not in validargs:
                    invalidarg()
                argdict[arg]=getargvalue(arglist,arg)
            except(NoArgValue):
                invalidarg()
    if '-m' not in argdict and '-e' not in argdict:
        print('Please specify encoded type.')
        exit()
    elif '-m' in argdict and '-e' in argdict:
        print('Please pick -m or -e')
        exit()
    
    if '-f' in argdict:
        morsefile=argdict['-f']
    if '-w' in argdict:
        wspace=argdict['-w']
    if '-c' in argdict:
        cspace=argdict['-c']
        
    if '-m' in argdict:
        englishstring=converttoenglish(cspace=cspace,wspace=wspace, file=arglist[len(arglist)-1], morsesheet=morsesheet)
        for sent in englishstring:
            print(sent)
    else:
        converttomorse(cspace=cspace,wspace=wspace, file=arglist[len(arglist)-1], morsesheet=morsesheet)
