walls = []
source = None

def setup():
    global walls, source
    size(750, 750)
    
    for _ in range(10):
        walls.append(Wall(PVector(random(0, width), random(0, width)),
                          PVector(random(0, height), random(0, height))))
    
    source = Source(PVector(width/2, height/2), step=15)
    
def draw():
    background(0)
    
    source.create_rays(walls)
    
    stroke(255)
    strokeWeight(4)
    for wall in walls:
        wall.show()
        
    stroke(255, 255, 0, 75)
    strokeWeight(2)
    source.show()
    source.update_pos(PVector(mouseX, mouseY))

def mousePressed():
    global walls
    walls = []
    for _ in range(10):
        walls.append(Wall(PVector(random(0, width), random(0, width)),
                      PVector(random(0, height), random(0, height))))
    


class Wall:
    def __init__(self, start_p, end_p):
        self.start_p = start_p
        self.end_p = end_p
        
    def show(self):
        line(self.start_p.x, self.start_p.y, self.end_p.x, self.end_p.y)
        
class Source:
    def __init__(self, pos, start_angle=0, end_angle=360, step=30):
        self.pos = pos
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.step = step
        self.rays = []
        
    def update_pos(self, pos):
        self.pos = pos
        
    def create_rays(self, walls):
        self.rays = []
        for angle in range(self.start_angle, self.end_angle, self.step):
            x = self.pos.x + width * cos(radians(angle))
            y = self.pos.y + height * sin(radians(angle))
            ray = Wall(self.pos, PVector(x, y))
            
            
            lowest_dist = width * height
            wanted_point = PVector(x, y)
            for wall in walls:
                u_pos = self.U(ray, wall)
                t_pos = self.T(ray, wall)
                if t_pos is not None and u_pos is not None:
                    d = dist(self.pos.x, self.pos.y, u_pos[0], u_pos[1])
                    if d < lowest_dist:
                        wanted_point = PVector(u_pos[0], u_pos[1])
                        lowest_dist = d
                
            self.rays.append(Wall(self.pos, wanted_point))
            
            
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
        
    def show(self):
        for ray in self.rays:
            line(ray.start_p.x, ray.start_p.y, ray.end_p.x, ray.end_p.y)
