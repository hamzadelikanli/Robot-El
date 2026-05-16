
# Robot-El
Bu proje, bilgisayarlı görü (Computer Vision) teknikleri kullanarak insan el hareketlerini gerçek zamanlı olarak algılayan ve fiziksel bir robot ele aktaran otonom bir sistemdir. Aynı zamanda sistem, kullanıcısıyla karşılıklı Taş-Kağıt-Makas oynayabilen bir yapay zeka oyun mantığına ve gerçekçi bir sesli geri bildirim sistemine sahiptir.

Özellikler
Gerçek Zamanlı Taklit: Eldiven veya fiziksel sensör gerektirmeden, sadece kamera görüntüsü üzerinden parmak hareketlerini algılar ve motorlara aktarır.

Taş-Kağıt-Makas Modu: Sistemin sadece bir "ayna" olmadığını kanıtlayan interaktif oyun modu. Robot sizin hamlenizi okur, kendi yapay zekasıyla bir hamle seçer ve sonucu belirler.

Masaüstü Arayüzü (GUI): Terminal ekranı yerine, kamera görüntüsünün ve oyun sonuçlarının anlık olarak takip edilebildiği, kullanımı kolay modern bir Tkinter arayüzü.

Gerçekçi Sesli Geri Bildirim: Robotik sesler yerine, Microsoft Edge TTS (Neural Voice) kullanılarak sisteme doğal, vurgulu ve gerçekçi bir karakter sesi kazandırılmıştır.
Kullanılan Teknolojiler
Yazılım (Python):

OpenCV: Kamera kontrolü ve görüntü işleme.

Google MediaPipe: El iskeleti çıkarma (Hand Landmark Detection).

Tkinter & Pillow: Masaüstü kullanıcı arayüzü (GUI).

Edge-TTS & PyGame: Yeni nesil sinirsel yapay zeka sesi oluşturma ve oynatma.

PySerial: Python ve Arduino arası seri haberleşme.

Donanım:

Arduino (UNO / Nano)

5x Servo Motor (Her parmak için bir adet)

İp/Misine tabanlı parmak çekme mekanizması

Webcam

https://github.com/user-attachments/assets/6da20d3f-c25b-40df-8d69-c199aab65c5d

<img width="1536" height="2048" alt="WhatsApp Image 2026-05-16 at 11 04 34 (3)" src="https://github.com/user-attachments/assets/10a33e97-d427-4f15-85b6-5713d995f26d" />
<img width="1152" height="2048" alt="WhatsApp Image 2026-05-16 at 11 04 34 (2)" src="https://github.com/user-attachments/assets/60931787-0584-4cc2-ac05-819ec0bce668" />
<img width="1152" height="2048" alt="WhatsApp Image 2026-05-16 at 11 04 34 (1)" src="https://github.com/user-attachments/assets/9df1b7e0-ea4b-47c4-910c-445e8ec75c4c" />
<img width="1152" height="2048" alt="WhatsApp Image 2026-05-16 at 11 04 39" src="https://github.com/user-attachments/assets/6f644314-707a-464e-88e1-d2d425b2b819" />
