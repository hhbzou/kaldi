# coding=utf-8
from sys import argv
import os

wantTestClassList = ["None", "jixubofang",  "shangyishou","shengyindayidian", "shengyinxiaoyidian", "xiayishou", "zantingbofang"]

#以下用于统计各类别准确率
expectClassCountDict = {}
realityClassCountDict = {}
for i in wantTestClassList:
    expectClassCountDict[i] = 0
    realityClassCountDict[i] = 0

#以下用于统计各语速准确率
expectSpeakSpeed = ["fast", "norm", "slow", "None"]
expectSpeakSpeedCountDict = {}
realitySpeakSpeedCountDict = {}
for i in expectSpeakSpeed:
    expectSpeakSpeedCountDict[i] = 0
    realitySpeakSpeedCountDict[i] = 0

#以下用于统计各年龄段准确率
expectAge = ["f1t12", "f13t18", "f19t28", "f29t49", "f50t80", "None"]
expectAgeCountDict = {}
realityAgeCountDict = {}
for i in expectAge:
    expectAgeCountDict[i] = 0
    realityAgeCountDict[i] = 0

#以下用于统计各性别准确率
expectSpeakGender = ["male", "female", "None"]
expectGenderCountDict = {}
realityGenderCountDict = {}
for i in expectSpeakGender:
    expectGenderCountDict[i] = 0
    realityGenderCountDict[i] = 0

#混淆矩阵
wantTestClassIndexDict = {}
cnt = 0
for i in wantTestClassList:
    wantTestClassIndexDict[i] = cnt
    cnt = cnt + 1

confusionMatrix = []
for i in range(len(wantTestClassList)):
    tmpPerRow = []
    for i in range(len(wantTestClassList)):
        tmpPerRow.append(0)
    confusionMatrix.append(tmpPerRow)

def getSpeakSpeed(currentFile):
    if "norm" in currentFile:
        return "norm"
    if "fast" in currentFile:
        return "fast"
    if "slow" in currentFile:
        return "slow"
    return "None"

def getGender(currentFile):
    if "-m-" in currentFile:
        return "male"
    if "-f-" in currentFile:
        return "female"
    return "None"

def getAge(currentFile):
    try:
       age = int(currentFile.split("-")[4])
       if age >= 1 and age <= 12:
            return "f1t12"
       if age >= 13 and age <= 18:
            return "f13t18"
       if age >= 19 and age <= 28:
            return "f19t28"
       if age >= 29 and age <= 49:
            return "f29t49"
       if age >= 50 and age <= 80:
            return "f50t80"
       return "None"
    except:
        return "None"

def getAdddress(currentFile, expectAdress):
    try:
       addrsss = currentFile.split('-')[5]
       if addrsss not in expectAdress:
           return "None"
       return addrsss
    except:
        return "None"

def printSingleItem(wantList, realityCountDict, expectCountDict, item):
    for i in wantList:
        if i == "None":
            continue
        try:
            acc = str(realityCountDict[i] / expectCountDict[i])
            realityCount = str(realityCountDict[i])
            expectCount = str(expectCountDict[i])
            print(item + i + " 准确率:" + acc + " 正确识别数:" + realityCount + " 样本总数:" + expectCount)
        except ZeroDivisionError:
            pass

def printSingleItemForExcel(wantList, realityCountDict, expectCountDict, item, count):
    print(item+ " count:" + str(count))    
    for i in wantList:
            if i == "None":
                continue
            try:
                realityCount = str(realityCountDict[i])
                print(realityCount)
            except ZeroDivisionError:
                pass

