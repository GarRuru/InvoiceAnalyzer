#from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
from collections import Counter
from tkinter import Tk, Menu, ttk, messagebox, Scrollbar, Frame
from tkinter.ttk import Treeview
import requests
import re
import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import threading

# Variable Declare
Year_Selector = ['102', '103', '104', '105', '106', '107']          #年份選擇
Month_Selector = ['01', '03', '05' ,'07','09','11']                 #月份選擇
URL_ORIGIN = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'   #_後面接上年份+月份
CITY = ['基隆市', '臺北市' , '新北市', '桃園市' , '新竹市', '新竹縣', '苗栗縣', '臺中市', '彰化縣', 
        '南投縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣', '宜蘭縣', 
        '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣']              #縣市清單
#CITY_ENG_FULL = ['Keelung', 'Taipei', 'New Taipei', 'Taoyuan', 'HsinChu City', 'HsinChu County', 'MaloLi', 'TaiChung', 'ChungHwa',
#            'Nantou', 'YunLin', 'Chiayie County', 'Chiayie City', 'Tainan', 'KaoHsiang', 'PingTung', 'YiLan',
#            'HuaLien', 'TaiTung', 'PengHu', 'Kinmen', 'LianJiang']

CITY_ENG = ['KLU', 'TPE', 'TPH', 'TYC', 'HSC', 'HSH', 'MAL', 'TXG', 'CWH',
            'NTO', 'YUN', 'CHY', 'CYI', 'TNN', 'KHH', 'IUH', 'YLN',
            'HWA', 'TTT', 'PEH', 'KMN', 'LNN']
CITY_1000 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     #縣市1000萬出現次數統計
CITY_200 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]      #縣市200萬出現次數統計
Selected_YMList = []        #選擇的範圍會隨著Parsing後逐個加入清單
OptionList=['102','01','102','01']      #下拉選單參數（起始年月、終止年月）
Place_1000 = []     #1000萬中獎地點
Place_200 = []      #200萬中獎地點
Grocery_1000 = []   #1000萬品項
Grocery_200 = []    #200萬品項
Cat_1000 = {}       #1000萬品項統計（出現次數）
Cat_200 = {}        #200萬品項統計（出現次數）
global lock     #Mutex Lock

def ZERO():
    for i in range(len(CITY)):
        CITY_1000[i] = 0
        CITY_200[i] = 0
    Selected_YMList.clear()
    Place_1000.clear()
    Place_200.clear()
    Grocery_1000.clear()
    Grocery_200.clear()
    Cat_1000.clear()
    Cat_200.clear()

def ANALYSIS(*args):
    #1000萬
    for i in Place_1000:
        #print(i,'|',i[0:1],'|',i[0:2])
        for k in i:
            if k[0:2] == '桃園':
                CITY_1000[3] += 1
            else:
                cnt = 0
                for j in CITY:
                    if k[0:3] == j:
                       CITY_1000[cnt]+= 1
                       break
                    cnt+=1
    #200萬
    for i in Place_200:
        #print(i,'|',i[0:1],'|',i[0:2])
        for k in i:
            if k[0:2] == '桃園':
                CITY_200[3] += 1    
            else:
                cnt = 0
                for j in CITY:
                    if k[0:3] == j:
                       CITY_200[cnt]+= 1
                       break
                    cnt+=1
    
    #1000萬品項分類統計
    cnt = 0
    for i in Grocery_1000:
        print(i)
        for j in i:
            #print(j)
            try:
                name = ''
                #10201 - 10209 這幾期的品項不帶金額
                if Selected_YMList[cnt] == '10201' or Selected_YMList[cnt] == '10203' or Selected_YMList[cnt] == '10205' or Selected_YMList[cnt] == '10207' or Selected_YMList[cnt] == '10209':
                    #name = re.split('(.[^\s，]*)\s?',j)
                    name = j
                else:
                    #name = re.split(r'(.[^，,]*)(，|,)共?(\d*,?\d*)?元?\s?',j)
                    name = re.split("1|2|3|4|5|6|7|8|9|,|，|共|計",j)
                    name = name[0]
                
                #print(j, name)
                #如果品項中含有「等等」字眼，去掉
                if name.find('等') != -1:
                    name = name[0:name.find('等')]
                
                if Cat_1000.get(name,'none') == 'none':
                    print('catgory not found, add new catgory into dict...')
                    Cat_1000.update({name: 1})
                else:
                    Cat_1000[name] += 1
            except:
                print('error')
        cnt+=1
    
    #200萬品項分類統計
    cnt = 0
    for i in Grocery_200:
        print(i)
        for j in i:
            #print(j)
            try:
                name = ''
                #10201 - 10209 這幾期的品項不帶金額
                if Selected_YMList[cnt] == '10201' or Selected_YMList[cnt] == '10203' or Selected_YMList[cnt] == '10205' or Selected_YMList[cnt] == '10207' or Selected_YMList[cnt] == '10209':
                    #name = re.split('(.[^\s，]*)\s?',j)
                    name = j
                else:
                    #name = re.split(r'(.[^，,]*)(，|,)共?(\d*,?\d*)?元?\s?',j)
                    name = re.split("1|2|3|4|5|6|7|8|9|,|，|共|計",j)
                    name = name[0]
                
                #print(j, name)
                #如果品項中含有「等等」字眼，去掉
                if name.find('等') != -1:
                    name = name[0:name.find('等')]
                
                if Cat_200.get(name,'none') == 'none':
                    print('catgory not found, add new catgory into dict...')
                    Cat_200.update({name: 1})
                else:
                    Cat_200[name] += 1
            except:
                print('error')
        cnt+=1

    print(Cat_1000)
    print(Cat_200)
    
    
