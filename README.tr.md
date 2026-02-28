# Rope Simulation

Bu proje, **Verlet entegrasyonu** kullanarak fizik tabanlı ip simülasyonu yapar. Kullanıcı etkileşimli olarak ipi hareket ettirebilir, yerçekimini ve sönümlemeyi ayarlayabilir.

## Özellikler

- **Verlet Entegrasyonu**: Gerçekçi fizik simülasyonu için Verlet entegrasyonu kullanılır.
- **İnteraktif Kullanım**: Fare ile ip segmentlerini sürükle ve bırak.
- **Gerçek Zamanlı Ayarlar**: Yerçekimi, sönümleme, segment sayısı ve segment uzunluğu ayarları.
- **Kamera Sistemi**: Zoom (yakınlaş/uzaklaş), pan (kamera hareketi) özellikleri.
- **Etkileşimli Arayüz**: Kaydırma çubukları (slider) ve butonlarla kolay kontrol.

## Kullanılan Teknolojiler

| Teknoloji | Versiyon | Açıklama |
|-----------|----------|----------|
| **Python** | `3.14` | Ana programlama dili |
| **Pygame** | `2.6.1` | 2D grafikler, oyun döngüsü ve kullanıcı arayüzü |

### Paket Yapısı

```
rope_sim/
├── src/
│   ├── main.py          # Ana giriş noktası ve oyun döngüsü
│   ├── requirements.txt # Bağımlılıklar (pygame==2.6.1)
│   ├── rope.py          # Rope sınıfı (Verlet entegrasyonu)
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── particle.py  # Partikül (kütle) sınıfı
│   │   └── constraint.py # Constraint (mesafe kısıtlaması) sınıfı
│   └── gui/
│       ├── __init__.py
│       └── gui.py       # Kullanıcı arayüzü sınıfları
└── venv/                # Python sanal ortamı
```

## Kurulum

1. **Depoyu klonla**
```bash
git clone <repourl>
cd rope_sim
```

2. **Sanal ortam oluştur ve aktif et**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükle**
```bash
cd src
pip install -r requirements.txt
```

## Çalıştırma

```bash
cd src
python main.py
```

### Tuş Kontrolleri

| Tuş | Fonksiyon |
|-----|----------|
| `SPACE` | Simülasyonu başlat/durdur |
| `R` | İpi sıfırla |
| `ESC` | Çıkış |
| `+` / `Kp+` | Yakınlaş |
| `-` | Uzaklaş |
| `Sürükle` | İp segmentlerini hareket ettir |

### UI Kontrolleri

- **Reset Rope**: İpi başlangıç konumuna sıfırla
- **Gravity Slider**: Yerçekimi kuvveti (0.1 - 2.5)
- **Damping Slider**: Sönümleme katsayısı (0.85 - 1.0)
- **Segments Slider**: Segment sayısı (2 - 5000)
- **Segment Length Slider**: Her segmentin uzunluğu (15 - 187)
- **Zoom +/-/Reset**: Kamera yakınlaştırma kontrolü

## Teknik Detaylar

### Verlet Entegrasyonu

Proje, fizik simülasyonu için Verlet entegrasyonu yöntemini kullanır:

```
v = (current_pos - old_pos) * damping
new_pos = current_pos + v + gravity * dt²
```

Bu yöntem, numerik stabilite sağlar ve ip gibi esnek yapıların gerçekçi görünmesine yardımcı olur.

### Sistem Bileşenleri

1. **Particle (Partikül)**
   - Kütle temsil eder
   - Pozisyon, velocity, kütle bilgilerini tutar
   - `is_fixed`: Sabit nokta mı?
   - `is_being_dragged`: Kullanıcı sürüklüyor mu?

2. **Constraint (Kısıtlama)**
   - İki partikül arasındaki mesafeyi sabit tutar
   - Stiffness (katılık) parametresiyle esneklik kontrolü
   - Iteratif çözüm ile stabilite sağlar

3. **Rope (İp)**
   - Parçacıklar ve kısıtlamaları birleştirir
   - `update()`: Fizik güncellemesi
   - `draw()`: Ekran çizimi
   - `drag_particle()`: Fare ile etkileşim

4. **Camera (Kamera)**
   - Zoom ve pan işlemleri
   - Dünya koordinatları ↔ Ekran koordinatları dönüşümü

## Ekran Görüntüsü

Simülasyon ekranı şu bileşenleri içerir:

- **Arka plan**: Grid (ızgara) sistemi
- **İp**: Beyaz partiküller ve gri segmentler
- **UI Paneli**: Sağ üst köşede parametre ayarları
- **Bilgi Paneli**: Gerçek zamanlı simülasyon istatistikleri

---

**Not**: Proje, eğitim amaçlı bir fizik simülasyonudur. Pygame kütühanesi ile yazılmıştır.

**Vibe Coding Notu**: Bu proje, vibe coding ile yaklaşık 2 saatlik çalışma sonucunda geliştirilmiştir.
