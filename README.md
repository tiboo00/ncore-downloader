# nCore Torrent Downloader

Automatizált torrent letöltő script az ncore.pro oldalhoz. A script lehetővé teszi kategóriák szerinti szűrést, tömeges letöltést, valamint okos folytatási funkcióval rendelkezik.

**FONTOS:** Ez a script egy felhasználó által készített, nyílt forráskódú alkalmazás. Semmilyen formában nem köthető az nCore staff-hoz vagy az nCore fejlesztőihez, nem hivatalos eszköz.

## Főbb Funkciók

- Automatikus bejelentkezés - Cookie-alapú session kezelés
- Kategória szerinti szűrés - 32 különböző kategória közül választhatsz
- Tömeges letöltés - Egyszerre akár több ezer torrent letöltése
- Okos folytatás - Félbehagyott letöltések folytatása
- History követés - Kategóriánként nyilvántartja az utoljára letöltött torrent ID-t
- Rate limiting - Automatikus várakozás minden 25. letöltés után (2 mp)
- Duplikátum kezelés - Fájlnév ütközés esetén automatikus sorszámozás
- Időbecslés - Megmutatja, kb. mennyi ideig fog tartani a letöltés
- Rendezett letöltés - Legrégebbi torrentek felől halad az újabbak felé

## Előfeltételek

- Python 3.6 vagy újabb
- Aktív nCore fiók
- Internetkapcsolat

## Telepítés

### Ubuntu / Debian

```bash
# 1. Python és pip telepítése (ha még nincs)
sudo apt update
sudo apt install python3 python3-pip -y

# 2. Script letöltése
wget https://raw.githubusercontent.com/tiboo00/ncore-downloader/refs/heads/main/ncore_downloader.py
# vagy
git clone https://github.com/tiboo00/ncore-downloader.git
cd ncore-downloader

# 3. Szükséges könyvtárak telepítése
pip3 install requests

# 4. Script futtathatóvá tétele
chmod +x ncore_downloader.py

# 5. Futtatás
python3 ncore_downloader.py
```

### macOS

```bash
# 1. Homebrew telepítése (ha még nincs)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Python telepítése
brew install python3

# 3. Script letöltése
curl -O https://raw.githubusercontent.com/tiboo00/ncore-downloader/refs/heads/main/ncore_downloader.py
# vagy
git clone https://github.com/tiboo00/ncore-downloader.git
cd ncore-downloader

# 4. Szükséges könyvtárak telepítése
pip3 install requests

# 5. Futtatás
python3 ncore_downloader.py
```

### Windows

<details>
<summary>Módszer 1: Python letöltése a hivatalos weboldalról</summary>

```powershell
# 1. Töltsd le a Python-t: https://www.python.org/downloads/
# Telepítés közben pipáld be: "Add Python to PATH"

# 2. Nyisd meg a PowerShell-t vagy Command Prompt-ot

# 3. Szükséges könyvtárak telepítése
pip install requests

# 4. Script letöltése a letöltések mappádba

# 5. Navigálj a script mappájába
cd C:\Users\YourName\Downloads

# 6. Futtatás
python ncore_downloader.py
```
</details>

<details>
<summary>Módszer 2: Chocolatey használata (haladóknak)</summary>

```powershell
# 1. PowerShell futtatása adminisztrátorként

# 2. Python telepítése Chocolatey-vel
choco install python -y

# 3. Szükséges könyvtárak telepítése
pip install requests

# 4. Script futtatása
python ncore_downloader.py
```
</details>

## Konfiguráció

### Első indítás

Amikor először futtatod a scriptet, automatikusan végigvezet a konfigurációs lépéseken:

1. Felhasználónév megadása
2. Jelszó megadása
3. Letöltési mappa megadása (opcionális)
4. Beállítások mentése - eldöntheted, hogy elmented-e a config fájlba

### Kézi konfiguráció

Létrehozhatsz egy `ncore.cfg` fájlt a script könyvtárában:

```ini
username=your_username
password=your_password
download_path=/path/to/downloads
```

**Fontos:** A `download_path` opcionális. Ha nincs megadva, az aktuális mappába tölt le.

## Használat

### Alapvető használat

```bash
python3 ncore_downloader.py
```

### Lépések

