# 2. modul workshop - Hálózatprogramozás és automatizáció

## RESTCONF feladatok

1.) Kérdezzük le a naplózó puffer méretét, ha nincs beállítva, legyen 16 kB

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    # letiltjuk a fölösleges figyelmeztetéseket:
    requests.packages.urllib3.disable_warnings()

    # beállítjuk a YANG modell alapján az URL-t, majd a szükséges fejléc- és hitelesítő adatokat:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/"
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")
    # elküldjük a GET kérést:
    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    # ha nincs beállítva, akkor kivételkezeléssel akadályozzuk meg a program leállását: 
    try:
        outdict = output.json()
        print(json.dumps(outdict, indent=3))
    except:
        print("Nem jó...nincs beállítva?")

    # az új érték beállításához összeállítjuk egy szótárban a szükséges adatokat, ismét a YANG modell alapján:
    adat={ "Cisco-IOS-XE-native:buffered" : {
            "size-value" : 10000,
            "severity-level" : "errors" }
        }
    # a szótárat átalakítjuk JSON formátumra:
    adatj = json.dumps(adat)
    # megadjuk a módosításhoz az URL-t, és a PUT metódussal el is végezzük azt:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/buffered"
    output = requests.put(url, auth=auth, data=adatj, headers=fejlec, verify=False)
    # lekérjük az állapotkódot:
    print(output.status_code)

```

</details>

2.) Kérdezzük le a domain nevet, és ha nem "proba.lan", akkor állítsuk be

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    # megkeressük a megfelelő URL-t, esetünkben ez a következő:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/domain/name"

    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")

    # az előzetesen definiált adatokkal elküldjük a GET kérést:
    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    # lekezeljük, ha esetleg nincs beállítva semmilyen érték:
    try:
        outdict = output.json()
        print(json.dumps(outdict, indent=3))
    except:
        print("Nem jó...nincs beállítva?")

    # az új értéket egy szótárban definiáljuk, amit JSON formátumra alakítunk:
    adat={ "Cisco-IOS-XE-native:name" : "proba.lan"  }
    adatj = json.dumps(adat)

    # a PUT metódussal küldjük el a módosítandó adatokat, majd lekérdezzük az állapotkódot:
    output = requests.put(url, auth=auth, data=adatj, headers=fejlec, verify=False)
    print(output.status_code)

```

</details>

3.) Kérdezzük le a POOL1 DHCP poolt, majd módosítsuk benne a DNS szerver címét és a domain-nevet

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    # A DHCP pool-ok listában vannak definiálva a YANG adatmodellben.
    # Adott pool-ra a neve alapján tudunk hivatkozni, ez a kulcs:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1"
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")

    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    # ha nincs kivételkezelés, a következő sor hibát okoz:
    print(json.dumps(output.json(), indent=4))

    # új DNS szerver adatait adjuk meg a pool-on belül:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1/dns-server"
    # a módosítandó adatokat többsoros szövegként is megadhatjuk:
    payload = '''
    {
        "Cisco-IOS-XE-dhcp:dns-server": {
            "dns-server-list": [
                "4.4.4.4",
                "8.8.4.4"
            ]
        }
    }
    '''
    output = requests.put(url, auth=auth, headers=fejlec, data=payload, verify=False)
    print(output.status_code)

    # másik domain név megadása, ezt interaktívan kérjük be:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1/domain-name"
    d = input("Új domain: ")
    payload = {
        "domain-name": d
    }
    # a payload változót a PATCH metódus meghívásakor is átalakíthatjuk JSON formátumra:
    response = requests.patch(url, headers=fejlec, auth=auth, data=json.dumps(payload), verify=False)
    print(response.status_code)

```

</details>

4.) Kapcsoljuk be a jelszótitkosítást

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")
    # kikeressük a YANG modellből az URL-t, a keresett beállítás egy leaf objektum:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/service/password-encryption"

    # bekapcsolni egy nullsztringet tartalmazó lista átadásával tudjuk, a PUT metódussal:
    adat = { "Cisco-IOS-XE-native:password-encryption": [ "" ] }
    adatj = json.dumps(adat)

    output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
    print(output.status_code)
    # ellenőrzésképpen lekérdezzük:
    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    print(json.dumps(output.json(), indent=4))

```

</details>

5.) Állítsunk be FTP usernevet és jelszót

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")
    # a felhasználónév egy leaf objektum:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/username"
    # definiáljuk az új értéket, JSON formátumra alakítjuk, meghívjuk a PUT metódust a beállításhoz, majd ellenőrizzük:
    adat = { "Cisco-IOS-XE-native:username": "ftpuser" }
    adatj = json.dumps(adat)

    output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
    print(output.status_code)

    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    print(json.dumps(output.json(), indent=4))

    # a jelszó egy másik konténer alatt található:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/password/password-container/password"
    adat = { "Cisco-IOS-XE-native:password": "ftppass" }
    adatj = json.dumps(adat)
    # a beállítás és ellenőrzés hasonló módon történik:
    output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
    print(output.status_code)

    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    print(json.dumps(output.json(), indent=4))

