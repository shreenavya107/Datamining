import sys

PATH="D:\MSGSP_Data"
FILE="para.txt"
LOCATIONMIS=PATH+"\\"+FILE
SEQ="data.txt"
LOCATIONSEQ=PATH+"\\"+SEQ
dictOfSupportCount={}
dictOfItems ={}
F2=[]
OrderedC2=[]
orderedF2=[]
mainList=[] #list of datasequence with eacb transaction as a set
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

#M value is obtained here. A sorted list of Items is returned
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
    
    tranSets=[]
    for dataSequence in dataSequenceList:
        tempDictOfKeys={}
        regexSpace=re.compile(r'\s+')
        dataSequenceNoSpace=regexSpace.sub('',dataSequence)
        transactions=re.findall(r'{[\d,]+}',dataSequenceNoSpace)
        
##        print transactions
        tranSets=[]
        for transaction in transactions:
##            print transaction
            itemsList=((transaction[transaction.index("{")+1:transaction.index("}")]).split(','))
            tempitemList=[]

            for item in itemsList:
                if item not in tempDictOfKeys:
                    tempDictOfKeys[item]=1

                tempitemList.append(item)
##                print item            
            tranSets.append(set(tempitemList))
        mainList.append(tranSets)
        for item in list(tempDictOfKeys.keys()):
            dictOfSupportCount[item]=dictOfSupportCount[item]+1
            
        
     

#init-pass
def initPass(sortedMISList, dataSequenceList):
    minMisItem=0
    L=[]
    for key in sortedMISList:
        #print key+" is the key..1"
        #print " float(dictOfItems[key]) is " +str((dictOfItems[key]))+"||"+" dictOfSupportCount[key]/float(len(dictOfSupportCount)) is "+str(dictOfSupportCount[key]/float(len(dictOfSupportCount)))
        if (float(dictOfItems[key]))<=(dictOfSupportCount[key]/float(len(dataSequenceList))):
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
        if float(dictOfSupportCount[itemL]/float(len(dataSequenceList)))>=float(dictOfItems[itemL]):            
            F1.append(itemL)
    return F1



#level-2 Candidate gen
def level2CandidateGen(L,sdc,dataSequenceList):
    #tempListAfterl=[]
    c2=[]

    for l in L:
        if float(dictOfSupportCount[l]/float(len(dataSequenceList)))>=float(dictOfItems[l]):
            #tempListAfterl=L[L.index(l)+1:]
            for itemAfterl in L[L.index(l)+1:]:
##                print "icamehere"
                print str(l)+ ","+str(itemAfterl)+"::: MIS of "+str(l)+":"+dictOfItems[l]+" supp% of"+str(itemAfterl)+": "+str(float(dictOfSupportCount[itemAfterl]/float(len(dataSequenceList))))+" sdc: "+str(abs((dictOfSupportCount[itemAfterl]/float(len(dataSequenceList)))-(dictOfSupportCount[l]/float((len(dataSequenceList))))))
                if (float(dictOfSupportCount[itemAfterl]/float(len(dataSequenceList)))>=float(dictOfItems[l])) and abs((dictOfSupportCount[itemAfterl]/float(len(dataSequenceList)))-(dictOfSupportCount[l]/float((len(dataSequenceList)))))<=sdc:
                    print "after checking sdc,support count joining in 3 diff posibilitites "+str(l)+ ","+str(itemAfterl)
                    c2.append([set([l,itemAfterl])])
                    OrderedC2.append([[l,itemAfterl]])
                    
                    c2.append([set([l]),set([itemAfterl])])
                    OrderedC2.append([[l],[itemAfterl]])

                    c2.append([set([itemAfterl]),set([l])])
                    OrderedC2.append([[itemAfterl],[l]])
                    
       
    return c2
    

#MSCandidateGen-SPM(FkMinusOne)

##def MSCandidateGenSPM(FkMinusOne):
    
