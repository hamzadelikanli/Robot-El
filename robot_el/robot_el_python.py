import cv2
import mediapipe as mp
import serial
import time
import os
import random
import pygame

# --- 1. GERÇEKÇİ YAPAY ZEKA SES AYARLARI (Edge TTS) ---
pygame.mixer.init()
ses_dosyasi = "robot_gercekcii_selam.mp3" # Eski sesle karışmaması için yeni isim verdik

def ses_olustur_ve_cal(metin, dosya_adi):
    # Dosya yoksa edge-tts ile yeni nesil sesi oluştur
    if not os.path.exists(dosya_adi):
        print("Gerçekçi yapay zeka sesi hazırlanıyor, lütfen bekleyin...")
        try:
            # DÜZELTME BURADA: Terminal hatasını önlemek için "python -m edge_tts" kullanıyoruz
            komut = f'python -m edge_tts --voice tr-TR-AhmetNeural --text "{metin}" --write-media {dosya_adi}'
            os.system(komut)
        except Exception as e:
            print("Ses oluşturulurken hata:", e)
            return

    # Sesi çal
    try:
        dosya_yolu = os.path.abspath(dosya_adi)
        pygame.mixer.music.load(dosya_yolu)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Ses çalınamadı hatası: {e}")

# --- 2. ARDUINO BAĞLANTISI ---
try:
    # Portunu kendi bilgisayarına göre kontrol et (Örn: COM4)
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=0.05)
    time.sleep(2)
    print("Arduino başarıyla bağlandı!")
except Exception as e:
    print(f"Arduino bulunamadı! Portu kontrol et. Hata: {e}")

# --- BAŞLANGIÇ SELAMINI VER ---
print("Robot selam veriyor...")
acilis_metni = "Selam millet! Henüz tam bir vücudum yok, şimdilik sadece mekanik bir elden ibaretim... Ama inanın bana, taş kağıt makasta beni yenmeniz çok zor! Denemeye ne dersiniz?"
ses_olustur_ve_cal(acilis_metni, ses_dosyasi)

# --- 3. MEDIAPIPE AYARLARI ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
tip_ids = [4, 8, 12, 16, 20]

# --- OYUN DEĞİŞKENLERİ ---
oyun_modu = False
oyun_baslama_zamani = 0
robotun_hamlesi = []
oyun_durumu = "BEKLEMEDE" # BEKLEMEDE, SAYIM, SONUC
insan_hamlesi_metin = ""
robot_hamlesi_metin = ""
sonuc_metin = ""

# Hamle açıları (Baş, İşaret, Orta, Yüzük, Serçe)
HAMLELER = {
    "TAS": [0, 0, 0, 0, 0],
    "KAGIT": [180, 180, 180, 180, 180], # Robot kağıt yaparken serçe kasıyorsa sondaki 180'i düşürebilirsin
    "MAKAS": [0, 180, 180, 0, 0]
}
hamle_listesi = ["TAS", "KAGIT", "MAKAS"]

def el_hareketi_tani(acilar):
    """MediaPipe'tan gelen açılara bakarak insanın el şeklini tahmin eder."""
    acik_parmak_sayisi = sum([1 for aci in acilar if aci > 90])
    
    if acik_parmak_sayisi <= 1:
        return "TAS"
    elif acik_parmak_sayisi >= 4:
        return "KAGIT"
    elif acilar[1] > 90 and acilar[2] > 90 and acilar[3] < 90 and acilar[4] < 90:
        return "MAKAS"
    else:
        return "BILINMEYEN"

# --- 4. ANA DÖNGÜ ---
while cap.isOpened():
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    angles = [0, 0, 0, 0, 0]

    # KLAVYE KONTROLÜ
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' ') and oyun_durumu == "BEKLEMEDE":
        # Boşluk tuşuna basıldığında oyunu başlat
        oyun_durumu = "SAYIM"
        oyun_baslama_zamani = time.time()
        sonuc_metin = ""

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                lm_list.append([int(lm.x * w), int(lm.y * h)])

            if lm_list:
                # Baş parmak kontrolü
                if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0]-1][0]: 
                    angles[0] = 180
                
                # Diğer parmakların kontrolü
                for i in range(1, 5):
                    if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i]-2][1]: 
                        
                        # EĞER SERÇE PARMAK (i==4) KASIYORSA BURADAKİ AÇIYI DEĞİŞTİR!
                        if i == 4:
                            angles[i] = 180 # <-- Serçe parmak açısı (Kasarsa burayı 90 veya 110 yap)
                        else:
                            angles[i] = 180
            
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    # --- OYUN MANTIĞI ---
    if oyun_durumu == "BEKLEMEDE":
        # Normal taklit modu
        cv2.putText(img, "Taklit Modu - Oynamak icin BOSLUK tusuna bas", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Açıları Arduino'ya gönder
        cmd = ",".join(map(str, angles)) + "\n"
        if 'arduino' in locals() and arduino.is_open:
            try:
                arduino.write(cmd.encode())
            except: pass

    elif oyun_durumu == "SAYIM":
        gecen_sure = time.time() - oyun_baslama_zamani
        
        if gecen_sure < 1.0:
            cv2.putText(img, "TAS...", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        elif gecen_sure < 2.0:
            cv2.putText(img, "KAGIT...", (180, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        elif gecen_sure < 3.0:
            cv2.putText(img, "MAKAS!", (160, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        else:
            # Saniye doldu, hamleleri al
            insan_hamlesi_metin = el_hareketi_tani(angles)
            robot_hamlesi_metin = random.choice(hamle_listesi)
            robotun_hamlesi = HAMLELER[robot_hamlesi_metin]
            
            # Robotun hamlesini Arduino'ya gönder
            cmd = ",".join(map(str, robotun_hamlesi)) + "\n"
            if 'arduino' in locals() and arduino.is_open:
                try:
                    arduino.write(cmd.encode())
                except: pass
            
            # Kazananı Belirle
            if insan_hamlesi_metin == "BILINMEYEN":
                sonuc_metin = "Hamleni anlayamadim!"
            elif insan_hamlesi_metin == robot_hamlesi_metin:
                sonuc_metin = "Berabere!"
            elif (insan_hamlesi_metin == "TAS" and robot_hamlesi_metin == "MAKAS") or \
                 (insan_hamlesi_metin == "KAGIT" and robot_hamlesi_metin == "TAS") or \
                 (insan_hamlesi_metin == "MAKAS" and robot_hamlesi_metin == "KAGIT"):
                sonuc_metin = "SEN KAZANDIN!"
            else:
                sonuc_metin = "ROBOT KAZANDI!"
                
            oyun_durumu = "SONUC"
            oyun_baslama_zamani = time.time() # Sonucu ekranda tutmak için zamanı sıfırla

    elif oyun_durumu == "SONUC":
        cv2.putText(img, f"Sen: {insan_hamlesi_metin}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, f"Robot: {robot_hamlesi_metin}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, sonuc_metin, (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        
        # 4 saniye sonucu göster, sonra taklit moduna dön
        if time.time() - oyun_baslama_zamani > 4.0:
            oyun_durumu = "BEKLEMEDE"

    cv2.imshow("Otonom Robot El", img)

cap.release()
if 'arduino' in locals() and arduino.is_open:
    arduino.close()
cv2.destroyAllWindows() 