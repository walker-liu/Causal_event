# -*- coding: utf-8 -*-
'''
Created on 2018年11月17日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import re
import jieba.posseg as pseg
from pyltp import SentenceSplitter
from sentence_parser import LtpParser
import os
from pymongo import MongoClient
import codecs
import threading
import pandas as pd
class CausalityExractor():
    def __init__(self):
        pass

    '''1由果溯因配套式'''
    def ruler1(self, sentence): 
        '''
        conm2:〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        '''
        a=[[],0]
        datas = list()
        word_pairs =[['之?所以', '因为'], ['之?所以', '由于'], ['之?所以', '缘于']]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)' % (word[0], word[1]))#将句子中的词和词性进行了拼接
#             print(sentence)
            result1 = pattern.findall(sentence)
            data = dict()
            if result1:
                a=[word,1]
                break
        return a
            

    def ruler10(self, sentence): 
        '''
        conm2:〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        '''
        datas = list()
        word_pairs =[['起','作用'], ['是','原因'],['是','目的']]
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'(%s)/[v]+\s(.*)(%s)/[n]+\s(.*)' % (word[0],word[1]))#将句子中的词和词性进行了拼接
#             print(sentence)
            
            result = pattern.findall(sentence)
            if result:
#                 print(sentence)
                a=[word,1]
                break
        return a
    '''2由因到果配套式'''
    def ruler2(self,sentence):
        '''
        conm1:〈因为,从而〉、〈因为,为此〉、〈既[然],所以〉、〈因为,为此〉、〈由于,为此〉、〈只有|除非,才〉、〈由于,以至[于]>、〈既[然],却>、
        〈如果,那么|则〉、<由于,从而〉、<既[然],就〉、〈既[然],因此〉、〈如果,就〉、〈只要,就〉〈因为,所以〉、 <由于,于是〉、〈因为,因此〉、
         <由于,故〉、 〈因为,以致[于]〉、〈因为,因而〉、〈由于,因此〉、<因为,于是〉、〈由于,致使〉、〈因为,致使〉、〈由于,以致[于] >
         〈因为,故〉、〈因[为],以至[于]>,〈由于,所以〉、〈因为,故而〉、〈由于,因而〉
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        '''
        datas = list()
        word_pairs =[['因为', '从而'], ['因为', '为此'], ['既然?', '所以'],
                    ['因为', '为此'], ['由于', '为此'], ['除非', '才'],
                    ['只有', '才'], ['由于', '以至于?'], ['既然?', '却'],
                    ['如果', '那么'], ['如果', '则'], ['由于', '从而'],
                    ['既然', '就?'], ['既然?', '因此'], ['如果', '就'],
                    ['只要', '就'], ['因为', '所以'], ['由于', '于是'],
                    ['因为', '因此'], ['由于', '故'], ['因为', '以致于?'],
                    ['因为', '以致'], ['因为', '因而'], ['由于', '因此'],
                    ['因为', '于是'], ['由于', '致使'], ['因为', '致使'],
                    ['由于', '以致于?'], ['因为', '故'], ['因为?', '以至于?'],
                    ['由于', '所以'], ['因为', '故而'], ['由于', '因而'],['因为','所以']]
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c|d]+\s(.*)' % (word[0], word[1]))
#             print(pattern)
#             print(sentence)
            result1 = pattern.findall(sentence)
#             print(result)
            data = dict()
            if result1:
                a=[word,1]
                break
        return a
               
    '''3由因到果居中式明确'''
    def ruler3(self, sentence):
        '''
        cons2:于是、所以、故、致使、以致[于]、因此、以至[于]、从而、因而、是因为
        cons2_model:{Cause},<Conj...>{Effect}
        '''
#         print(sentence)
        pattern1 = re.compile(r'(.*)[,，]+.*(于是|所以|故|致使|以致于?|因此|以至于?|从而|因而)/[p|c]+\s(.*)')
        result1 = pattern1.findall(sentence)
        data = dict()
        if result1:
            return [result1[0][1],1]
        else:
            return [[],0]
        
    '''4由因到果居中式精确'''
    def ruler4(self, sentence):#删除‘引导’、‘引入’,'决定','作用','|指引'，|推进\s+
        '''
        verb1:牵动、导向、使动、导致、勾起、指引、使、予以、产生、促成、造成、造就、促使、酿成、
            引发、渗透、促进、引起、诱导、引来、促发、引致、诱发、推进、诱致、推动、招致、影响、致使、滋生、归于、
            作用、使得、决定、攸关、令人、引出、浸染、带来、挟带、触发、关系、渗入、诱惑、波及、诱使，满足
        verb1_model:{Cause},<Verb|Adverb...>{Effect}
        '''
        pattern = re.compile(r'.*[,|，](.*)(预示着|促进|导致|将会|标志着|满足|意味着|推进|引导|牵动|已致|导向|使动|导致|使|予以|产生|促成|造成|造就|促使|酿成|引发|渗透|促进|引起|诱导|引来|促发|引致|诱发|诱致|推动|招致|影响|致使|滋生|归于|使得|攸关|令人|引出|浸染|带来|挟带|触发|关系|渗入|诱惑|波及|诱使)/[d|v]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict() 
        
        if result:
            return [result[0][1],1]
        else:
            return [[],0]
    '''5由因到果前端式模糊'''
    def ruler5(self, sentence):#去掉'按照'
        '''
        prep:为了、依据、为、按照、因[为]、按、依赖、照、比、凭借、由于
        prep_model:<Prep...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(为了|依据|因为|因|按|依赖|凭借|由于)/[p|c]+\s(.*)[,，]+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
                return [result[0][0],1]
        else:
                return [[],0]

    '''6由因到果居中式模糊'''
    def ruler6(self, sentence):
        '''
        adverb:以免、以便、为此、才
        adverb_model:{Cause},<Verb|Adverb...>{Effect}
        '''
        pattern = re.compile(r'(.*)(以免|以便|为此|才)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]

    '''7由因到果前端式精确'''
    def ruler7(self, sentence):#既然?
        '''
        cons1:既[然]、因[为]、如果、由于、只要
        cons1_model:<Conj...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(因|因为|如果|由于|只要)/[p|c]+\s(.*)+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][0],1]
        else:
            return [[],0]
    '''8由果溯因居中式模糊'''
    def ruler8(self, sentence):
        '''
        3
        verb2:根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、源于、根源于、立足[于]
        verb2_model:{Effect}<Prep...>{Cause}
        '''

        pattern = re.compile(r'(.*)(根源于|取决|来源于|出于|取决于|缘于|在于|出自|起源于|来自|发源于|发自|源于|根源于|立足|立足于)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]
    '''9由果溯因居端式精确'''
    def ruler9(self, sentence):
        '''
        cons3:因为、由于
        cons3_model:{Effect}<Conj...>{Cause}
        '''
        pattern = re.compile(r'(.*)是?\s(因为|由于)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]

    '''抽取主函数'''
    def recognise_causality(self, sentence):
        infos = list()
      #  print(sentence)
        if self.ruler1(sentence)[1]:
            infos.append(self.ruler1(sentence)[0])
        elif self.ruler2(sentence)[1]:
            infos.append(self.ruler2(sentence)[0])
        elif self.ruler3(sentence)[1]:
            infos.append(self.ruler3(sentence)[0])
        elif self.ruler4(sentence)[1]:
            infos.append(self.ruler4(sentence)[0])
        elif self.ruler5(sentence)[1]:
            infos.append(self.ruler5(sentence)[0])
        elif self.ruler6(sentence)[1]:
            infos.append(self.ruler6(sentence)[0])
        elif self.ruler7(sentence)[1]:
            infos.append(self.ruler7(sentence)[0])
        elif self.ruler8(sentence)[1]:
            infos.append(self.ruler8(sentence)[0])
        elif self.ruler9(sentence)[1]:
            infos.append(self.ruler9(sentence)[0])
        elif self.ruler10(sentence)[1]:
            infos.append(self.ruler10(sentence)[0])
        else:
            return[[],0]
        return [infos,1]

    '''抽取主控函数'''
    def extract_main(self, content):
    
        for sent in set(content):
            sent1 = ' '.join([word.word + '/' + word.flag for word in pseg.cut(sent)])
#             print(sent1)
            result = self.recognise_causality(sent1)
#             print(sent)
#             print(result)
#             print(result)
            if result[1]:
                mu = threading.Lock()
                with codecs.open('../data/causality_sentences.txt','a',encoding='utf-8') as f:
                    if  mu.acquire(True): #确保文件写入成功
                        f.write(sent.replace('\n','')+'  '+str(result[0]).replace('[','').replace(']','')+'\n')
                        f.flush()
                        os.fsync(f)
                        f.close()
                        mu.release()
#                 return (sent,result[0])
            else:
                with codecs.open('../data/other_sentences.txt','a',encoding='utf-8') as f2:
                    f2.write(sent) 
#         return datas

    '''文章分句处理'''
    def process_content(self, content):
        return [sentence for sentence in SentenceSplitter.split(content) if sentence]

    '''切分最小句'''
    def fined_sentence(self, sentence):
        return re.split(r'[？！；]', sentence)


'''测试'''
def test():
    content1 = """
     截至2008年9月18日12时，5·12汶川地震共造成69227人死亡，374643人受伤，17923人失踪，是中华人民共和国成立以来破坏力最大的地震，也是唐山大地震后伤亡最严重的一次地震。
     """
    content2 = '''
     2015年1月4日下午3时39分左右，贵州省遵义市习水县二郎乡遵赤高速二郎乡往仁怀市方向路段发生山体滑坡，发生规模约10万立方米,导致多辆车被埋，造成交通双向中断。此事故引起贵州省委、省政府的高度重视，省长陈敏尔作出指示，要求迅速组织开展救援工作，千方百计实施救援，减少人员伤亡和财物损失。遵义市立即启动应急救援预案，市应急办、公安、交通、卫生等救援力量赶赴现场救援。目前，灾害已造成3人遇难1人受伤，一辆轿车被埋。
     当地时间2010年1月12日16时53分，加勒比岛国海地发生里氏7.3级大地震。震中距首都太子港仅16公里，这个国家的心脏几成一片废墟，25万人在这场骇人的灾难中丧生。此次地震中的遇难者有联合国驻海地维和部队人员，其中包括8名中国维和人员。虽然国际社会在灾后纷纷向海地提供援助，但由于尸体处理不当导致饮用水源受到污染，灾民喝了受污染的水后引发霍乱，已致至少2500多人死亡。
     '''
    content3 = '''
     American Eagle,四季度符合预期 华尔街对其毛利率不满导致股价大跌。
     我之所以考试没及格，是因为我没有好好学习。
     因为天晴了，所以我今天晒被子。
     因为下雪了，所以路上的行人很少。
     我没有去上课是因为我病了。
     因为早上没吃的缘故，所以今天还没到放学我就饿了.
     因为小华身体不舒服，所以她没上课间操。
     因为我昨晚没睡好，所以今天感觉很疲倦。
     因为李明学习刻苦，所以其成绩一直很优秀。
     雨水之所以不能把石块滴穿，是因为它没有专一的目标，也不能持之以恒。
     他之所以成绩不好，是因为他平时不努力学习。
     你之所以提这个问题，是因为你没有学好关联词的用法。
     减了税,因此怨声也少些了。
     他的话引得大家都笑了，室内的空气因此轻松了很多。
     他努力学习，因此通过了考试。
     既然明天要下雨，就不要再出去玩。
     既然他还是那么固执，就不要过多的与他辩论。
     既然别人的事与你无关，你就不要再去过多的干涉。
     既然梦想实现不了，就换一个你自己喜欢的梦想吧。
     既然别人需要你，你就去尽力的帮助别人。
     既然生命突显不出价值，就去追求自己想要的生活吧。
     既然别人不尊重你，就不要尊重别人。 因果复句造句
     既然题目难做，就不要用太多的时间去想，问一问他人也许会更好。
     既然我们是学生，就要遵守学生的基本规范。
深化体制改革，推进经济增长。
  活着是吃饭的重要原因。
     '''
    extractor = CausalityExractor()
#      path = r'E:\\Causal_events\\forum50_articles'
#      #sentence="我爱你,中国"
#      files = os.listdir(path)
#      #print(files)
#      for file in files :
#          pathname = os.path.join(path, file)
#          print(file)
#          #准确获取一个txt的位置，利用字符串的拼接
#          txt_path = pathname.encode('utf-8')
#          #把结果保存了在contents中
#          with codecs.open(txt_path,'rb',encoding='utf-8') as f1:
#              lines = f1.readlines()
#          for line in lines:
#              line+=line   
    datas = extractor.extract_main(content3)
#     for data in datas:
#         print('******'*4)
#         print('cause', ''.join([word.split('/')[0] for word in data['cause'].split(' ') if word.split('/')[0]]))
#         print('tag', data['tag'])
#         print('effect', ''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]]))
# test()
if __name__ == '__main__':
    extractor = CausalityExractor()
    with codecs.open('E:\Causal_events\sina_economics_newline\sina_text_line.txt','r',encoding='utf-8') as f1:
        context=f1.readlines()
    extractor.extract_main(context)
    
#     mongo_con=MongoClient('172.20.69.233', 27017)
#     db=mongo_con.Causal_event
#     collection=db.forum50_articles_causality_extract_1
#     extractor = CausalityExractor()
#     path = r'E:\\Causal_events\\sina_economics_articles'
#     #sentence="我爱你,中国"
#     files = os.listdir(path)
#     for file in files :
#         pathname = os.path.join(path, file)
#         print(file)
#         #准确获取一个txt的位置，利用字符串的拼接
#         txt_path = pathname.encode('utf-8')
#         #把结果保存了在contents中
#         with codecs.open(txt_path,'r',encoding='utf8',errors='strict') as f1:
#             try:
#                 lines = f1.readlines()
#             except UnicodeDecodeError:#含有gb2312编码
#                 f1.encoding='gb2312'
#                 lines =f1.readlines()
#             line = str([line.strip() for line in lines]).replace('[','').replace(']','').replace('\\u3000', '')
#         datas = extractor.extract_main(line)
#         biglist=[]
#         for data in datas:
#             cause=''.join([word.split('/')[0] for word in data['cause'].split(' ') if word.split('/')[0]])
#             tag=data['tag']
#             effect=''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]])
#             yuanju=data['原句']
#             if len(cause)>3 and len(effect)>3:
# #                 collection.insert({'栏目':'sina财经经济评论','file':file.replace('.txt',''),'原句':yuanju,'cause':cause,'tag':tag,'effect':effect})
#                 print(yuanju)
#                 print('tag', data['tag'])
#                 print('effect', ''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]]))
#                 print('cause:'+cause)
# #                 biglist.append(['forum50财经经济评论',file.replace('.txt',''),cause,tag,effect])
#             else:
#                 continue
#         list2=[]#去重
#         for i in biglist:
#             if i not in list2:
#                 list2.append(i)
#         name=['栏目','文件名','原因','标签','结果']
#         article_anaysis=pd.DataFrame(columns=name,data=list2)
#         article_anaysis.to_csv('E:\\Causal_events\\forum50_articles_causality_extract\\'+file.replace('.txt','.csv'),encoding='utf-8') 
        