def WebParsingPreProcess(*args):
    print(int(OptionList[0]),int(OptionList[1]),int(OptionList[2]),int(OptionList[3]))
    if (int(OptionList[0]) > int(OptionList[2])) or (int(OptionList[0]) == int(OptionList[2]) and int(OptionList[1]) > int(OptionList[3])):
        print('alert!')
        tk.messagebox.showerror(title='錯誤', message='結束期別不應早於起始期別!')
        return

    ZERO()          #歸零參數
    #範圍是有效的，並逐個生成期別（爬蟲字串）
    for i in range(Year_Selector.index(OptionList[0]), Year_Selector.index(OptionList[2])+1):
        for j in range(6):
            if (i == Year_Selector.index(OptionList[0]) and j < Month_Selector.index(OptionList[1])) or (i == Year_Selector.index(OptionList[2]) and j > Month_Selector.index(OptionList[3])):
                continue
            Selected_YMList.append(Year_Selector[i]+Month_Selector[j])
            
    #print(Selected_YMList)
    
    
    #多線程擷取資料
    for i in Selected_YMList:
        #print('i= ',i)
        J1 = threading.Thread(target=WebParsing(i))
        J1.start()
        J1.join()
        
    ANALYSIS()
    print('1000:',CITY_1000)
    print('200:',CITY_200)

    #擷取資料結束，釋出其他操作
    PlotButtom.place(x=140,y=360)
    ExportButtom.place(x=260,y=260)
    CatgoryButtom.place(x=260,y=360)


def WebParsing(YM):
    #TODO : 選定的範圍執行loop(DONE)
    #TODO : 修正月份的範圍BUG(DONE)
    #TODO : 多線程執行緒爬蟲(DONE)

    #顯示其他Button（爬蟲後即可解鎖）
    PLIST_200 = []
    PLIST_1000 = []
    GLIST_200 = []
    GLIST_1000 = []
    url = URL_ORIGIN+YM
    html = requests.get(url).content.decode('utf-8')
    
    print('選擇期別：{}'.format(YM))
    #f.write('\n\n選擇期別：{}\n'.format(Year_Selector[i]+Month_Selector[j]))
    
    lock.acquire()
    print('1000萬')
    #f.write('1000萬\n')
    for idx_1000 ,PR_1000 in enumerate(re.finditer(r'<td headers=\"companyAddress\">([^<]*?)<\/td>\s*<td headers=\"tranItem\">([^<]*?)<\/td>',html)):
        print(PR_1000[1], '|'  ,PR_1000[2])
        #f.write('{} | {}\n'.format(PR_1000[1],PR_1000[2]))
        PLIST_1000.append(PR_1000[1])
        GLIST_1000.append(PR_1000[2])
    
    print('200萬')
    #f.write('200萬\n')
    for idx_200 ,PR_200 in enumerate(re.finditer(r'<td headers=\"companyAddress2\">([^<]*?)<\/td>\s*<td headers=\"tranItem2\">([^<]*?)<\/td>',html)):
        print(PR_200[1], '|'  ,PR_200[2])
        #f.write('{} | {} \n'.format(PR_200[1],PR_200[2]))
        PLIST_200.append(PR_200[1])
        GLIST_200.append(PR_200[2])
        
    
    Place_1000.append(PLIST_1000)
    Place_200.append(PLIST_200)
    Grocery_1000.append(GLIST_1000)
    Grocery_200.append(GLIST_200)
    lock.release()
 
