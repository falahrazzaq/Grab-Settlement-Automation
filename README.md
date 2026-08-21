# Grab-Settlement-Automation
# Grab Corporate Settlement Automation

Automasi pengisian form settlement Grab (Taxivoucher) pakai Playwright.

## Requirements

- Python 3.8+
- Google Chrome / Chromium (auto-install lewat Playwright)

## Instalasi

```bash
pip install playwright
playwright install chromium
```

## Konfigurasi

Buka `grab_settlement_automation.py`, edit dua bagian di paling atas file:

### 1. `URL`

Paste URL lengkap dengan `authToken` yang masih valid. Token biasanya expired dalam ~1 jam, jadi ambil URL fresh dari browser tiap mau run.

```python
URL = "https://app.metrodata.co.id/Taxivoucher/Default.aspx?authToken=...&client-request-id=..."
```

### 2. `RECORDS`

Isi data booking yang mau diproses. Bisa lebih dari satu record.

```python
RECORDS = [
    {
        "booking_code": "A-XXXXXXXXXXX",
        "so_number": "XXXXXXXXX",
        "charge_type": "Cost",
        "customer_code": "XXXXXXXXXX",
        "customer_pic": "John doe",
        "multiple_location": False,
        "trip_purpose": "Otiwi kantur"
    },
    {
        "booking_code": "A-XXXXXXXXXXX",
        "so_number": "XXXXXXXXX",
        "charge_type": "Cost",
        "customer_code": "XXXXXXXXXX",
        "customer_pic": "John doe",
        "multiple_location": False,
        "trip_purpose": "Otiwi kantur"
    },
    # tambah record lain di sini, copy blok di atas (multiple input)
]
```

| Field | Keterangan |
|---|---|
| `booking_code` | Kode booking Grab (format `A-...`) |
| `so_number` | Nomor SO yang akan dicari & divalidasi |
| `charge_type` | Value dropdown Charge Type (contoh: `"Cost"`) |
| `customer_code` | Kode customer (dicari lewat popup Customer Lookup) |
| `customer_pic` | Nama PIC customer, diisi manual ke field Customer PIC |
| `multiple_location` | `True` / `False` — centang checkbox Multiple Location |
| `trip_purpose` | Teks tujuan perjalanan |

**Catatan:** `Part Number`, `Charge to Company`, dan `Charge to Department` **tidak** diisi script — dibiarkan sesuai auto-populate dari website setelah SO valid.

## Menjalankan

```bash
python grab_settlement_automation.py
```

## Alur Eksekusi

1. Browser Chromium terbuka (bukan headless, jadi keliatan prosesnya)
2. Jika diminta login manual → login di browser, lalu tekan `ENTER` di terminal
3. Untuk tiap record, script akan:
   - Isi Booking Code → klik Settle
   - Pilih Charge Type
   - Cari & pilih SO (validasi SO yang ditemukan cocok dengan yang diminta)
   - Klik Check SO
   - Cari & pilih Customer (validasi Customer ID yang ditemukan cocok)
   - Isi Customer PIC
   - Set Multiple Location
   - Isi Trip Purpose
   - Validasi ulang semua value sebelum submit
4. **Safety pause**: sebelum klik Confirm Settlement, script berhenti dan minta `ENTER` supaya lo bisa cek dulu semua data di form
5. Jika record error, screenshot otomatis disimpan (`error_<booking_code>.png`), lalu ditanya lanjut ke record berikutnya atau stop
6. Di akhir, ringkasan status semua record ditampilkan

## Mode Full-Auto (opsional)

Untuk skip safety pause per record, ubah di dalam `process_record()`:

```python
CONFIRM_AUTOMATICALLY = False   # ganti jadi True
```

⚠️ Pakai dengan hati-hati — ini langsung submit settlement tanpa konfirmasi manual.

## Troubleshooting

| Masalah | Penyebab umum |
|---|---|
| `SO mismatch!` / `Customer mismatch!` | Nomor SO / kode customer salah, atau data belum terdaftar di sistem |
| Field disabled terus | Halaman belum selesai postback — coba naikkan `wait_for_page_update` timeout |
| Auth error / redirect ke login | Token di `URL` sudah expired — ambil ulang dari browser |
