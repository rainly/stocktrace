'''
Created on 2011-3-7

@author: simon
'''
def parseFinanceData(code):
    from lxml import etree
    from lxml.html import parse
    url = 'http://www.windin.com/home/stock/stock-div/600309.SH.shtml'
    #print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       #f.writelines(result)
       pass 
    
    r = page.xpath('//div[@class="tab01"]');
    #print len(r)    
    from stock import Stock
    stock = Stock(code)
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 
        datas = tree.xpath('//td') 
        #print len(datas)
        index =0
        for data in datas:
            dataTree = etree.ElementTree(data);
            #print etree.tostring(dataTree)
            values = dataTree.xpath('//text()')
            index +=1
            #print index
            if (len(values)==1 ):
                #print values
                #print len(values[0])
                #print str(values[0])
                if (index == 32):
                    mgsy = values[0]
                    #print mgsy+'***************'
                    stock.mgsy = mgsy
                elif (index == 52):
                    mgjzc = values[0]
                    #print mgjzc+'***************'
                    stock.mgjzc = mgjzc
                elif (index == 2):
                    last_update = values[0]
                    #print last_update
                    stock.lastUpdate = last_update                    
         
        return stock  

        
if __name__ == '__main__':
    print parseFinanceData('600327')
    parseFinanceData('600327')
#    import logging
#    LOG_FILENAME = 'example.log'
#    logging.basicConfig(level=logging.DEBUG)
#
#    logging.error('This message should go to the log file')
