# -*- coding: utf-8 -*-
'''
挑选识别不到的音频，按照识别结果，对文件进行分类，将pcm文件转为wav
'''
import os
import time
import logging
import contextlib
import wave

# 相关配置信息
# adb 工具所在绝对路径：

from sys import argv

pyname, audioSavePath = argv

def __matchKeyWord__(id):
    dic_key = {"5":"shangyishou","10":"xiayishou","6":"shengyindayidian",
               "7":"shengyinxiaoyidian","3":"jixubofang","11":"zantingbofang"}
    set_id = {"3","5","7","6","10","11"}
    others = "None"
    if id in set_id:
        return dic_key[id]
    return others

def ExamSingleWav(fN):
    # 完成一首音频的测试，返回测试结果

    cmdStr = "./tdnn_tflite " + fN
    # print(fN)
    ret = os.popen(cmdStr)
    id = "0"
    # time.sleep(1)
    #print(ret.readlines())
    for i in ret.readlines():
        # print(i)
        if "Trigger type:" in i :
            id = i.split(":")[1].strip("\n").strip(" ")
            break
    # print("id is "+ id,"\t",__matchKeyWord__(id))
    return __matchKeyWord__(id)

def Exam(f,fN,expectRes):
    '''
    :param f: 测试wav音频名称
    :param fN:测试wav音频绝对名称
    :param expectRes:
    :return:
    '''

    realRes = ExamSingleWav(fN)

    if realRes == expectRes:
        logging.info("Right\texpect:%s\treal:%s\tfile:%s"%(expectRes,realRes,f))
        return 1
    logging.info("Error\texpect:%s\treal:%s\tfile:%s"%(expectRes,realRes,f))
    print("expect is :" + expectRes,"\t real is :" + realRes)
    return -1

def CountWavTim(fn):
    with contextlib.closing(wave.open(fn, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
    print(wav_length)

def main():
    '''准确率离线测试
    :return:
    '''
    COUNT = 0
    right = 0
    error = 0
    audio_path = "D:/Desktop/模型调测/三米外噪情况分析/SavePcmData3m-0419"
    os.chdir(audio_path)
    for expectRes in os.listdir("./SavePcmData"):
        for f in os.listdir(os.path.join("./SavePcmData",expectRes)):
            fN = os.path.join("./SavePcmData",expectRes,f)
            ret = Exam(f=f,fN=fN,expectRes=expectRes)
            # print(ret)
            COUNT += 1
            if (ret == 1):
                right += 1
            else:
                error += 1
            if (COUNT % 100 == 0):
                print("当前已处理%d个音频"%COUNT)
                print("COUNT", COUNT, "\t", "right", right, "\t", "error", error)
                print("准确率:%f" % (float(right) / float(COUNT)))
                logging.info("COUNT:%d\taccuracy:%f\t"%(COUNT,float(right) / float(COUNT)))
            if (COUNT > 200):
                break
        logging.info("keyWord:%s\t准确率:%f"%(expectRes,(float(right) / float(COUNT))))
        if COUNT > 200:
            break
    print("COUNT",COUNT,"\t","right",right,"\t","error",error)
    print("准确率：%f"%(float(right)/float(COUNT)))
    logging.info("COUNT:%d\taccuracy:%f\t" % (COUNT, (float(right) / float(COUNT))))

def error_wakeup_main():
    '''准确率离线测试
    :return:
    '''
    COUNT = 0
    right = 0
    error = 0
    audio_path = audioSavePath#"../audio_1"
    expectRes = ""
    for expectRes in os.listdir(audio_path):
    # for f in os.listdir(audio_path):
        for f in os.listdir(os.path.join(audio_path,expectRes)):
            fN = os.path.join(audio_path, expectRes, f)
            ret = Exam(f=f,fN=fN,expectRes=expectRes)
            # print(ret)
            COUNT += 1
            if (ret == 1):
                right += 1
            else:
                error += 1
            if (COUNT % 100 == 0):
                print("当前已处理%d个音频"%COUNT)
                print("COUNT", COUNT, "\t", "right", right, "\t", "error", error)
                print("准确率:%f" % (float(right) / float(COUNT)))
                logging.info("COUNT:%d\taccuracy:%f\t"%(COUNT,float(right) / float(COUNT)))
            if (COUNT > 2500):
                break
            logging.info("keyWord:%s\t准确率:%f"%(expectRes,(float(right) / float(COUNT))))
            if COUNT > 2500:
                break
        print("COUNT",COUNT,"\t","right",right,"\t","error",error)
        print("准确率：%f"%(float(right)/float(COUNT)))
        logging.info("COUNT:%d\taccuracy:%f\t" % (COUNT, (float(right) / float(COUNT))))
    print("COUNT",COUNT,"\t","right",right,"\t","error",error)
    print("准确率：%f"%(float(right)/float(COUNT)))
    logging.info("COUNT:%d\taccuracy:%f\t" % (COUNT, (float(right) / float(COUNT))))

def __():
    error_wakeup_main()
logDir = "../log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
curTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
logName = 'log-' + curTime + '.txt'
logging.basicConfig(filename=os.path.join(logDir, logName), level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logging.info("Begin Offline Exam")
logging.info("3m外噪场景pcm流测试-设备端侧代码-20帧一次，sleep时间缩短")
__()
# main()
# ExamSingleWav("4976090-shangyishou-m-fast-11-anhui-057.wav")

# adbPath = "D:\\Desktop\\OFFLINPCM\\adb\\adb.exe"
