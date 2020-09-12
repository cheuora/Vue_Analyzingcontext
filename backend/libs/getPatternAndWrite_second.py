# -*- coding: UTF-8 -*-
from libs.Combination import getDeepestArray
import copy

####


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])



def getFirstTrue(ArrData):
    for i in ArrData:
        if i[-1] == 1:
            return i


def getFirstFalse(ArrData):
    for i in ArrData:
        if i[-1] == 0:
            return i



def parsingExpresison(ExpressionStr):
    andArr = ExpressionStr.split('&&')
    retArr = []
    for i in andArr:
        if i.find('||') > 0:
            orArr = i.split('||')
            for j in orArr:
                retArr.append(j.strip())
                retArr.append('||')
            retArr.pop()
        else:
            retArr.append(i.strip())
        retArr.append('&&')
    retArr.pop()
    return retArr


def convertOperator(Operator):
    temp = Operator.replace("_AND_","&&")
    temp = temp.replace("_OR_","||")
    return temp


class makingMCDC:
    def __init__(self):
        pass


    def parsingExpresison(self, ExpressionStr):
        andArr = ExpressionStr.split('&&')
        retArr = []
        for i in andArr:
            if i.find('||') > 0:
                orArr = i.split('||')
                for j in orArr:
                    retArr.append(j)
                    retArr.append('||')
                retArr.pop()
            else:
                retArr.append(i)
            retArr.append('&&')
        retArr.pop()
        return retArr

    def addRearAnd(self, BaseArr=[[1, 1], [0, 0]], AddedArr=[[1, 1], [0, 0]]):

        temp = []
        lastArr = []
        for i, value in enumerate(BaseArr):
            if value[-1] == 1:
                lastArr = copy.deepcopy(BaseArr[i])
            temp.append(value[:-1])
            # temp[-1].append(1)
            temp[-1] = temp[-1] + getFirstTrue(AddedArr)[:-1]
            if value[-1] and 1:
                temp[-1].append(1)
            else:
                temp[-1].append(0)

        # append last low

        if lastArr[-1] and 0:
            # lastArr = lastArr[:-1] + [0]
            lastArr = lastArr[:-1] + getFirstFalse(AddedArr)[:-1]
            lastArr.append(1)
        else:
            # lastArr = lastArr[:-1] + [0]
            lastArr = lastArr[:-1] + getFirstFalse(AddedArr)[:-1]
            lastArr.append(0)

        temp.append(lastArr)

        # add remained AddedArr

        for AddedArrOneRow in AddedArr:
            if AddedArrOneRow in [getFirstTrue(AddedArr), getFirstFalse(AddedArr)] :
                pass
            else:
                secondTemp = getFirstTrue(BaseArr)[:-1] + AddedArrOneRow[:-1]

                if (getFirstTrue(AddedArr)[-1] == 1 and AddedArrOneRow[-1] == 1):
                    secondTemp.append(1)
                else:
                    secondTemp.append(0)

                temp.append(secondTemp)

        return temp


    def addRearOr(self, BaseArr=[[1,1],[0,0]], AddedArr = [[1,1],[0,0]]):
        temp = []
        lastArr = []
        for i, value in enumerate(BaseArr):
            if value[-1] == 0:
                lastArr = copy.deepcopy(BaseArr[i])
            temp.append(value[:-1])
            #temp[-1].append(1)
            temp[-1] = temp[-1] + getFirstFalse(AddedArr)[:-1]
            if value[-1] or 0 :
                temp[-1].append(1)
            else :
                temp[-1].append(0)

        # append last low
        if lastArr[-1] or 1:
            # lastArr = lastArr[:-1] + [0]
            lastArr = lastArr[:-1] + getFirstTrue(AddedArr)[:-1]
            lastArr.append(1)
        else:
            # lastArr = lastArr[:-1] + [0]
            lastArr = lastArr[:-1] + getFirstTrue(AddedArr)[:-1]
            lastArr.append(0)

        temp.append(lastArr)

        # add remained AddedArr

        for AddedArrOneRow in AddedArr:
            if AddedArrOneRow in [getFirstTrue(AddedArr), getFirstFalse(AddedArr)] :
                pass
            else:

                secondTemp = getFirstFalse(BaseArr)[:-1] + AddedArrOneRow[:-1]

                if (getFirstFalse(AddedArr)[-1] == 1 or AddedArrOneRow[-1] == 1):
                    secondTemp.append(1)
                else:
                    secondTemp.append(0)

                temp.append(secondTemp)

        return temp



    def getSubstitutedExprAndArray(self, Expr, Dict):

        retExpr = ''
        retArr = []

        for i in list(Dict.keys()):
            if i in Expr:
                temp = i.replace("&&", "_AND_")
                temp = temp.replace("||", "_OR_")
                if retExpr == '':
                    retExpr = Expr.replace(i, temp)
                else:
                    retExpr = retExpr.replace(i, temp)

        ItemInExpr = parsingExpresison(retExpr)

        for item in ItemInExpr:
            if item == "&&" or item == "||":
                pass
            else:
                Operator = convertOperator(item)
                try:
                    Operator = min(list(parenthetic_contents(Operator)))[1]
                except ValueError:
                    pass

                if Operator in Dict:
                    retArr = retArr + [Dict[Operator]]
                else:
                    retArr = retArr + [[[1, 1], [0, 0]]]

        return  (retExpr, retArr)




    def makeMCDCArray(self, Expression="A && B", ArrayTuple=([[1,1],[0,0]],[[1,1],[0,0]])):
        ExpressionArr = parsingExpresison(Expression)
        ArrayLen = len(ArrayTuple)
        ExpressionLen = len(ExpressionArr)
        if (ArrayLen*2 -1) != ExpressionLen:
            return -1

        BaseArr = ArrayTuple[0]
        for i,value in enumerate(ExpressionArr):
            try:
                if value not in ['||', '&&'] :
                    if ExpressionArr[i + 1] == '&&':
                        BaseArr = self.addRearAnd(BaseArr, ArrayTuple[(i+2)//2])
                    elif ExpressionArr[i + 1] == '||':
                        BaseArr = self.addRearOr(BaseArr, ArrayTuple[(i+2)//2])
                    else:
                        pass
            except IndexError:
                break

        return BaseArr
### END Class ###



#####


def MakeMCDCResults(Expression):
    TempVal = list(parenthetic_contents(Expression))
    objMakingMCDC = makingMCDC()
    ReturnMCDCFormat = []

    ParamsArr = parsingExpresison(Expression)

    HeaderRow = []
    for i, ParamsArrRow in enumerate(ParamsArr):
        if i%2 == 0:
            ParamsArrRow = ParamsArrRow.replace('(','').replace(')','')
            HeaderRow.append(ParamsArrRow.strip())

    HeaderRow.append("Results")

    StackDict = {}
    tempArr = []
    chgArr = []
    for kk in range(100):
        indexes = [i for i, x in enumerate(TempVal) if x[0] == kk]
        if indexes == []:
            break

        for i, value in TempVal:
            if i in indexes:
                if i == max(TempVal)[0]:  # Max Value means Bottom states
                    ItemCount = len(parsingExpresison(value)) // 2 + 1
                    AddedArr = [[[1, 1], [0, 0]]] * ItemCount
                    chgArr = objMakingMCDC.makeMCDCArray(value, AddedArr)
                else:
                    # Search in StackDick and make Expression, ArrayTuple
                    ExprAndArr = objMakingMCDC.getSubstitutedExprAndArray(value, StackDict)

                    chgArr = objMakingMCDC.makeMCDCArray(ExprAndArr[0], ExprAndArr[1])

                StackDict.clear()

                tempArr.append((value, chgArr))

                if len(tempArr) > 0:
                    for oneTempArr in tempArr:
                        StackDict[oneTempArr[0]] = oneTempArr[1]

        del tempArr[:]

    #convert chgArr to Formatting Result
    ReturnMCDCFormat.append(HeaderRow)

    for chgArrOneRow in chgArr:
        ConvertOneRow = str(chgArrOneRow).strip('[').strip(']')
        ConvertOneRow = ConvertOneRow.replace('1', 'TRUE').replace('0','FALSE')
        ConvertOneRow = ConvertOneRow.replace(' ','')
        ReturnMCDCFormat.append([ConvertOneRow])


    return ReturnMCDCFormat




def getHeaderOfStatementHTML(Header):
    #Insert <h3> </h3> Tags at each element of Header List.
    for i in range(len(Header)):
        HeaderItem = Header[i]
        HeaderItem = HeaderItem.replace('{','')
        HeaderItem = '<h3>' + HeaderItem + '</h3>'
        Header[i] = HeaderItem

    return Header

def getTableElementsHTML(CombinationElements):
    #Insert and Merge <tr><td>element 1</td><td>element 2</td>... </td> at eche element of Arraylist
    CombinationElements_lang = len(CombinationElements)
    HTML_Elements = []

    for i in range(CombinationElements_lang):
        TempString = "<tr>"

        for j in range(len(CombinationElements[i])):
            TempString = TempString + "<td>" + str(CombinationElements[i][j]) + "</td>"

        TempString = TempString + "</tr>"
        HTML_Elements.append(TempString)


    return HTML_Elements

def AllPair2ToList(AllPair2_Instance):
    PairingResult = []
    for j, v in enumerate(AllPair2_Instance):
        for i in range(len(v)):
            v[i] = v[i][0].split(',')
        PairingResult.append(v)

    return PairingResult


def printArray(arrayData):
    for i in range(len(arrayData)):
        print(arrayData[i])


def addDummyRow(BTree, MCDC):
    '''
    Scanning BTree, if it is not independent row, add DUMMY data
    example)
    [['FALSE,TRUE,FALSE'], ['TRUE,FALSE,FALSE'], ['TRUE,TRUE,TRUE']]
    [['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE'],['-,-,-']] #independent clause
    [['FALSE,TRUE,FALSE,FALSE'], ['TRUE,FALSE,FALSE,FALSE'], ['TRUE,TRUE,FALSE,TRUE'], ['FALSE,TRUE,TRUE,TRUE'], ['-,-,-']]#independent  clause
    [['FALSE,TRUE,FALSE'], ['TRUE,FALSE,FALSE'], ['TRUE,TRUE,TRUE'], ['-,-,-']]#independent clause
    [['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']]
    '''

    for i, BTree_value in enumerate(BTree):
        if BTree_value[0] == -1 and BTree_value[-1] == -1:
            pass
        else :
            dummy = '-,'
            MCDC_row_len = len(MCDC[i])
            dummy = dummy * MCDC_row_len
            dummy = dummy[:-1]
            MCDC[i].append([dummy])

    return MCDC



def searchItem_in_Array(arrayData, Item):
    # 수정해야 한다.(20200318)
    # 같은 부분을 Whole searching 하지 말고 바로 자기 앞부분까지 찾아 Search 하고 찾으면 빠져나오는 것으로.. 
    rowcount = len(arrayData)
    retVal = []

    for i in range(rowcount):
        try:
            col_index = arrayData[i].index(Item)
            retVal.append([i,col_index])
        except ValueError :
            pass

    return retVal



def getFilter(HeaderData):

    HeaderData_length = len(HeaderData)

    """
    HeaderData내에 있는 각 Item들의 위치가 기록된 List를 돌려준다.
    example)
    ['CheckBoardStatus()', 'CaptureScreen()', 'Results'],
    ['CheckBoardStatus()', 'SearchFile()', 'Results'],
    ['CheckAutoCalibration()', 'CaptureScreen()', 'Results']
    을 이용하면 아래와 같이 바뀐다.

    [[[0, 0], [1, 0]]],
    [[[0, 0], [1, 0]]],
    [[[2, 0]], [[0, 1], [2, 1]]],

    @2015.11.19
    Get rid of 'Result' part
    """

    filterArray = []
    for i in range(HeaderData_length):
        filterArray_row = []
        for j in range(len(HeaderData[i])-1) :
            #temp = searchItem_in_Array(HeaderData, HeaderData[i][j])
            temp = searchItem_in_Array(HeaderData[:i+1], HeaderData[i][j])

            filterArray_row.append(temp)
        filterArray.append(filterArray_row)

    return filterArray



def InitializeElseStack(ArrayData):
    '''
    @InitializeElseStack()
    Elseスタックの最後のアイテムを読んで、リストの場合は最後のみ、その以外の場合は全部'[]'で初期化する。
    '''
    if ArrayData == [] :
        #受け入れたArrayData自体が[]の場合。 処理しなくてそのまま返却
        return ArrayData

    if type(ArrayData[-1]) == list :
        #再帰呼び出し
        ArrayData[-1] = InitializeElseStack(ArrayData[-1])
    else :
        #全部初期化
        ArrayData = []

    return ArrayData

def AppendElseStack(ArrayData,appendItem):
    '''
    @AppendElseStack()
    Elseスタックの最後のアイテムを読んで、リストの場合は最後のアイテムで、その以外の場合いは全体でappendを遂行する。
    '''
    if ArrayData == [] :
        #直接にappendする。
        ArrayData.append(appendItem)
    elif type(ArrayData[-1]) == list :
        #再帰呼び出し
        AppendElseStack(ArrayData[-1],appendItem)
    else :
        ArrayData.append(appendItem)

    return ArrayData


def writeDependencyInFilterArray(ArrayData, rowNum, dependentIndex, ElseStack):
    '''
    rowNum에 해당하는 filterArray열에 dependentIndex를 기록한다.
    @2014.11.25
    보강 로직을 추가함.
    if일 경우에 Else Stack에 값이 들어오는 경우가 있음(오류는 아님)
    이 경우에는 if의 depencency 값 및 else stack 값의 보정 로직이 필요함.
    Else 스택의 가장 마지막 값 + 1 로 보정
    '''
    #print "writeDependencyInFilterArray : --------->"
    ArrayData[rowNum][-1].append(dependentIndex)
    ArrayData[rowNum][-1].append(ElseStack)

    if dependentIndex > 0 and len(getDeepestArray(ElseStack)) != 0 :
        CalifiedDependentIndex = getDeepestArray(ElseStack)[-1] + 1
        ArrayData[rowNum][-1][0] = CalifiedDependentIndex

    #printArray(ArrayData)
    return ArrayData





def divideItem_in_Array(arrayData) :
    """
    arrayData = [['FALSE,TRUE,FALSE'], ['TRUE,FALSE,TRUE'], ['TRUE,FALSE,TRUE']]이면
    arrayData = [['FALSE','TRUE','FALSE'], ['TRUE','FALSE','TRUE'], ['TRUE','FALSE','TRUE']]
    로 끊어 준다.
    """
    arrayData_len = len(arrayData)

    for i in range(arrayData_len) :
        for j in range(len(arrayData[i])):
            temp = arrayData[i][j].split(',')
            arrayData[i] = temp

    return arrayData


def findFactor_in_Array(arrayData, Location):
    """
    Location (row, column) 을 받아 여기에 해당하는 Item을 돌려준다.
    예를 들어
    arrayData = [['FALSE,TRUE,FALSE'], ['TRUE,FALSE,TRUE'], ['TRUE,FALSE,TRUE']] , Location = (1,1) 이면
    'FALSE'를 돌려준다.

    단 입력받을 데이터가 'FALSE,TRUE,FALSE' 의 형태로 묵여 있으면 이를 list로 쪼개어 받아야 한다.
    """
    #arrayData = divideItem_in_Array(arrayData)

    location_row = Location[0]
    location_col = Location[1]

    try:
        returnVal = arrayData[location_row][location_col]
    except IndexError :
        # 위치에 맞는 값이 없다면 -1를 돌려준다.
        returnVal = -1


    return returnVal


def compareValues_in_Array(arrayData, Locations):
    """
    Location에 있는 좌표에 해당되는 값을 arrayData에서 찾아 해당 값들을 비교,
    전부 동일하면 True를, 아니면False를 돌려준다.
    못찾아도 True를 돌려준다.
    ex)
    Locations = [[0,0], [1,2]] , arrayData = [[1,2,3], [4,5,6]] 일 때
    [0,0] 에 해당되는 1과 [1,2]에 해당되는 6을 비교. 이 경우에는 False 를 돌려줌.


    2014.9.20 추가
    비교 데이터중 하나가 Dummy data ('-') 라면, False가 아니라 TRUE를 돌려줌.
    비교하는 방법을 변경함.
    Value[0]이 반복되는 갯수 = a
    '-'이 반복되는 갯수 = b
    Value의 길이 - b 값과 a 를 비교하여 같으면, True 다르다면 a 이외의 뭔가가 있다는 의미이므로 False를 돌려줌.
    """

    Locations_len = len(Locations)

    if Locations_len == 1 :
        return True

    Value = []
    # for i in range(Locations_len-1) :
    #     for j in Locations[i]:
    #         Value.append(findFactor_in_Array(arrayData, j))

    for i in Locations:
        Value.append(findFactor_in_Array(arrayData,i))

    # -1값은 비교 대상에서 제외시킨다.
    while Value.count(-1) > 0 :
        Value.remove(-1)


    for i in range(Value.count('-')):
        Value.remove('-')

    if (len(set(Value)) == 1):
        return True
    else:
        return False

    # BaseValue = Value[0]
    # countDummy = Value.count('-')

    # if (len(Value) - countDummy) == Value.count(BaseValue) :
    #     return True
    # else :
    #     return False


def setResultValueFirst(arrayData, resultValue, targetRow ):
    '''
    Results의 값을 받아서 해당 값이 우선적으로 리스트에 먼저 오도록 정렬하여 돌려준다.
    '''
    leng = len(arrayData[targetRow]) #targetRow의 데이터를 변경한다.
    findHitArrr = []
    otherArrr = []
    for i in range(leng):
        k = arrayData[targetRow][i][-1].split(',')
        if k[-1] == resultValue:
            findHitArrr.append(arrayData[targetRow][i])
        else :
            otherArrr.append(arrayData[targetRow][i])


    returnArrr = findHitArrr + otherArrr

    arrayData[targetRow] = returnArrr

    return arrayData


