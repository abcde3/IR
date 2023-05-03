#  建索引
import jieba
import math
import json


class Index:
    def __init__(self, filePath):
        self.filePath = filePath
        self.Index = {}  # 不带词频
        self.invertIndex = {}  # 不带词频
        self.indexCount = {}
        self.finalIndex = {}
        self.finalInvertIndex = {}

    def getPreIndex(self):
        with open(self.filePath, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines:
            if line == '':
                continue
            pageInfos = line.split("\t\t")
            pageId = pageInfos[0]
            # pageTitle = pageInfos[1]
            # pageLink = pageInfos[2]
            with open(pageId, 'r', encoding='utf-8') as f:
                content = f.read()
            wordList = jieba.cut_for_search(content)
            # 文档:关键词
            self.Index[pageId] = set()
            # 关键词:文档号
            # 建立倒排索引
            for word in wordList:
                if word == '': continue
                #
                self.Index[pageId].add(word)
                if word not in self.invertIndex:
                    self.invertIndex[word] = set()
                    self.invertIndex[word].add(pageId)
                else:
                    self.invertIndex[word].add(pageId)
                    # print(self.invertIndex[word])
                # 统计出现频率
                if word + '|' + pageId not in self.indexCount:
                    self.indexCount[word + '|' + pageId] = 1
                else:
                    tmp = self.indexCount[word + '|' + pageId]
                    self.indexCount[word + '|' + pageId] = tmp + 1

    def getFinalIndex(self):
        for k, v in self.Index.items():
            self.finalIndex[k] = []
            for word in v:
                wordCount = self.indexCount[word + '|' + k]

                self.finalIndex[k].append(
                    (word, wordCount)
                )
        # key为word
        for k, v in self.invertIndex.items():
            # print(k)
            self.finalInvertIndex[k] = []
            for pageId in v:
                # print(k + '|' + pageId in self.indexCount)
                wordCount = self.indexCount[k + '|' + pageId]
                self.finalInvertIndex[k].append((pageId, wordCount))

    def saveToFile(self):
        with open('index', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.finalIndex, indent=2, ensure_ascii=False))
        with open('invertIndex', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.finalInvertIndex, indent=2, ensure_ascii=False))

    def do(self):
        self.getPreIndex()
        self.getFinalIndex()
        self.saveToFile()


if __name__ == '__main__':
    i = Index("docs.txt")
    i.do()
    pass
