import hashlib
import math
import random

class HyperLogLog:
    """
    Buyuk Veri Analitigi: Olasiliksal Veri Yapilari
    Cardinality Estimation (Kume Buyuklugu Tahmini) - HyperLogLog Tasarimi
    """
    def __init__(self, p=12):
        """
        p: Hassasiyet parametresi. m = 2^p kova (register) olusturur.
        Standart hata payi yaklasik 1.04 / sqrt(m) formuluyle hesaplanir.
        """
        if not (4 <= p <= 16):
            raise ValueError("p degeri genelde 4 ile 16 arasinda secilmelidir.")
            
        self.p = p
        self.m = 1 << p  # 2^p adet kova (bucket)
        self.registers = [0] * self.m # Her kova baslangicta 0
        self.alpha = self._get_alpha() # Duzeltme katsayisi

    def _get_alpha(self):
        """Kova sayisina (m) gore teorik duzeltme katsayisi (alpha_m) dondurur."""
        if self.m == 16: return 0.673
        elif self.m == 32: return 0.697
        elif self.m == 64: return 0.709
        else: return 0.7213 / (1 + 1.079 / self.m)

    def _hash(self, item):
        """
        Yuksek kaliteli bir hash fonksiyonu (SHA-256).
        Veriyi 64 bitlik bir tamsayiya donusturur.
        """
        hash_hex = hashlib.sha256(str(item).encode('utf-8')).hexdigest()
        return int(hash_hex[:16], 16) # Ilk 16 karakter (64-bit)

    def _rho(self, w):
        """
        Binary formdaki degerde en soldaki (leading) 1 bitinin pozisyonunu bulur.
        Bu, 'ardisik sifir sayisi + 1' degerine esittir.
        """
        if w == 0:
            return 64 - self.p + 1
        return (bin(w)[2:].zfill(64 - self.p)).find('1') + 1

    def add(self, item):
        """Veriyi kovalamaca (bucketing) mantigiyla register'a ekler."""
        x = self._hash(item)
        
        # Ilk p bit kova indeksini belirler
        idx = x >> (64 - self.p)
        
        # Kalan bitler ardisik sifir sayisini belirlemek icin kullanilir
        w = x & ((1 << (64 - self.p)) - 1)
        
        # Register'daki degeri sadece daha buyuk bir sifir serisi bulursak guncelleriz
        self.registers[idx] = max(self.registers[idx], self._rho(w))

    def estimate(self):
        """Harmonik Ortalama kullanarak nihai kume buyuklugunu tahmin eder."""
        # Harmonik Ortalama Formulu: E = alpha * m^2 / sum(2^-Rj)
        sum_registers = sum(2.0**-r for r in self.registers)
        raw_estimate = self.alpha * (self.m**2) * (1.0 / sum_registers)

        # --- Duzeltme Faktorleri (Ref: Flajolet et al.) ---
        
        # 1. Kucuk Veri Duzeltmesi (Linear Counting)
        if raw_estimate <= 2.5 * self.m:
            v = self.registers.count(0) # Bos kova sayisi
            if v != 0:
                return self