1. Bejelentkezés - Automatikus, cookie-alapú
2. Kategória választás - 32 kategória közül választhatsz számmal
3. Mennyiség megadása - Megadhatod, hány torrentet akarsz letölteni
4. Időbecslés - Megmutatja, kb. mennyi ideig fog tartani
5. Megerősítés - Elindítod vagy megszakítod a letöltést
6. Letöltés - Automatikus letöltés, 25 torrentenként 2 mp szünettel

<details>
<summary>Példa használat kimenet</summary>

```
==================================================
nCore Torrent Downloader
==================================================
Bejelentkezés...
Cookies OK, bejelentkezve.

Elérhető kategóriák:
--------------------------------------------------
 1. Film SD/HU
 2. Film SD/EN
 3. Film DVDR/HU
 4. Film DVDR/EN
 5. Film DVD9/HU
 6. Film DVD9/EN
 7. Film HD/HU
 8. Film HD/EN
 9. Sorozat SD/HU
10. Sorozat SD/EN
11. Sorozat DVDR/HU
12. Sorozat DVDR/EN
13. Sorozat HD/HU
14. Sorozat HD/EN
15. Játék PC/ISO
16. Játék PC/RIP
17. Játék Konzol
18. Program PROG/ISO
19. Program PROG/RIP
20. Program PROG/Mobil
21. Könyv eBook/HU
22. Könyv eBook/EN
23. Zene MP3/HU
24. Zene MP3/EN
25. Zene LOSSLESS/HU
26. Zene LOSSLESS/EN
27. Zene Klip
28. XXX SD
29. XXX DVDR
30. XXX Imageset
31. XXX HD
--------------------------------------------------

Válassz egy kategóriát (szám): 21
Kiválasztva: Könyv eBook/HU (ebook_hun)

Kategória lekérdezése: ebook_hun
Összesen 72652 torrent található.
Oldalak: 2907

INFO: A torrentek a legrégebbiek felől haladnak az újabbak felé.
(Rendezés: feltöltési idő szerint növekvő sorrend)

Hány torrentet szeretnél letölteni?
  - Írd be a számot (pl: 50)
  - vagy írd: 'összes' az összes letöltéséhez

Mennyiség: 150

==================================================
Becsült letöltési idő: ~48 másodperc
  • 150 torrent letöltése
  • ~6 x 2 mp várakozás (25 torrentenként)
  • Számítás: ~8 mp / 25 torrent
==================================================

Indítod a letöltést? (i/n): i

Letöltés indítása... (Mentés helye: /home/user/torrents)
Letöltendő: max 150 torrent
(Ctrl+C a megszakításhoz)

--- Oldal 1/2907 ---
[1/150] filename_1.torrent (ID: 9)
[2/150] filename_2.torrent (ID: 11)
...
[25/150] filename_25.torrent (ID: 4133)
  → 25 letöltés megtörtént, várakozás 2 másodperc...

--- Oldal 2/2907 ---
[26/150] filename_26.torrent (ID: 5755)
...

Kész! Összesen 150 új torrent letöltve.
Előzmények mentve: download_history.json
```
</details>

## Folytatási funkciók

### 1. Félbehagyott letöltés folytatása

<details>
<summary>Részletek</summary>

Ha megszakítod a letöltést (Ctrl+C), a következő indításkor felajánlja a folytatást:

```
Található félbehagyott letöltés: ebook_hun
Oldal: 5, Letöltve: 120
Maximum letöltések: 150
Utolsó letöltött torrent ID: 4077551

FIGYELEM: A letöltés a legrégebbi torrentektől folytatódik!
(A torrentek feltöltési idő szerint növekvő sorrendben vannak)

Folytatod a félbehagyott letöltést? (i/n): i
Biztonsági okokból az oldal 5 helyett 1-tól indul.
(A már letöltött torrenteket ID alapján kihagyja)
Folytatás...
```

A script:
- Visszalép 5 oldalt a biztonság kedvéért
- ID alapján kihagyja a már letöltött torrenteket
- Pontosan ott folytatja, ahol abbahagytad
</details>

### 2. History-alapú folytatás

<details>
<summary>Részletek</summary>

Ha már egyszer letöltöttél egy kategóriából, a következő indításkor csak az új torrenteket ajánlja fel:

