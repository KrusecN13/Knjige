import os
import requests
import sys
import re
import html 
import csv


def pripravi_imenik(ime_datoteke): 
    
     '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.''' 
     imenik = os.path.dirname(ime_datoteke) 
     if imenik: 
         os.makedirs(imenik, exist_ok=True) 
          
 
 
def shrani(url, ime_datoteke, vsili_prenos=False): 
 '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.''' 
 try: 
     print('Shranjujem {}...'.format(url), end='') 
     sys.stdout.flush() 
     if os.path.isfile(ime_datoteke) and not vsili_prenos: 
         print('shranjeno že od prej!') 
         return 
     r = requests.get(url) 
 except requests.exceptions.ConnectionError: 
     print('stran ne obstaja!') 
 pripravi_imenik(ime_datoteke) 
 with open(ime_datoteke, 'w', encoding="utf-8") as datoteka: 
     datoteka.write(r.text) 
     print('shranjeno!') 


def vsebina_datoteke(ime_datoteke): 
 '''Vrne niz z vsebino datoteke z danim imenom.''' 
 with open(ime_datoteke, encoding="utf-8") as datoteka: 
     vsebina = datoteka.read() 
 return vsebina 


def datoteke(imenik): 
 '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.''' 
 return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)] 

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding="utf-8") as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)



####################

            
#knjige, ki so prejela prvo nagrado na choice award (v letih od 2010-2014):


slovar1 = {'Naslov_knjige': [], 'Leto_nagrade': [],'Zvrst': []}

for i in range(2010,2015):
     shrani('https://www.goodreads.com/choiceawards/best-books-' + str(i),'zajete-strani/nagrada' + str(i) + '.html')
     
     with open('zajete-strani/nagrada' + str(i) + '.html','r',encoding = 'utf-8') as u:
          if i == 2010 or i == 2011:
               for vrstica in u.read().split('\n'):

                    
                    knjiga = re.findall(r'<img alt="([^"]+)" title="', vrstica, flags=re.DOTALL)
                    if knjiga != []:
                         naslov, pisatelj = knjiga[0].split(' by ')
                         slovar1['Naslov_knjige'].append(html.unescape(naslov))
                    
                    
                         slovar1['Leto_nagrade'].append(i)
                         
                    zvrst = re.findall(r'<h3><a href="/choiceawards/[^>]+>([^<]+)</a></h3>', vrstica, flags=re.DOTALL)
                    if zvrst != []:
                         slovar1['Zvrst'].append(html.unescape(zvrst[0]))
          else:
               for vrstica in u.read().split('\n'):
                    

                    naslov = re.findall(r'<img class="winner" alt="([^(]+)" src="', vrstica, flags=re.DOTALL)
                    zvrst = re.findall(r'"><h4>([^"]+)</h4>', vrstica, flags=re.DOTALL)
                   
                    if naslov != []:
                         slovar1['Naslov_knjige'].append(html.unescape(naslov[0]))
                    if zvrst != []:
                         slovar1['Leto_nagrade'].append(i)
                         slovar1['Zvrst'].append(html.unescape(zvrst[0]))
               


                         
######################


#najboljše knjige po stoletjih:
            
shrani('https://www.goodreads.com/list/show/7', 'zajete-strani/best21.html')
shrani('https://www.goodreads.com/list/show/6', 'zajete-strani/best20.html')
shrani('https://www.goodreads.com/list/show/16', 'zajete-strani/best19.html')
shrani('https://www.goodreads.com/list/show/30', 'zajete-strani/best18.html')
shrani('https://www.goodreads.com/list/show/53', 'zajete-strani/best17.html')
shrani('https://www.goodreads.com/list/show/52', 'zajete-strani/best16.html')
shrani('https://www.goodreads.com/list/show/74', 'zajete-strani/best15.html')
shrani('https://www.goodreads.com/list/show/73', 'zajete-strani/best14.html')

slovar = {'Naslov_knjige': [], 'Pisatelj': [], 'Leto_izdaje': [], 'Povprecna_ocena': [], 'Vrstni_red':[]}
sez = [] 

