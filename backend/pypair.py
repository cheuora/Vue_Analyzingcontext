import itertools

def itemCount2by2(array):
    length = 0
    for i in array:
        length = length + len(i)
    return length

def getCoverage(parameters, way):
    pairCoverage = list(itertools.combinations(parameters,way))
    pairCovArray = []
    for i in pairCoverage:
        pairCovArray.append(list(itertools.product(*i)))
    
    return pairCovArray

def executor(fullcomb, coverageObj):
    remainedCoverage = 1
    selectedCaseIndex = []
    ret_cases = []
    threshold = len(coverageObj.originCoverage)

    for i in range(threshold,0, -1):
        selectedCaseIndex = []
        for selectedIndex, value in enumerate(fullcomb):
            bingo = coverageObj.checkCoverage(value)
            if (len(bingo) >= i):
                if (fullcomb[selectedIndex] not in coverageObj.nonDictFilter) :
                    selectedCaseIndex.append(selectedIndex)
                    for items in bingo:
                        if items:
                            remainedCoverage =  coverageObj.updateCoverage(items)


        for case_index in selectedCaseIndex:
            ret_cases.append(fullcomb[case_index])
        
        if (remainedCoverage == 0):
            break

        for ele in sorted(selectedCaseIndex, reverse = True): 
            # fullcomb업데이트 :  
            del fullcomb[ele] 

    return ret_cases


class Coverage:
    originCoverage = ''
    def __init__(self, coverageAll, num_of_way, filter, nonDictFilter):
        Coverage.originCoverage = coverageAll
        self.num_of_way = num_of_way
        self.filter = filter
        #MCDC필터는 filter구조로 거르지 못하는 구조를 2by2 list로 만든 필터임. Optional Filter임. 
        self.nonDictFilter = nonDictFilter

    def updateCoverage(self,coordinate):
        # 인덱스(x,y)에 맞는 커버리지 list배열(2x2)배열을 삭제 및 업데이트
        # 남아 있는 item수를 항상 return
        try:
            Coverage.originCoverage[coordinate[0]].pop(coordinate[1])
        except IndexError:
            #pop index error면 Pass
            pass

        return itemCount2by2(Coverage.originCoverage)

    def searchCoverageItem(self, itemVal, fromIndex = ()):
        # 커버리지 list배열(2x2)에서 item을 찾아 인덱스를(x,y) return
        # 못찾으면 [] return

        x = 0
        y = 0
        retval = []

        for i,values in enumerate(Coverage.originCoverage):
            if ( itemVal in values):
                y = values.index(itemVal)
                x = i
                if ((len(fromIndex)>0 and x > fromIndex[0]) or len(fromIndex) == 0 ):
                    retval.append((x,y))
                
                break

        return retval
        
    def checkFilter(self, one_combinations_case):
        try:
            #one_combinations_case의 type이 list이면 tuple로 변환
            if isinstance(one_combinations_case[0],list) and isinstance(one_combinations_case[0],list):    
                tmp = self.filter[one_combinations_case[0][0]]
                isIn = tmp.count(one_combinations_case[1])
            else:
                tmp = self.filter[one_combinations_case[0]]
                isIn = tmp.count(one_combinations_case[1])

            if isIn > 0 :
                return False
                
        except KeyError:
            pass
    
        return True

    def checkCoverage(self,itemCaseFromFull):
        retval = []
        combinations_case = list(itertools.combinations(itemCaseFromFull,self.num_of_way))
        #필터 적용해야 한다.
        for i in combinations_case:
            if self.checkFilter(i):

                if retval == []:
                    searchResult = self.searchCoverageItem(i)
                else:
                    searchResult = self.searchCoverageItem(i,fromIndex=retval[-1])

                if (searchResult): 
                    retval = retval + searchResult
            else:
                #pass
                break
        
        return retval


def pypair(parameters,way, filter = {}, nonDictFilter=[]):
    # main function
    fullcomb = list(itertools.product(*parameters))
    coverageObj = Coverage(getCoverage(parameters,way), way, filter, nonDictFilter)
    Test_cases = executor(fullcomb, coverageObj)

    return Test_cases
