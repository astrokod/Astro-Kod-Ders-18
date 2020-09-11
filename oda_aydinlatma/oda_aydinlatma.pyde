# walls ve source adlı global değişkenler
walls = []
source = None

# Setup Fonksiyonu
def setup():
    # walls ve source'u global scpoe'tan al
    global walls, source
    #750x750'lik bir pencere oluştur
    size(750, 750)
    
    # 10 tane rastgele duvar oluştur
    for _ in range(10):
        walls.append(Wall(PVector(random(0, width), random(0, width)),
                          PVector(random(0, height), random(0, height))))
    
    # pencerenin tam ortsında bir kaynak oluştur
    source = Source(PVector(width/2, height/2), step=15)
    
# Draw fonksiyonu
def draw():
    # Arka alanı siyah yap
    background(0)
    
    # Işınları oluştur
    source.create_rays(walls)
    
    # Duvarları beyaz ve 4 piksel kalınlığında göster
    stroke(255)
    strokeWeight(4)
    for wall in walls:
        wall.show()
        
    # Kaynağı sarı, 75/255 oranda saydam ve 2 piksel kalınlığında göter
    stroke(255, 255, 0, 75)
    strokeWeight(2)
    source.show()
    # Kaynağın konumunu güncelle
    source.update_pos(PVector(mouseX, mouseY))

# Mouse'a tıklandığında fonksiyonu
def mousePressed():
    # walls'u global scope'tan al
    global walls
    # walls'un içini boşalt
    walls = []
    # wall'su içine 10 tane rastege duvar at
    for _ in range(10):
        walls.append(Wall(PVector(random(0, width), random(0, width)),
                      PVector(random(0, height), random(0, height))))
    

# Duvar sınıfı
class Wall:
    # constructor metodu
    # Dışarıdan başlangıç ve son değerlerini PVector olarak al
    def __init__(self, start_p, end_p):
        self.start_p = start_p
        self.end_p = end_p
        
    # Duvarı Göster
    def show(self):
        line(self.start_p.x, self.start_p.y, self.end_p.x, self.end_p.y)
        
        
# Kaynak Sınıfı
class Source:
    # Constructor metodu
    # Dışarıdan konum, başlangıç açısı, bitiş açısı ve adım değerlerini al
    def __init__(self, pos, start_angle=0, end_angle=360, step=30):
        self.pos = pos
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.step = step
        self.rays = []
        
    # pos değerini dışarıdan gelen değer ile güncelle
    def update_pos(self, pos):
        self.pos = pos
        
    # Işınları oluştur
    def create_rays(self, walls):
        #Işınlar değişkeninş boşalt
        self.rays = []
        # verilen açılar aralığında, ve verilet adımlarla açı değeri oluştur
        for angle in range(self.start_angle, self.end_angle, self.step):
            # Oluşan açı için ekranın genişliği ve yüksekliğince x ve y koordinatı hesapla
            x = self.pos.x + width * cos(radians(angle))
            y = self.pos.y + height * sin(radians(angle))
            # Konumdan, hesaplanan x, y koodinatına bir çizgi oluştur
            ray = Wall(self.pos, PVector(x, y))
            
            # En kısa çizgiyi bulmamız gerek
            # En kısa uzunluk değerine, pencere üzerinde olabilen eni büyük değerden daha büyük olan
            # Genişlik x Yükseklik değerini at
            lowest_dist = width * height
            # Aranan noktanın x, y olduğunu varsay
            wanted_point = PVector(x, y)
            # Tüm duvarlar için:
            for wall in walls:
                # U ve T değerleriniden gelen x ve y'yi hesapla
                u_pos = self.U(ray, wall)
                t_pos = self.T(ray, wall)
                # Eğer U ve T değer döndürdüyse. Yani hem U hem T [0, 1] ise.
                # Yani duvar ve ışın'ın kesişim noktası, ışın ve duvar'ın üzerindeyse
                if t_pos is not None and u_pos is not None:
                    # Kesişim ve bulunduğum nokta arasındaki uzaklığa bak.
                    d = dist(self.pos.x, self.pos.y, u_pos[0], u_pos[1])
                    # Eğer uzaklık en kısa uzaklıktan daha kısa ise
                    if d < lowest_dist:
                        # aranan nokta kesişim noktasıdır
                        wanted_point = PVector(u_pos[0], u_pos[1])
                        # En kısa uzaklık bu hesaplanan uzaklıktır.
                        lowest_dist = d
            
            # Işınlar dizisine, pozisyondan, en yakın duvara kadar bir ışın koy
            self.rays.append(Wall(self.pos, wanted_point))
            
    
    # T'yi hesapla: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    def T(self, ray, wall):
        x1 = ray.start_p.x
        y1 = ray.start_p.y
        x2 = ray.end_p.x
        y2 = ray.end_p.y
        
        x3 = wall.start_p.x
        y3 = wall.start_p.y
        x4 = wall.end_p.x
        y4 = wall.end_p.y
        
        tu = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        tl = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        t = tu / tl
        if 0 <= t <= 1:
            x, y = x1 + t * (x2 - x1), y1 + t *(y2 - y1)
            return x, y
    
    # U'yu hesapla: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    def U(self, ray, wall):
        x1 = ray.start_p.x
        y1 = ray.start_p.y
        x2 = ray.end_p.x
        y2 = ray.end_p.y
        
        x3 = wall.start_p.x
        y3 = wall.start_p.y
        x4 = wall.end_p.x
        y4 = wall.end_p.y
        
        uu = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
        ul = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        u = -uu / ul
        if 0 <= u <= 1:
            x, y = x3 + u * (x4 - x3), y3 + u *(y4 - y3)
            return x, y        
        
    # Kaynağı göster
    def show(self):
        for ray in self.rays:
            line(ray.start_p.x, ray.start_p.y, ray.end_p.x, ray.end_p.y)
