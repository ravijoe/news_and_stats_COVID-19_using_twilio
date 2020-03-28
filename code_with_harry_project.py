import bs4
import urllib
import requests
import pprint
import pandas as pd
sauce=requests.get('https://www.worldometers.info/coronavirus/')
soup=bs4.BeautifulSoup(sauce.text,'html.parser')
account_sid = ''
auth_token = ''
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


from twilio.rest import Client

client=Client(account_sid, auth_token
              )
from_whatsapp_number=""
to_whatsapp_number=""
client.messages.create(body=str(final),from_=from_whatsapp_number,to=to_whatsapp_number)
client.messages.create(body='\n'.join(array_of_news[:10]),from_=from_whatsapp_number,to=to_whatsapp_number)