```
Található korábbi letöltés ebben a kategóriában: ebook_hun
Utolsó letöltött torrent ID: 292607
Csak az új torrenteket töltöd le (utolsó ID után)? (i/n): i
Folytatás az ID 292607 után...

Kategória lekérdezése: ebook_hun
Összesen 72652 torrent található.
Oldalak: 2907

INFO: A torrentek a legrégebbiek felől haladnak az újabbak felé.

Hány ÚJ torrentet szeretnél letölteni (az utolsó ID után)?
  - Írd be a számot (pl: 50)
  - vagy írd: 'összes' az összes letöltéséhez

Mennyiség: 100
100 új torrent letöltése (ID > 292607).
```

Ez lehetővé teszi, hogy:
- Csak az új tartalmakat töltsd le
- Ne kelljen újra letölteni a régieket
- Kategóriánként külön követhető legyen az előrehaladás
</details>

## Fájlok

A script a következő fájlokat hozza létre:

- `ncore.cfg` - Felhasználói beállítások (username, password, download_path)
- `cookies.txt` - Bejelentkezési cookie-k (JSON formátum)
- `download_state.json` - Félbehagyott letöltés állapota
- `download_history.json` - Kategóriánkénti letöltési előzmények

<details>
<summary>download_history.json példa</summary>

```json
{
  "ebook_hun": {
    "last_torrent_id": 4077551,
    "last_download": "2024-12-29 15:30:00"
  },
  "xvid_hun": {
    "last_torrent_id": 5123456,
    "last_download": "2024-12-28 10:15:00"
  },
  "hd_hun": {
    "last_torrent_id": 8765432,
    "last_download": "2024-12-27 20:45:00"
  }
}
```
</details>

## Biztonság

- **Jelszó tárolás**: A jelszó sima szövegként kerül tárolásra a `ncore.cfg` fájlban
- **Fájl jogosultságok**: Ajánlott korlátozni a config fájl hozzáférését:

```bash
chmod 600 ncore.cfg
```

- **Cookie-k**: A bejelentkezési cookie-k a `cookies.txt` fájlban tárolódnak

## Korlátozások

- **Rate limiting**: 25 torrentenként 2 másodperc várakozás (beépített védelem)
- **Torrent fájlok**: Csak .torrent fájlokat tölt le, nem a tartalmakat
- **Session timeout**: Ha a session lejár, automatikusan újra bejelentkezik

## Hibaelhárítás

<details>
<summary>"Login failed" hiba</summary>

```bash
# Ellenőrizd a felhasználónevet és jelszót
cat ncore.cfg

# Töröld a cookie fájlt és próbáld újra
rm cookies.txt
python3 ncore_downloader.py
```
</details>

<details>
<summary>"Permission denied" hiba</summary>

```bash
# Adj futtatási jogot a scriptnek
chmod +x ncore_downloader.py

# Vagy futtasd python-nal
python3 ncore_downloader.py
```
</details>

<details>
<summary>"Module not found: requests" hiba</summary>

```bash
# Telepítsd a requests könyvtárat
pip3 install requests

# Ha nem működik, próbáld:
python3 -m pip install requests
```
</details>

<details>
<summary>Windows: "python is not recognized"</summary>

- Ellenőrizd, hogy a Python telepítve van-e
- Add hozzá a Python-t a PATH környezeti változóhoz
- Indítsd újra a terminált a telepítés után
</details>

## Tippek és trükkök

### Háttérben futtatás (Linux/macOS)

<details>
<summary>nohup használata</summary>

```bash
nohup python3 ncore_downloader.py > output.log 2>&1 &

# Folyamat ellenőrzése
ps aux | grep ncore_downloader

# Folyamat leállítása
kill <PID>
```
</details>

<details>
<summary>screen használata</summary>

```bash
# Új screen session indítása
screen -S ncore

# Script futtatása
python3 ncore_downloader.py

# Leválasztás: Ctrl+A, majd D
# Visszacsatlakozás
screen -r ncore

# Session lista
screen -ls
```
</details>

### Automatizálás cron-nal (Linux/macOS)

<details>
<summary>Cron beállítása</summary>