#GUI Main Window
#TODO : 將數據繪製成圖表(Done)
#TODO : 處理中文顯示問題
def PlotDrawer():
    #新視窗組態
    plot_window = tk.Toplevel(root)
    plot_window.geometry('1600x400')
    plot_window.resizable(0,0)
    plot_window.title('統計圖表')
    
    #圖表顯示:subplot
    #font=FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc',size=10)
    
    f = Figure(figsize=(5,4),dpi=100)
    pltBAR = f.add_subplot(111)
    pltBAR.bar(CITY,CITY_1000,label='1000',align='edge',width=0.4)
    pltBAR.bar(CITY,CITY_200 ,label='200' ,align='edge',width=-0.4)
    pltBAR.set_title('中獎統計長條圖Bar Chart')
    pltBAR.legend()
    plt.rcParams['font.family']=['Noto Sans CJK TC']
    pltBAR.set_xlabel('城市名稱 City')#,fontproperties=font)
    pltBAR.set_ylabel('發票數 Count')#,fontproperties=font)
    plt.ylim(0,max(CITY_1000)+20)
    for x,y in zip(CITY,CITY_1000):
        pltBAR.text(x,y+0.1, '%d' % y, ha='left', va='bottom', fontsize=12)
    for x,y in zip(CITY,CITY_200):
        pltBAR.text(x,y+0.1, '%d' % y, ha='right', va='bottom',fontsize=10)
    #把圖表嵌進視窗裡面
    canvas = FigureCanvasTkAgg(f, plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand = 1)
    #圖表小工具
#    toolbar = NavigationToolbar2TkAgg(canvas, plot_window)
#    toolbar.update()
#    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    #p1000.rcParams['font.sans-serif'] =['Microsoft YaHei']
    
    
def exportFile():
    print('Export File Start')
    f = open('TAX.txt','w')
    f.write('選定範圍：{} - {}\n'.format(Selected_YMList[0],Selected_YMList[-1]))
    f.write(' '*14+'[中獎縣市統計]\n縣市名稱    1000萬中獎張數    200萬中獎張數\n')
    for i in range(len(CITY)):
        f.write('%5s    %10d    %10d\n' % (CITY[i],CITY_1000[i],CITY_200[i]))
    
    f.write('\n')
    f.write('[1000萬發票消費品項統計]\n品名               中獎次數\n')
    for k,v in Cat_1000.items():
        f.write(k.ljust(15) +'    %4d\n'%v)
    f.write('[200萬發票消費品項統計]\n品名               中獎次數\n')
    for k,v in Cat_200.items():
        f.write(k.ljust(15) +'    %4d\n'%v)

    f.write('\n\n' + '='*10 +'中獎縣市與品項明細'+'='*10+'\n')
    for i in Selected_YMList:
        f.write('發票期別：{}\n'.format(i))
        f.write('<1000萬>\n')
        ctemp = 0
        for i in Place_1000:
            for j in range(len(i)):
                f.write('{} | {}\n'.format(Place_1000[ctemp][j],Grocery_1000[ctemp][j]))
            ctemp+=1
        ctemp = 0
        f.write('<200萬>\n')
        for i in Place_200:
            for j in range(len(i)):
                f.write('{} | {}\n'.format(Place_200[ctemp][j],Grocery_200[ctemp][j]))
            ctemp+=1
        f.write('\n\n')
    
    print('Finish Exporting File')
    f.close()
    tk.messagebox.showinfo(title='完成', message='檔案輸出完成')

