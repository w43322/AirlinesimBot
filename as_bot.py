from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from time import sleep
from win10toast import ToastNotifier


from secrets import username,password,server

class Offer():
    started=""
    remaining_time=0.0
    plane_varient=""
    owner=""
    reg=""
    age=""
    condition=""
    location=""
    price=1e20
    def __init__(self,raw_offer):
        try:
            self.plane_varient=raw_offer.find_element_by_xpath('./h3/a').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.started=raw_offer.find_element_by_xpath('./h3/span[1]/span').get_attribute("class")
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            if self.started=="counter":
                self.remaining_time=raw_offer.find_element_by_xpath('./h3/span[1]/span').get_attribute("data-seconds")
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.owner=raw_offer.find_element_by_xpath('./div/div[1]/div[1]/a').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.reg=raw_offer.find_element_by_xpath('./div/div[1]/div[2]/span').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.age=raw_offer.find_element_by_xpath('./div/div[1]/div[3]/span').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.condition=raw_offer.find_element_by_xpath('./div/div[1]/div[4]/span').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            self.location=raw_offer.find_element_by_xpath('./div/div[1]/div[5]/a').text
        except StaleElementReferenceException:
            sleep(0.05)
        try:
            price_text=raw_offer.find_element_by_xpath('./div/div[2]/div/table/tbody/tr[2]/td[5]').text
            price_text=price_text.replace(",","")
            price_text=price_text.replace(" ","")
            price_text=price_text.replace("AS$","")
            self.price=int(price_text)
        except StaleElementReferenceException:
            sleep(0.05)
    def update(self,other):
        if self.started=="not-started" and other.started=="counter":
            self.price=other.price
            self.remaining_time=other.remaining_time
            return 0 #价格更新 有人开始第一次抢飞机
        else:
            if self.started=="counter" and self.price<other.price:
                self.price=other.price
                self.remaining_time=other.remaining_time
                return 1 #价格更新 有人加价
        return 2 #没有改变
    def __eq__(self,other):
        return self.reg==other.reg
    def __lt__(self,other):
        return self.reg<other.reg
    

class AirlinesimBot():
    stat='main'
    lowprice=1e20
    def __init__(self):
        self.driver=webdriver.Chrome()
    def login(self):
        #server=input("please input server:")
        #username=input("please input username:")
        #password=input("please input password:")
        self.driver.get('https://'+server+'.airlinesim.aero')

        login_button=self.driver.find_element_by_xpath('//*[@id="as-navbar-meta-collapse"]/ul/li[4]/a')
        login_url=login_button.get_attribute('href')
        self.driver.get(login_url)
        username_in=self.driver.find_element_by_xpath('//*[@id="id1"]/div/input[1]')
        username_in.send_keys(username)
        password_in=self.driver.find_element_by_xpath('//*[@id="id1"]/div/input[2]')
        password_in.send_keys(password)
        login_button_2=self.driver.find_element_by_xpath('//*[@id="id1"]/div/input[3]')
        login_button_2.click()
    def market(self):
        market_button=self.driver.find_element_by_xpath('//*[@id="as-navbar-main-collapse"]/ul/li[5]/ul/li[3]/a')
        market_url=market_button.get_attribute('href')
        self.driver.get(market_url)
        self.stat='market'

    def _debug_clicker_inner(self,div_1,div_2,tr,td):
        while self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/form/div/div['+str(div_1)+']/div['+str(div_2)+']/div/table/tbody/tr['+str(tr)+']/td['+str(td)+']/input').is_selected()==0:
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/form/div/div['+str(div_1)+']/div['+str(div_2)+']/div/table/tbody/tr['+str(tr)+']/td['+str(td)+']/input').send_keys(Keys.SPACE)

    def _debug_clicker(self,var1,var2,var3,var4,var5,var6,var7,var8,cla):
        self._debug_clicker_inner(1,1,var1,cla)
        self._debug_clicker_inner(1,2,var2,cla)
        self._debug_clicker_inner(1,3,var3,cla)
        self._debug_clicker_inner(1,4,var4,cla)
        self._debug_clicker_inner(2,1,var5,cla)
        self._debug_clicker_inner(2,2,var6,cla)
        self._debug_clicker_inner(2,3,var7,cla)
        self._debug_clicker_inner(2,4,var8,cla)

    def _debug_save_data(self,var1,var2,var3,var4,var5,var6,var7,var8,cla):
        typ=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/div/table/tbody/tr[1]/th').text
        typ=typ.replace(" ","")
        typ=typ.replace(",","")
        typ=typ.replace("km","")
        fil=open('result.txt','a')
        fil.write(str(var1)+" ")
        fil.write(str(var2)+" ")
        fil.write(str(var3)+" ")
        fil.write(str(var4)+" ")
        fil.write(str(var5)+" ")
        fil.write(str(var6)+" ")
        fil.write(str(var7)+" ")
        fil.write(str(var8)+" ")
        fil.write(str(cla)+" ")
        fil.write(typ+" ")
        for rec in range(1,12):#11
            res=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/div/table/tbody/tr['+str(rec)+']/td['+str(cla-2)+']/img').get_attribute("src")
            res=res.replace("https://wright.airlinesim.aero/assets/img/rating/","")
            res=res.replace(".png","")
            fil.write(res+" ")
        if typ=="500" or typ=="800":
            res=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/div/table/tbody/tr[12]/td['+str(cla-2)+']/img').get_attribute("src")
            res=res.replace("https://wright.airlinesim.aero/assets/img/rating/","")
            res=res.replace(".png","")
            fil.write(res+" ")
        mon=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/table/tbody/tr['+str(cla-2)+']/td').text
        mon=mon.replace(" ","")
        mon=mon.replace("AS$","")
        fil.write(mon)
        fil.write('\n')
        fil.close()

    def _debug_service_testing(self):
        self.driver.get('https://'+server+'.airlinesim.aero/action/enterprise/serviceProfile?id=3288')
        cla=3 #3/y 4/c 5/f
        lin=len(open("result.txt").readlines())
        i=1
        for var1 in range(1,5):#4
            for var2 in range(1,5):#4
                for var3 in range(1,8):#7
                    for var4 in range(1,4):#3
                        for var5 in range(1,6):#5
                            for var6 in range(1,5):#4
                                for var7 in range(1,7):#6
                                    for var8 in range(1,6):#5
                                        if i<=lin:
                                            i=i+1
                                            continue
                                        self._debug_clicker(var1,var2,var3,var4,var5,var6,var7,var8,cla)
                                        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div/form/ul[1]/li/button').click()
                                        #sleep(1)
                                        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/ul/li[2]/a').click()
                                        self._debug_save_data(var1,var2,var3,var4,var5,var6,var7,var8,cla)
                                        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/ul/li[1]/a').click()


            
