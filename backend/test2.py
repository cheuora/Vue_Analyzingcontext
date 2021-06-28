from pypair import pypair, getCoverage


a = [['if(a==0||b==1)', 'if(ss)'], ['if(a==0||b==1)', 'elseif(sss)'], ['if(a==0||b==1)', 'elseif(sskmakm)'], ['elseif(sksmsk)', 'if(NNN)', 'if(sKkSKks)'], ['elseif(smkdmkfla)']]

temp = [[['a==0', 'b==1', 'Results'], ['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']],
[['C', 'D', 'Results'], ['TRUE,FALSE,FALSE'], ['TRUE,TRUE,TRUE'], ['FALSE,TRUE,FALSE']],
[['C', 'D', 'Results'], ['TRUE,FALSE,TRUE'], ['FALSE,FALSE,FALSE'], ['FALSE,TRUE,TRUE']]]

for i, value in enumerate(temp) :
    del value[0]
    temp[i] = value


def nonDictFilter(parameters):

    filter = []

    # temp = getCoverage(parameters,len(parameters))
    temp = pypair(parameters,3)



    for i in temp:
        tempRow = []
        for slider in range(len(i)):
            tempRow.append(i[slider][0].split(',')[-1])
        if tempRow.count('TRUE') == 1 :
            filter.append(i)
                 
    return filter

filter = nonDictFilter(temp)

for i in filter:
    print(i)

# results = pypair(temp,3,nonDictFilter=filter)


# for i in results:
#     print(i)
