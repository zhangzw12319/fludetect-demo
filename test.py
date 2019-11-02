from langdetect import DetectorFactory
from langdetect import detect

# text = "\u2606\u8b70\u8ad6\u597d\u304d\u306b\u3064\u304d\u6ce8\u610f\u3002\u60aa\u6c17\u306a\u304f\u5c41\u7406\u5c48\u3092\u634f\u306d\u308b\u3088\u3002\u3000\u2606\u8457\u4f5c\u6a29\u6cd5\u618e\u3057\u3067\u52c9\u5f37\u4e2d\u3002\u3000\u2606Follow\u3001Remove\u3001Block\u3001Reply\u3054\u81ea\u7531\u306b\u3002RT\u306f\u5185\u5bb9\u306b\u624b\u3092\u52a0\u3048\u305f\u5834\u5408\u306f\u305d\u306e\u65e8\u306e\u660e\u8a18\u3092\u304a\u9858\u3044\u3057\u307e\u3059(\u7565\u8868\u793a\u3001\u6539\u8868\u793a\u7b49)\u3002\u3000\u2606reply\u3044\u305f\u3060\u3051\u308c\u3070\u3001\u30d5\u30a9\u30ed\u30fc\u8fd4\u3057\u3059\u308b\u3053\u3068\u304c\u3042\u308a\u307e\u3059\uff08\u4e0a\u304b\u3089\u76ee\u7dda\uff09\u3002"
# keywords = ["flu", "health", "phisician", "fever", "cold", "ill", "sick",
#               "cough", "sneeze", "tremble", "medicine", "thermometer",
#               "illness", "headache", "sore throat"]
# DetectorFactory.seed = 0
# print(detect(text))

# text = text.decode()
# word_split = text.split()
# for each_word in keywords:
#     if each_word in word_split:



import json

path=r"F:\twitter13\2009\20091226\20091226-73.json"
with open(path, 'r') as load_f:
    for line in load_f:
        print(line)



