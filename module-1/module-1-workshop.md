# 1. modul workshop - Hálózatprogramozás és automatizáció



1.) Írassuk ki egy hálózat OSPF routereinek hosztnevét és router-ID-it!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler
   # felvisszük az eszközök adatait egy-egy szótárba, ügyelve az IP címekre és belépési adatokra:
   r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
   r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

   # betesszük őket egy listába:
   rlist = [r1, r2 ]

   # egy ciklusban sorban kapcsolódunk hozzájuk:
   for rtr in rlist:
      k = ConnectHandler(**rtr)
      print("Hosztnév: ",k.find_prompt()[0:-1], end=',')
      # a megfelelő show paranccsal kiíratjuk a router-ID-t tartalmazó sort:
      output = k.send_command("show ip ospf | include ID")
      # a kimenetet szétbontjuk és egy listát kapunk:
      line = output.split()
      # a keresett ID a lista 6. indexű eleme:
      ospfid = line[6]
      print(" OSPF ID: ",ospfid)
      k.disconnect()
```

</details>

2.) Cseréljük le az OSPF hitelesítő kulcsokat!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler
   # az 1. feladathoz hasonlóan az eszközök adatait felvesszük, és listába rakjuk:
   r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
   r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }
   rlist = [r1, r2 ]

   ujkulcs = input("Új OSPF kulcs értéke: ")

   for rtr in rlist:
      k = ConnectHandler(**rtr)
      print("Hosztnév: ",k.find_prompt()[0:-1])
      # az OSPF folyamatban részt vevő interfészek listája kezdetben üres:
      intlist = []
      # a megfelelő show parancs kimenetét szétbontjuk sorokra:
      output = k.send_command("show ip ospf interface brief").splitlines()
      # a fejlécet tartalmazó sor utáni összes sorra végrehajtjuk, hogy szavakra bontjuk, és az így előállt lista 0. eleme a keresett interfész neve, amit berakunk a listába:
      for sor in output[1:]:
         intlist.append(sor.split()[0])
      print(intlist)
      # az interfészeket kivesszük a listából, és mindegyikre alkalmazzuk a megfelelő konfigurációt:
      for i in intlist:
         k.send_config_set(["interface "+i, "no ip ospf message-digest 1", \
                              "ip ospf message-digest-key 1 md5 "+ujkulcs])
      k.disconnect()
```

</details>

3.) Állítsuk át az OSPF referencia-sávszélességet minden routeren a jelenlegi 10-szeresére!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
   r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

   rlist = [r1, r2 ]

   for rtr in rlist:
      k = ConnectHandler(**rtr)
      print("Hosztnév: ",k.find_prompt()[0:-1], end=',')
      # lekérdezzük az aktuális beállítást a futó konfigurációból:
      output = k.send_command("show run | include auto-cost")
      # ha nem kapun vissza értéket, akkor az alapértelmezett 100 van érvényben:
      if output == '':
         cref = '100'
      # egyébként pedig a kimenetet szétbontjuk, és az így kapott lista 2. indexű eleme a keresett érték:
      else:
         cref=output.split()[2]
      print(cref+' Mbps')
      # számmá alakítjuk és kiszámítjuk az új értéket:
      ref = int(cref)*10
      # végül kiadjuk a megfelelő konfigurációs parancsot (stringgé való visszaalakítás is kell):
      k.send_config_set(['router ospf 1','auto-cost reference-bandwidth '+str(ref)])
      k.disconnect()
```

</details>

4.) Állítsunk be Predictor tömörítést azokra a soros interfészekre, ahol PPP a beágyazási mód!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
   r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

   rlist = [r1, r2]

   for rtr in rlist:
      k = ConnectHandler(**rtr)
      p = k.find_prompt()
      # kigyűjtjük a soros interfészek neveit egy kezdetben üres listába:
      o = k.send_command('sh ip interface brief | include Serial')
      serials = []
      for i in o.splitlines():
         serials.append(i.split()[0])
      # egy következő paranccsal megállapítjuk, melyiken van PPP beágyazási mód:
      for i in serials:
         o = k.send_command('show interfaces '+i+' | include Encapsulation PPP')
         # ha találtunk ilyen interfészt, vagyis a kimenet nem üres, akkor kiíratjuk, melyik eszköz melyik interfésze:
         if o != '':
               print(p,i)
               # végül bekonfiguráljuk:
               k.send_config_set(['interface '+i,'compress predictor'])
      k.disconnect()
```

</details>

5.) Kérdezzük le, hogy adott VLAN-ba melyik portok tartoznak egy switchen!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   s1 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }

   v = input('Melyik VLAN tagjait keressük: ')

   k = ConnectHandler(**s1)
   # a megfelelő show parancs kimenetét sorokra bontjuk:
   output = k.send_command('show interfaces status')
   for sor in output.splitlines():
      # ha nem üres a sor, akkor szavakra bontjuk:
      if sor != '':
         sor = sor.split()
         # ha a VLAN azonosítót tartalmazó szó megegyezik a keresettel, kiírjuk:
         if sor[2] == v:
               print(sor[0])
      
   k.disconnect()
