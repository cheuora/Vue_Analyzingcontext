# -*- coding: UTF-8 -*-

import re  # @UnresolvedImport

#Library 모음.

#문자열 정리 : 탭(\t), 공백, 엔터 제거
def calibrate_text(string):
    string = string.replace(' ', '')
    string = string.replace('\n', '')
    string = string.replace('\r', '') #CR 제거
    string = string.replace('\t', '')
    return string




def catch_conditions(string):
    #개행(改行)제거
    string = string.replace('\n', '')
    string = string.replace('\r', '')

    #()문자는 일단 @로 치환.

    string = string.replace('()', '@')


    #find Whole Sentences in Most outer parenthesis!
    outer = re.compile("\((.+)\)")
    m = outer.search(string)
    outer_str = m.group(1)
    #print "outer_str : %s" % outer_str
    left_operand_patt = re.compile(".*['\|\||&&'].*\((.+)\)")
    right_operand_patt = re.compile("\((.+)\).*['\|\||&&'].*")
    outer_statements = analyzing_statements(outer_str)
    WholeParam = []

    if (left_operand_patt.search(outer_str) and  right_operand_patt.search(outer_str)) :
        #(..) .. (..) Pattern이다.
        #일단 이대로 Return
        WholeParam = outer_statements

    elif (left_operand_patt.search(outer_str)) :
        #(.. ()) pattern이다. 앞 단에 1, 2번째를취해 innerstr결과 뒤에 붙인다.
        #inner를 구분해야 함.
        m = outer.search(outer_str)
        innerstr =  m.group(1)
        InnerParams = analyzing_statements(innerstr)
        WholeParam = InnerParams + [outer_statements[1]]+[outer_statements[0]]
    elif (right_operand_patt.search(outer_str)) :
        #((...) ....) pattern이다. 뒤 1, 2번째를취해 innerstr결과 뒤에 붙인다.
        #inner를 구분해야 함.
        m = outer.search(outer_str)
        innerstr =  m.group(1)
        InnerParams = analyzing_statements(innerstr)
        WholeParam = InnerParams + [outer_statements[len(outer_statements)-2]] + [outer_statements[len(outer_statements)-1]]
    else :
        #(....) pattern이다 이대로 return
        WholeParam = outer_statements

    return WholeParam




def analyzing_statements(string):
    #먼저 정규식을 이용하여 String을 and,or 연산자 단위로 자른다.
    patt = re.compile('\|\||&&')
    Params = re.split(patt, string)
    if (len(Params) == 1) :
        #String내에 연산자가 없는 경우(단일 조건)는 그대로 그냥 돌려 준다.
        return [calibrate_text(string)]
    elif len(Params) > 1 :
        operators = re.findall(patt, string)
        retParams = []
        for i in range(len(Params)):
            #자른 결과에 공백 없애기
            Params[i] = calibrate_text(Params[i])
            if ( i == 0):
                retParams = retParams + [Params[i]]
            elif(i > 0) :
                retParams = retParams + [operators[i-1]] + [Params[i]]

        return retParams     #최종적으로 Params의 구성은 [인자A, and/or, 인자B, ... ]로 구성된다.
    else :
        return ['error']

