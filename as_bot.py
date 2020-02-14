from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
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
            self.started=raw_offer.find_element_by_xpath('./h3/span[1]/span').get_attribute("class")
            if self.started=="counter":
                self.remaining_time=raw_offer.find_element_by_xpath('./h3/span[1]/span').get_attribute("data-seconds")
            self.owner=raw_offer.find_element_by_xpath('./div/div[1]/div[1]/a').text
            self.reg=raw_offer.find_element_by_xpath('./div/div[1]/div[2]/span').text
            self.age=raw_offer.find_element_by_xpath('./div/div[1]/div[3]/span').text
            self.condition=raw_offer.find_element_by_xpath('./div/div[1]/div[4]/span').text
            self.location=raw_offer.find_element_by_xpath('./div/div[1]/div[5]/a').text
            
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
            if self.price<other.price:
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
            offer_list=self.driver.find_elements_by_xpath("//div[@class='odd']|//div[@class='even']")
            for raw_offer in offer_list:
                new_offers.append(Offer(raw_offer))

            for offer in existing_offers:
                if offer not in new_offers:
                    del offer
            
            for offer in new_offers:
                if offer not in existing_offers:
                    existing_offers.append(offer)
                    if offer.price<send_if_lower_than:
                        output_string="有低于设定价格的飞机出现("+str(offer.price)+")"
                        ToastNotifier().show_toast("AirlinesimBot通知",output_string)
                else:
                    idx=existing_offers.index(offer)
                    old_price=existing_offers[idx].price
                    returned_value=existing_offers[idx].update(offer)
                    if returned_value==0:
                        output_string="有人下手，原价"+str(old_price)+"的飞机，现价"+str(offer.price)
                        ToastNotifier().show_toast("AirlinesimBot通知",output_string)
                    else:
                        if returned_value==1:
                            output_string="有人加价，原价"+str(old_price)+"的飞机，现价"+str(offer.price)
                            ToastNotifier().show_toast("AirlinesimBot通知",output_string)


bot=AirlinesimBot()
bot.login()
bot.market_monitoring()

#python -i as_bot.py