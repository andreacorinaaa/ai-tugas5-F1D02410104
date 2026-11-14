import json

with open("aturan_sampah.json", "r", encoding="utf-8") as file:
    data = json.load(file)

aturan = data["aturan"]
pertanyaan = data["pertanyaan"]

fakta = {}
aturan_digunakan = []

tujuan_menu = {
    "1": ("sampah_mudah_terurai", "Sampah mudah terurai"),
    "2": ("sampah_dapat_didaur_ulang", "Sampah dapat didaur ulang"),
    "3": ("sampah_perlu_penanganan_khusus", "Sampah perlu penanganan khusus"),
    "4": ("sampah_dapat_digunakan_kembali", "Sampah dapat digunakan kembali"),
    "5": ("dapat_dipertimbangkan_untuk_kompos", "Kelayakan untuk dipertimbangkan sebagai kompos"),
    "6": ("sampah_residu", "Sampah residu"),
    "7": ("pisahkan_dari_sampah_biasa", "Pemisahan dari sampah biasa"),
    "8": ("periksa_peluang_pemanfaatan_kembali", "Peluang pemanfaatan kembali")
}

def tanya(kondisi):
    if kondisi in fakta:
        return fakta[kondisi]

    teks = pertanyaan[kondisi]
    print("\n" + teks)
    jawaban = input("Jawab (y/n): ").lower().strip()

    while jawaban not in ["y", "n"]:
        print("Jawaban tidak valid. Masukkan y atau n.")
        jawaban = input("Jawab (y/n): ").lower().strip()

    fakta[kondisi] = jawaban == "y"
    return fakta[kondisi]

def buktikan(tujuan, jalur=None):
    if jalur is None:
        jalur = []

    if tujuan in jalur:
        return False

    if tujuan in fakta:
        return fakta[tujuan]

    aturan_tujuan = []

    for rule in aturan:
        if rule["maka"] == tujuan:
            aturan_tujuan.append(rule)

    for rule in aturan_tujuan:
        semua_syarat_benar = True

        for syarat in rule["jika"]:
            if syarat in pertanyaan:
                hasil_syarat = tanya(syarat)
            else:
                hasil_syarat = buktikan(syarat, jalur + [tujuan])

            if not hasil_syarat:
                semua_syarat_benar = False
                break

        if semua_syarat_benar:
            fakta[tujuan] = True

            if rule not in aturan_digunakan:
                aturan_digunakan.append(rule)

            return True

    fakta[tujuan] = False
    return False


print("=" * 58)
print(" SISTEM PAKAR PEMILAHAN SAMPAH RUMAH TANGGA")
print("=" * 58)
print("Pilih kesimpulan yang ingin diperiksa:\n")

for nomor, item in tujuan_menu.items():
    print(nomor + ".", item[1])

pilihan = input("\nMasukkan pilihan (1-8): ").strip()

while pilihan not in tujuan_menu:
    print("Pilihan tidak valid.")
    pilihan = input("Masukkan pilihan (1-8): ").strip()

tujuan = tujuan_menu[pilihan][0]
nama_tujuan = tujuan_menu[pilihan][1]

print("\nTujuan pemeriksaan:", nama_tujuan)
print("Sistem akan menanyakan kondisi yang diperlukan.")

hasil = buktikan(tujuan)

print("\n" + "=" * 58)
print("HASIL PEMERIKSAAN")
print("=" * 58)

if hasil:
    print("Kesimpulan:", nama_tujuan)
    print("\nAlasan dan aturan yang digunakan:")

    for rule in aturan_digunakan:
        print("\n" + rule["id"] + " - " + rule["nama"])
        print("IF          :", " DAN ".join(rule["jika"]))
        print("THEN        :", rule["maka"])
        print("Penjelasan  :", rule["penjelasan"])
        print("Rekomendasi :", rule["rekomendasi"])
else:
    print("Kesimpulan belum dapat dibuktikan.")
    print("Jawaban yang diberikan belum memenuhi syarat aturan.")
    print("Ini tidak berarti jenis sampah sudah diketahui dengan pasti.")

print("\n" + "=" * 58)
print("RINGKASAN PROSES BACKWARD CHAINING")
print("=" * 58)
print("Tujuan diperiksa :", tujuan)
print("Aturan digunakan:", len(aturan_digunakan))

if len(aturan_digunakan) > 0:
    urutan = []

    for rule in aturan_digunakan:
        urutan.append(rule["id"])

    print("Urutan aturan   :", " -> ".join(urutan))
else:
    print("Tidak ada aturan yang berhasil membuktikan tujuan.")


