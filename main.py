import sys

class NotFound(Exception):
    pass

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
        morselist[0]=(' ',' ')

    return morselist

def getmorsetree(file='morsesheet.csv'):
    file = open(file)
    morselist = getsortedmorselist(file)
    file.close()
    morsetree = BTS()
    for i in range(1,len(morselist)):
        morsetree.append(morselist[i][0],morselist[i][1])
        
    return morsetree;

helpstring ="""python main.py [options] file
[options]
-h: prints this chunck of text.
-f: Uses custom file for morse code. Must be formatted with char,code. Defaults to morsesheet.csv.
-w: Character used to signify a space between words. Defaults to |.
-c: Character used to signify a new character. Defaults to a space.
"""

if __name__ == '__main__':
    arglist=sys.argv
    morsefile=arglist[len(arglist)-1]
    if morsefile[0] == '-':
        print('No file to decode')
        exit()
    del arglist[0]
    del arglist[len(arglist)-1]
    print(arglist)