def showCatgory():
    Cat1_window = tk.Toplevel(root)
    Cat1_window.geometry('300x400')
    Cat1_window.resizable(0,0)
    Cat1_window.title('1000萬發票 消費品項統計表')
    frame1 = Frame(Cat1_window)
    frame1.place(x=0,y=10,width=280,height=400)
    scrBar1 = tk.Scrollbar(Cat1_window)
    scrBar1.pack(side = tk.RIGHT, fill=tk.Y)
    tree1 = Treeview(Cat1_window,columns=('c1','c2'),show='headings',yscrollcommand = scrBar1.set)
    
    tree1.column('c1',width=200,anchor='center')
    tree1.column('c2',width=80,anchor='center')
    tree1.heading('c1', text='品項')
    tree1.heading('c2', text='出現次數')
    tree1.pack(side=tk.LEFT, fill= tk.Y)
    
    scrBar1.config(command = tree1.yview)
    tree1.bind('<Button-1>', treeviewClick)
    
    sort1000=[[v[1],v[0]] for v in Cat_1000.items()] 
    sort1000.sort() 
    sort1000.reverse()

    for z in sort1000:
        tree1.insert('','end',text=z[1],values=(z[1],z[0]))


    Cat2_window = tk.Toplevel(root)
    Cat2_window.geometry('300x400')
    Cat2_window.resizable(0,0)
    Cat2_window.title('200萬發票 消費品項統計表')
    frame2 = Frame(Cat2_window)
    frame2.place(x=0,y=10,width=280,height=400)
    scrBar2 = tk.Scrollbar(Cat2_window)
    scrBar2.pack(side = tk.RIGHT, fill=tk.Y)
    tree2 = Treeview(Cat2_window,columns=('w1','w2'),show='headings',yscrollcommand = scrBar2.set)
    
    tree2.column('w1',width=200,anchor='center')
    tree2.column('w2',width=80,anchor='center')
    tree2.heading('w1', text='品項')
    tree2.heading('w2', text='出現次數')
    tree2.pack(side=tk.LEFT, fill= tk.Y)
    
    scrBar2.config(command = tree2.yview)
    tree2.bind('<Button-1>', treeviewClick)
    
    sort200=[[v[1],v[0]] for v in Cat_200.items()] 
    sort200.sort() 
    sort200.reverse()

    for z in sort200:
        tree2.insert('','end',text=z[1],values=(z[1],z[0]))

def treeviewClick(event):
    pass


#下拉式選單的動作
def getSYR(*args):
    OptionList[0]= YRStartComboBOX.get()
    print(YRStartComboBOX.get(),OptionList)
def getEYR(*args):
    OptionList[2]=YREndComboBOX.get()
    print(YREndComboBOX.get(),OptionList)
def getSMH(*args):
    OptionList[1]=MHStartComboBOX.get()
    print(MHStartComboBOX.get(),OptionList)
def getEMH(*args):
    OptionList[3]=MHEndComboBOX.get()
    print(MHEndComboBOX.get(),OptionList)
    
def AboutUS():
    print('2018 Fall Python Programming')
    tk.messagebox.showinfo(title='關於', message='統一發票小工具\n2018 Python程式設計')

    
def _quit():
    root.destroy()
    root.quit()
    #exit()


