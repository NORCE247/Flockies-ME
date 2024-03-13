import pygame
import random
import math

class Boids:

    def __init__(self, x, y):
        
        #POSISJON OG RETNING
        self.pos = [x,y]
        self.retning = [random.randint(-100,100),random.randint(-100,100)]

        #FART FOR BOIDS
        self.FART = 5
        
        #ENDRING RATE
        self.FORCE = 0.03
        self.COHS_Force = 0.05
        self.SEP_Force = self.FORCE * 15

        #REGLER SETTING
        self.SEP_avstand = 7
        self.ALIGN_avstand = 50
        self.COHS_avstand = 75
        
        #SYNSVINKEL
        self.SEP_syvinkel = 135
        self.ALIGN_syvinkel = 80
        self.COHS_syvinkel = 90

    def move(self): 
        
        #OPPDATER POSISJON I FORHOLD TIL RETNING OG FART
        self.pos[0] += self.retning[0] * self.FART
        self.pos[1] += self.retning[1] * self.FART

        #OPPDATER RETNING, UNNGÅ KOLLISSJON MED VEGGEN
        if self.pos[0] > 900:
            self.retning[0] -= self.FORCE * 5
        elif self.pos[0] < 100:
            self.retning[0] += self.FORCE * 5
        if self.pos[1] > 700:
            self.retning[1] -= self.FORCE * 5
        elif self.pos[1] < 100:
            self.retning[1] += self.FORCE * 5
            
    
    # Bereegn vinkel basert på sitt retning og andre boidens posisjon  (u * v) /(∣u∣ ∣v∣) = cos(θ)
    # https://www.matematikk.org/artikkel.html?tid=192383&within_tid=154821
    def __vinkel__(self, other):
        #Retning til andre boid
        andre_V = [other.pos[0] - self.pos[0], other.pos[1] - self.pos[1]]
        sin_V = self.retning

        #Avstand (∣u∣ ∣v∣)
        avstand_til_andre = math.sqrt(andre_V[0]**2 + andre_V[1]**2)
        sin_avstand = math.sqrt(sin_V[0]**2 + sin_V[1]**2)

        # (u * v)
        norm = (andre_V[0] * sin_V[0] + andre_V[1] * sin_V[1])
        if avstand_til_andre * sin_avstand != 0:
            #cos(θ) = (u * v) / (∣u∣ ∣v∣)
            cosθ = norm / (avstand_til_andre * sin_avstand)

        #Feihåndtering
        if cosθ > 1:
            cosθ = 1
        elif cosθ < -1:
            cosθ = -1

        #finn θ radian
        radian = math.acos(cosθ)
        
        #Finn grader θ
        grader = math.degrees(radian)
        return grader

    def __separat__(self, boids):
        #Finn inverse gjennomsnitt retning til andre boids
        gjonnomsnitt_retning = [0,0]
        teller = 0
        for boid in boids:
            if boid != self:

                #FINN LENGDEN TIL EN VEKTOR
                avstand = math.sqrt((boid.pos[0] - self.pos[0])**2 + (boid.pos[1] - self.pos[1])**2)
                if avstand < self.SEP_avstand:
                    if self.__vinkel__(boid) < self.SEP_syvinkel:

                        #LEGG TIL INVERSE VEKTOR
                        gjonnomsnitt_retning[0] -= boid.pos[0] - self.pos[0]
                        gjonnomsnitt_retning[1] -= boid.pos[1] - self.pos[1]
                        teller += 1

        if teller > 0:
            #FINN GJENNOMSNITT
            gjonnomsnitt_retning[0] /= teller
            gjonnomsnitt_retning[1] /= teller

            #NORMALISER
            lengde = math.sqrt(gjonnomsnitt_retning[0]**2 + gjonnomsnitt_retning[1]**2)
            if lengde != 0:
                gjonnomsnitt_retning[0] /= lengde
                gjonnomsnitt_retning[1] /= lengde

            #ENDRE RETNING i forhold til gjennomsnitt retning og endrerate.
            self.retning[0] += gjonnomsnitt_retning[0] * (self.SEP_Force)
            self.retning[1] += gjonnomsnitt_retning[1] * (self.SEP_Force)

        #NORMALISER RETNING etter endring
        retning_lengde = math.sqrt(self.retning[0] ** 2 + self.retning[1] ** 2)
        if retning_lengde != 0:
            self.retning[0] /= retning_lengde
            self.retning[1] /= retning_lengde
    
    #[4] https://vanhunteradams.com/Pico/Animal_Movement/Boids-algorithm.html#Alignment
    def __align__(self, boids):
        teller = 0
        gjennsomsnitt_V = [0,0]

        #FINN GJENNOMSNITT BOIDS RETNING
        for boid in boids:
            if boid != self:
                #FINN AVSTAND FOR RADIUS DEFINISJON
                avstand = math.sqrt((boid.pos[0] - self.pos[0])**2 + (boid.pos[1] - self.pos[1])**2)
                if self.SEP_avstand < avstand < self.ALIGN_avstand:
                    if self.__vinkel__(boid) < self.ALIGN_syvinkel:
                        #SUM RETNING
                        gjennsomsnitt_V[0] += boid.retning[0]
                        gjennsomsnitt_V[1] += boid.retning[1]
                        teller += 1

        if teller > 0:
            #BEREGN GJENNOMSNITT
            gjennsomsnitt_V[0] /= teller
            gjennsomsnitt_V[1] /= teller

            #NORMALISER
            FELLES_V = [gjennsomsnitt_V[0] - self.retning[0],gjennsomsnitt_V[1] - self.retning[1]]
            lengde = math.sqrt(FELLES_V[0]**2 + FELLES_V[1]**2)
            if lengde != 0:
                FELLES_V[0] /= lengde
                FELLES_V[1] /= lengde

            #ENDRE RETNING
            self.retning[0] += FELLES_V[0] * self.FORCE 
            self.retning[1] += FELLES_V[1] * self.FORCE 

        #NORMALISER RENING
        avstand_S = math.sqrt(self.retning[0]**2 + self.retning[1]**2)
        self.retning[0] /= avstand_S
        self.retning[1] /= avstand_S
    
    #[5] https://vanhunteradams.com/Pico/Animal_Movement/Boids-algorithm.html#Cohesion
    def __cohesion__(self, boids):
        teller = 0
        gjennomsnitt_pos = [0,0] 

        #SUMER BOIDS I RADIUSEN
        for boid in boids:
            if boid != self:
                #DEFINER AVSTAND
                avstand = math.sqrt((boid.pos[0] - self.pos[0])**2 + (boid.pos[1] - self.pos[1])**2)
                if self.ALIGN_avstand < avstand < self.COHS_avstand:
                    if self.__vinkel__(boid) < self.COHS_syvinkel:
                        teller += 1
                        gjennomsnitt_pos[0] += boid.pos[0]
                        gjennomsnitt_pos[1] += boid.pos[1]

        #BERENG GJENNOMSNITT
        if teller > 0:
            gjennomsnitt_pos[0] /= teller
            gjennomsnitt_pos[1] /= teller

            #NORMALISER
            center_mass = [(gjennomsnitt_pos[0] - self.pos[0]), (gjennomsnitt_pos[1] - self.pos[1])]
            lengde = math.sqrt(center_mass[0]**2 + center_mass[1]**2)
            if lengde != 0:
                center_mass[0] /= lengde
                center_mass[1] /= lengde
            
            
            #ENDRING RATE FOR RETNING
            self.retning[0] += center_mass[0] * self.COHS_Force
            self.retning[1] += center_mass[1] * self.COHS_Force
            

        #NORMALISER RETNING
        avstand_S = math.sqrt(self.retning[0]**2 + self.retning[1]**2)
        self.retning[0] /= avstand_S
        self.retning[1] /= avstand_S

