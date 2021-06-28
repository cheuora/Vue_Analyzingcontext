header = [['a==0', 'b==1', 'Results'], ['ss', 'Results'], ['a==0', 'b==1', 'Results'], ['sss', 'Results'], ['a==0', 'b==1', 'Results'], ['sskmakm', 'Results'], ['sksmsk', 'Results'], ['NNN', 'Results'], ['sKkSKks', 'Results'], ['smkdmkfla', 'Results']]

ifstatement = [['if(a==0||b==1)', 'if(ss)'], ['if(a==0||b==1)', 'elseif(sss)'], ['if(a==0||b==1)', 'elseif(sskmakm)'], ['elseif(sksmsk)', 'if(NNN)', 'if(sKkSKks)'], ['elseif(smkdmkfla)']]

data= [[(['TRUE,FALSE,TRUE'], ['TRUE,TRUE']), (['TRUE,FALSE,TRUE'], ['FALSE,FALSE']), (['FALSE,FALSE,FALSE'], ['-']), (['FALSE,TRUE,TRUE'], ['TRUE,TRUE']), (['FALSE,TRUE,TRUE'], ['FALSE,FALSE'])], [(['TRUE,FALSE,TRUE'], ['TRUE,TRUE']), (['TRUE,FALSE,TRUE'], ['FALSE,FALSE']), (['FALSE,FALSE,FALSE'], ['-']), (['FALSE,TRUE,TRUE'], ['TRUE,TRUE']), (['FALSE,TRUE,TRUE'], ['FALSE,FALSE'])], [(['TRUE,FALSE,TRUE'], ['TRUE,TRUE']), (['TRUE,FALSE,TRUE'], ['FALSE,FALSE']), (['FALSE,FALSE,FALSE'], ['-']), (['FALSE,TRUE,TRUE'], ['TRUE,TRUE']), (['FALSE,TRUE,TRUE'], ['FALSE,FALSE'])], [(['TRUE,TRUE'], ['TRUE,TRUE'], ['TRUE,TRUE']), (['TRUE,TRUE'], ['TRUE,TRUE'], ['FALSE,FALSE']), (['TRUE,TRUE'], ['FALSE,FALSE'], ['-']), (['FALSE,FALSE'], ['-'], ['-'])], [(['TRUE,TRUE'],), (['FALSE,FALSE'],)]]

# for i in data:
#     for j in i:
#         print(j)
    
#     print("_________")


def convert(listval):
    temp = listval[0].split(',')
    retVal = ""
    for i in temp:
        retVal = retVal + '<td>' + i + '</td>'
    
    return retVal


headerIndex = 0
valueIndex = 0
headerStartIndex = 0

for value in ifstatement:
    headers = ""
    for v in value:
        spanValue = str(len(header[headerIndex]))
        headerIndex = headerIndex + 1
        headers = headers + "<td colspan=" + spanValue + ">" + v + "</td>"
    
    row_if = "<tr>" + headers + "</tr>"

    params = ""
    for i in range(headerStartIndex, headerIndex):
        for j in header[i]:
            params = params + '<td>' + j + '</td>'

    headerStartIndex = headerIndex

    row_params = "<tr>" + params + '</tr>'

    
    temp = ""
    for v in data[valueIndex]:
        for j in v:
            temp = temp + convert(j)
        temp = '<tr>' + temp + '</tr>'
    
    row_values = temp

    valueIndex = valueIndex +1

    print(row_if)
    print(row_params)
    print(row_values)

    

