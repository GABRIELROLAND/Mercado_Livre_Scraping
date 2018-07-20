#Mercado Livre Search Scrapper (Hix3nn)

from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('data.csv','a',newline='')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Anúncio','Preço','Parcela','Juros','Frete','Vendas','Localização','Link'])
usr_input =input('Digite a Pesquisa: ')
usr_input = usr_input.replace(" ","-")

pages_increment = ['0','49','101','151','202','253']


#Actually scraping
for x in range(0,3):
    source = requests.get('https://lista.mercadolivre.com.br/'+usr_input+'_Desde_'+pages_increment[x]+'_DisplayType_LF').text
    soup = BeautifulSoup(source,"html5lib")
    for item_shop in soup.find_all('li', class_="results-item article stack "):    
        name_item = item_shop.find('span',class_="main-title").text
        price_item = item_shop.find('span',class_="price__fraction").text
        link = item_shop.find('a',class_="item__info-title")['href']
        sales = item_shop.find('div',class_="item__condition").text
        #Parte decimal do preço pode não existir, no caso corresponde a zero
        if (item_shop.find('span',class_="price__decimals") == None):     
            price_d_item = '00'
        else:
            price_d_item = item_shop.find('span',class_="price__decimals").text
        #quando o frete não é grátis
        if item_shop.find('p', class_="stack-item-info ") == None:
            delivery = 'Combinar com o vendedor'
        else:
            delivery = item_shop.find('p', class_="stack-item-info ").text
        # Caso não apareça no "pré" anúncio as parcelas
        if item_shop.find('span',class_="item-installments-multiplier") == None:
            pre_text = '' 
            cc_t = 'Não divide no cartão'
            cc_price =''
        else:        
            pre_text = 'Divide em'
            cc_t = (item_shop.find('span',class_="item-installments-multiplier").text + 'de')
            cc_price = item_shop.find('span', class_="item-installments-price").text
        #Caso não tenha a informação dos sem juros
        if (item_shop.find('span',class_="item-installments-interest") == None):
            interest = ' com juros'
       
        else:
            interest = item_shop.find('span',class_="item-installments-interest").text
        #quando não há informação nenhuma
        if (item_shop.find('div',class_="item__condition") == None):
            sales_2 = ['0 vendidos','Sem Localização']
        #Quando não há vendas apenas a localização
        elif ' - ' not in (item_shop.find('div',class_="item__condition").text):
            sales_2 = ['0 vendidos',item_shop.find('div',class_="item__condition").text]
        #quando não tem frete grátis e tem vendas
        elif item_shop.find('p', class_="stack-item-info item__free-shipping-disabled") != None:
            if item_shop.find('p', class_="stack-item-info item__free-shipping-disabled").text == ' Envio para todo o país  ':
                sales_2=sales.split("-")
            else:
                sales_2 = ['0',item_shop.find('p', class_="stack-item-info item__free-shipping-disabled").text]
        else:
            sales = item_shop.find('div',class_="item__condition").text
            sales_2=sales.split("-")

        #Printando resultado
        print('Anúncio: ' + name_item)
        print('Preço R$ ' + price_item +',' + price_d_item)
        print(pre_text + cc_t + cc_price + interest) 
        print('Frete: ' + delivery)
        print('Link: ' +link)
        print('Vendas:'+ sales_2[0])
        print('Localização:' + sales_2[1])
        
        print('\n')
        csv_writer.writerow([name_item,price_item+','+price_d_item,cc_price,interest,delivery,sales_2[0],sales_2[1],link])

csv_file.close
    
