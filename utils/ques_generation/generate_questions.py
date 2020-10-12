import spacy
from spacy.lang.en import English
from spacy.pipeline import Sentencizer

import nltk
import en_core_web_sm


nlp = spacy.load("en_core_web_sm",disable=['ner','textcat'])
# nlp = English()


def chunk_search(segment, chunked):
    m = len(chunked)
    list1 = []
    for j in range(m):
        if (len(chunked[j]) > 2 or len(chunked[j]) == 1):
            list1.append(j)
        if (len(chunked[j]) == 2):
            try:
                str1 = chunked[j][0][0] + " " + chunked[j][1][0]
            except Exception:
                pass
            else:
                if (str1 in segment) == True:
                    list1.append(j)
    return list1

def segment_identify(sen):
    segment_set = sen.split(",")
    return segment_set


def clause_identify(segment):
    tok = nltk.word_tokenize(segment)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?|VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    flag = 0
    for j in range(len(chunked)):
        if (len(chunked[j]) > 2):
            flag = 1
        if (len(chunked[j]) == 2):
            try:
                str1 = chunked[j][0][0] + " " + chunked[j][1][0]
            except Exception:
                pass
            else:
                if (str1 in segment) == True:
                    flag = 1
        if flag == 1:
            break

    return flag


def verbphrase_identify(clause):
    tok = nltk.word_tokenize(clause)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    str1 = ""
    str2 = ""
    str3 = ""
    list1 = chunk_search(clause, chunked)
    if len(list1) != 0:
        m = list1[len(list1) - 1]
        for j in range(len(chunked[m])):
            str1 += chunked[m][j][0]
            str1 += " "

    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked1 = chunkparser1.parse(tag1)

    list2 = chunk_search(str1, chunked1)
    if len(list2) != 0:

        m = list2[0]
        for j in range(len(chunked1[m])):
            str2 += (chunked1[m][j][0] + " ")

    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<VB.?|MD|RP>+}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked2 = chunkparser1.parse(tag1)

    list3 = chunk_search(str1, chunked2)
    if len(list3) != 0:

        m = list3[0]
        for j in range(len(chunked2[m])):
            str3 += (chunked2[m][j][0] + " ")

    X = ""
    str4 = ""
    st = nltk.word_tokenize(str3)
    if len(st) > 1:
        X = st[0]
        s = ""
        for k in range(1, len(st)):
            s += st[k]
            s += " "
        str3 = s
        str4 = X + " " + str2 + str3

    if len(st) == 1:
        tag1 = nltk.pos_tag(st)
        if tag1[0][0] != 'are' and tag1[0][0] != 'were' and tag1[0][0] != 'is' and tag1[0][0] != 'am':
            if tag1[0][1] == 'VB' or tag1[0][1] == 'VBP':
                X = 'do'
            if tag1[0][1] == 'VBD' or tag1[0][1] == 'VBN':
                X = 'did'
            if tag1[0][1] == 'VBZ':
                X = 'does'
            str4 = X + " " + str2 + str3
        if (tag1[0][0] == 'are' or tag1[0][0] == 'were' or tag1[0][0] == 'is' or tag1[0][0] == 'am'):
            str4 = tag1[0][0] + " " + str2

    return str4


def subjectphrase_search(segment_set, num):
    str2 = ""
    for j in range(num - 1, 0, -1):
        str1 = ""
        flag = 0
        tok = nltk.word_tokenize(segment_set[j])
        tag = nltk.pos_tag(tok)
        gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
        chunkparser = nltk.RegexpParser(gram)
        chunked = chunkparser.parse(tag)

        list1 = chunk_search(segment_set[j], chunked)
        if len(list1) != 0:
            m = list1[len(list1) - 1]
            for j in range(len(chunked[m])):
                str1 += chunked[m][j][0]
                str1 += " "

            tok1 = nltk.word_tokenize(str1)
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            list2 = chunk_search(str1, chunked1)
            if len(list2) != 0:
                m = list2[len(list2) - 1]
                for j in range(len(chunked1[m])):
                    str2 += (chunked1[m][j][0] + " ")
                flag = 1

        if flag == 0:
            tok1 = nltk.word_tokenize(segment_set[j])
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            list2 = chunk_search(str1, chunked1)
            st = nltk.word_tokenize(segment_set[j])
            if len(chunked1[list2[0]]) == len(st):
                str2 = segment_set[j]
                flag = 1

        if flag == 1:
            break

    return str2


