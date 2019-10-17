from selenium import webdriver 
from lxml import html 
import csv

def GetAllURL():
    #Get a driver
    #Switches devmode
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
    
    #options.add_argument('--headless')
    wdriver = webdriver.Chrome(options=options)
    wdriver.implicitly_wait(20)  #20s max waiting
    
    #start search
    
    flog = open('clsall\\coles_{0}_log.txt','w',encoding='utf-8')

    startpage = 'https://shop.coles.com.au/a/a-national/everything/browse'
    #go page1
    wdriver.get(startpage)    
    #wait
    #catalogue look like
    #<div id="cat-nav-list-1" class="colrs-animate nav-animate-item item-l1 category-list-container category-list-top-border"
    spyer = wdriver.find_element_by_xpath('//div[@class="colrs-animate nav-animate-item item-l1 category-list-container category-list-top-border"]')
    
    hdoc = wdriver.page_source
    selector = html.fromstring(hdoc)
    
    #get pages number
    Ctlg_l1 = selector.xpath('//div[@class="colrs-animate nav-animate-item item-l1 category-list-container category-list-top-border"]')
    l1_List = Ctlg_l1[0].xpath('./ul/li')
    
    ctgy_l1_list = []

    for li in l1_List:
        ctlgid = li.xpath('./a/@data-category-id')[0]
        url = li.xpath('./a/@href')[0]
        ctlgname = li.xpath('./a/div/span[@class="item-title"]/text()')[0]
        itemsnum = li.xpath('./a/div/span[@class="items-found"]/text()')[0]
        itemsnum = itemsnum.replace(',','')
        flog.write('{0},{1},{2},{3}\n'.format(ctlgid,ctlgname,itemsnum,url))

        ctgy_l1_list.append({ 
                    'level': '1', 
                    'name': ctlgname, 
                    'id': ctlgid, 
                    'num': itemsnum, 
                    'url': url})
    #go for catalogue level 2
    urlhead = 'https://shop.coles.com.au'
    ctgy_l2_list = []

    flog2 = open('clsall\\coles_{1}_log.txt','w',encoding='utf-8')

    start_expand = 0

    for i in ctgy_l1_list:
        if start_expand == 0:
            if i['name'] ==  "Bread & Bakery":
                start_expand = 1
            else:
                continue

        if i['name'] ==  "Tobacco":
            continue

        urll2 = urlhead + i['url']
        wdriver.get(urll2)
        spyer = wdriver.find_element_by_xpath('//div[@class="colrs-animate nav-animate-item item-l2 category-list-container"]')
        hdoc = wdriver.page_source
        selector = html.fromstring(hdoc)
        Ctlg_l2 = selector.xpath('//div[@class="colrs-animate nav-animate-item item-l2 category-list-container"]')
        l2_List = Ctlg_l2[0].xpath('./ul/li')
        for li in l2_List:
            ctlgid = li.xpath('./a/@data-category-id')[0]
            url = li.xpath('./a/@href')[0]
            ctlgname = li.xpath('./a/div/span[@class="item-title"]/text()')[0]
            itemsnum = li.xpath('./a/div/span[@class="items-found"]/text()')[0]
            itemsnum = itemsnum.replace(',','')
            flog2.write('{0},{1},{2},{3}\n'.format(ctlgid,ctlgname,itemsnum,url))

            ctgy_l2_list.append({ 
                'l1name': i['name'], 
                'l1id':i['id'],
                'l2name': ctlgname, 
                'l2id': ctlgid, 
                'num': itemsnum, 
                'url': url})


    with open('clsall\\clsurl_week20190911.csv', 'w', newline='') as csvfile:
        fieldnames = ['l1name','l1id','l2name','l2id','num','url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in ctgy_l2_list:
            writer.writerow(i)


    flog.close()    
    flog2.close()    
    wdriver.quit()
    return



if __name__ == '__main__':
    a = []
    GetAllURL()    
    input('wait for quit:')
