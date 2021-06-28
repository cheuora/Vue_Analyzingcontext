# -*- coding: UTF-8 -*-

from libs.getPatternAndWrite import MakeMCDCResults
from libs.checkParenthesis import AnalyzeIfStatement
from parsingif import getWholeIfPath, nonDictFilter
from pypair import pypair



def convert(listval):
    temp = listval[0].split(',')
    retVal = ""
    for i in temp:
        retVal = retVal + '<td>' + i + '</td>'
    
    return retVal

def convertHTML_TABLE(ifStatements, if_variables, Results):
    headerIndex = 0
    valueIndex = 0
    headerStartIndex = 0

    retVal =""
    tableContents = ""
    
    if len(ifStatements) != len(Results):
        return False
    
    for c, value in enumerate(ifStatements):
        headers = ""
        for v in value:
            spanValue = str(len(if_variables[headerIndex]))
            headerIndex = headerIndex + 1
            headers = headers + "<th colspan=" + spanValue + ">" + v + "</th>"
        
        row_if = "<tr>" + headers + "</tr>"

        params = ""
        for i in range(headerStartIndex, headerIndex):
            for j in if_variables[i]:
                params = params + '<td>' + j + '</td>'

        headerStartIndex = headerIndex

        row_params = "<tr>" + params + '</tr>'

        
        temp = ""
        for v in Results[valueIndex]:
            for j in v:
                temp = temp + convert(j)
            temp = '<tr>' + temp + '</tr>'
        
        row_values = temp

        valueIndex = valueIndex +1

        tableContents = tableContents + '<table>' + row_if + row_params + row_values + '</table>'


    return tableContents
    


def getXpression(lists):
    retVal = []
    for i,value in enumerate(lists):
        retVal.append(value.replace('elseif','').replace('if',''))
    
    return retVal

def MakeResults(data):


    AnalyzedIF = AnalyzeIfStatement(data)

    ifBlock = AnalyzedIF.getIFBlock()

    if_statements_list = getWholeIfPath(ifBlock)

    fullMCDC = []
    for if_stream in if_statements_list:
        temp = getXpression(if_stream)
        one_path = []
        for i in temp:
            MCDC = MakeMCDCResults(i)
            one_path.append(MCDC)
        
        fullMCDC.append(one_path)


    MCDC_Results = []
    if_statement_variables = []

    for i, cases in enumerate(fullMCDC):
        for h, value in enumerate(cases):
            if h > 0 :
                value.append(['-'])

            if_statement_variables.append(value.pop(0))
            #del value[0]
        
        mcdcFilter = nonDictFilter(cases)
        temp = pypair(cases,len(cases),nonDictFilter=mcdcFilter)

        MCDC_Results.append(temp)

    
    resultHTML = convertHTML_TABLE(if_statements_list, if_statement_variables ,MCDC_Results)

    return resultHTML
