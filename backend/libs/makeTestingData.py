#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
from itertools import groupby

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def compareBeforeExpression(valueExpression, equalExpression):
    exec(valueExpression)
    exec("global retVal; retVal = %s" % equalExpression)
    return retVal


def checkExpressions(targetValue, listOfExpr):
    #check targetValue into listOfExpr
    #if at least find one False return False
    for expr in listOfExpr:
        if compareBeforeExpression(targetValue, expr):
            pass
        else:
            return False

    return True


def str2bool(v):
    return v.lower() in ("true")

def changeExpressionByCondition(expr, conditionBoolStr):
    equalExpression = re.compile('>=|<=|==|!=')
    withoutEqualExpression = re.compile('>|<')
    # >=|<=|==|!= 이 들어간 statement의 경우
    isEqualExpressionFind = equalExpression.findall(expr)
    isNonEqualExpressionFind = withoutEqualExpression.findall(expr)
    conditionBool = str2bool(conditionBoolStr)

    if conditionBoolStr == '-':
        return '-'

    if isEqualExpressionFind == []:
        # Cannot find expression Case
        pass

    elif isEqualExpressionFind == ["!="]:
        if conditionBool == False:
            #!=를 ==로 변경
            return expr.replace("!=", "==")
        else:
            return expr

    elif isEqualExpressionFind == ['=='] :
        if conditionBool == False:
            # ==를 !=로 변경
            return expr.replace("==", "!=")
        else:
            return expr

    elif isEqualExpressionFind == ['>='] :
        if conditionBool == False:
            # >=를 < 로 변경
            return expr.replace(">=", "<")

        else:
            return expr

    elif isEqualExpressionFind == ['<='] :
        if conditionBool == False:
            # <=를 > 로 변경
            return expr.replace("<=", ">")
        else:
            return expr

    if isNonEqualExpressionFind == []:
        if conditionBool == False:
            return "!" + expr
        else:
            return expr

    elif isNonEqualExpressionFind == ['<'] :
        if conditionBool == False:
            # <를 >= 로 변경
            return expr.replace("<", ">=")
        else:
            return expr

    elif isNonEqualExpressionFind == ['>'] :
        if conditionBool == False:
            # >를 <= 로 변경
            return expr.replace(">", "<=")
        else:
            return expr


class ClosestValue:
    def __init__(self):
        self.equalExpression = re.compile('>=|<=|==|!=')
        self.withoutEqualExpression = re.compile('>|<')

    def getClosestValue(self,expression):
        # >=|<=|==|!= 이 들어간 statement의 경우
        isEqualExpressionFind = self.equalExpression.findall(expression)
        if isEqualExpressionFind == []:
            # Cannot find expression Case
            pass
        elif isEqualExpressionFind == ['!='] :
            #return left value + 1
            #return (float(expression.split('!=')[1])+1)
            return (float(expression.split('!=')[1])+1 if is_float(expression.split('!=')[1]) else expression)

        elif isEqualExpressionFind == ['=='] :
            #return left value
            return (float(expression.split('==')[1]) if is_float(expression.split('==')[1]) else expression)
        else :
            # This is '<=', ">=" case. assinged values would be returned without change
            if isEqualExpressionFind == ['>=']:
                #return (float(expression.split('>=')[1]))
                return (float(expression.split('>=')[1]) if is_float(expression.split('>=')[1]) else expression)

            elif isEqualExpressionFind == ['<=']:
                #return (float(expression.split('<=')[1]))
                return (float(expression.split('<=')[1]) if is_float(expression.split('<=')[1]) else expression)

        isNonEqualExpressionFind = self.withoutEqualExpression.findall(expression)
        if isNonEqualExpressionFind == []:
            return expression
        elif isNonEqualExpressionFind == ['>'] :
            # return left value + 1
            #return (float(expression.split('>')[1]) + 1)
            return (float(expression.split('>')[1]) + 1 if is_float(expression.split('>')[1]) else expression)

        elif isNonEqualExpressionFind == ['<'] :
            # return left value - 1
            #return (float(expression.split('<')[1]) - 1)
            return (float(expression.split('<')[1])-1 if is_float(expression.split('<')[1]) else expression)

    def updateValueWithCondition(self,expressions):
        valueStack = []

        for i, expr in enumerate(expressions):
            fCurrentVal = self.getClosestValue(expr)
            if is_float(fCurrentVal) == False :
                return fCurrentVal

            isEqualExpressionFind = self.equalExpression.findall(expr)
            isNonEqualExpressionFind = self.withoutEqualExpression.findall(expr)
            leftValue = expr.split(isEqualExpressionFind[0])[0] if isEqualExpressionFind != [] else \
            expr.split(isNonEqualExpressionFind[0])[0]
            execStatement = leftValue + '=' + str(fCurrentVal)


            if i == 0:
                valueStack.append(execStatement)
            else :
                #compair currentStatement with expressions[0 ~ i]
                #compair exStatement with expressions[0~i]
                #if both results are False, return Fail
                #if either side is True, True side would be value
                #if both results are True, return latest value


                if checkExpressions(execStatement, expressions[:i+1]):
                    valueStack.append(execStatement)
                else:
                    if checkExpressions(valueStack[-1],expressions[:i+1]):
                        pass
                    else :
                        return False
                        #pass

        return valueStack[-1]


    def getClosestValues(self,Valiables):
        retVal = []
        for data in Valiables:
            updateValueWithConditionResult = self.updateValueWithCondition(data)
            retVal.append(updateValueWithConditionResult if updateValueWithConditionResult else '')

        return ", ".join(retVal)