def postprocess(string):
    tok = nltk.word_tokenize(string)
    tag = nltk.pos_tag(tok)

    str1 = tok[0].capitalize()
    str1 += " "
    if len(tok) != 0:
        for i in range(1, len(tok)):
            if tag[i][1] == "NNP":
                str1 += tok[i].capitalize()
                str1 += " "
            else:
                str1 += tok[i].lower()
                str1 += " "
        tok = nltk.word_tokenize(str1)
        str1 = ""
        for i in range(len(tok)):
            if tok[i] == "i" or tok[i] == "we":
                str1 += "you"
                str1 += " "
            elif tok[i] == "my" or tok[i] == "our":
                str1 += "your"
                str1 += " "
            elif tok[i] == "your":
                str1 += "my"
                str1 += " "
            elif tok[i] == "you":
                if i - 1 >= 0:
                    to = nltk.word_tokenize(tok[i - 1])
                    ta = nltk.pos_tag(to)
                    # print ta
                    if ta[0][1] == 'IN':
                        str1 += "me"
                        str1 += " "
                    else:
                        str1 += "i"
                        str1 += " "
                else:
                    str1 += "i "

            elif tok[i] == "am":
                str1 += "are"
                str1 += " "
            else:
                str1 += tok[i]
                str1 += " "

    return str1



def get_chunk(chunked):
    str1 = ""
    for j in range(len(chunked)):
        str1 += (chunked[j][0] + " ")
    return str1

def what_whom1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|VBG|DT|POS|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    s = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = "to whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " to whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = "to what"

                str4 = str1 + str2 + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = postprocess(str4)
                # str4 = 'Q.' + str4
                s.append(str4)
    return s


def what_whom2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    list1 = chunk_search(segment_set[num], chunked)
    s = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = " " + chunked[j][0][0] + " whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " " + chunked[j][0][0] + "whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = " " + chunked[j][0][0] + " what"

                str4 = str1 + str2 + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = postprocess(str4)
                # str4 = 'Q.' + str4
                s.append(str4)
    return s


