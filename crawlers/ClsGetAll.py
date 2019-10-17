from selenium import webdriver 
from lxml import html 
import time
import csv

def GetAllItem():
    
    totaltimestart = time.time()
    totalitem = 0
    #Get a driver
    #Switches devmode
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
    
    #options.add_argument('--headless')
    wdriver = webdriver.Chrome(options=options)
    wdriver.implicitly_wait(20)  #20s max waiting
    
    #start search
    urlhead = 'https://shop.coles.com.au'
    
    urllines = []
    with open('clsall\\clsurl_week20190911.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urllines.append(row)
    
    timestr = time.strftime("%y%m%d", time.localtime())
    itemfilename = 'clsall\\clsitem_{0}.csv'.format(timestr)
    
    with open(itemfilename, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames = ['l1name','l1id','l2name','l2id',
                    'ImgAddr','Title','PartID','ItemID',
                    'Link','Brand','Name','OrgPrice','Size','UnitPrice',
                    'DscType','DscPrice','DscText','PrcSav']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
   

    def PLfromPage(dictctgr,selector,itemfilename):
        #list
        # wdriver selector proved to be too slow,use seletor xpath
        # header_list = wdriver.find_elements_by_xpath('//header[@role="presentation"]')
        header_list = selector.xpath('//header[@role="presentation"]')
        m = len(header_list)
        n = 0

        categoryl1 = dictctgr['l1name']
        categoryl1id = dictctgr['l1id']
        categoryl2 = dictctgr['l2name']
        categoryl2id = dictctgr['l2id']

        itemlist = []

        for header in header_list:
            n = n + 1
            try:       
                #img info     
                pImg =  header.xpath('.//img')
                if pImg != []:
                    pImgAddr = pImg[0].xpath('./@data-ng-src')[0]
                    pTitle = pImg[0].xpath('./@alt')[0]
                else:
                    pImgAddr = ""
                    pTitle = ""
                #main info ph3
                ph3 = header.xpath('.//h3')
                if ph3 !=[]:
                    pPartID = ph3[0].xpath('./@data-partnumber')[0]
                    pItemID = ph3[0].xpath('./@data-itemid')[0]
                    pLink = ph3[0].xpath('./a/@href')[0]
                    pBrand = ph3[0].xpath('.//span[@class="product-brand"][1]/text()')[0]
                    pName = ph3[0].xpath('.//span[@class="product-name"][1]/text()')[0]
                else:
                    pPartID = ""
                    pItemID = ""
                    pLink = ""
                    pBrand = ""
                    pName = ""
                
                pDollar = header.xpath('.//span[@class="dollar-value"][1]/text()')
                pCent = header.xpath('.//span[@class="cent-value"][1]/text()')
                if (pDollar!=[]) and (pCent!=[]) :
                    pOrgPrice = pDollar[0] + pCent[0]
                else:
                    pOrgPrice = ""
                #product info
                pSize = header.xpath('.//span[@class="package-size"][1]/text()')
                if pSize !=[] :
                    pSize = pSize[0]
                else:
                    pSize = ""
                pUnitPrice = header.xpath('.//span[@class="package-price"][1]/text()')
                if pUnitPrice !=[] :
                    pUnitPrice = pUnitPrice[0]
                else:
                    pUnitPrice = ""
                
                #find special
                pDscType = "None"
                pDscPrice = pOrgPrice
                pDscText = ""
                pPrcSav = "0.00%"
                
                pDscTag = header.xpath('.//span[@class="accessibility-inline" and @data-ng-bind="product.promo_desc_ally"]')
                
                if pDscTag !=[]:
                    pDscType = "buyNforN" #Example: buy any 4 for $44.00
                    pDscText = pDscTag[0].xpath('./text()')[0]
                    pDscNumber = int(pDscText.split(' ')[2])
                    pDscSum = float(pDscText.split('$')[1])
                    pDscPrice = str(pDscSum/pDscNumber)                   
                    pPrcSav = '{:.2%}'.format(1-float(pDscPrice)/float(pOrgPrice))
                else :
                    #find saving tag
                    pDscTag = header.xpath('.//span[@class="product-save-value"]')
                    if  pDscTag !=[]:
                        pDscType = "SaveX " #Example: save X
                        pSavValue = pDscTag[0].xpath('./strong/text()')[0][1:]
                        pOrgPrice = '{:.2f}'.format(float(pDscPrice)+float(pSavValue))
                        pPrcSav = '{:.2%}'.format(float(pSavValue)/float(pOrgPrice))
                        pDscText = pPrcSav+' off'
                    else:
                        #seem no special 
                        pass
                
                dictitem = {'l1name': categoryl1,
                            'l1id':categoryl1id,
                            'l2name':categoryl2,
                            'l2id':categoryl2id,
                            'ImgAddr':pImgAddr,
                            'Title':pTitle,
                            'PartID':pPartID,
                            'ItemID':pItemID,
                            'Link':pLink,
                            'Brand':pBrand,
                            'Name':pName,
                            'OrgPrice':pOrgPrice,
                            'Size':pSize,
                            'UnitPrice':pUnitPrice,
                            'DscType':pDscType,
                            'DscPrice':pDscPrice,
                            'DscText':pDscText,
                            'PrcSav':pPrcSav}

                itemlist.append(dictitem)

            except Exception as e:
                pass

        with open(itemfilename, 'a+', newline='',encoding='utf-8') as csvfile:
            fieldnames = ['l1name','l1id','l2name','l2id',
                        'ImgAddr','Title','PartID','ItemID',
                        'Link','Brand','Name','OrgPrice','Size','UnitPrice',
                        'DscType','DscPrice','DscText','PrcSav']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(itemlist)
        return m
    #go over pages
    for index in urllines:
        urltail = index['url']
        categoryl2 = index['l2name']
'''
        fails = 'Hair Removal,\
            Hardware,\
            Frozen Vegetables,\
            Tea,\
            Vegetables'
             
        if categoryl2 not in fails:
            continue
'''
        urlpage = urlhead + urltail
        wdriver.get(urlpage)    
        #wait
        try:
            spyer_page = wdriver.find_element_by_xpath('//div[@class="pagination-container" and @data-colrs-pagination=""]')
        except Exception as e:
            print('FAIL {0} PAGE 1'.format(categoryl2))
            continue
        #debug writing
        hdoc = wdriver.page_source
        selector = html.fromstring(hdoc)
         #get pages number
        pgCt = selector.xpath('//div[@class="pagination-container"]')# and @data-colrs-pagination=""]')
        pgList = pgCt[0].xpath('./ul/li')
        if len(pgList) > 1 :
            pgMax = pgList[-1].xpath('.//span[@class="number"]/text()')[0]
        else:
            pgMax = 1  
        pgMax = int(pgMax)

        totalitem += PLfromPage(index,selector,itemfilename)
        #print('DONE {0} PAGE {1}'.format(categoryl2,1)) 

        if(pgMax > 1):
            for j in range(2,int(pgMax)+1):
                pageUrl = urlpage.replace('pageNumber=1','pageNumber={0}'.format(j))
                wdriver.get(pageUrl)
                try:
                    spyer_page = wdriver.find_element_by_xpath('//div[@class="pagination-container" and @data-colrs-pagination=""]')
                except Exception as e:
                    print('FAIL {0} PAGE {1}'.format(categoryl2,j))
                    continue
                
                selector = html.fromstring(wdriver.page_source)
                #parsing
                totalitem += PLfromPage(index,selector,itemfilename)
                
                #print('DONE {0} PAGE {1}'.format(categoryl2,j)) 
        print('DONE {0}'.format(categoryl2)) 
                

    totaltimeend = time.time()
    costtime = totaltimeend - totaltimestart

    print('SUM ITEM:{0} , TIME:{1}s'.format(totalitem,costtime)) 
    wdriver.quit()

    return

if __name__ == '__main__':

    GetAllItem()    
    input('wait for quit:')
