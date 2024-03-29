'''
Created on 2012-7-5

@author: Simon
'''
from yahooparser import triggerNhNl
from stocktrace.dao.stockdao import findAllExistentTickers,findLastStockByDays,checkStockWithMA,getMa
import sys, traceback
from stocktrace.util import settings,slf4p

logger = slf4p.getLogger(__name__)

#find quotes triggered nhnl index during the last days
def findByNhnl(lastDays=200,nearDays=5):
    stocks = findAllExistentTickers()
    nhnlList = {'nhList':[],'nlList':[]}
    nh = 0
    nl = 0
   
    for code in stocks:       
                try:
                    triggered = triggerNhNl(code,lastDays,nearDays) 
                    print triggered
                    if triggered == 0:
                        continue
                    elif triggered.get('value') == 1:
                        nhnlList['nhList'].append({'date':triggered['date'],'code':code})
                        nh += 1;
                    elif triggered.get('value') == -1:
                        nhnlList['nlList'].append({'date':triggered['date'],'code':code})
                        nl += 1;
                                                                                            
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
    nhnlList['nh'] = nh
    nhnlList['nl'] = nl
    nhnlList['nhnl'] = nh - nl
    return nhnlList  

#find quotes by MA index
#ma=10/20/50/200
#condition=1(high)/2(low)
#return those price is higher/lower than MA during the last days
def findByMa(lastDays=40,ma=10,condition=settings.HIGHER):
    stocks = findAllExistentTickers()
    result = []
    
    for code in stocks:       
                try:
                    triggered = checkStockWithMA(code,lastDays,ma,condition) 
                    print code+str(triggered)
                    if triggered:
                        result.append(code)                      
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
      
        
    return result     

#find quotes by MA index
#ma1=10/20/50/200
#ma2=10/20/50/200
#condition=1(high)/2(low)
#return those ma1 is higher or lower than ma2 during the last days
def findByMa2(lastDays=40,ma1=10,ma2=20,condition=settings.HIGHER):
    stocks = findAllExistentTickers()
    result = []
    
    for code in ['600600']:       
                try:
                    temp = getMa(code,lastDays,ma1) 
                    print temp   
                    
                    temp2 = getMa(code,lastDays,ma2) 
                   
                    size = len(temp)
                    print code+':'+str(size)
                    
                    flag = True
                    for i in range(1,size):
                        print temp2[i]
                        print temp[i]
                        if temp2[i] > temp[i]:
                            flag = False     
                            logger.warn(code+' does not pass MA:'+str(i))                       
                            break;
                            
                    if flag:         
                        result.append(code)    
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
      
        
    return result 

#find top N quotes by Price Volatility during last days
#condition=1(high)/2(low)
def findByPriceVolatility(lastDays=40,top=10,condition=settings.HIGHER):
    stocks = findAllExistentTickers()
    result = []
    
    for code in stocks:       
                try:
                    triggered = checkStockWithMA(code,lastDays,top,condition) 
                    print code+str(triggered)
                    if triggered:
                        result.append(code)                      
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
      
        
    return result   

#find top N quotes by Price Volatility from yearLow or yearHigh
#condition=1(high)/2(low)
def findByYearLowOrHigh(top=20,condition=settings.HIGHER):
    from stocktrace.dao.stockdao import findByYearLow,findByYearHigh
    result = []
    if condition == settings.HIGHER:
        cursor = findByYearLow(top)              
    else:
        cursor = findByYearHigh(top)

    for record in cursor:
        stock = {}
        code = record.get('code')
        if condition == settings.HIGHER:
            stock[code] = record.get('percentFromYearLow')
        else:
            stock[code] = -record.get('percentFromYearHigh')            
        
        result.append(stock)   
    return result        
    
if __name__ == '__main__':
    #print findByNhnl()
    print findByMa(5,10,condition=settings.HIGHER)
    print findByMa(5,10,condition=settings.LOWER)
    #print findByMa2(10,10,20,condition=settings.HIGHER)
    #print findByYearLowOrHigh(10,settings.HIGHER)
    #print findByYearLowOrHigh(10,settings.LOWER)