def whose(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<NN.?>*<PRP\$|POS>+<RB.?>*<JJ.?>*<NN.?|VBG|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    s = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            str2 = " whose "
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")
                if chunked[j][1][1] == 'POS':
                    for k in range(2, len(chunked[j])):
                        str2 += (chunked[j][k][0] + " ")
                else:
                    for k in range(1, len(chunked[j])):
                        str2 += (chunked[j][k][0] + " ")

                str4 = str1 + str2 + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = postprocess(str4)
                # str4 = 'Q.' + str4
                s.append(str4)
    return s


def howmany(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<DT>?<CD>+<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    s = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            str2 = " how many "
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                st = get_chunk(chunked[j])
                tok = nltk.word_tokenize(st)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(st, chunked1)
                z = ""

                for k in range(len(chunked1)):
                    if k in list2:
                        z += get_chunk(chunked1[k])

                str4 = str1 + str2 + z + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = postprocess(str4)
                # str4 = 'Q.' + str4
                s.append(str4)
    return s


def howmuch_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<\$>?<CD>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    s = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            str2 = " how much "
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                str2 = chunked[j][0][0] + str2
                str4 = str1 + str2 + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = postprocess(str4)
                # str4 = 'Q.' + str4
                s.append(str4)
    return s


def whom_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|VBG|DT|POS|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = " to whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):

                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " to whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = "to what "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)
                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3


def whom_2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = " " + chunked[j][0][0] + " whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " " + chunked[j][0][0] + " whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = " " + chunked[j][0][0] + " what "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)
                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3


def whom_3(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<VB.?|MD|RP>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = " whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " what "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " what time "
                            else:
                                str2 = " what "

                strx = get_chunk(chunked[j])
                tok = nltk.word_tokenize(strx)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<VB.?|MD>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                strx = get_chunk(chunked1[0])

                str1 += strx

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)

                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3


def whose(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<DT|NN.?>*<PRP\$|POS>+<RB.?>*<JJ.?>*<NN.?|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for i in range(len(chunked)):
            if i in list1:
                str1 = ""
                str3 = ""
                str2 = ""
                for k in range(i):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                str1 += " whose "

                for k in range(i + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[i][1][1] == 'POS':
                    for k in range(2, len(chunked[i])):
                        str2 += (chunked[i][k][0] + " ")

                if chunked[i][0][1] == 'PRP$':
                    for k in range(1, len(chunked[i])):
                        str2 += (chunked[i][k][0] + " ")

                str2 = str1 + str2 + str3
                str4 = ""

                for l in range(0, len(segment_set)):
                    if l < num:
                        str4 += (segment_set[l] + ",")
                    if l > num:
                        str2 += ("," + segment_set[l])
                str2 = str4 + str2
                str2 += '?'
                str2 = postprocess(str2)
                # str2 = 'Q.' + str2
                list3.append(str2)

    return list3


def what_to_do(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<VB|VBP|RP>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT>*}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                ls = get_chunk(chunked[j])
                tok = nltk.word_tokenize(ls)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked2 = chunkparser.parse(tag)
                lis = chunk_search(ls, chunked2)
                if len(lis) != 0:
                    x = lis[len(lis) - 1]
                    ls1 = get_chunk(chunked2[x])
                    index = ls.find(ls1)
                    str2 = " " + ls[0:index]
                else:
                    str2 = " to do "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)
                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    if chunked2[j][1][1] == 'PRP':
                        tr = " whom "
                    else:
                        for x in range(len(chunked[j])):
                            if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                    chunked[j][x][1] == "NN"):
                                break

                        for x1 in range(len(ner)):
                            if ner[x1][0] == chunked[j][x][0]:
                                if ner[x1][1] == "PERSON":
                                    tr = " whom "
                                elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                    tr = " where "
                                elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                    tr = " when "
                                else:
                                    tr = " what "

                    st = str5 + tr + str4 + str2 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3


def who(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(list1)):
            m = list1[j]
            str1 = ""
            for k in range(m + 1, len(chunked)):
                if k in list1:
                    str1 += get_chunk(chunked[k])
                else:
                    str1 += (chunked[k][0] + " ")

            str2 = get_chunk(chunked[m])
            tok = nltk.word_tokenize(str2)
            tag = nltk.pos_tag(tok)

            for m11 in range(len(tag)):
                if tag[m11][1] == 'NNP' or tag[m11][1] == 'NNPS' or tag[m11][1] == 'NNS' or tag[m11][1] == 'NN':
                    break
            s11 = ' who '
            for m12 in range(len(ner)):
                if ner[m12][0] == tag[m11][0]:
                    if ner[m12][1] == 'LOC':
                        s11 = ' which place '
                    elif ner[m12][1] == 'ORG':
                        s11 = ' who '
                    elif ner[m12][1] == 'DATE' or ner[m12][1] == 'TIME':
                        s11 = ' what time '
                    else:
                        s11 = ' who '

            gram = r"""chunk:{<RB.?>*<VB.?|MD|RP>+}"""
            chunkparser = nltk.RegexpParser(gram)
            chunked1 = chunkparser.parse(tag)

            list2 = chunk_search(str2, chunked1)
            if len(list2) != 0:
                str2 = get_chunk(chunked1[list2[0]])
                str2 = s11 + str2
                for k in range(list2[0] + 1, len(chunked1)):
                    if k in list2:
                        str2 += get_chunk(chunked[k])
                    else:
                        str2 += (chunked[k][0] + " ")
                str2 += (" " + str1)

                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    if tok_1[h] == "am":
                        str2 += " is "
                    else:
                        str2 += (tok_1[h] + " ")

                for l in range(num + 1, len(segment_set)):
                    str2 += ("," + segment_set[l])
                str2 += '?'

                str2 = postprocess(str2)
                # str2 = 'Q.' + str2
                list3.append(str2)

    return list3


def howmuch_2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<\$>*<CD>+<MD>?<VB|VBD|VBG|VBP|VBN|VBZ|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(list1)):
            m = list1[j]
            str1 = ""
            for k in range(m + 1, len(chunked)):
                if k in list1:
                    str1 += get_chunk(chunked[k])
                else:
                    str1 += (chunked[k][0] + " ")

            str2 = get_chunk(chunked[m])
            tok = nltk.word_tokenize(str2)
            tag = nltk.pos_tag(tok)
            gram = r"""chunk:{<RB.?>*<VB.?|MD|RP>+}"""
            chunkparser = nltk.RegexpParser(gram)
            chunked1 = chunkparser.parse(tag)
            s11 = ' how much '

            list2 = chunk_search(str2, chunked1)
            if len(list2) != 0:
                str2 = get_chunk(chunked1[list2[0]])
                str2 = s11 + str2
                for k in range(list2[0] + 1, len(chunked1)):
                    if k in list2:
                        str2 += get_chunk(chunked[k])
                    else:
                        str2 += (chunked[k][0] + " ")
                str2 += (" " + str1)

                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    if tok_1[h] == "am":
                        str2 += " is "
                    else:
                        str2 += (tok_1[h] + " ")

                for l in range(num + 1, len(segment_set)):
                    str2 += ("," + segment_set[l])
                str2 += '?'

                str2 = postprocess(str2)
                # str2 = 'Q.' + str2
                list3.append(str2)

    return list3


