# 1. modul - Hálózatprogramozás és automatizáció

## A hagyományos hálózatkezelés és korlátai

A hálózati eszközeink konfigurálása hagyományos módon történhet parancssorból (CLI), vagy távolról Telnet/SSH, SNMP, webes alkalmazások
(CCP, ASDM) segítségével

### A hagyományos eljárás:

- belépünk az eszközökre **egyenként**
- megvizsgáljuk a jelenlegi beállításokat
- kiadjuk a megfelelő konfigurációs parancsokat - ellenőrizzük az eredményt

### Ennek a módszernek a problémái:

- a CLI-ket emberi interakcióra tervezték, gép számára nehezen kiértékelhető pl. egy _show_ parancs kimenete
- ahány eszköz, annyi féle interfész és kimenet (még adott cég eszközein belül is)
- sok eszköz esetében sok időbe telik a beállítás
- az ember hibázhat (főleg ismétlődő feladatoknál)

## Modern hálózatkonfigurálás

### A modern megközelítés:

- a hálózati eszközök szabványos interfészével kommunikálunk: általában hozzá illeszkedve írunk egy programot, ami végrehajtja az adott feladatot
- kell hozzá egy API, illetve szabványos adatleíró nyelvek (XML, JSON, YAML) - no meg némi programozási ismeret :)

### Előnyei:

- a programkód újra felhasználható, átalakítható
- ugyanazon program akár többféle gyártó eszközéhez is felhasználható, kis átalakítással
- sok eszköz gyorsan és hibamentesen felprogramozható

A hálózatprogramozás tulajdonképpen a hálózati eszközök szabványos API-n keresztüli, programok segítségével történő beállítása. Ez az újfajta megközelítés vezet el a Software Defined Networking elnevezésű technológiához is.

## Netmiko

Jelenleg sajnos nem minden eszköz támogatja az SDN modern megközelítését, az SSH viszont minden eszközön elérhető. Írhatunk tehát olyan programokat, amik segítségével

- kapcsolódunk az eszközökhöz,
- lekérdezhetjük, elemezhetjük a beállításaikat,
- ezek alapján pedig átkonfigurálhatjuk őket.

