import datetime

# Exception untuk kasus khusus pada aplikasi parkir
class ParkirError(Exception):
    pass

# Kelas utama aplikasi parkir
class Parkir:
    def __init__(self):
        # Dictionary untuk menyimpan data kendaraan yang masuk dan histori transaksi
        self.kendaraan_masuk = {}
        self.histori_transaksi = []
        # Tarif parkir per detik (default: Rp 10.000 per 60 detik)
        self.tarif_per_detik = 10000  
        # Durasi maksimal tarif parkir (4 menit)
        self.durasi_max_tarif = 240  

    # Fungsi untuk mencatat masuknya kendaraan ke dalam area parkir
    def kendaraan_masuk_area(self, nomor_kendaraan):
        try:
            if nomor_kendaraan in self.kendaraan_masuk:
                raise ParkirError("Kendaraan dengan nomor {} sudah tercatat masuk.".format(nomor_kendaraan))

            waktu_masuk = datetime.datetime.now()
            self.kendaraan_masuk[nomor_kendaraan] = {'waktu_masuk': waktu_masuk, 'sudah_keluar': False}
            print("Waktu masuk kendaraan {} dicatat pada {}".format(nomor_kendaraan, waktu_masuk))
            print("Gerbang masuk terbuka. Silahkan masuk.")
        except ParkirError as e:
            print("Parkir Error:", str(e))

    # Fungsi untuk mencatat keluarnya kendaraan dari area parkir
    def kendaraan_keluar_area(self, nomor_kendaraan):
        try:
            if nomor_kendaraan not in self.kendaraan_masuk:
                raise ParkirError("Kendaraan dengan nomor {} tidak tercatat masuk.".format(nomor_kendaraan))
            
            if self.kendaraan_masuk[nomor_kendaraan]['sudah_keluar']:
                raise ParkirError("Kendaraan dengan nomor {} sudah keluar sebelumnya.".format(nomor_kendaraan))

            waktu_masuk = self.kendaraan_masuk[nomor_kendaraan]
            waktu_keluar = datetime.datetime.now()
            durasi_parkir = waktu_keluar - waktu_masuk

            total_detik = durasi_parkir.total_seconds()
            total_detik_bulat = max(round(total_detik / 60), 1) * 60  # Pembulatan waktu parkir (minimal 60 detik)

            # Maksimal waktu parkir adalah 4 menit (240 detik)
            total_detik_bulat = min(total_detik_bulat, self.durasi_max_tarif)

            biaya_parkir = total_detik_bulat / 60 * self.tarif_per_detik
            denda = 0

            # Logika penentuan denda berdasarkan durasi parkir
            if total_detik > self.durasi_max_tarif:  # Lebih dari 4 menit
                denda = biaya_parkir * 0.1  # Denda 10% dari total biaya
                if total_detik > 360:  # Lebih dari 6 menit
                    denda = biaya_parkir * 0.25  # Denda 25% dari total biaya

            total_biaya = biaya_parkir + denda

            # Menampilkan informasi transaksi
            print("Waktu keluar kendaraan {} dicatat pada {}".format(nomor_kendaraan, waktu_keluar))
            print("Durasi parkir: {} detik".format(total_detik))
            print("Biaya parkir: Rp {:.2f}".format(biaya_parkir))
            print("Denda: Rp {:.2f}".format(denda))
            print("Total biaya: Rp {:.2f}".format(total_biaya))

            # Merekam transaksi ke dalam histori transaksi
            self.histori_transaksi.append({
                'Nomor Kendaraan': nomor_kendaraan,
                'Waktu Masuk': waktu_masuk,
                'Waktu Keluar': waktu_keluar,
                'Durasi Parkir': total_detik,
                'Biaya Parkir': biaya_parkir,
                'Denda': denda,
                'Total Biaya': total_biaya
            })

            # Menghapus kendaraan dari daftar yang masih masuk
            self.kendaraan_masuk.pop(nomor_kendaraan)  

            # Proses pembayaran
            while True:
                try:
                    nominal_pembayaran = float(input("Masukkan nominal pembayaran: Rp "))
                    if nominal_pembayaran < total_biaya:
                        raise ParkirError("Pembayaran kurang.")
                    else:
                        kembalian = nominal_pembayaran - total_biaya
                        print("Pembayaran berhasil. Kembalian: Rp {:.2f}".format(kembalian))
                        print("Gerbang keluar terbuka. Terima Kasih.")
                        break
                except ValueError:
                    print("Error: Harap masukkan nilai numerik.")
        except ParkirError as e:
            print("Error:", str(e))

    # Fungsi untuk menu admin parkir
    def admin_parkir(self, pin):
        if pin != "1234":  # PIN admin parkir (ganti sesuai kebutuhan)
            print("Error: PIN salah.")
            return

        while True:
            print("\nMenu Admin Parkir:")
            print("1. Cetak Seluruh Transaksi Parkir")
            print("2. Kendaraan Sedang Parkir")
            print("3. Keluar")
            choice = input("Pilih menu: ")

            if choice == "1":
                self.cetak_transaksi_parkir()
            elif choice == "2":
                self.cetak_kendaraan_sedang_parkir()
            elif choice == "3":
                break
            else:
                print("Error: Pilihan tidak valid.")

    # Fungsi untuk mencetak seluruh transaksi parkir
    def cetak_transaksi_parkir(self):
        print("\nSeluruh Transaksi Parkir:")
        for transaksi in self.histori_transaksi:
            print("Nomor Kendaraan: {}".format(transaksi['Nomor Kendaraan']))
            print("Waktu Masuk: {}".format(transaksi['Waktu Masuk']))
            print("Waktu Keluar: {}".format(transaksi['Waktu Keluar']))
            print("Durasi Parkir: {} detik".format(transaksi['Durasi Parkir']))
            print("Biaya Parkir: Rp {:.2f}".format(transaksi['Biaya Parkir']))
            print("Denda: Rp {:.2f}".format(transaksi['Denda']))
            print("Total Biaya: Rp {:.2f}".format(transaksi['Total Biaya']))
            print("--------------------")

    # Fungsi untuk mencetak kendaraan yang sedang parkir
    def cetak_kendaraan_sedang_parkir(self):
        print("\nKendaraan Sedang Parkir:")
        for nomor_kendaraan, waktu_masuk in self.kendaraan_masuk.items():
            print("Nomor Kendaraan: {}".format(nomor_kendaraan))
            print("Waktu Masuk: {}".format(waktu_masuk))
            print("--------------------")

if __name__ == "__main__":
    # Inisialisasi objek aplikasi parkir
    parkir_app = Parkir()

    while True:
        print("\nMenu Utama:")
        print("1. Masuk Area Parkir")
        print("2. Keluar Area Parkir")
        print("3. Admin Parkir")
        print("4. Keluar Aplikasi")
        choice = input("Pilih menu: ")

        if choice == "1":
            nomor_kendaraan = input("Masukkan nomor kendaraan: ")
            parkir_app.kendaraan_masuk_area(nomor_kendaraan)
        elif choice == "2":
            nomor_kendaraan = input("Masukkan nomor kendaraan: ")
            parkir_app.kendaraan_keluar_area(nomor_kendaraan)
        elif choice == "3":
            pin_admin = input("Masukkan PIN Admin Parkir: ")
            parkir_app.admin_parkir(pin_admin)
        elif choice == "4":
            break
        else:
            print("Error: Pilihan tidak valid.")
