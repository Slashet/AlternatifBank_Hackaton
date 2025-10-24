import psycopg2
try:
    # Azure PostgreSQL bağlantı bilgilerin
    conn = psycopg2.connect(
        host="bank-server.postgres.database.azure.com",
        database="postgres",
        user="bankuser",
        password="pass.word12",
        sslmode="require"
    )

    # SQL çalıştırmak için cursor aç
    cur = conn.cursor()

    cur.execute("SET search_path TO bank;")
except:
    pass

def sendMoney(who):
    # Şema seç

    # Hesapları listele
    cur.execute("SELECT full_name, iban, balance FROM accounts;")
    accounts = cur.fetchall()
    print("📋 Hesaplar:")
    for acc in accounts:
        print(acc)

    # Para gönderme fonksiyonunu test et
    cur.execute("""
        SELECT send_money(
            'TR120006200000000123456789',
            '{}',
            150.00
        );
    """.format(who))

    # Değişiklikleri kaydet
    conn.commit()

    # Transferleri kontrol et
    cur.execute("SELECT * FROM transfers ORDER BY created_at DESC;")
    transfers = cur.fetchall()
    print("\n💸 Transfer Geçmişi:")
    for t in transfers:
        print(t)

    # Bağlantıyı kapat
    cur.close()
    conn.close()