```bash
# Crontab szerkesztése
crontab -e

# Naponta éjjel 2-kor futtatás
0 2 * * * cd /path/to/script && python3 ncore_downloader.py

# Minden héten vasárnap éjjel 3-kor
0 3 * * 0 cd /path/to/script && python3 ncore_downloader.py

# Minden nap 6 óránként
0 */6 * * * cd /path/to/script && python3 ncore_downloader.py
```
</details>

### Letöltési mappa testreszabása indításkor

Ha nincs elmentve a config-ban, minden indításkor megadhatod:

```
Letöltési útvonal nincs megadva a config fájlban.
Meg szeretnél adni egy letöltési útvonalat? (i/n): i
Letöltési útvonal: /home/user/torrents
El akarod menteni ezt az útvonalat a config fájlba? (i/n): i
Letöltési útvonal elmentve a config fájlba.
```

## Kategóriák

<details>
<summary>Összes elérhető kategória (32 db)</summary>

| Szám | Kategória | Belső kód |
|------|-----------|-----------|
| 1 | Film SD/HU | xvid_hun |
| 2 | Film SD/EN | xvid |
| 3 | Film DVDR/HU | dvd_hun |
| 4 | Film DVDR/EN | dvd |
| 5 | Film DVD9/HU | dvd9_hun |
| 6 | Film DVD9/EN | dvd9 |
| 7 | Film HD/HU | hd_hun |
| 8 | Film HD/EN | hd |
| 9 | Sorozat SD/HU | xvidser_hun |
| 10 | Sorozat SD/EN | xvidser |
| 11 | Sorozat DVDR/HU | dvdser_hun |
| 12 | Sorozat DVDR/EN | dvdser |
| 13 | Sorozat HD/HU | hdser_hun |
| 14 | Sorozat HD/EN | hdser |
| 15 | Játék PC/ISO | game_iso |
| 16 | Játék PC/RIP | game_rip |
| 17 | Játék Konzol | console |
| 18 | Program PROG/ISO | iso |
| 19 | Program PROG/RIP | misc |
| 20 | Program PROG/Mobil | mobil |
| 21 | Könyv eBook/HU | ebook_hun |
| 22 | Könyv eBook/EN | ebook |
| 23 | Zene MP3/HU | mp3_hun |
| 24 | Zene MP3/EN | mp3 |
| 25 | Zene LOSSLESS/HU | lossless_hun |
| 26 | Zene LOSSLESS/EN | lossless |
| 27 | Zene Klip | clip |
| 28 | XXX SD | xxx_xvid |
| 29 | XXX DVDR | xxx_dvd |
| 30 | XXX Imageset | xxx_imageset |
| 31 | XXX HD | xxx_hd |

</details>

## Changelog

<details>
<summary>Verzió előzmények</summary>

### v1.0.0 (2025-01-29)
- Első stabil verzió
- Automatikus bejelentkezés és cookie kezelés
- 32 kategória támogatása
- Tömeges letöltés funkcionalitás
- Félbehagyott letöltések folytatása
- History-alapú inkrementális letöltés
- Rate limiting (25 torrent / 2 mp)
- Időbecslés funkció
- Duplikátum fájlnév kezelés
- Cross-platform támogatás (Linux, macOS, Windows)
- Interaktív config létrehozás
- Biztonsági funkcióként 5 oldallal visszalépés folytatáskor

</details>

## Licenc

Ez a projekt nyílt forráskódú és szabadon felhasználható. Bárki használhatja, módosíthatja és terjesztheti.

## Közreműködés

Hibát találtál? Van ötleted? Nyiss issue-t vagy küldj pull request-et!

## Jogi nyilatkozat

**FONTOS INFORMÁCIÓ:**

- Ez a script egy felhasználó által készített, nyílt forráskódú alkalmazás
- Semmilyen formában nem köthető az nCore staff-hoz vagy az nCore fejlesztőihez
- Nem hivatalos eszköz és nem támogatott az nCore csapata által
- A projekt nyílt forráskódú, bárki szabadon használhatja, módosíthatja és terjesztheti

## Támogatás

Ha problémába ütközöl, először nézd meg a **Hibaelhárítás** szekciót. Ha ott nem találsz megoldást, nyiss egy issue-t a GitHub repository-ban.

---

**Verzió:** 1.0.0  
**Python verzió:** 3.6+  
**Utolsó frissítés:** 2025-01-29