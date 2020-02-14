from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from win10toast import ToastNotifier

from secrets import username,password,server

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
        type_select.select_by_value(plane_value)
    def select_varient(self):
        if(self.stat!='market'):
            self.market()
        varient_select=Select(self.driver.find_element_by_xpath('//*[@id="id9"]'))
        for plane_varient in varient_select.options:
            print(plane_varient.get_attribute('value'),plane_varient.text)
        varient_value=input("please input value:")
        varient_select.select_by_value(varient_value)
    def select_sort_method(self):
        if(self.stat!='market'):
            self.market()
        sort_method=Select(self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div/div[5]/select'))
        for methods in sort_method.options:
            print(methods.get_attribute('value'),methods.text)
        method_value=input('please input value:')
        sort_method.select_by_value(method_value)
    def alert_when_lower(self):
        if(self.stat!='market'):
            self.market()
        first_offer_price=self.driver.find_element_by_xpath('//*[@id="id3"]/div[1]/div/div[2]/div/table/tbody/tr[2]/td[5]')
        first_offer_price=first_offer_price.text
        first_offer_price=first_offer_price.replace(",","")
        first_offer_price=first_offer_price.replace(" ","")
        first_offer_price=first_offer_price.replace("AS$","")
        self.lowprice=int(first_offer_price)
        br=0
        while br==0:
            first_offer_price=self.driver.find_element_by_xpath('//*[@id="id3"]/div[1]/div/div[2]/div/table/tbody/tr[2]/td[5]')
            first_offer_price=first_offer_price.text
            first_offer_price=first_offer_price.replace(",","")
            first_offer_price=first_offer_price.replace(" ","")
            first_offer_price=first_offer_price.replace("AS$","")
            if(int(first_offer_price)<self.lowprice):
                br=1
                self.lowprice=1e20
        self.send_alert()
        #lease_url=self.driver.find_element_by_xpath('//*[@id="id3"]/div[1]/ul/li/div/ul/li[5]/a').get_attribute('href')
        #print(lease_url)
    def send_alert(self):
        toaster = ToastNotifier()
        toaster.show_toast("AirlinesimBot通知","有更低价格飞机出现")


bot=AirlinesimBot()
bot.send_alert()

#python -i as_bot.py
