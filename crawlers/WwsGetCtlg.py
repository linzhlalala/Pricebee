import json
import csv

def Json2Csv():
    ctgy_file = open("wwsall//Category1013.json",'r')
    ctgy_json = json.load(ctgy_file)
    ctgy_file.close()

    urlbase = "/shop/browse/"
    #to skip

    listl1 = []
    listl2 = []

    category = ctgy_json["Categories"]

    for l1ct in category:
        if l1ct ["IsSpecial"] or l1ct ["IsBundle"] or l1ct["IsRestricted"] :
            continue
        l1name = l1ct["Description"]
        l1id = l1ct["NodeId"]
        l1url = urlbase+l1ct["UrlFriendlyName"]
        children = l1ct["Children"]
        l1item = {"l1name":l1name,
            "l1id":l1id,
            "l1url":l1url
        }
        listl1.append(l1item)
        for l2ct in children:
            if l2ct ["IsSpecial"] or l2ct ["IsBundle"] or l2ct["IsRestricted"] :
                continue
            l2name = l2ct["Description"]
            l2id = l2ct["NodeId"]
            l2url = l1url+'/'+l2ct["UrlFriendlyName"]
            l2item = {"l1name":l1name,
                "l1id":l1id,
                "l2name":l2name,
                "l2id":l2id,
                "l2url":l2url
            }
            listl2.append(l2item)

    with open('wwsall\\wwsurll1_20191013.csv', 'w', newline='') as csvfile:
        fieldnames = ['l1name','l1id','l1url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in listl1:
            writer.writerow(i)
    
    with open('wwsall\\wwsurll2_20191013.csv', 'w', newline='') as csvfile:
        fieldnames = ['l1name','l1id','l2name','l2id','l2url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in listl2:
            writer.writerow(i)

    return



if __name__ == '__main__':
    Json2Csv()
    input('wait for quit:')
