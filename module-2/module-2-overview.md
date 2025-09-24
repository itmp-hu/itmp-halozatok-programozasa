# 2. modul - Hálózatprogramozás és automatizáció

## Modern hálózatkonfigurálás

### A modern megközelítés:

- a hálózati eszközök szabványos interfészével kommunikálunk: általában hozzá illeszkedve írunk egy programot, ami végrehajtja az adott feladatot
- kell hozzá egy API, illetve szabványos adatleíró nyelvek (XML, JSON, YAML) - no meg némi programozási ismeret :)

### Előnyei:

- a programkód újra felhasználható, átalakítható
- ugyanazon program akár többféle gyártó eszközéhez is felhasználható, kis átalakítással
- sok eszköz gyorsan és hibamentesen felprogramozható

A hálózatprogramozás tulajdonképpen a hálózati eszközök szabványos API-n keresztüli, programok segítségével történő beállítása. Ez az újfajta megközelítés vezet el a Software Defined Networking elnevezésű technológiához is.

## API fogalma

### Mi az API?

Definíció szerint:

_"Az API (Application Programming Interface) alatt egy olyan programozási interfészt, programozási felületet és annak részletes dokumentációját értjük, amelynek segítségével egy rendszer egy másik programhoz (esetleg rendszerprogramhoz) csatlakozhat. Ennek révén a másik programrendszer szolgáltatási használhatóak, anélkül, hogy a program belső részleteit ismerni kellene.”_
_(https://industry4.hu/fogalomtar/)_

Általában nem tudjuk, hogy az API háttérmunkáiban mi történik, de nem is igazán érdekel minket, hiszen gyors választ várunk és meg is kapjuk. Az API általában nem kötődik programozási nyelvhez, ami azt jelenti, hogy megfelelő paraméterekkel bármilyen programnyelvből meghívható.

Tehát az **API olyan szoftver, amely lehetővé teszi, hogy más alkalmazások hozzáférjenek adataihoz vagy szolgáltatásaihoz.** Egy olyan szabálykészlet, ami leírja, hogy az egyik alkalmazás hogyan tud kölcsönhatásba lépni a másikkal, valamint ennek a kölcsönhatásnak a létrejöttét lehetővé tevő utasításokat is.

Az API hasonló a pincérhez egy étteremben. A vendég azt szeretné, hogy az ételt az asztalára szállítsák. Az ételt a konyhán főzik és készítik el. A pincér a közvetítő, hasonlóan egy API-hoz. A pincér (az API) az a személy, aki felveszi az ügyfél rendelését (a kérést), és megmondja a konyhának, hogy mit kell tennie. Amikor az étel elkészült, a pincér szolgálja fel az ételt (a választ) a vásárlónak.

KÉP

A hálózatprogramozásnál egy általunk **írt program kommunikál a hálózati eszköz API-jával**, szabványos módon - adatformátumban - **kérve** tőle bizonyos funkciókat (pl. konfigurációs adatok lekérdezése, módosítása), amire **az eszköz elvégzi a műveletet**, és szintén szabványos adatformátumban **információt szolgáltat**.

## REST API

A modern hálózati eszközök tipikusan a REST API-t használják (REpresentational State Transfer).

- A **reprezentáció** azt jelenti, hogy egy erőforrás reprezentációját (leírását) egy szerver és egy kliens között továbbítjuk. Ehhez a megjelenítéshez szabványos adatformátumot használunk, általában JSON-t vagy XML-t.
- Az **állapotátvitel** azt jelenti, hogy minden REST API-val végzett művelet önálló. Minden kérés hordoz (átküld) minden információt (állapotot) a művelet befejezéséhez.

KÉP

A REST API HTTP-üzeneteket (metódusokat) használ a hálózati eszköz és egy másik alkalmazás közötti információk küldésére és fogadására.

A REST API esetén a metódusok a következők lehetnek:

| Metódus neve | Célja                          |
| ------------ | ------------------------------ |
| GET          | erőforrás lekérése             |
| POST         | új erőforrás készítése         |
| PUT          | erőforrás teljes frissítése    |
| PATCH        | erőforrás részleges frissítése |
| DELETE       | erőforrás törlése              |

A művelet sikerességét egy **állapotkód**dal jelzi a szerver, ezek fő kategóriái:

| Állapotkód | Jelentés              |
| ---------- | --------------------- |
| 2xx        | sikeres művelet       |
| 3xx        | átirányítás szükséges |
| 4xx        | kliens oldali hiba    |
| 5xx        | szerver oldali hiba   |

A REST API nyilvános URL-címeket tesz közzé, amelyeket az ügyfélalkalmazások használnak a webszolgáltatás erőforrásainak eléréséhez. Ezeket az URL-eket egy API-val összefüggésben **végpont**oknak (endpoint) nevezzük.

Nézzük a következő példát! Egy cég ügyféladatbázisát a http://ceg.hu/api/ bázis URL-en érhetjük el, amin belül a következő metódusok és végpontok lehetnek:

| Metódus neve | Végpont URL                 | Leírás                                   |
| ------------ | --------------------------- | ---------------------------------------- |
| GET          | `http://ceg.hu/api/vevo`    | összes vevő lekérdezése                  |
| POST         | `http://ceg.hu/api/vevo/15` | a 15-ös ID-jű vevő lekérdezése           |
| PUT          | `http://ceg.hu/api/vevo`    | új vevő hozzáadása                       |
| PATCH        | `http://ceg.hu/api/vevo/15` | adott vevő bizonyos adatainak módosítása |
| DELETE       | `http://ceg.hu/api/vevo/15` | adott vevő törlése                       |

A hálózatprogramozásban hasonló dolgot csinálunk, mint a weboldal böngészése, csak ezúttal nem weboldalt vagy képet kérünk, hanem egy adott objektumot az eszköztől, például egy listát a hálózat összes VLAN-járól.

KÉP

Amikor az eszköz megkapja pl. a HTTP GET-kérést, egy HTTP GET-választ küld a kért információkkal. Ezeket az információkat közös **adatformátum**ban szállítjuk.
A két leggyakrabban használt adatformátum a következő:

- JSON (JavaScript Object Notation)
- XML (eXtensible Markup Language)

## Hálózatkonfigurációs protokollok

Ahogy már volt róla szó, a hagyományos hálózatkezelésnek vannak korlátai és problémái.

A modern hálózatokban szükség van a következőkre:

- programozható interfész (API) az eszközkonfigurációhoz
- a konfigurációs és az üzemi adatok elkülönítése
- integrált hibaellenőrzés és helyreállítás.

Több olyan protokoll is van, ami ezeknek eleget tesz:

- **NETCONF** (2006) - IETF szabvány
- **RESTCONF** (2017)
- **gRPC** (2015) - Google szabvány

Mindhárom használja a YANG adatmodelleket.

### NETCONF

A NETCONF célja, hogy „telepítse, kezelje és törölje a hálózati eszközök konfigurációját”, vagyis a hálózat automatizálásának megkönnyítése. XML-t használ az adatok kódolásához és Remote Procedure Call-t (RPC) az üzenetekhez. SSH felett fut.

A NETCONF adatformátumként XML-t használ: a konfigurálni, vagy a hálózati eszközről lekérni kívánt elemek a <data> címkébe vannak beágyazva.

Különféle műveleteink vannak, például a <get-config> a konfiguráció lekéréséhez vagy az <edit-config> az eszköz konfigurálásához.

A műveleteket távoli eljáráshívásként (RPC) hajtjuk végre. Ezt az <rpc> és az <rpc-reply> címkék segítségével ismerhetjük fel.

KÉP

### RESTCONF

A RESTCONF egy olyan protokoll, amely a REST API-hoz hasonlóan működik. HTTPS protokollt használ a szállításhoz. Adatformátumként használhat JSON-t vagy XML-t.

A RESTCONF újabb, mint a NETCONF, de nem helyettesíti azt. Ez inkább egy másik (könnyebb) lehetőség a REST API-kat ismerő mérnökök számára.

KÉP

### YANG

A YANG (Yet Another New Generation) egy adatmodellező nyelv, és az SNMP Management Information Base-hez (MIB) hasonló adatmodelleket használ. A YANG egy szabvány, amelyet az RFC 6020 ír le, és egyre népszerűbb. A YANG olyan adatmodelleket használ, amelyek leírják:

- mit lehet konfigurálni egy eszközön,
- mit lehet monitorozni egy eszközön, és
- az eszközön végrehajtható adminisztratív műveleteket (például egy interfész számlálóinak törlése vagy az OSPF folyamat újraindítása).

A YANG adatmodellek lehetnek:

- **általános** adatmodellek: iparági szintű szabványos YANG-modellek olyan szervezetektől, mint az IETF és az IEEE.
- **gyártóspecifikus** adatmodellek: speciális modellek, amelyek csak a gyártó termékeire vagy szolgáltatásaira vonatkoznak.

Ezek az adatmodellek egységes módon teszik lehetővé a hálózati eszközök konfigurálását, megfigyelését és a velük való interakciót. A hálózatautomatizálási eszközök - például a NETCONF, a RESTCONF és a gRPC - YANG adatmodelleket igényelnek.

A YANG az XML adatformátumhoz hasonló hierarchikus fastruktúrát használ. Világos különbséget tesz a konfigurációs adatok és az állapotinformációk között.

KÉP

### A RESTCONF URL

Ahhoz, hogy lekérdezni/módosítani tudjuk az eszköz beállításait, meg kell keresnünk a megfelelő YANG modult, azon belül a megfelelő objektumot, aminek RESTCONF esetén van egy URL-je.

A YANG modult többféleképpen meg lehet találni:

- Github-ról beszerezni: https://github.com/YangModels/yang

  ```bash
  git clone --recurse-submodules https://github.com/YangModels/yang.git`
  ```

- a PYANG segítségével:

  ```bash
  pip3 install pyang`
  $ pyang -f tree ietf-interfaces.yang
  ```

- a yangcatalog.org weboldalon:
  https://yangcatalog.org/yang-search/module_details

Előfordul, hogy több modulban is megtaláljuk a minket érdeklő adatokat (pl. interfész-információkhoz lehet használni a _Cisco-IOS-XE-native_ és az _ietf-interfaces_ modult is).

Az adatmodell kiválasztása után össze kell állítani a RESTCONF URL-t, amin keresztül elérjük a kívánt beállítást (hasonlóan egy weboldal URL-jéhez)

KÉP

### A laboreszközök elérhetősége

A NETCONF és RESTCONF protokollok a hagyományos IOS-en nem elérhetők, viszont a cég modern operációs rendszerein (IOS-XE, IOS-XR, NX-OS), valamint számos egyéb gyártó eszközein igen.

A képzésen IOS-XE rendszert használunk.

A gyakorlatok elvégzéséhez három féle módszer kínálkozik:

- a. : valós eszközök révén

  ISR 4200/4300-as routerek, 3650/3750-es switchek

- b. : CSR1000v virtuális routerrel

  letölthető a https://software.cisco.com oldalról, a Netacad Maintenance keretében

- c. : DevNet Sandbox szolgáltatással

  https://developer.cisco.com/site/sandbox/

### Előzetes eszközkonfiguráció

Ahhoz, hogy távolról elérhessük az eszközeinket, NETCONF esetén az SSH, RESTCONF esetén a HTTPS szolgáltatásnak futnia kell.

A konfiguráció a saját eszközökön:

```bash
hostname isr
ip domain-name etw.netacad.com
crypto key generate rsa modulus 2048
username cisco privilege 15 password cisco123!
netconf-yang
restconf
ip http secure-server
ip http authentication local
line vty 0 4
login local
transport input ssh
```

Tesztelés az eszközön:

```bash
show platform software yang-management process
```

Tesztelés a kliensen:

```bash
curl -k https://router.ip.cime/restconf/ -u "cisco:cisco123!"
```

## Első példa: router állomásnevének lekérdezése

1. Meg kell keresnünk a megfelelő YANG adatmodellt. Ehhez jól használható online eszköz a yangcatalog.com weboldal: https://yangcatalog.org/yang-search/module_details

Offline használhatjuk a **pyang** alkalmazást.

A példában a _Cisco-IOS-XE-native_ modult használjuk, annak _native_ konténerét.

Fa nézetben (Tree view) keressük meg a minket érdeklő beállítást, ez esetünkben a _hostname_ nevű leaf lesz.

A "Sensor Path" oszlop alapján az URL-be beírandó címrészlet: _Cisco-IOS-XE-native:native/hostname_

Ez alapján összeállíthatjuk az eszköznek elküldendő megfelelő kérést. Ennek tesztelésére jól használható parancssori eszköz a **curl**, illetve GUI eszköz a **Postman**.

A curl-el kiadandó parancs (egy sorba írandó!):

```
curl -H "Accept: application/yang-data+json" -k -u "cisco:cisco123!" https://192.168.122.232/restconf/data/Cisco-IOS-XE-native:native/hostname
```

-H: megadjuk a fejléc (header) paraméterben, hogy milyen adatformátumot kérünk

-k: nem ellenőrizzük a szervertanúsítványt

-u: megadjuk a hitelesítési adatokat

2. A példákban a RESTCONF protokollt használjuk, ennek megfelelően írjuk meg a Python programot:

- beimportáljuk a szükséges modulokat, letiltjuk a figyelmeztetéseket:

```python
import json
import requests
requests.packages.urllib3.disable_warnings()
```

- beállítjuk az elküldendő kérés elemeit (URL, fejléc, hitelesítő adatok):

```python
url = "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/Cisco-IOS-XE-native:native/hostname"
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("developer", "C1sco12345")
```

- elküldjük a kérést az eszköznek:

```python
adat = requests.get(url, auth=auth, headers=fejlec, verify=False)
```

- átalakítjuk a kapott választ JSON formátumra, és képezünk belőle egy szótárat (dictionary):

```python
adat_json = adat.json()
print(adat_json)
```

- kiszedjük a minket érdeklő adatot egy változóba:

```python
h = adat_json["Cisco-IOS-XE-native:hostname"]
print("Hosztnév: "+h)
```

Gyakorló példaként kérdezzünk le egyéb adatokat is, pl.:

- napi üzenet
- enable titkos jelszó
- felhasználók nevei
- interfészek neve és leírása

## Második példa: router állomásnevének átállítása

A program nagyrészt egyezik az előzővel, csak a GET utasítás helyett PATCH-et használunk, és megfelelő formátumban el kell küldeni a módosítandó adatot is:

```python
import json
import requests
requests.packages.urllib3.disable_warnings()
url = "https://192.168.122.232/restconf/data/Cisco-IOS-XE-native:native/hostname"
myheaders = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
myauth = ("cisco", "cisco123!")
resp = requests.get(url, auth=myauth, headers=myheaders, verify=False)
akt_hostnev = resp.json()["Cisco-IOS-XE-native:hostname"]
print("Aktuális hosztnév: "+akt_hostnev)
ujnev=input("Kérem az új hosztnevet: ")
yang_adat = {"Cisco-IOS-XE-native:hostname": ujnev }
resp = requests.patch(url, auth=myauth, headers=myheaders, data=json.dumps(yang_adat), verify=False)
print(resp.status_code)
```

## Harmadik példa: loopback interfész létrehozása

Egy új objektum létrehozásához ismét új metódust kell használni (POST), és a megfelelő adatokat átadni. A program első felében bekérjük az interfész paramétereit:

```python
import json
import requests
requests.packages.urllib3.disable_warnings()

url = "https://192.168.122.232/restconf/data/Cisco-IOS-XE-native:native/interface"
myheaders = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
myauth = ("cisco", "cisco123!")

NEV = input("Interfész sorszáma: ")
DESC = input("Interfész leírása: ")
IPCIM = input("IP cím: ")
MASZK = input("Netmaszk: ")
```

A második részben JSON formátumban létrehozzuk az átküldendő adatokat, majd elküldjük, végül kiírjuk a válaszkódot:

```python
data = {'Cisco-IOS-XE-native:Loopback':
          {'name': int(NEV),
           'description': DESC,
           'ip':
              {'address':
                  {'primary':
                     {'address': IPCIM,
                      'mask': MASZK
                     }
                  }
              }
          }
        }
resp = requests.post(url, auth=myauth, headers=myheaders, data=json.dumps(data), verify=False)
print(resp.status_code)
```

## Negyedik példa: loopback interfész törlése

Az előző példában létrehozott interfészt töröljük a DELETE metódussal:

```python
import json
import requests
requests.packages.urllib3.disable_warnings()

NEV = input("Törlendő interfész sorszáma: ")
url = "https://192.168.122.232/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback="+NEV
myheaders = { "Accept": "application/yang-data+json",
              "Content-type":"application/yang-data+json" }
myauth = ("cisco", "cisco123!")

resp = requests.delete(url, auth=myauth, headers=myheaders, verify=False)
print(resp.status_code)
```