# BEVEG FRA OBJEKT
    def _move_from_objekt_(self, objekt):
        avstand = math.sqrt((objekt.pos[0] - self.pos[0])**2 + (objekt.pos[1] - self.pos[1])**2)
        if avstand < 75:
            #BEGRENS SYNSVINKEL
            if self.__vinkel__(objekt) < 135:
                #ENDRING RATE
                self.retning[0] -= (objekt.pos[0] - self.pos[0]) * 0.008
                self.retning[1] -= (objekt.pos[1] - self.pos[1]) * 0.008

        avstand_S = math.sqrt(self.retning[0]**2 + self.retning[1]**2)
        self.retning[0] /= avstand_S
        self.retning[1] /= avstand_S
            
#BEVEG FRA ANGREPER
    def _move_from_attacker_(self, attacker):
        #Finn avstand
        avstand = math.sqrt((attacker.pos[0] - self.pos[0])**2 + (attacker.pos[1] - self.pos[1])**2)
        if avstand < 75:
            #BEGRENS SYNSVINKEL
            if self.__vinkel__(attacker) < 135:
                self.retning[0] -= (attacker.pos[0] - self.pos[0]) * 0.01
                self.retning[1] -= (attacker.pos[1] - self.pos[1]) * 0.01
            
        #Normaliser retning
        avstand_S = math.sqrt(self.retning[0]**2 + self.retning[1]**2)
        self.retning[0] /= avstand_S
        self.retning[1] /= avstand_S

#TEGN DET DEN SER
    def zone(self, boids, skjerm):
        for boid in boids:
            if boid != self:
                avstand = math.sqrt((boid.pos[0] - self.pos[0])**2 + (boid.pos[1] - self.pos[1])**2)
                if avstand < self.SEP_avstand:
                    if self.__vinkel__(boid) < self.SEP_syvinkel:
                        pygame.draw.line(skjerm, "red", self.pos, boid.pos, 1)

                if self.SEP_avstand < avstand < self.ALIGN_avstand:
                    if self.__vinkel__(boid) < self.ALIGN_syvinkel:
                        pygame.draw.line(skjerm, "yellow", self.pos, boid.pos, 1)
                
                if self.ALIGN_avstand < avstand < self.COHS_avstand:
                    if self.__vinkel__(boid) < self.COHS_syvinkel:
                        pygame.draw.line(skjerm, "green", self.pos, boid.pos, 1)


    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, 2)
        head = [self.pos[0] + self.retning[0] * 5, self.pos[1] + self.retning[1] * 5]
        pygame.draw.line(screen, (0, 255, 153), self.pos, head, 1)

if __name__ == "__main__":
    boid1 = Boids(42, 400)
    boid2 = Boids(600, 4)

    boid1.retning = [9, 4]
    boid2.retning = [-1, 5]

    print(boid1.__vinkel__(boid2))