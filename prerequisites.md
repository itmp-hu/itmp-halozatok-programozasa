# Hálózatprogramozás és automatizáció - előfeltételek
## Hardver:
- minimum 8 GB RAM-mal ellátott Windows 10/11 számítógép.
## Szoftver:
- VMware Workstation Pro virtualizációs szoftver <br> 
regisztrációt igénylő hivatalos letöltési hely: [Broadcom weboldala](https://support.broadcom.com/)<br>
Az oldalra belépve a bal oldali “My downloads” kategóriára klikkelve megjelenik a “Free Software Downloads available <u>HERE</u>” felirat. A linket aktiválva kikereshető a VMware Workstation Pro menüpont, válasszuk ki az operációs rendszert és a verziót. El kell olvasni és elfogadni a licenszszerződést, és indulhat a letöltés. 
<b>A telepítés előtt kapcsoljuk ki a “Windows hipervizor platformja”, valamint a Hyper-V szolgáltatásokat!</b>
- [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) SSH kliens és [WinSCP](https://winscp.net/eng/download.php) kliens
- Cisco Modeling Labs (CML) virtuális gép OVA telepítő fájl és RefPlat (Reference Platform) ISO fájl
(az első lépések megtételében segítséget nyújt az Infotanárium [2025. januári előadása](https://infotanarium.hu/archivum/39))
- DEVASC virtuális gép
- CSR1000v virtuális router
Az utóbbiak letölthetők a képzéshez kapcsolódó [Google Drive tárhelyről](https://shorturl.at/TBai1). 

## Előzetes teendők:
A VMware Workstation telepítése után töltsük le a három virtuális gép OVA fájlját, valamint az ISO fájlt. A <b>File/Open...</b> menüpont segítségével importáljuk be elsőként a DEVASC (a DevNet Associate kurzushoz illeszkedő), 
majd a CSR1000v gépet. Ezeket tesztelés jelleggel el is indíthatjuk. A DEVASC gépen a “devasc” felhasználó automatikusan bejelentkezik, de egyébként a jelszava “cisco”. 
A CSR1000v betöltése hosszabb időt vesz igénybe!<br>
A CML gépet importálása után még ne indítsuk el, hanem tegyük be a CD-meghajtójába a RefPlat ISO fájlt. Ne felejtsük el az alsó állapotsorban a CD meghajtót aktiválni (Connect)! Ezután a gép indítható, a lényeges pont az első indulás közben, 
hogy meg kell adni az “admin” és a “sysadmin” felhasználó jelszavait. Figyeljünk rá, hogy alapesetben angol billentyűkiosztás van érvényben! Sikeres betöltés után a megjelenő IP címre irányított böngészőben az “admin” felhasználó nevében tudjuk kezelni a rendszert.<br>
Az egérvezérlés a bal CTRL-ALT billentyűkombinációval szerezhető vissza, ha a virtuális gépek ablakába történő kattintás után elveszne.<br>
A virtuális gépeket úgy állítsuk be, hogy a hálózati kártyájuk a <i>Bridged: Connected directly to the physical network</i> üzemmódban legyen csatlakoztatva.
