# -*- coding: UTF-8 -*-

from libs.checkParenthesis import getUpperConditionListIndex

def getResultColumnVal (ArrayData) :
    return ArrayData[0].split(',')[-1]

#make a Full Combination.

def checkingTWOValuesWithFilterArray(BTree, RunningRow, CurrentRowNum) :

    #Reading BTree and find upper if or else if statement location.
    UpperConditionIndex = getUpperConditionListIndex(BTree,CurrentRowNum)

    if UpperConditionIndex == 'd' :
        return True
    else :
        if UpperConditionIndex[1] == 'if': #If upper Condition is IF statement
            if RunningRow[UpperConditionIndex[0]][-1] == 'FALSE' and RunningRow[CurrentRowNum][-1] == '-':
                return True
            elif RunningRow[UpperConditionIndex[0]][-1] == 'TRUE' and RunningRow[CurrentRowNum][-1] != '-':
                return True
            elif RunningRow[UpperConditionIndex[0]][-1] == '-' and RunningRow[CurrentRowNum][-1] == '-':
                return True
        elif UpperConditionIndex[1]  == 'else_if': #If upper condtion is ELSE IF statement
            if RunningRow[UpperConditionIndex[0]][-1] == 'FALSE' and RunningRow[CurrentRowNum][-1] != '-':
                return True
            elif RunningRow[UpperConditionIndex[0]][-1] == 'TRUE' and RunningRow[CurrentRowNum][-1] == '-':
                return True
            elif RunningRow[UpperConditionIndex[0]][-1] == '-' and RunningRow[CurrentRowNum][-1] == '-':
                return True

    return False




def makeLongList(Length,Value):
    #make ['Value' * Length] Array
    retVal = []
    for i in range(Length):
        retVal.append(Value)

    return retVal


def popFromColumnValue(dumpList, checkingValue) :
    i_count = dumpList.count(checkingValue)
    #print " "
    #print dumpList
    #print checkingValue
    #print " "
    if i_count > 0 :
        dumpList.pop(dumpList.index(checkingValue))

    return i_count

def getDeepestArray(ArrayData):
    '''
    getDeepestArray
    重ねてるリストの一番奥のリストの値を返却する。
    2014.11.29
    最後のアイテムがBlankList([])であればBlank以外の値をリストで返却するように変更。
    '''
    if ArrayData == []:
        return ArrayData

    if type(ArrayData[-1]) == list and ArrayData[-1] != []:
        retval = getDeepestArray(ArrayData[-1])
    elif type(ArrayData[-1]) == list and ArrayData[-1] != []:
        retval = ArrayData[:-1]
    else:
        retval = ArrayData



    return retval
