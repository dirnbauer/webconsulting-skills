#!/usr/bin/env python3
from pathlib import Path
import json, re, urllib.parse
import requests
from bs4 import BeautifulSoup

OUT=Path('probe-out'); OUT.mkdir(exist_ok=True)
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'

urls={
 'wien':'https://schulfuehrer.bildung-wien.gv.at/schoolguide/',
 'stmk':'https://service.bildung-stmk.gv.at/SchoolGuide',
 'ktn':'https://info.bildung-ktn.gv.at/schoolGuide',
 'noe':'https://schulfuehrer.bildung-noe.gv.at/Search',
 'bgld':'https://www.bildungsserver.com/schulfuehrer/',
}
summary={}
for name,url in urls.items():
    try:
        r=requests.get(url,timeout=60,headers={'User-Agent':UA,'Accept-Language':'de-AT,de;q=0.9'})
        r.raise_for_status()
        (OUT/f'{name}.html').write_bytes(r.content)
        soup=BeautifulSoup(r.text,'lxml')
        scripts=[urllib.parse.urljoin(r.url,x.get('src')) for x in soup.find_all('script',src=True)]
        links=[urllib.parse.urljoin(r.url,x.get('href')) for x in soup.find_all('link',href=True)]
        summary[name]={'url':r.url,'status':r.status_code,'scripts':scripts,'links':links}
        for i,script in enumerate(scripts):
            try:
                sr=requests.get(script,timeout=60,headers={'User-Agent':UA})
                if sr.ok:
                    safe=re.sub(r'[^A-Za-z0-9._-]+','_',urllib.parse.urlsplit(script).path.rsplit('/',1)[-1] or f'script{i}.js')
                    (OUT/f'{name}-{i:02d}-{safe}').write_bytes(sr.content)
            except Exception as e:
                summary[name].setdefault('script_errors',[]).append(f'{script}: {e}')
    except Exception as e:
        summary[name]={'error':repr(e)}

s=requests.Session(); s.headers.update({'User-Agent':UA,'Accept-Language':'de-AT,de;q=0.9'})
search='https://www.schulen-online.at/sol/oeff_suche_schulen.jsf'
try:
    r=s.get(search,timeout=60); r.raise_for_status(); (OUT/'schools-form.html').write_bytes(r.content)
    soup=BeautifulSoup(r.text,'lxml')
    form=soup.find('form',id='myform1')
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
    rr=s.post(action,data=data,timeout=90); rr.raise_for_status(); (OUT/'schools-results.html').write_bytes(rr.content)
    rsoup=BeautifulSoup(rr.text,'lxml')
    rows=[]
    for div in rsoup.select('div.skz'):
        a=div.find('a')
        rows.append({'text':' '.join(div.stripped_strings),'href':a.get('href') if a else None,'onclick':a.get('onclick') if a else None,'id':a.get('id') if a else None})
    candidates=[]
    for a in rsoup.find_all('a'):
        txt=' '.join(a.stripped_strings)
        if re.search(r'\b\d{6}\b',txt) or 'detail' in txt.lower() or (a.get('onclick') and 'submit' in a.get('onclick').lower()):
            candidates.append({'text':txt,'href':a.get('href'),'onclick':a.get('onclick'),'id':a.get('id')})
    summary['schools']={'action':action,'status':rr.status_code,'form_fields':data,'skz_rows':rows[:10],'skz_count':len(rows),'candidates':candidates[:30],'candidate_count':len(candidates),'text':' '.join(rsoup.stripped_strings)[:4000]}
except Exception as e:
    summary['schools']={'error':repr(e)}

api_hits={}
for p in OUT.iterdir():
    if p.suffix.lower() not in {'.js','.html'} and '.js' not in p.name: continue
    try: text=p.read_text(encoding='utf-8',errors='ignore')
    except Exception: continue
    hits=sorted(set(re.findall(r'https?://[^"\'\s<>]+|/[A-Za-z0-9_.~!$&()*+,;=:@%/-]*(?:api|school|schule|search|query|graphql)[A-Za-z0-9_.~!$&()*+,;=:@%/?-]*',text,re.I)))
    if hits: api_hits[p.name]=hits[:500]
summary['api_hits']=api_hits
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:(v if k=='schools' else {'status':v.get('status'),'scripts':len(v.get('scripts',[])),'error':v.get('error')}) for k,v in summary.items() if k!='api_hits'},ensure_ascii=False,indent=2))