class makeTestData:
    def __init__(self):
        pass

    def testValuables(self, tableDict):
        headerArray = []
        caseVailablesArray = []
        
        for k, data in enumerate(tableDict):
            #conditionArray = []
            #k = 조건절의 갯수를 의미
            #data = 각 조건절의 변수들.
            headerDict = {}
            conditionDict = {}

            for j, vali_and_cond in enumerate(data):
                #j = Row수를 의미. J[0] = Header부분, j[1...] = It means Case number
                if j == 0 : #header처리
                    headerArray = []
                    headerDict = data[vali_and_cond]
                    for i in range(len(headerDict)-1):
                        if i > 0 :
                            tempStr = headerDict[i].replace("(","")
                            tempStr = tempStr.replace(")","")
                            #for loop 구문 처리
                            if len(tempStr.split(";")) == 1 :
                                pass
                            else:
                                tempStr = tempStr.split(";")[1] # ..;..;.. 중에서 가운데 변수만 취함.

                            headerArray.append(tempStr)

                else : # Condition 데이터 처리
                    conditionDict = data[vali_and_cond]
                    temp = []

                    for i in range(len(conditionDict)-1):
                        if i > 0 :
                            temp.append(changeExpressionByCondition(headerArray[i - 1], conditionDict[i]))

                    if k == 0:
                        caseVailablesArray.append(temp)
                    else:
                        caseVailablesArray[j-1] = caseVailablesArray[j-1] + temp


        return caseVailablesArray


    def mergeTestData(self,OneRow):
        # grouping valiables in OneRow
        equalExpression = re.compile('>=|<=|==|!=')
        withoutEqualExpression = re.compile('>|<')
        groupingArray = []
        OneRow.sort()
        RetArray = []

        for data in OneRow:
            #make Tuple for grouping.
            isEqualExpressionFind = equalExpression.findall(data)
            iswithoutEqualExpression = withoutEqualExpression.findall(data)

            key = ""
            tempTuple=()
            if isEqualExpressionFind != []:
                key = data.split(isEqualExpressionFind[0])[0]
                tempTuple = (key, data)
            elif iswithoutEqualExpression != []:
                key = data.split(iswithoutEqualExpression[0])[0]
                tempTuple = (key, data)
            else:
                if data == '-':
                    pass
                else :
                    tempTuple = (data,data)

            if tempTuple != ():
                groupingArray.append(tempTuple)

        for key, group in groupby(groupingArray,lambda x:x[0]):
            RetArray.append([thing[1] for thing in group])

        return RetArray