#getMinMISItem(Set)
def getMinMISItem(itemSet):
    minMIS=99999999.0000000000
    for item in itemSet:
##        print "MIS Coming from dictionary for: " +str(item)+"is :"+str(float(dictOfItems[item]))
        if float(minMIS)>float(dictOfItems[item]):
            minMIS=float((dictOfItems[item]))
    return float(minMIS)
        
#line 9 -16
def line9to16(C2):
    candIndex=0
    dataIndex=0
    for candidate in C2:
        candidateCount=0
        for datarow in mainList:
            while(dataIndex<len(datarow)):
                if candidate[candIndex].issubset(datarow[dataIndex]):
                    candIndex=candIndex+1
                    dataIndex=dataIndex+1
##                    print "candidate: "+str(candidate)+ " Datarow is: "+str(datarow)+" candIndex: "+str(candIndex)+" DataIndex: "+str(dataIndex)
##                    print "entered" + str(candidate)+"candIndex is"+str(candIndex)+"DataIndex is"+str(dataIndex)
                    if candIndex==len(candidate):
                        candidateCount=candidateCount+1
                        candIndex=0
                        dataIndex=0
                        break
##                        if len(candidate)!=1:
##                            dataIndex=dataIndex-1

                else:
                    dataIndex=dataIndex+1
            if dataIndex==len(datarow):
                dataIndex=0
                candIndex=0
##                    continue
        print "Candidate count of "+ str(candidate)+" is "+str(candidateCount)
        cMinMIS=9999999.00000

        for sets in candidate:
##            print "MINIMIM of SET:" +str(sets)+ "is " +str(float(getMinMISItem(sets)))
            if float(getMinMISItem(sets))<float(cMinMIS):
                cMinMIS=float(getMinMISItem(sets))
            
        print "Candi Support of "+str(candidate)+":"+str(float(candidateCount/float(len(mainList))))+"cMinMIS is "+str(float(cMinMIS))
        if float(candidateCount/float(len(mainList)))>float(cMinMIS):
            indexOfItemInSet=C2.index(candidate)
            print "adding the candidate: "+str(candidate)
            orderedF2.append(OrderedC2[indexOfItemInSet]) #get the same thing as an ordered one from OrderedC2
            F2.append(candidate)

    print "no of candidates as a result of level 2 candidate gen are: "+ str(len(C2))
            

#L is List
#F1 is List
#dataSequenceList is List
# Define a main() function that prints a little greeting
def main():
    sdc=0.05
    misFileData=read_file(LOCATIONMIS)  #read the MIS File data
    dataSequenceFileData=read_file(LOCATIONSEQ)  #read the Sequence File data
    sortedMISList=sortItemsListWithMIS(readFileAndSplit(misFileData)) #Sort the values based on the MIS Values
    dataSequenceList=readFileAndSplit(dataSequenceFileData)
    supportCountofItems(dataSequenceList)
    L=initPass(sortedMISList, dataSequenceList)

    print str(len(dataSequenceList))
    
    print "L is :"
##    for itemL in L:
##        print itemL+"," 
    print "F1 is: "  
    F1=generateF1(L,dataSequenceList)
    for f1 in F1:
        print f1+" count: "+str(dictOfSupportCount[f1])

    C2=[]
    C2=level2CandidateGen(L,sdc,dataSequenceList)
##    for can in C2:
##        print "Level 2 Candidate is : "+ str(can)
        
       
    line9to16(C2)
    print "number of freq itemsets in F2 are: "+str(len(F2))

    for f2 in F2:
        

        print "Ordered Is: "+str(orderedF2[F2.index(f2)])+"Unordered is: "+str(f2)
##        print "Length of first itemset in each F is: "+str(len(f2[0]))
##        if len(f2[0])==1:
##            print "deleting first item in the second itemset"
##            tempf2=[x for x in f2[1]
            
        


##    MSCandidateGenSPM(F2)
    
        
    
  
   
    
    
  
if __name__ == '__main__':
  main()

    
