import wordcloud as wc
import jieba,jieba.analyse
import pandas as pd
from stylecloud import gen_stylecloud
import cv2


stop_words=['你','我','了','们','的',"山河四省","是",]
filename="微博数据获取-山河四省-230312.xlsx"
im=cv2.imread("image/azhun.jpg")

def data_import(filename:str):
    """
    :parma
    :filename:待导入的文件名,需为Excel格式
    """
    df=pd.read_excel(f"已获取数据/{filename}")
    text=df["微博正文"].tolist()
    return "".join([str(i) for i in text])
def data_anazyle(text:str):
    wordlist=jieba.lcut_for_search(text)
    result=" ".join(wordlist)

    word_clouds=""
    for word in result:
        if word  not in stop_words:
            word_clouds+=word

    tag=jieba.analyse.extract_tags(sentence=word_clouds, topK=10, withWeight=True)
    return tag,word_clouds
def word_cloud_drawing(text:str):
    WC=wc.WordCloud(
        font_path='msyh.ttc',
        background_color="white",
        width=683,
        height=380,
        max_font_size=100,
        min_font_size=10,
        mask=im
    )
    WC.generate(text)
    WC.to_file(f"词云/{filename.split('.')[0]}.jpg")

def word_cloud_drawing2(text):
    gen_stylecloud(
        text=text,
        font_path="msyh.ttc",
        output_name=(f"词云/{filename.split('.')[0]}.jpg")
    )

if __name__ == '__main__':
    text=data_import(filename=filename)
    tag,word_clouds=data_anazyle(text)
    word_cloud_drawing(word_clouds)