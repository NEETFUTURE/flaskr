# -*- coding: utf-8 -*-
import sys

"""
#########################################################
# #####  ######   ##   #####   ##   #####  #      ######
# #    # #       #  #    #    #  #  #    # #      #
# #    # #####  #    #   #   #    # #####  #      #####
# #    # #      ######   #   ###### #    # #      #
# #    # #      #    #   #   #    # #    # #      #
# #####  ###### #    #   #   #    # #####  ###### ######
#########################################################
IT iS THE MOST SIMPLE SOLUTION FOR YOUR IDEA PROCESS :-)
"""

#-------------------------------------------------------
# Name:        makexmldata
# Author:      geforce forever
# Created:     10/06/2012
# Copyright:   (c) geforce forever 2012
#-------------------------------------------------------

def iterkeys():
    i=1
    while True:
        yield i
        i += 1

def readFilename():
    try:
        if sys.argv[1]:
            f = open(sys.argv[1], "a+")
        return f
    except:
        pass

def makexml(name, **data):

    u"""
    この関数は、引数nameに親の名前(ex.twitter,RSS)を入れ、
    dataにはhiduke="12/25",tenki=u"晴れ"といった感じで引
    数を渡し使用します。改行があります。
    """

    #serach filename from commandline
    f = readFilename()

    #initialize
    key = data.keys()
    save = ""
    save2 = 0
    iterdata = iterkeys()

    #top of the xml data
    save += "<%s>\n" % "data"

    #make any info from parameter:data
    save += "".join(("<type>", "\n", "%s\n" % name, "</type>\n"))
    while save2 != len(key):
        save += "<%s>\n" % key[save2]
        save += "".join((data[key[save2]],"\n"))
        save += "</%s>\n" % key[save2]
        save2 = iterdata.next()
    save += "</data>\n"
    #save += "<%s>\n" % name

    #end of the xml data
    #save += "</%s>\n" % "data"

    #if file is available to use, write data
    if f:
        f.write(save)
        f.write("-----------------------------------------------\n")
        f.close()

    #return save
    return save

def withoutNewline(name, **data):

    u"""
    この関数は、引数nameに親の名前(ex.twitter,RSS)を入れ、
    dataにはhiduke="12/25",tenki=u"晴れ"といった感じで引
    数を渡し使用します。改行がありません。
    """

    #serach filename from commandline
    f = readFilename()

    #initialize
    key = data.keys()
    save = ""
    save2 = 0
    iterdata = iterkeys()

    #top of the xml data
    save += "<%s>\n" % "data"

    #make any info from parameter:data
    save += "".join(("<type>", "%s" % name, "</type>\n"))
    while save2 != len(key):
        save += "<%s>" % key[save2]
        save += data[key[save2]]
        save += "</%s>\n" % key[save2]
        save2 = iterdata.next()
    save += "</data>\n"

    #if file is available to use, write data
    if f:
        f.write(save)
        f.write("-----------------------------------------------\n")
        f.close()

    #return save
    return save


if __name__ == '__main__':

    #with new line in data
    print makexml("twitter",
                    tubuyaki = u"飲酒運転なうｗｗっうぇｗっうぇちょううける",
                    id = "yutori_sedai",
                    hiduke = u"2月12日 月曜日")

    #without new line in data
    print withoutNewline("twitter",
                    tubuyaki = u"飲酒運転なうｗｗっうぇｗっうぇちょううける",
                    id = "yutori_sedai",
                    hiduke = u"2月12日 月曜日")