Python-ban a **Paramiko** nevű library ad hozzáférést az SSH funkciókhoz, erre épül a [netmiko](https://github.com/ktbyers/netmiko) nevű függvénykönyvtár, ami kimondottan hálózati eszközök kezelését teszi
lehetővé.

### A [Netmiko](https://pynet.twb-tech.com/blog/netmiko-python-library.html) céljai:

- Hozzon létre SSH-kapcsolatot az eszközzel
- Egyszerűsítse a show parancsok végrehajtását és a kimeneti adatok lekérését
- Egyszerűsítse a konfigurációs parancsok végrehajtását, beleértve az esetleges véglegesítési műveleteket is
- Végezze el a fentieket a hálózati eszközök és platformok széles skáláján. Támogatja többek között a Cisco, HP, Juniper, Arista sokféle eszközét.

Telepíthető a _pip_ (a Python csomagkezelője) segítségével, vagy a Linux disztibúciónk beépített csomagkezelőjével.

### 1. példa

Az első példában kapcsolódunk egy Cisco routerhez, kiadjuk rajta a `show ip interface brief` parancsot, majd az eredményt kiírjuk:

```python
from netmiko import ConnectHandler
router = {              # definiáljuk az eszköz paramétereit egy szótárban
    'device_type': 'cisco_ios',
    'host': '10.10.10.10',
    'username': 'admin',
    'password': 'cisco',
}

# meghívjuk az importált függvényt, átadjuk paraméterként a szótárat:
k = ConnectHandler(**router)

# a send_command metódussal elküldjük a parancsot, az eredményt letároljuk, majd kiíratjuk:
output = k.send_command('show ip int brief')
print(output)
k.disconnect()
```

### 2. példa: trönkportok kiíratása

```python
from netmiko import ConnectHandler
cisco = {'device_type': 'cisco_ios','host': '10.10.10.10','username': 'admin','password': 'cisco'}

k = ConnectHandler(**cisco)
eszkoz = k.find_prompt()
print("A trunk portok a ",eszkoz," switchen:")
output = k.send_command("show interfaces trunk")
for line in output.splitlines(): # szetvágjuk a kimenetet sorokra
    if 'trunking' in line:       # ha szerepel a sorban a trunking szövegrészlet
        sor = line.split()       # szétdaraboljuk az adott sort
        intf = sor[0]            # kiszedjük az első mezőt
        print(intf)              # és kiíratjuk.
k.disconnect()
```

### 3. példa: nem aktív portok adminisztratív lekapcsolása

```python
from netmiko import ConnectHandler
cisco = {'device_type': 'cisco_ios','host': '10.10.10.10','username': 'admin','password': 'cisco'}
k = ConnectHandler(**cisco)
output = k.send_command("show interfaces status")
portok = []
for line in output.splitlines():    # szétvágjuk a kimenetet sorokra
    if 'notconnect' in line:        # ha szerepel a sorban a notconnect szövegrészlet
    sor = line.split()              # szétdaraboljuk az adott sort
    portok.append(sor[0])           # betesszük az interfész-neveket egy listába
for p in portok:
    o1 = k.send_config_set(["interface"+p, "shutdown"])
    print(o1)
k.disconnect()
```

### 4. példa: VTP jelszó egységes beállítása

```python
from netmiko import ConnectHandler
vtpass = input("VTP jelszo:")
s1 = {'device_type': 'cisco_ios','host': '192.168.122.29','username': 'admin','password': 'cisco' }
s2 = {'device_type': 'cisco_ios','host': '192.168.122.30','username': 'admin','password': 'cisco' }
switchlist = [s1, s2]
for switch in switchlist:
    k = ConnectHandler(**switch)
    print(switch["host"]," VTP jelszava:")
    output = k.send_command("show vtp password")
    print(output)
    line = output.split()
    if line[2] != vtpass:
        o1 = k.send_config_set(['vtp password' + vtpass])
        print(o1)
        k.disconnect()
```

## További hasznos lehetőségek

A példákban `k` jelöli a ConnectHandler által visszaadott objektumot.

**Interaktív parancsok kezelése:** olyan parancsok esetén, ahol az eszköz
bevitelre vár (pl. `copy run start`), a `send_command_expect(parancs,
expect_string="vizsgálandó router üzenet")` parancsot használhatjuk.

Ez elküldi a parancsot, majd várja a vizsgálandó router üzenet
megjelenését:

```python
print(k.send_command_expect('copy running-config startup-config',expect_string='Destination filename'))
print(k.send_command_expect('\n', expect_string='#'))
```

További példák: RSA kulcs létrehozása, OSPF resetelése, kiterjesztetett
ping, eszköz újraindítása.

**Konfigurációs parancsok küldése szövegfájlból:**

```python
config_file = 'r1-config.txt'
print(k.send_config_from_file(config_file))
```

## A TextFSM használata

A [TextFSM](https://pynet.twb-tech.com/blog/netmiko-and-textfsm.html) egy Python-modul, amely egy sablon alapú ú.n. állapotgépet
valósít meg "félig formázott" szöveg elemzéséhez. Lehetővé teszi
strukturálatlan adatok bevitelét és strukturált adatokká való
átalakítását. Vagy másképp fogalmazva, vesz egy szövegtömböt, majd
listákká és szótárakká (vagy ezek kombinációivá) alakítja.

A TextFSM engine két bemenetet kap -- egy sablonfájlt és egy szöveget (például egy eszköz parancssori felületének parancsválaszait), és visszaadja a rekordok listáját, amely tartalmazza a szövegből kielemzett adatokat.

A Netmiko beépítve tudja használni a szolgáltatást. Szükséges hozzá az
ntc-templates nevű modul, amit függőségként felrak. Ebben sokféle
eszközhöz előre megírták a legtöbb 'show' parancs kimenetét feldolgozó
sablont, itt ellenőrizhetjük ezeket:

https://github.com/networktocode/ntc-templates/blob/master/ntc_templates/templates/index

Ha a kívánt parancs nincs a listán, akkor hagyományosan sztringként
kapjuk meg a kimenetet.

Használatára példa:

```python
output = k.send_command("show ip route", use_textfsm=True)
print(output)
```

_[{'protocol': 'C', 'type': '', 'network': '10.0.0.0', 'mask': '27',
'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_if':
'Ethernet0/1', 'uptime': ''}, {'protocol': 'L', 'type': '', 'network':
'10.0.0.1', 'mask': '32', 'distance': '', 'metric': '', 'nexthop_ip':
'', 'nexthop_if': 'Ethernet0/1', 'uptime': ''}, {'protocol': 'C',
'type': '', 'network': '10.0.0.96', 'mask': '27', 'distance': '',
'metric': '', 'nexthop_ip': '', 'nexthop_if': 'Ethernet0/0', 'uptime':
''}, {'protocol': 'L', 'type': '', 'network': '10.0.0.97', 'mask': '32',
'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_if':
'Ethernet0/0', 'uptime': ''}\]_
