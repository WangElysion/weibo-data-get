#!python3

# define global argument
import requests
import random
import time,datetime
import pandas as pd
import bs4
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}
url_global = "https://m.weibo.cn/api/container/getIndex"
url_full_text = "https://m.weibo.cn/statuses/show/?id="


def get_global_index(keyword: str, page: int = 1):
    parma = {
        "containerid": "231522type=61&q={}".format(keyword),
        "page_type": "search_all",
        "luicode": "10000011",
        "page": page,
    }
    res = requests.get(url_global, params=parma, headers=headers)
    # res.encoding="unicode_escape"
    # res.encoding("utf-8")
    data = res.json().get("data").get("cards")
    cards_id_url_list = ["{0}{1}".format(
        url_full_text, card.get("mblog").get("bid")) for card in data]
    return cards_id_url_list


def info_get(card_id_url: str):
    res = requests.get(url=card_id_url, headers=headers)
    if res.json() != None:
        data = res.json().get("data")
        card = {
            "微博ID": data.get("user").get("id"),
            "微博名称": data.get("user").get("screen_name"),
            "微博描述": data.get("user").get("description"),
            "创建时间": timetrans(data.get("created_at")),
            "修改时间": timetrans(data.get("edit_at")),
            "发布IP所在地": data.get("region_name"),
            "发布设备": data.get("source"),
            # data.get("status_title"),
            "微博标题": full_text_get(data.get("status_title")),
            "微博正文": full_text_get(data.get("text")),
            # "微博正文链接":data.get("page_info").get("page_url"),
        }
    else:
        print(f"该数据出现问题，返回为空！")
        card = {}
    return card


def full_text_get(text: str):
    soup = bs4.BeautifulSoup(text, "lxml")
    # text_get=str(soup.string)
    # d=re.compile("<.+>")   
    # text_return=d.sub(" ",text_get)
    text_return = "".join(soup.strings)
    return text_return

def timetrans(time_str:str):
    """
    parma:
    :time: the string of time
    # """
    if time_str==None:
        time_return=None
    else:
        time_return=datetime.datetime.strptime(time_str,"%a %b %d %X %z %Y")
        time_return.time
    return time_return

def main():
    card = []
    keyword = "宋慧乔演技感染力"#在此处修改搜索词
    i = 1
    card_len = len(card)
    error=0
    while True:
        try:

            print(f"\r正在获取第{i}页", end="......")
            card_url_list = get_global_index(keyword=keyword, page=i)
            for card_url in card_url_list:
                card.append(info_get(card_url))
                # time.sleep(random.randrange(1,3))
            if card_len == len(card):
               error+=1
               if error>2:
                    print(f"爬取结束！获取{card_len}条数据！")
                    break
            else:
                error=0
                card_len = len(card)
                print(f"已获取{card_len}条数据")
                i += 1
        except Exception as e:
            print(e)

    df = pd.DataFrame(card)
    df["创建时间"]=df["创建时间"].dt.tz_localize(None)
    df["修改时间"]=df["修改时间"].dt.tz_localize(None)
    df.to_excel(
                f"已获取数据/微博数据获取-{keyword}-{time.strftime('%y%m%d',time.localtime())}.xlsx", index=None)


if __name__ == "__main__":

    #   res=requests.get(headers=headers,url=f"{url_full_text}{'Mt0nYj3oC'}")
    #   print(res.status_code)
    main()
