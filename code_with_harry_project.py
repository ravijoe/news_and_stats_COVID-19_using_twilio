import bs4
import urllib
import requests
import pprint
import pandas as pd
sauce=requests.get('https://www.worldometers.info/coronavirus/')
soup=bs4.BeautifulSoup(sauce.text,'html.parser')
account_sid = 'AC2117e2416b41a6dccbda8814c173e898'
auth_token = 'd58dedcdb3a8f93caaca3e05b6740292'
# table=soup.find('table')
# table_rows=table.find_all("tr")
# table = soup.find('table', id="main_table_countries_today")
# rows = table.findAll('tr')
# res=pd.DataFrame()
# for r in rows:
#     res=res.append(pd.DataFrame(r.get_text()))
# print(res)
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
header = extract_contents(soup.tr.find_all('th'))
res=pd.DataFrame(columns=header)
all_rows = soup.find_all('tr')
stats=[]
for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    # stat=['NA' for i in stat if i=='']
    # res=res.append(pd.DataFrame(stat))
    # res.loc[i]=stat
    stats.append(stat)
# res.to_csv('coronavirus_stats.csv',index=False)
final=pd.DataFrame()
final=res.append(stats)
final=final.iloc[:,:10]
final.columns = header
final=final[final['Country,Other']=='India']
print('                 ###################    STATS     #############')
# pprint.pprint(final.head(50))
# final.rename(columns = {0:'TotalCases'}, inplace = True)
# final.columns=['a','b','c','d','e','f','g','h','i','j','k']


# data=pd.read_csv('cc.csv')

# # data.drop(data.index[0],inplace=True)
# # data.to_csv('covid_stats.csv',index=False)
# data.to_csv('c2.csv',index=False)
print('                   ###################    NEWS     #############')

array_of_news=str(soup.find(id='news_block').get_text()).replace('\xa0','').split('\n')
for i in array_of_news[:50]:
    if i!='':
        pprint.pprint(i)


# import json
# webhook_url='https://hooks.slack.com/services/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'
# text={'text':'alert from python'}
# requests.post(webhook_url,data=json.dumps(text))
# from plyer import notification
# def notifyMe(title,message,timeout):
#     notification.notify(
#     title=title,
#     message=message,
#     app_icon=None,
#     timeout=timeout
#     )
# notifyMe('first',str(final.loc[1,:]).replace('\xa0',''),6000)

from twilio.rest import Client

client=Client(account_sid, auth_token
              )
from_whatsapp_number=""
to_whatsapp_number=""
client.messages.create(body=str(final),from_=from_whatsapp_number,to=to_whatsapp_number)
client.messages.create(body='\n'.join(array_of_news[:10]),from_=from_whatsapp_number,to=to_whatsapp_number)
