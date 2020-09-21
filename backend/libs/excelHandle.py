#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlsxwriter
import uuid
from libs.makeTestingData import makeTestData
from libs.makeTestingData import ClosestValue
import pyparsing
#TEMP_DIR='/root/AnalztingContext/AnanyzingContext/static/temp/' #change when install in other site
def save_result_excel(resultData, tempPath):
	#resultData(html)을 읽어들여 excel파일로 변환후 저장하는 함수.
	h3Start,h3End = pyparsing.makeHTMLTags("h3")
	tableStart,tableEnd = pyparsing.makeHTMLTags("table")
	h3 = h3Start + pyparsing.SkipTo(h3End).setResultsName("body") + h3End
	table = tableStart + pyparsing.SkipTo(tableEnd).setResultsName("body") + tableEnd
	headers = []
	tables = []
	resultData_NonHTMLCode = resultData.replace("&nbsp;", " ")
	resultData_NonHTMLCode = resultData_NonHTMLCode.replace("&lt;", "<")
	resultData_NonHTMLCode = resultData_NonHTMLCode.replace("&gt;", ">")
	
	for tokens, start, end in h3.scanString(resultData_NonHTMLCode.encode("UTF-8")):
		headers.append(tokens.body)

	for tokens, start, end in table.scanString(resultData_NonHTMLCode.encode("UTF-8")) :
		temp = "<table>"+tokens.body+"</table>"
		tables.append(html_table_to_excel(temp))


	#write XLSX file from here.

	try:
		xlsxFile = str(uuid.uuid4()).replace("-", "")+".xlsx"
		workbook = xlsxwriter.Workbook(tempPath + xlsxFile)
		merge_format = workbook.add_format({'align': 'center', 'bold' : 1})
		worksheet = workbook.add_worksheet()
		#write Data here
		tablewidth = 0
		mT = makeTestData()
		testDataArray = mT.testValuables(tables)

		for i, tableTuple in enumerate(tables):

			write_date_to_excel(worksheet, headers[i], tableTuple, tablewidth, 3, merge_format, testDataArray)
			tablewidth = tablewidth + len(tableTuple[0]) - 1

		workbook.close()

		return xlsxFile

	except IOError:
		print ("IOError")
		return False



def html_table_to_excel(table):

	""" html_table_to_excel(table): Takes an HTML table of data and formats it so that it can be inserted into an Excel Spreadsheet.
	"""
	data = {}
	table = table[table.index('<tr>'):table.index('</table>')]
	
	rows = table.strip('\n').split('</tr>')[:-1]
	for (x, row) in enumerate(rows):
		columns = row.strip('\n').split('</td>')[:-1]
		data[x] = {}
		for (y, col) in enumerate(columns):
			data[x][y] = col.replace('<tr>', '').replace('<td>', '').strip()

	return data



def write_date_to_excel(worksheet, header, data, shiftx, shifty, merge_format, testDataArray):
	""" export_to_xls(data, title, filename): Exports data to an Excel Spreadsheet.
	Data should be a dictionary with rows as keys; the values of which should be a dictionary with columns as keys; the value should be the value at the x, y coordinate.
	"""
	mkCV = ClosestValue()
	mkMT = makeTestData()

	for x in sorted(data.keys()):
			for y in sorted(data[x].keys()):
				if shiftx != 0 and y == 0:
					pass
				else:
					worksheet.write(x+shifty, y+shiftx, data[x][y])
					if x > 0 :
						mergedData =  mkMT.mergeTestData(testDataArray[x-1])
						worksheet.write(x + shifty, y + shiftx + 1, mkCV.getClosestValues(mergedData))

				#make header
				if y == 1 and x == 0 :
					temp = len(data[x]) - 2
					worksheet.merge_range(shifty-1, y+shiftx, shifty-1, y+shiftx + temp, header, merge_format)