```

</details>

6.) Vegyünk fel két állomást az állomástáblába (ip host)

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")
    # az URL végén lévő host-list egy lista objektum:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/host/host-list"
    # lekezeljük azt, ha még nincsenek host bejegyzések:
    output = requests.get(url, auth=auth, headers=fejlec, verify=False)
    try:
        print(json.dumps(output.json(), indent=4))
    except:
        print("még nincsenek bejegyzések...")

    # új bejegyzések létrehozásához, a feltöltéshez most a szülő konténert kell megadni, aminek URL-je:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/host"
    # a szótár kulcsa magára a listára mutat, amibe az adatok kerülnek:
    adat = {
        "Cisco-IOS-XE-native:host-list": [
            {
                "name": "pc2",
                "ip-list": [
                    "1.1.1.2"
                ]
            },
        {
                "name": "pc3",
                "ip-list": [
                    "1.1.1.3"
                ]
            }  
        ]
    }
    adatj = json.dumps(adat)
    # a POST metódust kell használni új objektumok létrehozásához:
    output = requests.post(url, auth=auth, headers=fejlec, data=adatj, verify=False)
    print(output.status_code)

```

</details>

7.) Kapcsoljuk be az IPv6 routing-ot

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")
    # a unicast-routing egy leaf objektum:
    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ipv6/unicast-routing"

    # a bekapcsoláshoz itt is egy nullsztringet tartalmazó listát adunk át, az adat többsoros szöveg:
    adat = '''
    {
        "Cisco-IOS-XE-native:unicast-routing": [""]
    }
    '''
    # a módosításhoz PUT metódus szükséges:
    output = requests.put(url, auth=auth, headers=fejlec, data=adat, verify=False)
    # ha az állapotkód 300-nál kisebb, akkor a művelet sikeres:
    if output.status_code < 300:
        print("Sikeres.")

```

</details>

8.) Állítsunk be konzoljelszót és szinkron konzolnaplózást

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import requests
    import json
    USER = 'admin'
    PASS = 'cisco'
    # disable warnings from SSL/TLS certificates
    requests.packages.urllib3.disable_warnings()
    headers = { 'Accept': "application/yang-data+json",'Content-Type': "application/yang-data+json"  }

    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/password"
    adat = '''
    { "secret" : "conpass" }
    '''
    response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
    print(response.status_code, response.text)

    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0"
    adat = '''
    { "login" : {} }
    '''
    response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
    print(response.status_code, response.text)

    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/logging"
    adat = '''
    { "synchronous" : {} }
    '''
    response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
    print(response.status_code, response.text)

```

</details>

9.) Állítsunk be SNMP stringeket és kontakt személyt

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()

    baseurl = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native"
    url = baseurl +"/snmp-server"

    fejlec = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")

    adat = '''
    {
    "Cisco-IOS-XE-native:snmp-server": {
        "Cisco-IOS-XE-snmp:community-config": [
        {
            "name": "titkos",
            "permission": "rw"
        },
        {
            "name": "nyilvanos",
            "permission": "ro"
        }
        ],
        "Cisco-IOS-XE-snmp:contact": "Teszt Elek"
    }
    }
    '''
    output = requests.put(url, headers=fejlec, data=adat, auth=auth, verify=False)
    print(output.status_code)

    output = requests.get(url, headers=fejlec, auth=auth, verify=False)
    print(output.text)

```

</details>

10.) Használjuk az ietf-interfaces modellt; hozzunk létre egy loopback interfészt, majd módosítsuk az IP címét!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import json
    import requests
    requests.packages.urllib3.disable_warnings()

    baseurl = "https://192.168.122.150/restconf/data/ietf-interfaces:interfaces"
    url = baseurl +"/"

    fejlec = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json" }
    auth = ("admin", "cisco")

    adat = { "interface" : [
    {      
    "name": "Loopback3",
    "type": "iana-if-type:softwareLoopback",
    "enabled": False,
    "ietf-ip:ipv4": {
        "address": [
                { "ip": "1.1.1.3",
                "netmask": "255.255.255.0" }
                ]
        }
    }
    ]
    }
    adatj= json.dumps(adat)

    output = requests.post(url, headers=fejlec, data=adatj, auth=auth, verify=False)
    print(output.status_code, output.text)

    x = input("Nyomj ENTER-t:")
    output = requests.get(url, headers=fejlec, auth=auth, verify=False)
    print(output.text)

```

</details>

11.) Kérdezzük le az interfészek részletes működési adatait a megfelelő YANG modul segítségével!
<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```python
    import requests
    import json

    USER = 'admin'
    PASS = 'cisco'

    # disable warnings from SSL/TLS certificates
    requests.packages.urllib3.disable_warnings()

    url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1"

    headers = {
        'Accept': "application/yang-data+json",
        'Content-Type': "application/yang-data+json",
        'cache-control': "no-cache",
        }

    response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
    print(response.text)

```

</details>