def printStatisticsRes(count = 0):
    print("#########################  每类别准确率- START ##########################")
    item = "类别:"
    printSingleItem(wantTestClassList, realityClassCountDict, expectClassCountDict, item)
    print("*************************  每类别准确率-  END  **************************\n")

    print("#########################  不同语速准确率- START ##########################")
    item = "语速:"
    printSingleItem(expectSpeakSpeed, realitySpeakSpeedCountDict, expectSpeakSpeedCountDict, item)
    print("*************************  不同语速准确率-  END  **************************\n")

    print("#########################  不同性别准确率- START ##########################")
    item = "性别:"
    printSingleItem(expectSpeakGender, realityGenderCountDict, expectGenderCountDict, item)
    print("*************************  不同性别准确率-  END  **************************\n")

    print("#########################  不同年龄段准确率- START ##########################")
    item = "年龄段:"
    printSingleItem(expectAge, realityAgeCountDict, expectAgeCountDict, item)
    print("*************************  不同年龄段准确率-  END  **************************\n")

    print("#########################   准确率- START   ##########################")
    realityCount = 0
    expectCount = 0
    for i in wantTestClassList:
        if i == "None":
            continue
        realityCount = realityCount + realityClassCountDict[i]
        expectCount = expectCount + expectClassCountDict[i]
    if expectCount > 0:
        acc = str(realityCount / expectCount)
    else:
        acc = 0
    print("准确率：" + str(acc) + " 正确识别数目:" + str(realityCount) + " 样本总数:" + str(expectCount))
    print("*************************   准确率- END   **************************\n")

    print("#########################  混淆矩阵- START   ##########################")
    for i in range(len(confusionMatrix)):
        print(' '.join((str)(confusionMatrix[i][:])))
    print("#########################  混淆矩阵-  END    ##########################\n")

    item = "类别:"
    printSingleItemForExcel(wantTestClassList, realityClassCountDict, expectClassCountDict, item, count)
    item = "语速:"
    printSingleItemForExcel(expectSpeakSpeed, realitySpeakSpeedCountDict, expectSpeakSpeedCountDict, item, count)
    item = "性别:"
    printSingleItemForExcel(expectSpeakGender, realityGenderCountDict, expectGenderCountDict, item, count)
    item = "年龄段:"
    printSingleItemForExcel(expectAge, realityAgeCountDict, expectAgeCountDict, item, count)
    
    item = "混淆矩阵:"
    print(item + " count:" + str(count))
    for j in range(len(confusionMatrix[0])):
            print(str(wantTestClassList[j]))
            for i in range(len(confusionMatrix)):
                print(str(confusionMatrix[i][j]))

if __name__ == "__main__":
    pyname, wantParseFile = argv
    with open(wantParseFile, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if "Right" in line or "Error" in line:
                rightFlag = False
                if "Right" in line:
                    rightFlag = True
                line = line.split(":")
                fileName = line[-1]
                exceptClass = line[3].split("\t")[0]
                realClass = line[4].split("\t")[0]
                print(fileName, exceptClass, realClass)
                #copy
                currentFile = fileName
                realityClass = realClass
                expectClass = exceptClass
                age = getAge(currentFile)
                speakSpeed = getSpeakSpeed(currentFile)
                gender = getGender(currentFile)
                expectClassCountDict[expectClass] = expectClassCountDict[expectClass] + 1
                expectSpeakSpeedCountDict[speakSpeed] = expectSpeakSpeedCountDict[speakSpeed] + 1
                expectAgeCountDict[age] = expectAgeCountDict[age] + 1
                expectGenderCountDict[gender] = expectGenderCountDict[gender] + 1
                confusionMatrix[wantTestClassIndexDict[expectClass]][wantTestClassIndexDict[realityClass]] = confusionMatrix[wantTestClassIndexDict[expectClass]][wantTestClassIndexDict[realityClass]]  + 1
                if rightFlag:
                   realityClassCountDict[expectClass] = realityClassCountDict[expectClass] + 1
                   realitySpeakSpeedCountDict[speakSpeed] = realitySpeakSpeedCountDict[speakSpeed] + 1
                   realityAgeCountDict[age] = realityAgeCountDict[age] + 1
                   realityGenderCountDict[gender] = realityGenderCountDict[gender] + 1
    printStatisticsRes()

