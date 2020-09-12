#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re


def getIndexFromBinTree(OneIndexData):
    return OneIndexData[1][0]



def index_of_if_while(text):
    if text.find('if') >0 :
        return text.find('if')
    elif text.find('while') > 0:
        return text.find('while')
    elif text.find('for') > 0:
        return text.find('for')


def quicksort(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if getIndexFromBinTree(x) < getIndexFromBinTree(pivot):
                less.append(x)
            if getIndexFromBinTree(x) == getIndexFromBinTree(pivot):
                equal.append(x)
            if getIndexFromBinTree(x) > getIndexFromBinTree(pivot):
                greater.append(x)
        # Don't forget to return something!
        return quicksort(less)+equal+quicksort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array


def getIterNumInBTree(BTree, value):
    for i, TreeValue in enumerate(BTree):
        if TreeValue[1] == value:
            return i

def getUpperConditionListIndex(BTree, CurrentRow):
    #Analyze BTree and find upper if statement String Ptr and get List index in BTree
    OneBTreeData = BTree[CurrentRow]
    if OneBTreeData[0] == -1 and OneBTreeData[-1] == -1:
        #Doesn't have uppder if statement
        return 'd'
    else:
        if (OneBTreeData[0] != -1 and OneBTreeData[2] == -1):
            i = getIterNumInBTree(BTree, OneBTreeData[0])
            return [i, 'if']
        elif (OneBTreeData[0] == -1 and OneBTreeData[2] != -1):
            i = getIterNumInBTree(BTree, OneBTreeData[2])
            return [i, 'else_if']




def countBetweenCondition(String):
    #added MAY 2016
    #return value --> [ count of ';', +1] : { ;;;;
    #                 [ count of ';', 0 ] : ;;;;
    #                 [ count of ';', -1 ] : ;;;; }
    temp = []
    temp_right = []
    for i,value in enumerate(String):
        if value == "{":
            temp.append(i)
        elif value == "}":
            if len(temp) > 0 :
                temp.pop()
            else :
                temp_right.append(i)

    if len(temp) == 0 and len(temp_right) == 0:
        return [String.count(';'),0]
    elif len(temp) > 0 and len(temp_right) == 0 :
        return [String[:temp[0]].count(';'), 1]

    elif len(temp) == 0 and len(temp_right) > 0 :
        return [String.count(';'), -1]



def getLeftValue(dependency_Array, value):
    #added MAY 2016
    for i in dependency_Array:
        if value == i[1]:
            if i[0] == -1 and i[2] != -1:
                return getLeftValue(dependency_Array, i[2])
            else:
                return i[0]

def getRightValue(dependency_Array, value):
    #added MAY 2016
    for i in dependency_Array:
        if value == i[1]:
            if i[2] == -1 and i[0] != -1 :
                return getRightValue(dependency_Array, i[0])
            else:
                return i[2]

class AnalyzeIfStatement:

    def __init__(self, wholeString):
        self.left_parenthesis_stack = []
        #self.right_parenthesis_stack = []
        self.binaryTree = []
        self.wholeString = wholeString
        self.wholeIFString = ''


    def getIFBlock(self):
        # get if block between 「```」
        k = re.compile("```")
        indexesOfDeliIter = re.finditer(k, self.wholeString)
        startPtr = 0
        endPtr = 0

        for i, value in enumerate(indexesOfDeliIter):
            if i%2 == 0 :
                startPtr = value.end()
                pass
            elif i%2 == 1:
                endPtr = value.start()
                self.wholeIFString = self.wholeIFString + self.wholeString[startPtr : endPtr]

        return  self.wholeIFString


    def makeBinaryTreeStructure(self):
        #find first if, while, for.

        IF_FOR_WHILE = re.compile('if|else if|for|while')
        IF_FOR_WHILE_Counts = re.finditer(IF_FOR_WHILE, self.wholeIFString)


        for i, condition in enumerate(IF_FOR_WHILE_Counts):
            temp = []
            now_condition_index = condition.start()
            if i == 0 :
                #independent Case
                temp.append(-1)
                temp.append(now_condition_index)
                temp.append(-1)
            else :
                # if_stack내 i-1번째 if|else if|for|while와 현재 if|else if|for|while사이에 콜론 「；」이 존재하는지 찾는다
                # else if 일 경우는 따로 Catch.

                front_condition_index = self.binaryTree[i-1][1]
                count_colon = countBetweenCondition(self.wholeIFString[front_condition_index:now_condition_index])
                now_is_else = self.wholeIFString[now_condition_index:now_condition_index+4].find('else')

                if count_colon[0] > 0 :
                    #사이에 ;들이 존재하는 경우
                    if now_is_else < 0 :
                        if self.binaryTree[i-1][0] == -1 and self.binaryTree[i-1][2] != -1 :
                            #front가 else if인 경우
                            find_same_level = self.binaryTree[i-1][2]
                            #else if면 BTree를 역으로 따라 올라가 else구문이 끝날때 까지 따라 올라가야 한다.
                            upper_level = getLeftValue(self.binaryTree, find_same_level)
                            temp.append(upper_level)
                            temp.append(now_condition_index)
                            temp.append(-1)
                        elif self.binaryTree[i-1][0] != -1 and self.binaryTree[i-1][2] == -1 :
                            #front가 if 이면서 TOP이 아닌 경우
                            upper_level = self.binaryTree[i-1][0]
                            temp.append(upper_level)
                            temp.append(now_condition_index)
                            temp.append(-1)
                        elif self.binaryTree[i-1][0] == -1 and self.binaryTree[i-1][2] == -1 :
                            #front가 if 이면서 TOP인 경우
                            if count_colon[1] > 0:
                                # {;; 의 경우
                                upper_level = self.binaryTree[i-1][1]
                                temp.append(upper_level)
                                temp.append(now_condition_index)
                                temp.append(-1)
                            else :
                                temp.append(-1)
                                temp.append(now_condition_index)
                                temp.append(-1)

                    elif now_is_else >= 0 :
                        temp.append(-1)
                        temp.append(now_condition_index)
                        temp.append(self.binaryTree[i-1][1])


                elif count_colon[0] == 0:
                    #사이에 ;이 존재하지 않은 경우
                    upper_level = self.binaryTree[i-1][1]
                    temp.append(upper_level)
                    temp.append(now_condition_index)
                    temp.append(-1)

                elif count_colon[1] < 0 and count_colon[0] > 0:
                    # condition사이에 「;}」 가 존재하는 경우
                    if now_is_else < 0 :
                        if self.binaryTree[i-1][0] == -1 and self.binaryTree[i-1][2] != -1 :
                            #front가 else if인 경우
                            #역으로 올라가 else if까지 찾아가야 한다
                            upper_level = getRightValue(self.binaryTree, self.binaryTree[i-1][2])
                            temp.append(upper_level)
                            temp.append(now_condition_index)
                            temp.append(-1)
                        elif self.binaryTree[i-1][0] != -1 and self.binaryTree[i-1][2] == -1 :
                            #front가 if인 경우
                            upper_level = getLeftValue(self.binaryTree, self.binaryTree[i-1][0])
                            temp.append(upper_level)
                            temp.append(now_condition_index)
                            temp.append(-1)
                    elif now_is_else >= 0:
                        if self.binaryTree[i-1][0] == -1 and self.binaryTree[i-1][2] != -1 :
                            #front가 else if인 경우
                            #역으로 else if 까지 따라 올라가야 한다
                            upper_level = self.binaryTree[i-1][2]
                            temp.append(-1)
                            temp.append(now_condition_index)
                            temp.append(upper_level)
                        elif self.binaryTree[i-1][0] != -1 and self.binaryTree[i-1][2] == -1 :
                            #front가 if인 경우
                            upper_level = self.binaryTree[i-1][0]
                            temp.append(-1)
                            temp.append(now_condition_index)
                            temp.append(upper_level)



            self.binaryTree.append(temp)


        return self.binaryTree


    def getIFstatements(self):
        IFstatements = []
        BlankStack = []
        for value in enumerate(self.binaryTree):
            start = value[1][1]
            #find the latest ')'
            temp = 0
            for left_blank, v in enumerate(self.wholeIFString[start:]) :
                if v == '(':
                    BlankStack.append(left_blank)
                    temp = 1
                elif v == ')' :
                    BlankStack.pop()

                if len(BlankStack) == 0 and temp == 1:
                    break

            end = start + left_blank + 1
            IFstatements.append(self.wholeIFString[start:end])

        return IFstatements