#python -i as_bot.py
    def select_type(self):
        if(self.stat!='market'):
            self.market()
        type_select=Select(self.driver.find_element_by_xpath('//*[@id="id8"]'))
        for plane_type in type_select.options:
            print(plane_type.get_attribute('value'),plane_type.text)
        plane_value=input("please input value:")
        try:
            type_select.select_by_value(plane_value)
        except NoSuchElementException:
            print("invalid value, changing nothing")
            return
    def select_varient(self):
        if(self.stat!='market'):
            self.market()
        varient_select=Select(self.driver.find_element_by_xpath('//*[@id="id9"]'))
        for plane_varient in varient_select.options:
            print(plane_varient.get_attribute('value'),plane_varient.text)
        varient_value=input("please input value:")
        try:
            varient_select.select_by_value(varient_value)
        except NoSuchElementException:
            print("invalid value, changing nothing")
            return
    def select_sort_method(self):
        if(self.stat!='market'):
            self.market()
        sort_method=Select(self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div/div[5]/select'))
        for methods in sort_method.options:
            print(methods.get_attribute('value'),methods.text)
        method_value=input('please input value:')
        try:
            sort_method.select_by_value(method_value)
        except NoSuchElementException:
            print("invalid value, changing nothing")
            return


    def market_monitoring(self):
        send_if_lower_than=int(input("please input your desired price, we'll send you an alert when there is an aircraft listed below that:"))
        
        self.select_type()

        self.select_varient()

        self.select_sort_method()

        if(self.stat!='market'):
            self.market()

        existing_offers=[]
        
        while True:
            sleep(15)
            print("-------------------------new round---------------------------")
            new_offers=[]
            offer_list=[]
            offer_list=self.driver.find_elements_by_xpath("//div[@class='odd']|//div[@class='even']")
            for raw_offer in offer_list:
                new_offers.append(Offer(raw_offer))

            for offer in existing_offers:
                if offer not in new_offers:
                    print(offer.reg,"不在新的列表内")
                    del offer
            
            for offer in new_offers:
                if offer not in existing_offers:
                    existing_offers.append(offer)
                    print(offer.reg,"被添加进列表")
                    if offer.price<send_if_lower_than:
                        output_string="有低于设定价格的飞机出现，飞机的价格是"+str(offer.price)
                        ToastNotifier().show_toast("AirlinesimBot通知",output_string,icon_path="custom.ico")
                else:
                    idx=existing_offers.index(offer)
                    old_price=existing_offers[idx].price
                    returned_value=existing_offers[idx].update(offer)
                    print(offer.reg,"信息被更新")
                    if returned_value==0:
                        output_string="有人下手，原价"+str(old_price)+"的飞机，现价"+str(offer.price)
                        ToastNotifier().show_toast("AirlinesimBot通知",output_string,icon_path="custom.ico")
                    else:
                        if returned_value==1:
                            output_string="有人加价，原价"+str(old_price)+"的飞机，现价"+str(offer.price)
                            ToastNotifier().show_toast("AirlinesimBot通知",output_string,icon_path="custom.ico")


bot=AirlinesimBot()
#input("debug")
bot.login()
#bot.market_monitoring()
bot._debug_service_testing()

#pyinstaller --onefile --add-binary 'C:\Users\raywa\AppData\Local\Google\Chrome\Application\chromedriver.exe;.' as_bot.py