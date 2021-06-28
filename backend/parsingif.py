from typing import List
from pyparsing import *
import itertools

text = '''
if(a ==0 || b == 1){
    if (ss){
        test()
    }
    else if (sss){
        test2()
    }
    else if (sskmakm){
        sskkk()
    }
}
else if (sksmsk){
    if (NNN){
        fsmklf
        if (sKkSKks){
            What?
        }
    }
    else{
        smfka
    }
}
else if (smkdmkfla){
    dmakmdaks
}
'''

def _getDeepestItem(List,retVal):
    temp = getListItem(List)
    if len(temp) > 0:
        for i in temp:
            _getDeepestItem(i,retVal)
    else:
        retVal.append(List)

def getStartItem(List):
    startItem = []
    _getDeepestItem(List, startItem)
    return startItem

    


def _getParents(List,item,retVal):
    if (item in List):
        retVal.extend(List)
    else:
        temp = getListItem(List)
        if len(temp) > 0 :
            for i in temp:
                _getParents(i, item, retVal)
        else:
            pass

def getParents(List,item):
    retVal = []
    _getParents(List,item,retVal)
    return retVal

def _getIfPath(List, item, retVal):
    parentList = getParents(List, item)
    if (len(parentList) > 0):
        itemIndex = parentList.index(item)
        temp = parentList[itemIndex-1]
        if (temp.find('if')>=0 or temp.find('elseif')>=0):
            retVal.append(temp)
            _getIfPath(List,parentList,retVal)

def getIfPath(List, item):
    retVal = []
    _getIfPath(List,item, retVal)

    retVal.reverse()
    
    return retVal


def getnonListItem(List):
    retVal = []
    for i in List:
        if isinstance(i,str):
            if i.find('if') == 0 or i.find('elseif') ==0:
                retVal.append(i)

    return retVal
        

def getListItem(List):
    retVal = []
    for i in List:
        if isinstance(i,list):
            retVal.append(i)

    return retVal



def getWholeIfPath(codes):
    retVal = []
    parsing_text = '{' + codes.replace(' ','') + '}'
    mParenthese = nestedExpr('{', '}').parseString(parsing_text).asList()
    startItem = getStartItem(mParenthese[0])
    for i in startItem:
        temp = getIfPath(mParenthese[0], i)
        if len(temp) >0 :
            retVal.append(temp)
    
    return retVal

# for i in getWholeIfPath(text):
#     print(i)

def getCoverage(parameters, way):
    pairCoverage = list(itertools.combinations(parameters,way))
    pairCovArray = []
    for i in pairCoverage:
        pairCovArray.append(list(itertools.product(*i)))
    
    return pairCovArray

def nonDictFilter(parameters):

    filter = []

    temp = getCoverage(parameters,len(parameters))

    for i in temp[0]:
        # 각 row별로 [TRUE, -], [FALSE,TRUE], [FALSE, FALSE] 가 있는지 sliding으로 검색하여
        # 있으면 있어서는 안될 열로 저장한다.

        for slider in range(len(i)-1):
            if (i[slider][0].split(',')[-1] == 'TRUE' and i[slider+1][0].split(',')[-1] == '-'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == 'FALSE' and i[slider+1][0].split(',')[-1] == 'TRUE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == 'FALSE' and i[slider+1][0].split(',')[-1] == 'FALSE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == '-' and i[slider+1][0].split(',')[-1] == 'TRUE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == '-' and i[slider+1][0].split(',')[-1] == 'FALSE'):
                filter.append(i)
    
    #print(filter)

    return filter     

print(getWholeIfPath(text))