######### Program Main ##########
if __name__ == '__main__':
    lock = threading.Lock()
    print("START")
    #主視窗：組態設定 
    root = Tk()
    root.title('統一發票中獎統計')
    root.geometry('500x500')
    root.resizable(0,0)
    menu = Menu(root)
    root.config(menu=menu)
    Mainmenu = Menu(menu)
    menu.add_cascade(label='Main Menu',menu=Mainmenu)
    Mainmenu.add_command(label="About", command = AboutUS)
    Mainmenu.add_command(label="Exit", command = _quit)
    
    TitleFontStyle = tkFont.Font(family='Consolas',size = 28)
    TitleHead = tk.Label(root,text='統一發票中獎統計小工具',font=TitleFontStyle)
    TitleHead.pack()
    tk.Label(root,text = '開始期別').place(x=100,y=160)
    tk.Label(root,text = '結束期別').place(x=100,y=200)
    
    #TODO : 下拉選單的防呆機制？（結束期別不可早於開始期別）(Done)
    YRVALUE = tk.StringVar()
    YRStartComboBOX = ttk.Combobox(root,textvariable=YRVALUE,width=8)
    YRStartComboBOX["values"] = ('102','103','104','105','106','107')
    YRStartComboBOX.current(0)
    YRStartComboBOX.bind("<<ComboboxSelected>>",getSYR)
    YRStartComboBOX.place(x=170,y=160)
    
    YRVALUE2 = tk.StringVar()
    YREndComboBOX = ttk.Combobox(root,textvariable=YRVALUE2,width=8)
    YREndComboBOX["values"] = ('102','103','104','105','106','107')
    YREndComboBOX.current(0)
    YREndComboBOX.bind("<<ComboboxSelected>>",getEYR)
    YREndComboBOX.place(x=170,y=200)
    
    MHVALUE = tk.StringVar()
    MHStartComboBOX = ttk.Combobox(root,textvariable=MHVALUE,width=8)
    MHStartComboBOX["values"] = ('01','03','05','07','09','11')
    MHStartComboBOX.current(0)
    MHStartComboBOX.bind("<<ComboboxSelected>>",getSMH)
    MHStartComboBOX.place(x=280,y=160)
    
    MHVALUE2 = tk.StringVar()
    MHEndComboBOX = ttk.Combobox(root,textvariable=MHVALUE2,width=8)
    MHEndComboBOX["values"] = ('01','03','05','07','09','11')
    MHEndComboBOX.current(0)
    MHEndComboBOX.bind("<<ComboboxSelected>>",getEMH)
    MHEndComboBOX.place(x=280,y=200)
    
    AnalysisButtom = tk.Button(root,text='抓取資料',width=10,height=4,command=WebParsingPreProcess)
    AnalysisButtom.place(x=140,y=260)
    
    PlotButtom = tk.Button(root,text='顯示統計圖表',width=10,height=4,command=PlotDrawer)
    #PlotButtom.place(x=200,y=260)
    
    ExportButtom = tk.Button(root,text='匯出至txt',width=10,height=4,command=exportFile)
    #ExportButtom.place(x=360,y=260)
    
    CatgoryButtom = tk.Button(root,text='顯示購買品項',width=10,height=4,command=showCatgory)
    
    root.mainloop()


# =============================================================================
# 要求
# 0.禁止先下載整理好的統一發票特別獎與特獎資料
# 1.要使用thread，分別抓取不同時間網頁
# 2.要使用matplotlib模組顯示相關資訊
# 3.能夠指定任意102/01~107/09統計時間區間
# 
# 選項要求(可有可無)
# 1.使用tkinter模組(或其他GUI模組)設計GUI，讓使用者可以輕易操作你的程式
# 2.程式還提供不同的統計(例如依照發票類別，如食品，停車費等)
# =============================================================================

# https://blog.csdn.net/houyanhua1/article/details/78174066
# https://stackoverflow.com/questions/39558908/combobox-not-present-in-tk
# https://stackoverflow.com/questions/4072150/how-to-change-a-widgets-font-style-without-knowing-the-widgets-font-family-siz
# https://stackoverrun.com/cn/q/8686428
# https://codeday.me/bug/20170313/4783.html
# http://www.cnblogs.com/shwee/p/9427975.html#D14
# https://medium.com/@wulala505/matplotlib-pyplot-%E5%9C%A8mac%E8%A8%AD%E5%AE%9A%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87%E5%AD%97%E5%9E%8B-88f5b027a352
# https://blog.csdn.net/gmr2453929471/article/details/78655834
# https://tinycorner.tw/2018/08/22/python%E6%95%B8%E6%93%9A%E5%9C%96%E5%BD%A2%E5%8C%96%E5%A5%97%E4%BB%B6-matplotlib-iii/
# https://hk.saowen.com/a/0c07c13b189e087b2b58762ef6cb2356988b384e0b561aa980b2333d734dd2bf
# http://www.10tiao.com/html/383/201702/2247484194/1.html
# 縣市中英縮寫：http://www.bwt.com.tw/eWeb/TKT/city_search_right.asp?NATN_CD=TW&search_tp=CITY
