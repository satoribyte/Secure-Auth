# Secure Auth Application

Secure Auth Application adalah aplikasi autentikasi berbasis Flask dengan fitur keamanan tingkat lanjut, termasuk autentikasi pengguna, perlindungan CSRF, 2FA, dan rate limiting.

## **Fitur Utama**
- User registration dengan password hashing (bcrypt)
- Login dengan autentikasi yang aman
- Rate limiting untuk mencegah brute-force attack
- Proteksi CSRF pada form
- Two-factor authentication (2FA) berbasis OTP

---

## **Instalasi & Setup**

1. **Clone repository**  
   ```bash
   git clone https://github.com/satoribyte/Secure-Auth.git
   cd Secure-Auth
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database (SQLite/MySQL/PostgreSQL)**  
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Jalankan aplikasi**  
   ```bash
   python app.py
   ```

5. **Akses di browser**  
   ```
   http://127.0.0.1:5000
   ```

---

## **Cara Menggunakan 2FA**
1. **Aktifkan 2FA pada akun setelah login**  
2. **Gunakan aplikasi seperti Google Authenticator atau Authy** untuk scan QR Code  
3. **Saat login berikutnya, masukkan kode OTP yang diberikan oleh aplikasi 2FA**

---

## **Dev**
- **Deni Gentar Candana**