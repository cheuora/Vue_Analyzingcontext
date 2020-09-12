# -*- coding: UTF-8 -*-
import copy

from libs.getParams import catch_conditions
from libs.getPatternAndWrite_second import MakeMCDCResults
from libs.getPatternAndWrite_second import getHeaderOfStatementHTML
from libs.getPatternAndWrite_second import getTableElementsHTML
from libs.getPatternAndWrite_second import AllPair2ToList
from libs.getPatternAndWrite_second import getFilter
from libs.getPatternAndWrite_second import divideItem_in_Array
from libs.getPatternAndWrite_second import compareValues_in_Array
from libs.getPatternAndWrite_second import addDummyRow
from libs.getPatternAndWrite_second import setResultValueFirst
from libs.getPatternAndWrite_second import parenthetic_contents
from libs.Combination import popFromColumnValue
from libs.Combination import makeLongList
from libs.Combination import checkingTWOValuesWithFilterArray
from libs.checkParenthesis import AnalyzeIfStatement
from libs.checkParenthesis import getUpperConditionListIndex
from pypict.tools import from_dict
from pypict.tools import compose_filter_funcs
from collections import OrderedDict



filterArray = []
BTree = []

def convertHTML_TABLE(Header, Table_title, Results):
    NumOfStatement = len(Header)
    HeaderOfStatement = getHeaderOfStatementHTML(Header)

    HTMLStatement = getTableElementsHTML(Table_title)
    #Result is all_pair2 instance. You should change instance!
    AllPairResult = AllPair2ToList(Results)

    #단일 if 문일 때 처리 ...
    #단일 if 문일 경우에는 AllPairResult의 길이가 1이 된다 . 하나의 list에 아이템들이 다 몰아 있기 때문.
    #이 경우에는 AllPairResult[0] 의 길이를 취한다.


    AllPairResult_len = len(AllPairResult)

    returnHTMLval = []
    for j in range(NumOfStatement):

        if HeaderOfStatement[j].find("else_") > 0 :
            #exclude "else only" case
            returnHTMLval.append(" ")
            pass
        else:
            returnHTMLval.append(HeaderOfStatement[j]) #make first item of returnHTMLval
            #Subtitute "<tr>" to <tr><td>&nbsp;</td> for LeftColumn Header
            returnHTMLval[j] = str(returnHTMLval[j]) + "<table border=1>"+str(HTMLStatement[j]).replace("<tr>", "<tr><td>&nbsp;</td>") #<h3> + Table header part


            #Result is all_pair2 instance. You should change it!

            '''
                if문이 단일 구문일 경우에는 다르게 테이블을 구성한다.
            '''
            if AllPairResult_len ==1 :
                HTMLResults = getTableElementsHTML(AllPairResult[0])
                for k in range(len(HTMLResults)):
                    returnHTMLval[j] = str(returnHTMLval[j]) + str(HTMLResults[k]).replace("<tr>", "<tr><td>Case %d</td>" %(k+1))
            else :
                for i in range(AllPairResult_len):
                    HTMLResults = getTableElementsHTML(AllPairResult[i])

                    #Subtitute "<tr>" to <tr><td>Case %1</td> for LeftColumn Header
                    returnHTMLval[j] = str(returnHTMLval[j]) + str(HTMLResults[j]).replace("<tr>", "<tr><td>Case %i</td>" %(i+1))


            returnHTMLval[j] = str(returnHTMLval[j]) + "</table>"

    return returnHTMLval


'''
Structure of HTML Result at each returnHTMLval element :q
<h3> Original Condition Statement (Header)</h3>
<table>
    <tr>
        <td> a > 21 </td><td> b <=32 </td><td> RESULT </td> : Table_title
    </tr>
    <tr>
        <td>TRUE </td><td>FALSE</td><td>FALSE</td> : Results
    </td>
</table>
'''


def _is_validate_combination(*argv):
    
    row = argv[0]   
    blockCount = len(BTree)

    rowArray = divideItem_in_Array([[i] for i in row.values()])


    if len(rowArray) == blockCount :

        # for i in range(len(filterArray[blockCount-1])):
        #     if i < len(filterArray[blockCount-1]): 
                # if compareValues_in_Array(rowArray, filterArray[blockCount-1][i]) :
                #     pass
                # else:
                #     return False
                
        for i in range(len(filterArray)):                
            for j in filterArray[i]:
                if compareValues_in_Array(rowArray, j) :
                    pass
                else:
                    return False


        for j in range(blockCount):
            if (checkingTWOValuesWithFilterArray(BTree, rowArray, j)) :
                pass
            else:
                return False

    return True




