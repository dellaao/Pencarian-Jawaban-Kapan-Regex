from bs4 import BeautifulSoup
from collections import Counter
import requests, lxml
import re

# 1 Cari Pertanyaan ke google search
headers = {
    'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
    'q': 'Kapan Indonesia Merdeka',  # Masukkan pertanyaan disini
    'gl': 'id',  # country to search from
    'hl': 'id',  # language
}

html = requests.get('https://www.google.com/search', headers=headers, params=params)
soup = BeautifulSoup(html.text, "lxml")

# 2 Get url dari hasil google search
url_source = []
for result in soup.select('.tF2Cxc'):
    link = result.select_one('.yuRUbf a')['href']
    if link not in url_source:
        url_source.append(link)

# 3 Hapus tag HTML dari link yang dihasilkan
kumpulan_tanggal = []
kumpulan_tanggal_bulan = []
kumpulan_bulan = []
kumpulan_bulan_tahun = []
kumpulan_tahun = []
kumpulan_tanggal_bulan_tahun =[]

for a in url_source:
    r = requests.get(a, stream=True)
    soup = BeautifulSoup(r.text, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print(text)

# 4 dan 5 Identifikasi jawaban dan kumpul seluruh jawaban
# --------------------------------------------------------
    #4 cari tanggal bulan tahun regex (tanggal)
    cari = re.findall(r"([\d]{1,2})", text)

    #5 Kumpul semua jawaban
    for b in cari:
        kumpulan_tanggal.append(b)

    # --------------------------------------------------------

    # 4 cari tanggal bulan tahun regex (tanggal bulan)
    cari = re.findall(r"[\d]{1,2} [ADFJMNOS]\w*", text)

    # 5 Kumpul semua jawaban
    for b in cari:
        kumpulan_tanggal_bulan.append(b)

    # --------------------------------------------------------

    #4 cari tanggal bulan tahun regex (bulan)
    cari = re.findall(r"\s(Januari|Agustus|Febuari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)", text)

    #5 Kumpul semua jawaban
    for b in cari:
        kumpulan_bulan.append(b)

    # --------------------------------------------------------

    #4 cari tanggal bulan tahun regex (bulan tahun)
    cari = re.findall(r"[ADFJMNOS]\w* [\d]{4}", text)

    #5 Kumpul semua jawaban
    for b in cari:
        kumpulan_bulan_tahun.append(b)

    # --------------------------------------------------------

    # 4 cari tanggal bulan tahun regex (tahun)
    cari = re.findall(r"(?:(?:18|19|20|21)[0-9]{2})", text)

    # 5 Kumpul semua jawaban
    for b in cari:
        kumpulan_tahun.append(b)

    # --------------------------------------------------------

    # 4 cari tanggal bulan tahun regex (tanggal bulan tahun)
    cari = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4}", text)

    # 5 Kumpul semua jawaban
    for b in cari:
        kumpulan_tanggal_bulan_tahun.append(b)

# --------------------------------------------------------

#6 & 7 (Menghitung kata terbanyak & Ambil ranking teratas)
print(Counter(kumpulan_tanggal).most_common(1)[-1])
print(Counter(kumpulan_tanggal_bulan).most_common(1)[-1])
print(Counter(kumpulan_bulan).most_common(1)[-1])
print(Counter(kumpulan_bulan_tahun).most_common(1)[-1])
print(Counter(kumpulan_tahun).most_common(1)[-1])
print(Counter(kumpulan_tanggal_bulan_tahun).most_common(1)[-1])