def howmuch_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<\$>?<CD>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                str2 = ' ' + chunked[j][0][0] + ' how much '

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)
                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3


def howmuch_3(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<MD>?<VB|VBD|VBG|VBP|VBN|VBZ>+<IN|TO>?<PRP|PRP\$|NN.?>?<\$>*<CD>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    list1 = chunk_search(segment_set[num], chunked)
    list3 = []

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                strx = get_chunk(chunked[j])
                tok = nltk.word_tokenize(strx)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<MD>?<VB|VBD|VBG|VBP|VBN|VBZ>+<IN|TO>?<PRP|PRP\$|NN.?>?}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                strx = get_chunk(chunked1[0])
                str1 += (" " + strx)

                str2 = ' how much '

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                list2 = chunk_search(str1, chunked1)

                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 = verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3

                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = postprocess(st)
                    # st = 'Q.' + st
                    list3.append(st)

    return list3



def chunk_search(segment, chunked):
    m = len(chunked)
    list1 = []
    for j in range(m):
        if (len(chunked[j]) > 2 or len(chunked[j]) == 1):
            list1.append(j)
        if (len(chunked[j]) == 2):
            try:
                str1 = chunked[j][0][0] + " " + chunked[j][1][0]
            except Exception:
                pass
            else:
                if (str1 in segment) == True:
                    list1.append(j)
    return list1

def segment_identify(sen):
    segment_set = sen.split(",")
    return segment_set


def clause_identify(segment):
    tok = nltk.word_tokenize(segment)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?|VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    flag = 0
    for j in range(len(chunked)):
        if (len(chunked[j]) > 2):
            flag = 1
        if (len(chunked[j]) == 2):
            try:
                str1 = chunked[j][0][0] + " " + chunked[j][1][0]
            except Exception:
                pass
            else:
                if (str1 in segment) == True:
                    flag = 1
        if flag == 1:
            break

    return flag


