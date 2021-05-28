import os
import json
import requests
import matplotlib.pyplot as plt
from datetime import datetime

city = {'臺北市': 'F-D0047-063', '台北市': 'F-D0047-063', '新北市': 'F-D0047-071', '桃園市': 'F-D0047-007', '臺中市': 'F-D0047-075', '台中市': 'F-D0047-075','臺南市': 'F-D0047-079', '台南市': 'F-D0047-079', '高雄市': 'F-D0047-067', '基隆市': 'F-D0047-051', '新竹縣': 'F-D0047-011', '新竹市': 'F-D0047-055', '苗栗縣': 'F-D0047-015', '彰化縣': 'F-D0047-019', '南投縣': 'F-D0047-023', '雲林縣': 'F-D0047-027', '嘉義縣': 'F-D0047-031', '嘉義市': 'F-D0047-059', '屏東縣': 'F-D0047-035', '宜蘭縣': 'F-D0047-003', '花蓮縣': 'F-D0047-043', '臺東縣': 'F-D0047-039','台東縣': 'F-D0047-039', '澎湖縣': 'F-D0047-047', '金門縣': 'F-D0047-087', '連江縣': 'F-D0047-083'}

def cwb_weather_download(city,zone) :
    dirname="cwb_weather"
    filepath = dirname + '/' + 'cwb_weather.json'

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/" + city + "?Authorization=CWB-DC7619B4-A189-4CFB-BFB3-7981022C6DBC&format=JSON&locationName=" + zone +"&elementName=PoP12h,T,WeatherDescription"
    response = requests.get(url)

    if os.path.isfile(filepath):
       print("檔案存在。")
    else:
       print("檔案不存在。")

       #建立名為cwb_weather的資料夾
       os.mkdir(dirname)

    #開啟資料夾並寫入
    with open(filepath,'wb') as f:
        f.write(response.content)

def data_analysis() :
    time = []
    #rain_chance = []
    mt = []
    weather_des = []

    #讀取檔案
    data =  json.load(open('cwb_weather/cwb_weather.json','r',encoding='utf-8'))

    city = data["records"]["locations"][0]["locationsName"]
    location = data["records"]["locations"][0]["location"][0]["locationName"]
    
    now = datetime.now()
    year = now.strftime("%Y")
    
    title = city + location + " ( " + year + " )"
    #print(title)
    
    ryear =  year + "-"

    for i in range(14) :
        time.append((data["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["startTime"]).replace(ryear,""))
        #rain_chance.append(data["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["elementValue"][0]["value"])
        mt.append(int(data["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][i]["elementValue"][0]["value"]))
        weather_des.append(data["records"]["locations"][0]["location"][0]["weatherElement"][2]["time"][i]["elementValue"][0]["value"])
    
    for i in range(14) :
       print(time[i])
       print(weather_des[i])
    
    graph(time,mt,title)



def graph(x,y,title) :
    y_min_mt = min(y)
    y_max_mt = max(y)
    x_min_mt = y.index(y_min_mt)
    x_max_mt = y.index(y_max_mt)
    
    # 標註值
    for i in range(14) :
      plt.annotate((" " + str(y[i])),(x[i],y[i]))
      plt.plot(x,y)
    
    # 極值標註
    plt.plot(x_max_mt,y_max_mt,'ko',color='red',alpha=1)
    plt.plot(x_min_mt,y_min_mt,'ko',color='blue',alpha=1)

    # 標題設置
    plt.title(title)
    
    # 軸標題設置
    plt.xlabel("Time")
    plt.ylabel("Temperature")

    # 中文字體支援設定
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # x軸 設定
    plt.xticks(rotation = 10,fontsize = 8)

    # 開啟網格
    plt.grid()

    # 風格設定
    #plt.style.use("seaborn-notebook")  

    plt.show()
    
if __name__ == "__main__":
    print("請輸入縣市")
    cityy = input()
    print("請輸入鄉鎮區")
    zone = input()
    cwb_weather_download(city[cityy],zone)
    data_analysis()