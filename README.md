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
