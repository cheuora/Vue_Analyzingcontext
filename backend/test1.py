from libs.getPatternAndWrite import MakeMCDCResults
from pypair import pypair, getCoverage
import itertools

t = [['if(a==0||b==1)', 'if(ss)'], ['if(a==0||b==1)', 'elseif(sss)'], 
['if(a==0||b==1)', 'elseif(sskmakm)'], ['elseif(sksmsk)', 'if(NNN)', 'if(sKkSKks)'], 
['elseif(smkdmkfla)']]

def getXpression(lists):
    for i,value in enumerate(lists):
        lists[i]=value.replace('elseif','').replace('if','')
        

for i in t:
    getXpression(i)

print(t)
temp = MakeMCDCResults(t[0][0])

print(temp)

'''
TestData: 
[['a==0', 'b==1', 'Results'], ['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']]
[['ss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE']]
[['Finalcontext', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE']]
'''
temp = [[['a==0', 'b==1', 'Results'], ['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']],
[['ss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE'],['-']]]

# temp = [[['ss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE'],['-']],
# [['sss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE'],['-']],
# [['ssss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE'],['-']] ]

temp2 = [[['a==0', 'b==1', 'Results'], ['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']],
[['ss', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE']],
[['Finalcontext', 'Results'], ['TRUE,TRUE'], ['FALSE,FALSE']] ]



def nonDictFilter(parameters):

    filter = []

    temp = getCoverage(parameters,len(parameters))

    for i in temp[0]:
        # 각 row별로 [TRUE, -], [FALSE,TRUE], [FALSE, FALSE] 가 있는지 sliding으로 검색하여
        # 있으면 있어서는 안될 열로 저장한다.

        for slider in range(len(i)-1):
            if (i[slider][0].split(',')[-1] == 'TRUE' and i[slider+1][0].split(',')[-1] == '-'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == 'FALSE' and i[slider+1][0].split(',')[-1] == 'TRUE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == 'FALSE' and i[slider+1][0].split(',')[-1] == 'FALSE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == '-' and i[slider+1][0].split(',')[-1] == 'TRUE'):
                filter.append(i)
            elif (i[slider][0].split(',')[-1] == '-' and i[slider+1][0].split(',')[-1] == 'FALSE'):
                filter.append(i)
    
    #print(filter)

    print("====end makeMCDC=====")
    return filter        


for i, value in enumerate(temp) :
    del value[0]
    temp[i] = value


for i, value in enumerate(temp2) :
    del value[0]
    temp2[i] = value

print("=====makefilter======")

mcdcFilter = nonDictFilter(temp)


results = pypair(temp,2,nonDictFilter=mcdcFilter)
print("======results======")

for i in results:
    print(i)

# parameters = [ [ "Brand X", "Brand Y","Brand A" ]
#              , [ "NT", "2000", "XP"]
#              , [ "Internal", "Modem" ]
#              , ['This', 'That']
#              ]

# filter = {"Brand X" : ["XP"], "Brand Y" : ["NT","That"]}

# temp = pypair(parameters,2, filter) 

# for i in temp:
#     print(i)

