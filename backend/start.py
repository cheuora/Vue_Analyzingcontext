#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import importlib
from pypict.tools import from_dict
from pypict.tools import compose_filter_funcs
import json
from flask import Flask, request, render_template, make_response
from collections import OrderedDict
from flask_cors import CORS
#from datetime import datetime
#from pyparsing import *


from libs.MakeCombination import MakeResults
from libs.excelHandle import save_result_excel

import traceback

app = Flask(__name__)
CORS(app)

#import importlib
#importlib.reload(sys)

#sys.setdefaultencoding('utf-8')

HOST = 'localhost'
SQLPORT = 3306
DB_USER = 'db_heyheyclub'
DB_USER_PWD = 'janux000'
MAX_TIME = 3600
#MAX_TIME = 3600
PAID_USER_MAX_TIME = 3600


logging.basicConfig(filename='./WSGI.log',level=logging.DEBUG)

def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


def isRegistered(email):
    #return [isRegistered, isPaidUser]
    return [True,True]


def devideByFirstItem(Arrays):
    tempFirstItems = []
    tempReturnArr = []
    for array in Arrays:
        if array[0] in tempFirstItems:
            for i, itemOftempReturnArr in enumerate(tempReturnArr):
                if itemOftempReturnArr.count(array[0]) > 0 :
                    tempReturnArr[i].append(array)
        else:
            tempFirstItems.append(array[0])
            tempReturnArr.append([array[0],array])


    return tempReturnArr


def changeSingleQuoteToHTMLCode(stringValues):
    tempString = ''
    tempString = stringValues.replace("'", "&#39;")
    return tempString


# def _validate_when_given(*argv) :

#     if (len(argv[0]) > 1) :
#         when = argv[0]['when']
#         given = argv[0]['given']

#         for dependencyPair in Dependency:
#             if (given == '__'.join(dependencyPair[0])) and (when == '__'.join(dependencyPair[1])):
#                 return False

#     return True





@app.route('/mcdcresult', methods=['POST'])
def MCDCCases():

    try:
        #authkey = request.cookies.get('authkey')

        #code_data = "```" + request.form['Codes'].decode('UTF-8') + "```"
        code_data = "```" + request.json['codes'] + "```"
        resultList = MakeResults(code_data)
        data = ''
        for i in range(len(resultList)):
            data = data + str(resultList[i])
            #print resultList[i]

        data = data.replace('@','()')
        xlsxFileName = save_result_excel(data)
        
        #return render_template('ECT_Cases.html', cases=data, key=authkey, xlsxfile='temp/'+xlsxFileName)
        return data


    except :
        var = traceback.format_exc()
        logging.info(var)
        #Error Page
        return render_template('Error.html')


@app.route('/mindmap', methods=['POST'])
def GetMindmapCases():
    try:    
        postData = json.loads(request.json['mindMapData'])
        postTreeData = json.loads(request.json['mindTreeData'])
        endPointDic = {}
        getLastPoint(postTreeData,endPointDic)
        Paths = getPaths(postData,endPointDic)
        GivenPath = []
        WhenPath = []
        authkey = 'free'

        for item in Paths:
            if item[::-1][1] == 'Given':
                GivenPath.append(item[::-1][2:])
            elif item[::-1][1] == 'When':
                if 'Yes' in item:
                    WhenPath.append(item[::-1][2:])

        #test
        DividedGivenArray = devideByFirstItem(GivenPath)

        #change format for pypict
        WhenArrayStrItemForPyPict = [ '__'.join(item) for item in WhenPath]
        pairingArray = []
        pairingArray.append(WhenArrayStrItemForPyPict)

        for itemOfDevidedGivenArray in DividedGivenArray:
            pairingArray.append(itemOfDevidedGivenArray[1:])


        #convert pairingArray to Dict
        pairingDic = {}
        pairingDic['when']  = pairingArray[0]

        for itemOfDevidedGivenArray in DividedGivenArray:
            pairingDic[itemOfDevidedGivenArray[0]] = [ '__'.join(item) for item in itemOfDevidedGivenArray[1:]]

        Pairs = from_dict(pairingDic,random_seed=2)

        PairsToList = list(Pairs)
        PairsWithOldTypr = []

        for PairsToListItem in PairsToList:
            temp = []
            temp.append(PairsToListItem['when'].split('__'))
            del PairsToListItem['when']
            for i, value in PairsToListItem.items():
                temp.append(value.split('__'))

            PairsWithOldTypr.append(temp)
        
        tableData = makeTableData(PairsWithOldTypr)
        return tableData
    except:
        var = traceback.format_exc()
        logging.info(var)
        #Error Page
        return render_template('Error.html')


    
def getLastPoint(postTreeData, EndPointDictionary):
    if 'children' in postTreeData:
        for j in postTreeData['children']:
            getLastPoint(j,EndPointDictionary)
    else:
        EndPointDictionary[postTreeData['id']] = postTreeData['topic']


def findPath(data, id, singlePathReturned):
    for dict_low in data:
        if dict_low['id'] == id:
            singlePathReturned.append(dict_low['topic'])
            if 'parentid' in dict_low:
                findPath(data, dict_low['parentid'],singlePathReturned)

def getPaths(data, endpoints):
    Paths = []
    for endpt in endpoints:
        path = []
        findPath(data, endpt, path)
        Paths.append(path)
    
    return Paths








def makeTableData(Pairs):
    tableData = "<table>"
    for rowNum, oneRow in enumerate(list(Pairs)):
        cellData = ""
        if rowNum == 0:  # make table header
            # tableData = tableData + "<th style='text-align: center'>No</th><th>When</th>"
            tableData = tableData + "<th>No</th><th>When</th>"
            for j in range(len(oneRow)):
                if j > 0:
                    tableData = tableData + "<th>" + "Given#" + str(j) + "</th>"

            tableData = tableData + "<th>Then</th>"

        tableData = tableData + "<tr>"
        # tableData = tableData + "<td style='text-align:center'>" + str(rowNum+1) + "</td>"
        tableData = tableData + "<td>" + str(rowNum + 1) + "</td>"

        for colData in enumerate(oneRow) : 
            oneCell = ":".join(colData[1])
            cellData = cellData + "<td>" + oneCell + "</td>"

        tableData = tableData + cellData + "<td> </td></tr>"
    tableData = tableData + "</table>"
    return tableData


if __name__ == "__main__":
    #app.run(host='172.18.0.2', port=80)
    app.run(host='0.0.0.0', port=5000)


