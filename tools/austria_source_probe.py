#!/usr/bin/env python3
from pathlib import Path
import json, re, urllib.parse
import requests
from bs4 import BeautifulSoup

OUT=Path('probe-out'); OUT.mkdir(exist_ok=True)
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'
SEARCH='https://www.schulen-online.at/sol/oeff_suche_schulen.jsf'

def submit_search():
    s=requests.Session(); s.headers.update({'User-Agent':UA,'Accept-Language':'de-AT,de;q=0.9'})
    r=s.get(SEARCH,timeout=60); r.raise_for_status()
    soup=BeautifulSoup(r.text,'lxml'); form=soup.find('form',id='myform1')
    data={}
    for x in form.find_all('input',attrs={'name':True}):
        typ=(x.get('type') or '').lower()
        if typ in {'submit','button','image','file'}: continue
        if typ in {'checkbox','radio'} and not x.has_attr('checked'): continue
        data[x['name']]=x.get('value','')
    for x in form.find_all('select',attrs={'name':True}):
        selected=x.find('option',selected=True) or x.find('option')
        data[x['name']]=selected.get('value','') if selected else ''
    data.update({'myform1:skz':'','myform1:bez':'','myform1:schulart':'UNDEFINED','myform1:art':'','myform1:plz':'','myform1:ort':'','myform1:strasse':'','myform1:bundesland':'-1','myform1:bezirke':'-1','myform1:sort':'0','myform1:anz':'50','myform1:j_id_1x':'Suchen','myform1_SUBMIT':'1'})
    action=urllib.parse.urljoin(r.url,form.get('action') or r.url)
    rr=s.post(action,data=data,timeout=90); rr.raise_for_status()
    return s,action,rr

def post_target(s,action,html,target):
    soup=BeautifulSoup(html,'lxml')
    form=soup.find('form',id='j_id_20')
    data={x['name']:x.get('value','') for x in form.find_all('input',attrs={'name':True}) if (x.get('type') or '').lower() not in {'submit','button','image','file'}}
    data['j_id_20_SUBMIT']='1'
    data['j_id_20:_idcl']=target
    r=s.post(action,data=data,timeout=90); r.raise_for_status(); return r

summary={}
# Detail target
s,action,result=submit_search(); (OUT/'schools-results.html').write_bytes(result.content)
rs=BeautifulSoup(result.text,'lxml')
first=rs.select_one('div.skz a')
first_code=' '.join(first.stripped_strings)
target=re.findall(r"'([^']+)'",first.get('onclick') or '')[1]
detail=post_target(s,action,result.text,target); (OUT/'schools-detail.html').write_bytes(detail.content)
ds=BeautifulSoup(detail.text,'lxml')
labels={}
for h5 in ds.select('#tabs-3 h5'):
    label=' '.join(h5.stripped_strings)
    nxt=h5.find_next_sibling()
    labels[label]=' '.join(nxt.stripped_strings) if nxt else ''
summary['detail']={'code':first_code,'target':target,'status':detail.status_code,'labels':labels,'text':' '.join(ds.select_one('#tabs-3').stripped_strings)[:5000] if ds.select_one('#tabs-3') else ''}

# Next page target from a fresh state
s2,action2,result2=submit_search()
next_page=post_target(s2,action2,result2.text,'j_id_20:next'); (OUT/'schools-next.html').write_bytes(next_page.content)
ns=BeautifulSoup(next_page.text,'lxml')
summary['next']={'status':next_page.status_code,'from':ns.select_one('#j_id_20\\:from').get_text(strip=True) if ns.select_one('#j_id_20\\:from') else '', 'to':ns.select_one('#j_id_20\\:to').get_text(strip=True) if ns.select_one('#j_id_20\\:to') else '', 'sum':ns.select_one('#j_id_20\\:sum').get_text(strip=True) if ns.select_one('#j_id_20\\:sum') else '', 'codes':[' '.join(x.stripped_strings) for x in ns.select('div.skz')[:5]]}
(OUT/'summary2.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
