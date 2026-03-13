# Büyük Veri Analitiğinde Olasılıksal Veri Yapıları: HyperLogLog Tasarımı

Bu proje, büyük veri setlerinde **Cardinality Estimation** (Küme Büyüklüğü Tahmini) problemini çözmek amacıyla geliştirilen **HyperLogLog (HLL)** algoritmasının sıfırdan tasarımını, gerçeklenmesini ve teorik analizini içermektedir.

## 📖 Proje Hakkında
Geleneksel yöntemler (örneğin HashSet kullanımı), milyonlarca tekil öğeyi saymak için devasa miktarda bellek gerektirir. HyperLogLog, sabit ve çok küçük bir bellek alanı kullanarak (birkaç KB), %2'nin altında bir hata payı ile milyarlarca eşsiz öğeyi tahmin edebilir. Bu projede, algoritmanın tüm temel bileşenleri akademik standartlara uygun olarak kodlanmıştır.

## 🛠️ Teknik Bileşenler
Tasarım süreci şu ana bileşenler üzerine kurulmuştur:

- **Yüksek Kaliteli Hash Fonksiyonu:** Verinin kovalara homojen dağılması ve çarpışmaların minimize edilmesi için `SHA-256` algoritması kullanılmıştır.
- **Kovalama (Bucketing) Mekanizması:** İlk $p$ bit kullanılarak veriler alt kümelere ayrılmış, varyansın düşürülmesi sağlanmıştır.
- **Register Yapısı:** Her kovadaki ardışık sıfır sayıları (`rho` fonksiyonu) takip edilerek, verinin nadirliği istatistiksel olarak kaydedilmiştir.
- **Harmonik Ortalama:** Uç değerlerin (outliers) tahmini saptırmasını engellemek amacıyla aritmetik ortalama yerine harmonik ortalama formülü entegre edilmiştir.
- **Düzeltme Faktörleri:** - Küçük veri setleri için **Linear Counting** düzeltmesi.
  - Büyük veri setleri için logaritmik hata düzeltmeleri.

## 🔗 Birleştirilebilir (Mergeable) Özellik
Algoritma, dağıtık sistemlerde kullanılmaya uygun şekilde tasarlanmıştır. İki farklı veri kaynağından gelen HLL yapıları, ham veri setlerine ihtiyaç duyulmadan sadece register değerleri üzerinden (`bitwise max`) veri kaybı yaşanmadan birleştirilebilir.

## 📊 Teorik Analiz ve Performans
Kova sayısının ($m$) artırılması, varyansı düşürerek tahmin doğruluğunu artırır. Standart hata sınırı şu matematiksel model ile analiz edilmiştir:

$$Standard Error = \frac{1.04}{\sqrt{m}}$$

Proje kapsamında yapılan testlerde, $p=10$ ($m=1024$) değeri için teorik olarak beklenen **%3.25** hata payı sınırı içerisinde sonuçlar elde edildiği doğrulanmıştır.

## 🚀 Kullanım
Projeyi yerel ortamınızda çalıştırmak için:

1. Repoyu klonlayın:
   ```bash
   git clone <repo-url>
