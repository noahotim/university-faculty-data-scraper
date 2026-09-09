# Demo — How It Works

Live: **https://github.com/noahotim/university-faculty-data-scraper**

## 1. What it does
Reads `input/Universities.csv` (or `input/Universities_Uganda_All.csv` with all 43 Ugandan universities) → `scraper.py` dispatches per-university parser → `cleaner.py` validates → `image_downloader.py` saves `output/images/` → `output_writer.py` + `excel_tools.py` → `output/universities.csv` + `output/universities.xlsx` + `output/logs/app.log` → `email_sender.py` summary.

## 2. Live demo run (2026-09-09)
Command:
```bash
pip install -r requirements.txt
python main.py
```

Input demo (4 universities):
```
Makerere University - CEDAT, https://cedat.mak.ac.ug/academic-staff/
Gulu University, https://gu.ac.ug/staff_category/academic/
Kyambogo University, https://kyu.ac.ug/faculty-of-science-staff/
Ahmadu Bello University, https://engineering.abu.edu.ng/academic.php
```

Output console:
```
2026-09-09 08:16:49 INFO successfully fetched: https://cedat.mak.ac.ug/academic-staff/
2026-09-09 08:16:49 INFO Makerere CEDAT: found 63 h3 tags
...
2026-09-09 08:17:37 INFO Gulu University: found 5 articles
...
2026-09-09 08:17:49 ERROR Failed to fetch: https://kyu.ac.ug/faculty-of-science-staff/ 404
...
Scraping Completed
Successful Universities: 3
Failed Universities: 1
Total Universities: 4
Valid Lecturer Records: 78
Invalid Lecturer Records: 0
```

Files produced:
```
output/universities.csv  78 records
output/universities.xlsx 78 records
output/images/ 73 .jpg (CEDAT 38 + Gulu 5 + ABU 9 + rest generic)
output/logs/app.log
```

Preview `output/universities.csv`:
```
University,Faculty,Department,Name,Position,Image_url,Image_file
Makerere University,"College of Engineering, Design, Art & Technology",CEDAT,"Prof. Moses Musinguzi, PhD",PhD,https://cedat.mak.ac.ug/.../Prof_Muzinguzi.jpg,output\images\...
```

## 3. All Uganda universities included
`input/Universities_Uganda_All.csv` — 43 universities:
Makerere (CoCIS, CEDAT), Gulu, MUST, Kyambogo, Busitema, Kabale, Lira, Muni, Soroti, MMU, Busoga, UMI, MUBS, KIU, UCU, UMU, IUIU, Ndejje, Nkumba, Bugema, BSU, VU, Cavendish, IUEA, ISBAT, AfRU, ABU, MRU, KU, Kumi, LivingStone, UPU, UNIK, CIU, AKU, ASU, AWU, GLRU, Ibanda, SLAU, Team University, etc.

To run all:
```bash
copy input\Universities_Uganda_All.csv input\Universities.csv
python main.py
```

Generic fallback `scraper.py:128` handles unknown Ugandan sites auto.

## 4. Architecture
`main.py:14` → `input_loader.py:5` → `scraper.py:172 scrape_university` → `cleaner.py:1` → `image_downloader.py:11` → `output_writer.py:9`/`excel_tools.py:8` → `logger.py:7`