def is_valid_Combination(row):
    # it is deprecated 2019-10-07!!!
    n = len(row)
    row = divideItem_in_Array(row)


    #row list data를 가지고 filterArray에 있는 좌표 데이터를 이용, 좌표에 해당되는 값끼리 같은지 비교하여
    #다르면 return False를 한다.


    retVal = True
    if n > 1 :
        now = n-1

        for j in range(len(filterArray[now])):

            if j < (len(filterArray[now])) :
                if compareValues_in_Array(row, filterArray[now][j]) :
                    #print "compareValues_in_Array OK"
                    pass
                else :
                    #print "compareValues_in_Array NOT OK"
                    return False

        #check dependency in here

        retVal = checkingTWOValuesWithFilterArray(BTree, row, now)


    return retVal


def MakeResults(data):

    #data = data.replace('\n', ' ')
    #data = data.replace('\r', ' ')
    #data = data.replace('\t', ' ')

    global filterArray
    global BTree

    AnalyzedIF = AnalyzeIfStatement(data)
    #change data
    data = AnalyzedIF.getIFBlock()

    BTree = AnalyzedIF.makeBinaryTreeStructure()
    if_data_StatementOnly = AnalyzedIF.getIFstatements()



    for i in range(len(if_data_StatementOnly)):
        #replace <, > with &gt, &lt
        if_data_StatementOnly[i] = if_data_StatementOnly[i].replace("<", "&lt;")
        if_data_StatementOnly[i] = if_data_StatementOnly[i].replace(">", "&gt;")


    #Get all Condition Statements from pattern searching result.
    MCDC = []
    '''
    make List like below -->
    [
        ['front==rear', '||', 'x==tens', '||', 'z=2'],
        ['front==rear', '||', 'x==emp', '&&', 'q==z'],
        ['xxx>2']
    ]

    2014.08.05 @cheuora
    In MCDC, One Row Consists like below.
    [
        ['Decision A', 'Decision B', 'Decision C', 'Decision D'],
        ['FALSE,TRUE,-,TRUE'],
        ['FALSE,FALSE,FALSE,FALSE'],
        ['TRUE,FALSE,FALSE,TRUE'],
        ['FALSE,FALSE,TRUE,TRUE']
    ]

    '''


    for i, if_statements in enumerate(if_data_StatementOnly):

        if_statements = min(list(parenthetic_contents(if_statements)))[1]
        if_statements = '(' + if_statements + ')'

        MCDC.append(MakeMCDCResults(if_statements))

    '''
    @2014.08.06
    Derive Header info from MCDC List. Afrer this,
    MCDC List contains only MCDC results.
    '''
    MCDC_Header = []

    for k in range(len(MCDC)) :
        MCDC_Header.append(MCDC[k][0])
        del MCDC[k][0]


    '''
    @2014.08.06
    Pairwising n=1 Combination.
    '''

    filterArray = getFilter(MCDC_Header)

    addDummyRow(BTree, MCDC)

    MCDC_Result = []
    if len(MCDC) > 1 :
        
        mcdcDictForPyPict = {}

        for keyNum, mcdcItem in enumerate(MCDC):
            mcdcDictForPyPict[keyNum] =   [ '__'.join(item) for item in mcdcItem]

        # print(mcdcDictForPyPict)

        '''
        ＠２０１４年１０月３０日
        filter_func機能でバグがあるので、この使用をやめる。
        その代わりに、Pairwiseの結果を条件なしに生成してありえないケースを削除する。
        '''

        Pairs = from_dict(OrderedDict(mcdcDictForPyPict), 
                filter_func= _is_validate_combination, order=1, random_seed=3)


        #PairsはTupleの集まりで構成してます。これをリストで変換する。
        for i in enumerate(Pairs):
            MCDC_Result.append(i[-1])


    else :
        mcdcDictForPyPict = {}
        for keyNum, mcdcItem in enumerate(MCDC[0]):
            mcdcDictForPyPict[keyNum] = [item for item in mcdcItem][0]
            
        MCDC_Result.append(mcdcDictForPyPict)
        

    MCDC_Result_Converted = [[[ret] for ret in result.values()] for result in MCDC_Result]


    resultHTML = convertHTML_TABLE(if_data_StatementOnly, MCDC_Header, MCDC_Result_Converted)
    
    return resultHTML


'''
각 구간간 변수 비교는 3가지 패턴이 있다.
2014.8.4
Clause A : if (a<1 || b<4)..
Clause B : if (a>4 && B <> 1)...

Pattern1 --> A-a 와 B-a가 일치하는 경우 : A-a 가 T면 B-a도T, F - F
Pattern2 --> A-a 와 B-a가 불일치
    범위가 겹치는 부분이 있는 경우 (A-a <5 , B-a <2)
        Don't care
    범위태 겹치는 부분이 전혀 없는 경우 T-F , F-T 관계
Pattern3 --> A-a가 불일치 연산인 경우
    Don't care.

@@2014.08.04 : 변수 비교는 하지 말자.. 큰 의미는 없을 것 같다는 생각이 든다.

'''