```

</details>

6.) Állapítsuk meg egy kapcsolt hálózatban, hogy
   melyik switch a root bridge!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
   s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }

   slist = [s1, s2]

   for sw in slist:
      k = ConnectHandler(**sw)
      output = k.send_command('show spanning-tree')
      for sor in output.splitlines():
         # ha a show parancs kimenetében megvan a keresett szöveg, akkor kiírjuk az állomásnevet és IP címet is:
         if 'This bridge is the root' in sor:
               rootbr = k.find_prompt()[0:-1]
               rootcim = k.host
               # ha megtaláltuk a root bridge-et, nem nézzük meg a többi switch-et:
               break
      
      k.disconnect()
   # az eredményt formázottan kiírjuk:
   print(f'A root bridge: {rootbr}, IP-címe: {rootcim}')
```

</details>

7.) Gyűjtsük be a switchekről az STP root portok neveit!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
   s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }

   switchlist = [s1, s2]

   for switch in switchlist:
      k = ConnectHandler(**switch)
      # csak a root portok adatait tartalmazó sorban szerepel a Root FWD szöveg:
      output = k.send_command('show spanning-tree | include Root FWD')
      # ha megtaláltuk a kimenetben, akkor a megtalált sort szavakra bontjuk, és a 0. indexű elem lesz a port neve:
      if output != '':
         port = output.split()[0]
         nev = k.find_prompt()[0:-1]
         print('A root port a '+nev+' switchen: '+port)
      k.disconnect()
```

</details>

8.) Ha a 10-es VLAN neve nem 'WORK', akkor állítsuk be!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler
   # használjunk reguláris kifejezést a pontos szövegkereséshez:
   import re

   sw = { 
      'device_type': 'cisco_ios',
      'host': '10.0.0.4',
      'username': 'admin',
      'password': 'cisco',}

   k = ConnectHandler(**sw)
   # hogy kevesebb adattal kelljen dolgozni, csak a 10 szövegrészletet tartalmazó kimenetet kérjük:
   output = k.send_command('show vlan brief | inc 10')

   for sor in output.splitlines():
      # a pontos egyezést reguláris kifejezéssel adjuk meg: a sor elején (^) keresünk 1, majd 0 karaktereket, amiket whitespace(ek) (\s) követ(nek):
      o = re.search("^10\s", sor)
      # ha van találat, és a VLAN neve nem WORK, akkor beállítjuk arra:
      if o:
         n1 = sor.split()[1]
         if n1 != 'WORK':
               ki = k.send_config_set(["vlan 10","name WORK"])
               print(ki)
   k.disconnect()

```

</details>

9.)  Generáljunk RSA kulcsot hagyományosan, majd cseréljük le! Kezeljük le az interaktív kérdéseket!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   r1 = {'device_type': 'cisco_ios',
         'host': '10.0.0.1',
         'username': 'admin',
         'password': 'cisco',
         'secret': "cisco" }

   k = ConnectHandler(**r1)
   # most nem alkalmazhatjuk a send_config_set() metódust, ezért "kézzel" lépünk be globális konfig módba:
   k.enable()
   k.config_mode()
   # kiadjuk a parancsot, amire megvárjuk, míg a routeren megjelenik a "replace them" szöveg:
   print(k.send_command_expect('crypto key generate rsa', expect_string='replace them'))
   # igennel (y) válaszolunk, erre megvárjuk, míg megjelenik a bitek számára vonatkozó kérdés:
   print(k.send_command_expect('y\n', expect_string='How many bits'))
   # beadjuk az értéket, amire a parancs lefut és vissza kell kapnunk a promtot, a végén hashtaggel:
   print(k.send_command_expect('1024\n', expect_string='#'))
   # kilépünk és kijelentkezünk:
   print(k.exit_config_mode())

   k.disconnect()
```

</details>

10.) Írjuk ki a szomszédok neveit CDP-vel, de csak ha switchek! Használjunk TextFSM-et!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
   from netmiko import ConnectHandler

   s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
   s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }

   switchlist = [s1, s2]

   for switch in switchlist:
      k = ConnectHandler(**switch)
      # bekapcsoljuk a TextFSM használatát, a kimenet nem szöveg, hanem egy szótárakat tartalmazó lista lesz:
      output = k.send_command('show cdp neighbor',use_textfsm=True)
      print(k.find_prompt(),"eszköz switch szomszédai:")
      # az e változó tehát egy szótár, aminek adott kulcsaival és értékeivel dolgozunk:
      for e in output:
         if e["capability"] == "S I":
               print(e["neighbor"])
      k.disconnect()

```

</details>

