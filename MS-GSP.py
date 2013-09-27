import sys

PATH="D:\\MSGSP_Data"
FILE="para.txt"
LOCATIONMIS=PATH+"\\"+FILE
SEQ="data.txt"
LOCATIONSEQ=PATH+"\\"+SEQ
dictOfSupportCount={}
dictOfItems ={}
#Read the file data and split them into strings based on each line
def readFileAndSplit(filedata):
    return filedata.split("\n")

#read the file from the given location in read only mode and return the content
def read_file(location):
    fHandler=open(location,'r')
    #print fHandler
    fileContent=fHandler.read()
    fHandler.close()
    return fileContent

#M value is obtained here. A dictionary of Item and its MIS value is returned in sorted order
def sortItemsListWithMIS(items):
        
    for item in items:
        if "(" and ")" in item:
            itemName = item[item.index("(")+1:item.index(")")]
            itemValue = item[item.index("=")+2:]
            dictOfItems[itemName]=itemValue
            dictOfSupportCount[itemName]=0


    sortedListOfItems=sorted(dictOfItems,key=dictOfItems.get)
    return sortedListOfItems

def supportCountofItems(dataSequenceList):
    import re
    for dataSequence in dataSequenceList:
        regexSpace=re.compile(r'\s+')
        dataSequenceNoSpace=regexSpace.sub('',dataSequence)
        transactions=re.findall(r'{[\d,]+}',dataSequenceNoSpace)
        for transaction in transactions:
            itemsList=((transaction[transaction.index("{")+1:transaction.index("}")]).split(','))
            for item in itemsList:
                dictOfSupportCount[item]=dictOfSupportCount[item]+1
 


#init-pass
def initPass(sortedMISList, dataSequenceList):
    minMisItem=0
    L=[]
    for key in sortedMISList:
        #print key+" is the key..1"
        #print " float(dictOfItems[key]) is " +str((dictOfItems[key]))+"||"+" dictOfSupportCount[key]/float(len(dictOfSupportCount)) is "+str(dictOfSupportCount[key]/float(len(dictOfSupportCount)))
        if (float(dictOfItems[key]))<=(dictOfSupportCount[key]/float(len(dataSequenceList)-1)):
            minMisItem=key
            break

    L.append(minMisItem)
    for key in sortedMISList:
        #print key+"is the key..2"
        #print "minMinItem is "+str(minMisItem)
        
        if dictOfItems[minMisItem]<=dictOfItems[key]:
            if minMisItem!=key:
                if float(dictOfSupportCount[key]/float(len(dictOfSupportCount)))>=float(dictOfItems[minMisItem]):
                    #print " dictOfSupportCount[key]/float(len(dictOfSupportCount)) is" +str(dictOfSupportCount[key]/float(len(dataSequenceList)-1))
                    #print "float(dictOfItems[minMisItem]) is: "+str(float(dictOfItems[minMisItem]))
                    L.append(key)
                    
            
    return L

    
#F1
def generateF1(L,dataSequenceList):
    F1=[]
    for itemL in L:
        #print "itemL"+str(itemL)
        #print "dictOfItems[itemL]"+str(dictOfItems[itemL])
        #print "float(dictOfSupportCount[itemL]/float(len(dataSequenceList)-1))"+str(float(dictOfSupportCount[itemL]/float(len(dataSequenceList)-1)))
        if float(dictOfSupportCount[itemL]/float(len(dataSequenceList)-1))>=float(dictOfItems[itemL]):            
            F1.append(itemL)
    return F1

#level-2 Candidate gen
def level2CandidateGen(F1):
    
# Define a main() function that prints a little greeting.
def main():
    misFileData=read_file(LOCATIONMIS)  #read the MIS File data
    dataSequenceFileData=read_file(LOCATIONSEQ)  #read the MIS File data
    sortedMISList=sortItemsListWithMIS(readFileAndSplit(misFileData)) #Sort the values based on the MIS Values
    

  
  
    dataSequenceList=readFileAndSplit(dataSequenceFileData)
    supportCountofItems(dataSequenceList)
    L=initPass(sortedMISList, dataSequenceList)
    print "L is :"
    for itemL in L:
        print itemL+"," 
    print "F1 is: "  
    F1=generateF1(L,dataSequenceList)
    for f1 in F1:
        print f1
       
        
        
    
  
   
    
    
  
if __name__ == '__main__':
  main()

    