for a in range(14,22):
    
     with open('zajete-strani/best' + str(a) + '.html','r',encoding = 'utf-8') as u:
          
          zac, kon =  u.read().split('<a name="voters"></a>')
          # datoteko razdelim tam, kjer se začnejo komentarji.
          # vzorce iščem le v prvem delu datoteke - zac
              
          for vrstica in zac.split('\n'):
               
               naslov = re.findall(r'<a title="([^"]+)"', vrstica, flags=re.DOTALL)  # seznam nizov
               pisatelj = re.findall(r'<span itemprop="name">([^<]+)', vrstica, flags=re.DOTALL)
               ocena = re.findall(r'(\d*\.\d*) avg rating', vrstica, flags=re.DOTALL)
               vrsta = re.findall(r'<td valign="top" class="number">(\d*)</td>',vrstica, flags=re.DOTALL)
               url_letnce = re.findall(r'<a title="[^"]+"\s*href="([^"]+)">',vrstica, flags=re.DOTALL)

               if url_letnce != []:
                    sez.extend(url_letnce)
                    
               if naslov != []:
                   slovar['Naslov_knjige'].append(html.unescape(naslov[0]))
                   
               if pisatelj != []:
                    slovar['Pisatelj'].append(html.unescape(pisatelj[0]))
               if ocena != []:
                    slovar['Povprecna_ocena'].extend(ocena)
               if vrsta != []:
                    slovar['Vrstni_red'].extend(vrsta)
                    

                    
for url in sez:
     
     st_letnce = re.findall(r'/book/show/(\d*)',url,flags=re.DOTALL)
     shrani('https://www.goodreads.com' + url,'zajete-strani/letnce'+ st_letnce[0]+'.html')
     
     with open('zajete-strani/letnce'+ st_letnce[0]+'.html','r',encoding = 'utf-8') as f:
          cela_vsebina = f.read()
          
          prva_objava = re.search(r'\(first published.*?\s(\d{4})\)', cela_vsebina, flags=re.DOTALL)
          
          objava = re.search(r'Published.*?\s(\d{4})\s.*?by', cela_vsebina, flags=re.DOTALL)
          leto = int(objava.group(1))

          # če obstaja podatek kdaj je bila knjiga prvič objavljena poberem tega, drugače pa poberem
          # kdaj je bila objavlena (ker imajo lahko več izdaj vzamem prvo).
          if prva_objava != None:
               prvo_leto = int(prva_objava.group(1))
               slovar['Leto_izdaje'].append(prvo_leto)

          else:
               slovar['Leto_izdaje'].append(leto)





###########################

######CSV:
##               
with open('csv-datoteke/knjige.csv','wt',encoding = 'utf-8') as csvdat:
     
     oznaka = ['Vrstni_red', 'Naslov','Pisatelj', 'Leto_izdaje', 'Ocena']
     napisi = csv.DictWriter(csvdat, fieldnames=oznaka)
     napisi.writeheader()
     for i in range(len(slovar['Leto_izdaje'])):
          
             
          napisi.writerow({'Vrstni_red': str(slovar['Vrstni_red'][i]),
                         'Naslov': str(slovar['Naslov_knjige'][i]),
                         'Pisatelj' : str(slovar['Pisatelj'][i]),
                         'Leto_izdaje' : str(slovar['Leto_izdaje'][i]),
                         'Ocena' : str(slovar['Povprecna_ocena'][i])})

with open('csv-datoteke/knjige-nagrade.csv','wt',encoding = 'utf-8') as csvdat:
     
     oznaka = ['Naslov','Leto_nagrade', 'Zvrst']
     napisi = csv.DictWriter(csvdat, fieldnames=oznaka)
     napisi.writeheader()
     for i in range(len(slovar1['Naslov_knjige'])):
          
             
          napisi.writerow({'Naslov': str(slovar1['Naslov_knjige'][i]),
                         'Leto_nagrade': str(slovar1['Leto_nagrade'][i]),
                         'Zvrst' : str(slovar1['Zvrst'][i])})





    
