import datetime

class ParkirError(Exception):
    pass

class Parkir:
    def __init__(self):
        self.kendaraan_masuk = {}
        self.histori_transaksi = []
        self.tarif_per_detik = 10000  

    def kendaraan_masuk_area(self, nomor_kendaraan):
        if nomor_kendaraan in self.kendaraan_masuk:
            print("Parkir Error: Kendaraan dengan nomor {} sudah tercatat masuk.".format(nomor_kendaraan))
            return

        waktu_masuk = datetime.datetime.now()
        self.kendaraan_masuk[nomor_kendaraan] = {'waktu_masuk': waktu_masuk, 'sudah_keluar': False}
        print("Waktu masuk kendaraan {} dicatat pada {}".format(nomor_kendaraan, waktu_masuk))
        print("Gerbang masuk terbuka. Silahkan masuk.")

    def kendaraan_keluar_area(self, nomor_kendaraan):
        if nomor_kendaraan not in self.kendaraan_masuk:
            print("Parkir Error: Kendaraan dengan nomor {} tidak tercatat masuk.".format(nomor_kendaraan))
            return

        if self.kendaraan_masuk[nomor_kendaraan]['sudah_keluar']:
            print("Parkir Error: Kendaraan dengan nomor {} sudah keluar sebelumnya.".format(nomor_kendaraan))
            return

        waktu_masuk = self.kendaraan_masuk[nomor_kendaraan]['waktu_masuk']
        waktu_keluar = datetime.datetime.now()
        durasi_parkir = waktu_keluar - waktu_masuk

        total_detik = durasi_parkir.total_seconds()
        total_detik_bulat = max(round(total_detik / 60), 1) * 60

        biaya_parkir = total_detik_bulat / 60 * self.tarif_per_detik
        denda = 0

        if total_detik > 240:
            denda = biaya_parkir * 0.1
            if total_detik > 360:
                denda = biaya_parkir * 0.25

        total_biaya = biaya_parkir + denda

        print("Waktu keluar kendaraan {} dicatat pada {}".format(nomor_kendaraan, waktu_keluar))
        print("Durasi parkir: {} detik".format(total_detik))
        print("Biaya parkir: Rp {:.2f}".format(biaya_parkir))
        print("Denda: Rp {:.2f}".format(denda))
        print("Total biaya: Rp {:.2f}".format(total_biaya))

        self.histori_transaksi.append({
            'Nomor Kendaraan': nomor_kendaraan,
            'Waktu Masuk': waktu_masuk,
            'Waktu Keluar': waktu_keluar,
            'Durasi Parkir': total_detik,
            'Biaya Parkir': biaya_parkir,
            'Denda': denda,
            'Total Biaya': total_biaya
        })

        self.kendaraan_masuk[nomor_kendaraan]['sudah_keluar'] = True  

        while True:
            try:
                nominal_pembayaran = float(input("Masukkan nominal pembayaran: Rp "))
                if nominal_pembayaran < total_biaya:
                    print("Parkir Error: Pembayaran kurang.")
                else:
                    kembalian = nominal_pembayaran - total_biaya
                    print("Pembayaran berhasil. Kembalian: Rp {:.2f}".format(kembalian))
                    print("Gerbang keluar terbuka. Terima Kasih.")
                    break
            except ValueError:
                print("Error: Harap masukkan nilai numerik.")

    def admin_parkir(self, pin):
        if pin != "1234":
            print("Parkir Error: PIN salah.")
            return

        while True:
            print("\nMenu Admin Parkir:")
            print("1. Cetak Seluruh Transaksi Parkir")
            print("2. Keluar")
            choice = input("Pilih menu: ")

            if choice == "1":
                self.cetak_transaksi_parkir()
            elif choice == "2":
                break
            else:
                print("Parkir Error: Pilihan tidak valid.")

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

if __name__ == "__main__":
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
            print("Parkir Error: Pilihan tidak valid.")