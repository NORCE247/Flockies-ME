from boids import *


class Objekt(Boids):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.pos = [x,y]
    
    
    def _draw_(self, screen):
        pygame.draw.circle(screen, "gray", self.pos, 15)

        
        
class Attacker(Boids):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 2 
        self.FART *= 1.15 # 15% raskere enn boids

            
    def _draw_(self, screen):
        head = [self.pos[0] + self.retning[0] * 5, self.pos[1] + self.retning[1] * 5]
        pygame.draw.circle(screen, "red", self.pos, self.size)
        pygame.draw.line(screen, "red", self.pos, head, 1)



if __name__ == "__main__": 
    o = Objekt(2,4)
    
