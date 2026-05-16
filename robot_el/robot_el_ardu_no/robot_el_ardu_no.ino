#include <Servo.h>

Servo servos[5];
// Pinleri sırasıyla: Baş, İşaret, Orta, Yüzük, Serçe (Kendi bağlantına göre değiştirebilirsin)
int pins[] = {2, 3, 4, 5, 6}; 

void setup() {
  // Python ile aynı haberleşme hızını (Baud Rate) ayarlıyoruz
  Serial.begin(115200);
  Serial.setTimeout(10); // Gecikmeyi önlemek için timeout'u kısalttık
  
  // Servoları pinlere bağla ve başlangıçta 0 dereceye al
  for(int i = 0; i < 5; i++) {
    servos[i].attach(pins[i]);
    servos[i].write(0);
  }
}

void loop() {
  // PYTHON'DAN VEYA SERİ PORTTAN GELEN MOTOR AÇILARINI OKU
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // "Enter" (yeni satır) karakterine kadar oku
    data.trim(); // Başındaki ve sonundaki boşluk/satır sonu karakterlerini temizle
    
    // Veri geçerliyse motorlara yaz
    if (data.length() > 0) {
      int commaIndex;
      for (int i = 0; i < 5; i++) {
        commaIndex = data.indexOf(',');
        
        // Virgül bulursa o kısma kadar olanı al, bulamazsa kalanı al
        String val = (commaIndex != -1) ? data.substring(0, commaIndex) : data;
        
        // Açıyı motora yaz
        servos[i].write(val.toInt());
        
        // İşlenen kısmı metinden atıp geri kalanıyla devam et
        if (commaIndex != -1) {
          data = data.substring(commaIndex + 1);
        }
      }
    }
  }
}