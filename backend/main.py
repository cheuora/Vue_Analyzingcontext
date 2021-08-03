#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from starlette.responses import HTMLResponse
import uvicorn
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pypair import pypair
from libs.MakeCombination import MakeResults
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import traceback
import os

HOST = 'localhost'
SQLPORT = 3306
DB_USER = 'db_heyheyclub'
DB_USER_PWD = ''
MAX_TIME = 3600
#MAX_TIME = 3600
PAID_USER_MAX_TIME = 3600
kTEMP_PATH = os.getcwd() + '/static/'
tempPath = os.getcwd() + '/templates/'

app = FastAPI()

app.mount('/static', StaticFiles(directory="/fastapi/static/"), name="static")


logging.basicConfig(filename='/fastapi/WSGI.log',level=logging.DEBUG)



origins = [
        settings.base_url + ":5000",
    settings.base_url,
    settings.base_url + ":8080",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCDCData(BaseModel):
    codes : str

class MindMapData(BaseModel):
    mindMapData : str
    mindTreeData : str

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

def convertToList(tuple):
    results = []
    for i in tuple:
        results.append(i.split("__"))
    
    return results




@app.post('/mcdcresult')
def MCDCCases(MCDCData: MCDCData):
    try:
        #authkey = request.cookies.get('authkey')

        #code_data = "```" + request.form['Codes'].decode('UTF-8') + "```"
        
        code_data = "```" + MCDCData.codes + "```"
        resultList = MakeResults(code_data)
        # data = ''
        # for i in range(len(resultList)):
        #     data = data + str(resultList[i])
        #     #print resultList[i]

        # data = data.replace('@','()')
        # xlsxFileName = save_result_excel(data, TEMP_PATH)
        
        #return render_template('ECT_Cases.html', cases=data, key=authkey, xlsxfile='temp/'+xlsxFileName)
        #merge data + xlsxFileName 
        # retData = data + ":::" + xlsxFileName
        return resultList


    except :
        var = traceback.format_exc()
        logging.info(var)
        #Error Page
        with open(tempPath+"Error.html", "r") as f:
            htmlData = ""
            lines = f.readlines()
            for line in lines:
                htmlData = htmlData + line

        return HTMLResponse(content=htmlData, status_code=200)


@app.post('/mindmap')
def GetMindmapCases(MindMapData : MindMapData):
    try:
        postData = json.loads(MindMapData.mindMapData)
        postTreeData = json.loads(MindMapData.mindTreeData)

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
        
        inputs = []
        inputs.append(pairingDic["when"])
        del pairingDic['when']

        for i in pairingDic.values() :
            inputs.append(i)

        Pairs = pypair(inputs,2)

        PairsWithOldTypr = []

        for i in Pairs:
            temp = convertToList(i)
            PairsWithOldTypr.append(temp)

        
        tableData = makeTableData(PairsWithOldTypr)
        return tableData
    except:
        var = traceback.format_exc()
        logging.info(var)
        #Error Page
        with open(tempPath+"Error.html", "r") as f:
            htmlData = ""
            lines = f.readlines()
            for line in lines:
                htmlData = htmlData + line

        return HTMLResponse(content=htmlData, status_code=200)

        




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
    uvicorn.run(app, host="0.0.0.0", port=5000)