def verbphrase_identify(clause):
    tok = nltk.word_tokenize(clause)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    str1 = ""
    str2 = ""
    str3 = ""
    list1 = chunk_search(clause, chunked)
    if len(list1) != 0:
        m = list1[len(list1) - 1]
        for j in range(len(chunked[m])):
            str1 += chunked[m][j][0]
            str1 += " "

    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked1 = chunkparser1.parse(tag1)

    list2 = chunk_search(str1, chunked1)
    if len(list2) != 0:

        m = list2[0]
        for j in range(len(chunked1[m])):
            str2 += (chunked1[m][j][0] + " ")

    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<VB.?|MD|RP>+}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked2 = chunkparser1.parse(tag1)

    list3 = chunk_search(str1, chunked2)
    if len(list3) != 0:

        m = list3[0]
        for j in range(len(chunked2[m])):
            str3 += (chunked2[m][j][0] + " ")

    X = ""
    str4 = ""
    st = nltk.word_tokenize(str3)
    if len(st) > 1:
        X = st[0]
        s = ""
        for k in range(1, len(st)):
            s += st[k]
            s += " "
        str3 = s
        str4 = X + " " + str2 + str3

    if len(st) == 1:
        tag1 = nltk.pos_tag(st)
        if tag1[0][0] != 'are' and tag1[0][0] != 'were' and tag1[0][0] != 'is' and tag1[0][0] != 'am':
            if tag1[0][1] == 'VB' or tag1[0][1] == 'VBP':
                X = 'do'
            if tag1[0][1] == 'VBD' or tag1[0][1] == 'VBN':
                X = 'did'
            if tag1[0][1] == 'VBZ':
                X = 'does'
            str4 = X + " " + str2 + str3
        if (tag1[0][0] == 'are' or tag1[0][0] == 'were' or tag1[0][0] == 'is' or tag1[0][0] == 'am'):
            str4 = tag1[0][0] + " " + str2

    return str4


def subjectphrase_search(segment_set, num):
    str2 = ""
    for j in range(num - 1, 0, -1):
        str1 = ""
        flag = 0
        tok = nltk.word_tokenize(segment_set[j])
        tag = nltk.pos_tag(tok)
        gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
        chunkparser = nltk.RegexpParser(gram)
        chunked = chunkparser.parse(tag)

        list1 = chunk_search(segment_set[j], chunked)
        if len(list1) != 0:
            m = list1[len(list1) - 1]
            for j in range(len(chunked[m])):
                str1 += chunked[m][j][0]
                str1 += " "

            tok1 = nltk.word_tokenize(str1)
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            list2 = chunk_search(str1, chunked1)
            if len(list2) != 0:
                m = list2[len(list2) - 1]
                for j in range(len(chunked1[m])):
                    str2 += (chunked1[m][j][0] + " ")
                flag = 1

        if flag == 0:
            tok1 = nltk.word_tokenize(segment_set[j])
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            list2 = chunk_search(str1, chunked1)
            st = nltk.word_tokenize(segment_set[j])
            if len(chunked1[list2[0]]) == len(st):
                str2 = segment_set[j]
                flag = 1

        if flag == 1:
            break

    return str2


def postprocess(string):
    tok = nltk.word_tokenize(string)
    tag = nltk.pos_tag(tok)

    str1 = tok[0].capitalize()
    str1 += " "
    if len(tok) != 0:
        for i in range(1, len(tok)):
            if tag[i][1] == "NNP":
                str1 += tok[i].capitalize()
                str1 += " "
            else:
                str1 += tok[i].lower()
                str1 += " "
        tok = nltk.word_tokenize(str1)
        str1 = ""
        for i in range(len(tok)):
            if tok[i] == "i" or tok[i] == "we":
                str1 += "you"
                str1 += " "
            elif tok[i] == "my" or tok[i] == "our":
                str1 += "your"
                str1 += " "
            elif tok[i] == "your":
                str1 += "my"
                str1 += " "
            elif tok[i] == "you":
                if i - 1 >= 0:
                    to = nltk.word_tokenize(tok[i - 1])
                    ta = nltk.pos_tag(to)
                    # print ta
                    if ta[0][1] == 'IN':
                        str1 += "me"
                        str1 += " "
                    else:
                        str1 += "i"
                        str1 += " "
                else:
                    str1 += "i "

            elif tok[i] == "am":
                str1 += "are"
                str1 += " "
            else:
                str1 += tok[i]
                str1 += " "

    return str1

