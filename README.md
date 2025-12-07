## Otonom Araç Yol Bulma ve Simülasyon 

Bu projede grid tabanlı bir harita üzerinde **otonom bir aracın** başlangıç noktasından (*S*) hedef noktasına (*G*) güvenli ve uygun bir rota bulmasını sağlayan bir yol planlama sistemi geliştirdim. Haritadaki hareketler **Pygame** kullanılarak gerçek zamanlı olarak simüle edilmektedir.

---

###  Kullanılan Teknolojiler
- Python 3
- Pygame (Grafiksel simülasyon)
- Yol bulma algoritmaları (BFS, Greedy, A*)

---

###  Yol Bulma Algoritmaları

| Algoritma | Açıklama |
|----------|---------|
| **BFS (Breadth First Search)** | Tüm yolları genişlik öncelikli tarar, **kesin en kısa yol** bulur |
| **Greedy Best-First Search** | Hedefe en yakın görünen yola yönelir, hızlıdır ancak **takılabilir** |
| **A\*** | Hem maliyet hem uzaklık hesaplar, **en verimli sonuç** sağlar |

Her bir algoritma çalışırken farklı yollar çizer ve sonuçlar karşılaştırılabilir.

---

###  Trafik Işığı Sistemi
Haritada bir **Trafik Lambası (T)** bulunmaktadır:

- Araç **kırmızıda durur**
- **Yeşil yandığında** devam eder
- Işık durumu zamanlayıcıyla otomatik değişir

Bu sayede araç **trafik kurallarına uyan** bir yapay zekaya dönüşür.

---

###  Dinamik Engel Yönetimi

- Fareyle haritaya yeni engeller ekleyebilirim
- Mevcut engelleri kaldırabilirim
- Rota anında **yeniden hesaplanır**
- Araç **yeni duruma adapte olur**

Gerçek hayattaki **ani yol kapanmalarına** başarılı tepki verir.

---

###  Kullanıcı Kontrolleri

Aşağıdaki tuşlar ile simülasyonu yönetebilirim:

| Tuş | Görev |
|-----|------|
| **1** | BFS algoritması |
| **2** | Greedy algoritması |
| **3** | A\* algoritması |
| **O** | Fare ile **engel ekle/kaldır** |
| **S** | Başlangıç noktasını **fare ile taşı** |
| **G** | Hedef noktasını **fare ile taşı** |
| **T** | Trafik lambasını **fare ile taşı** |
| **R** | Haritayı başlangıca sıfırla |
| **ESC / Close** | Çıkış |

> Kullanıcı haritayı değiştirirken araç **durmaksızın çalışmaya devam eder** ve **yeniden planlama** yapar.

---

###  Harita Yapısı

Harita bir matristir:

| Simge | Anlamı |
|------|-------|
| `S` | Başlangıç |
| `G` | Hedef |
| `T` | Trafik Işığı |
| `0` | Yol |
| `1` | Engel |

Araç hücre hücre ilerler, yol çizgisi simülasyonda mavi olarak gösterilir.

---

###  Projenin Amacı

Bu proje ile:

✔ Otonom araçlarda yol planlamayı  
✔ Yapay zekanın karar alma süreçlerini  
✔ Dinamik engel algılama ve trafik kurallarına uyumu  

gerçek zamanlı bir senaryoda gösterebildim.

---

###  Sonuç

Araç:

- **Hedefe başarılı şekilde ulaşıyor**
- **Her duruma uyarlanarak** rota güncelliyor
- Algoritmalar **karşılaştırılabilir** hale geliyor