def hNvalidation(sentence):
    flag = 1

    Length = len(sentence)
    if (Length > 4):
        for i in range(Length):
            if (i+4 < Length):
                if (sentence[i]==' ' and sentence[i+1]=='h' and sentence[i+2]==' ' and sentence[i+3]=='N' and sentence[i+4]==' '):
                    flag = 0
    return flag

def nerTagger(nlp, tokenize):
    doc = nlp(tokenize)

    finalList = []
    array = [[]]
    for word in doc:
        array[0] = 0
        for ner in doc.ents:
            if (ner.text == word.text):
                finalList.append((word.text, ner.label_))
                array[0] = 1
        if (array[0] == 0):
            finalList.append((word.text, 'O'))

    return finalList


class QuestionGenerator():
    def parse_text(self, sentence):
        nlp.add_pipe(Sentencizer())
        singleSentences = sentence.split(".")
        questionsList = []
        if len(singleSentences) != 0:
            for i in range(len(singleSentences)):
                segmentSets = singleSentences[i].split(",")

                ner = nerTagger(nlp, singleSentences[i])

                if (len(segmentSets)) != 0:
                    for j in range(len(segmentSets)):
                        try:
                            questionsList += howmuch_2(segmentSets, j, ner)
                        except Exception:
                            pass
                        if clause_identify(segmentSets[j]) == 1:
                            try:
                                questionsList += whom_1(segmentSets, j, ner)
                            except Exception:
                                print("Excep")
                                pass
                            try:
                                questionsList += whom_2(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += whom_3(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += whose(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += what_to_do(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += who(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += howmuch_1(segmentSets, j, ner)
                            except Exception:
                                pass
                            try:
                                questionsList += howmuch_3(segmentSets, j, ner)
                            except Exception:
                                pass


                            else:
                                try:
                                    s = subjectphrase_search(segmentSets, j)
                                except Exception:
                                    pass

                                if len(s) != 0:
                                    segmentSets[j] = s + segmentSets[j]
                                    try:
                                        questionsList += whom_1(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whom_2(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whom_3(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += whose(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += what_to_do(segmentSets, j, ner)
                                    except Exception:
                                        pass
                                    try:
                                        questionsList += who(segmentSets, j, ner)
                                    except Exception:
                                        pass

                                    else:
                                        try:
                                            questionsList += what_whom1(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += what_whom2(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += whose(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += howmany(segmentSets, j, ner)
                                        except Exception:
                                            pass
                                        try:
                                            questionsList += howmuch_1(segmentSets, j, ner)
                                        except Exception:
                                            pass

                questionsList.append('\n')
        return questionsList


    def all_questions(self, str):
        count = 0
        out = ""

        for i in range(len(str)):
            count = count + 1
            print("%d) %s" % (count, str[i]))
    
    def filtered_questions(self, str):
        count = 0
        ques = []
        for i in range(len(str)):
            if (len(str[i]) >= 3):
                if (hNvalidation(str[i]) == 1):
                    if ((str[i][0] == 'W' and str[i][1] == 'h') or (str[i][0] == 'H' and str[i][1] == 'o') or (
                            str[i][0] == 'H' and str[i][1] == 'a')):
                        WH = str[i].split(',')
                        if (len(WH) == 1):
                            str[i] = str[i][:-1]
                            str[i] = str[i][:-1]
                            str[i] = str[i][:-1]
                            str[i] = str[i] + "?"
                            if str[i] not in ques:
                                count = count + 1
                            else:
                                continue
                            ques.append(str[i])
                        
        return ques

def get_questions(input_text):
    ques_generator = QuestionGenerator()
    print(input_text)
    all_question = ques_generator.parse_text(input_text)
    print("all_ques",all_question)
    filter_question = ques_generator.filtered_questions(all_question)
    print(filter_question)
    return filter_question


