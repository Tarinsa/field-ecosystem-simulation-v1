import numpy as np
import random
import pygame
from collections import defaultdict
import matplotlib.pyplot as plt



#CONFIG ==========================================================================================================================================================================
SCREEN_HEIGHT =600
SCREEN_WIDTH = 1000
CELL_SIZE = 120
ENABLE_RENDER = True
MAX_TICKS = 5000
SEED = 1300


INITIAL_GRASS = 670
INITIAL_RABBIT = 100
INITIAL_FOX = 16

INITIAL_GRASS_ENERGY = 50
MAX_GRASS = 1500


#INITIAL DATA LISTS==========================================================================================================================================================================

grass_count_list = []
fox_count_list = []
rabbit_count_list = []


rabbit_speed_list = []
fox_speed_list = []

rabbit_detection_radius_list = []
fox_detection_radius_list = []


#Seed
random.seed(SEED)





#FAUNA SPECIES DICTIONARY
SPECIES = {
    "fox": {
        "diet": ["rabbit"],
        "speed": 2,
        "detection_radius": 90,
        "lifespan": 1500,
        "random_movement": 2.5,
        "reproduction_cost": 160,
        "reproduction_threshold": 440,
        "hunger_threshold": 350,
        "initial_energy": 1100,
        "litter": 1,

    },
    "rabbit": {
        "diet": ["grass"],
        "speed": 1.5,
        "detection_radius": 70,
        "lifespan": 700,
        "random_movement": 2,
        "reproduction_cost": 100,
        "reproduction_threshold": 210,
        "hunger_threshold": 150,
        "initial_energy": 600,
        "litter": 2

    }
    
}







#Fauna Class
class Fauna:
    def __init__(self, species, position, heritable_traits = {}):
        self.species = species
        self.data = SPECIES[species]
        h_t = heritable_traits

        #Non-hereditary Traits
        self.position = list(position)
        self.sex = random.randint(0, 1) # 0 = Male
        self.target = None
        self.mating_target = None
        self.energy = h_t.get("initial_energy", self.data ["initial_energy"])
        self.targetted = None

        #Hereditary Traits
        self.speed = h_t.get("speed", self.data ["speed"])
        self.detection_radius = h_t.get("detection_radius", self.data ["detection_radius"])
        self.lifespan = h_t.get("lifespan", self.data ["lifespan"])
        self.random_movement = h_t.get("random_movement", self.data ["random_movement"])
        self.reproduction_threshold = h_t.get("reproduction_threshold", self.data ["reproduction_threshold"])
        self.hunger_threshold = h_t.get("hunger_threshold", self.data ["hunger_threshold"])
        self.initial_energy = h_t.get("initial_energy", self.data ["initial_energy"])
        self.reproduction_cost = h_t.get("reproduction_cost", self.data ["reproduction_cost"])
        self.litter = h_t.get("litter", self.data ["litter"])
        




        #Time-Affected Traits
        self.mating_cooldown = 200 +random.randint(-50, 160)
        self.lifespan = float(SPECIES[species]["lifespan"])
        self.life_countdown = float(SPECIES[species]["lifespan"]) + random.randint(-250, 300)


    #Random Movement
    def move(self, speed):
        self.position[0] += random.uniform(-speed, speed)
        self.position[1] += random.uniform(-speed, speed)
        self.energy -= (0.4 + speed/6)

    #Hunting
    def hunt(self, prey_list, prey_species, speed, detection_radius):
        
        if self.target is not None and self.target.energy <= 0:
            self.target = None
        if self.target is None and self.mating_target is None:
            for prey in prey_list:
                if prey.species in prey_species:
                    square_distance = (self.position[0] - prey.position[0]) ** 2 + (self.position[1] - prey.position[1]) ** 2
                    if square_distance < detection_radius ** 2:
                        self.target = prey
                        break 
        elif self.target is not None:
                
                prey = self.target
                distance = np.linalg.norm(np.array(self.position) - np.array(prey.position))
                if distance > self.detection_radius * 1.2:
                    self.target = None

                if distance > 5:
                    directionVector = (np.array(prey.position) - np.array(self.position))/distance
                    self.position[0] += directionVector[0] * speed
                    self.position[1] += directionVector[1] * speed
                    self.energy -= (self.speed**2)/14

                    if not isinstance(prey, Flora) and distance <= prey.detection_radius and prey.targetted is None:
                        prey.targetted = self
                        prey.position[0] += directionVector[0] * prey.speed
                        prey.position[1] += directionVector[1] * prey.speed
                        prey.energy -= (prey.speed ** 2)/14
                else: 
                    if prey.energy > 0 :
                        prey.energy = 0
                        self.target = None
                        self.energy += 240
                    else:
                        self.target = None

    #Mating
    def mate(self, animals, speed, detection_radius, master_animals):
        
        if self.mating_cooldown <= 0:

            
            if self.mating_target is None and self.target is None and self.mating_cooldown == 0:

                for partner in animals:
                    distance = np.linalg.norm(np.array(self.position) - np.array(partner.position))
                    if partner.species == self.species and partner.sex != self.sex and distance < detection_radius and partner.mating_target is None:
                        partner.mating_target = self
                        self.mating_target = partner
                        break
            elif self.mating_target is not None:
                partner = self.mating_target
                distance = np.linalg.norm(np.array(self.position) - np.array(partner.position))
                
                if distance > 15:
                    partner = self.mating_target
                    direction_vector_self = (np.array(partner.position) - np.array(self.position))/distance
                    direction_vector_partner = (np.array(self.position) - np.array(partner.position))/distance
                    self.position[0] += direction_vector_self[0] * speed
                    self.position[1] += direction_vector_self[1] * speed
                    partner.position[0] += direction_vector_partner[0] * speed
                    partner.position[1] += direction_vector_partner[1] * speed
                else:
                    x = self.position[0]+10
                    y = self.position[1]+10


                    #Genetic Variation
                    new_speed = (self.speed + partner.speed)/2 + random.uniform(-0.3, 0.3)
                    new_random_movement = (self.random_movement + partner.random_movement)/2 + random.uniform(-0.3, 0.3)
                    new_detection_radius = (self.detection_radius + partner.detection_radius)/2 + random.uniform(-5, 5)
                    new_initial_energy = (self.reproduction_cost + partner.reproduction_cost)/self.litter

                    
                    
                    
                    #Adding new animal
                    for i in range (self.litter):
                        inherited_traits = {"speed": new_speed,
                                                                "random_movement": new_random_movement,
                                                                "detection_radius": new_detection_radius,
                                                                "initial_energy": new_initial_energy}
                        new_animal = Fauna(self.species, (x+random.randint(-7,7),y+random.randint(-7,7)), inherited_traits)
                        master_animals.append(new_animal)
                    self.mating_target = None
                    partner.mating_target = None
                    self.mating_cooldown = 240
                    partner.mating_cooldown = 240
                    self.energy -= self.reproduction_cost
                    partner.energy -= partner.reproduction_cost





#Flora Class
class Flora:
    def __init__(self, species, position, energy):
        self.species = species
        self.position = list(position)
        self.energy = float(energy)










#Obtain Adjacent Cells 
def get_adjacent(grid, position, cell_size):
    adjacent = []
    cell_x = int(position[0] // cell_size)
    cell_y = int(position[1] // cell_size)
    for i in range(-1, 2):
        for j in range(-1, 2):
            adjacent.extend(grid.get((cell_x + i, cell_y + j), []))
    return adjacent


#Update - runs once per tick
def update(animals, grass):
    #Update live organism lists
    grass = [grassPatch for grassPatch in grass if grassPatch.energy > 0]
    animals = [animal for animal in animals if animal.energy > 0]


    #Grid Creation
    animal_grid = defaultdict(list)
    positions = np.array([a.position for a in animals])
    cell_coords = (positions//CELL_SIZE).astype(int)

    for i, a in enumerate(animals):
        animal_grid[tuple(cell_coords[i])].append(a)


    grass_grid = defaultdict(list)
    positions_g = np.array([g.position for g in grass])
    cell_coords_g = (positions_g//CELL_SIZE).astype(int)

    for i, g in enumerate(grass):
        grass_grid[tuple(cell_coords_g[i])].append(g)





    #Animal Lifespan
    for animal in animals:
        animal.targetted = None
        if animal.life_countdown > 0:
            animal.life_countdown -=1
        elif animal.life_countdown <= 0:
            animal.energy = 0

    #Animal Mating Cooldown
        if animal.mating_cooldown > 0:
            animal.mating_cooldown -= 1


    #Animal Random Movement
        if animal.target is None and animal.mating_target is None:
            animal.move(animal.random_movement)


    #Hunting and Reproduction


    for a in animals:
        if a.energy <= a.hunger_threshold:
            
            for food in a.data["diet"]:
                if food == "grass":
                    grid = grass_grid
                else:
                    grid = animal_grid
                adjacent = (get_adjacent(grid, a.position, CELL_SIZE))
            a.hunt(adjacent, a.data["diet"], a.speed, a.detection_radius)
        elif a.energy >= a.reproduction_threshold:
            adjacent = get_adjacent(animal_grid, a.position, CELL_SIZE)
            a.mate(adjacent, a.speed, a.detection_radius, animals )



    #Grass Reproduction


    
    for grassPatch in grass:
        if grassPatch.energy > 0:
            grassPatch.energy += 1
            if grassPatch.energy > INITIAL_GRASS_ENERGY + random.randint(300, 600) :
                grassPatch.energy = 5

                crowding = max(0.0, 1 - len(grass)/MAX_GRASS)
                if random.random() < 0.8 * crowding:
                    x = grassPatch.position[0] + random.randint(-20,20)
                    y = grassPatch.position[1] + random.randint(-20,20)                   
                    grass.append(Flora("grass", (x,y), INITIAL_GRASS_ENERGY))

    n_new = int(0.8) + (random.random() < 0.8 % 1)
    for _ in range(n_new):
        if len(grass) < MAX_GRASS:
            grass.append(Flora("grass", (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), INITIAL_GRASS_ENERGY))




    grass = [grassPatch for grassPatch in grass if grassPatch.energy > 0]
    animals = [animal for animal in animals if animal.energy > 0]


    for a in animals:
        a.position[0] = min(max(a.position[0], 0), SCREEN_WIDTH)
        a.position[1] = min(max(a.position[1], 0), SCREEN_HEIGHT)

    return animals, grass

#Render Graphics and Entity Counts
def render(animals, grass):



    #organism counts
    rabbit_count = 0
    fox_count = 0
    grass_count = 0


    for a in animals:
        if a.species == "rabbit":
            rabbit_count += 1
            pygame.draw.circle(screen, ("white"), a.position, 2)
        elif a.species == "fox":
            fox_count += 1
            pygame.draw.circle(screen, (207, 131, 50), a.position, 3)

    for g in grass:
        grass_count += 1
        pygame.draw.circle(screen, (47, 135, 50), g.position, 1)






    

    rabbit_number = font.render(f'Rabbits: {rabbit_count}', True, "white")
    fox_number = font.render(f'Foxes: {fox_count}', True, "white")
    grass_number = font.render(f'Grass: {grass_count}', True, "white")

    screen.blit(rabbit_number, (10, 10))
    screen.blit(fox_number, (10, 40))
    screen.blit(grass_number, (10, 70))
    




#Initialising coordinates-------------------------------------------------------------

grass = []
for i in range(0, INITIAL_GRASS):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    grass.append(Flora("grass", (x,y), INITIAL_GRASS_ENERGY))


animals = []
for i in range(0, INITIAL_RABBIT):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    animals.append(Fauna("rabbit", (x,y)))



for i in range(0, INITIAL_FOX):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    animals.append(Fauna("fox", (x,y)))







#pygame setup


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)

running = True




#Debugging/Testing
fps_sum = float("0")
fps_list = []
tick_count = 0



while running and tick_count < MAX_TICKS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    tick_count += 1



    screen.fill((50, 50, 50))

#Update and Render


    animals, grass = update(animals, grass)






    if ENABLE_RENDER == True:
        render(animals, grass)



#Track Entity Quantities
    rabbits = 0
    foxes = 0
    rabbit_speed_sum = 0
    fox_speed_sum = 0
    rabbit_detection_radius_sum = 0
    fox_detection_radius_sum = 0


    for a in animals:
        if a.species == "rabbit":
            rabbits += 1
            rabbit_speed_sum += a.speed
            rabbit_detection_radius_sum += a.detection_radius
        else:
            foxes += 1
            fox_speed_sum += a.speed
            fox_detection_radius_sum += a.detection_radius

    grass_count_list.append(len(grass))
    fox_count_list.append(foxes)
    rabbit_count_list.append(rabbits)

    if rabbits > 0:
        rabbit_speed_list.append(rabbit_speed_sum/rabbits)
        rabbit_detection_radius_list.append(rabbit_detection_radius_sum/rabbits)
    else:
        rabbit_speed_list.append(float("nan"))
        rabbit_detection_radius_list.append(float("nan"))




    if foxes > 0:
        fox_speed_list.append(fox_speed_sum/foxes)
        fox_detection_radius_list.append(fox_detection_radius_sum/foxes)

    else:
        fox_speed_list.append(float("nan"))
        fox_detection_radius_list.append(float("nan"))




                    


    pygame.display.flip()

    clock.tick(500)


    fps = clock.get_fps()
    fps_sum += fps

    



pygame.quit()

ticks = range(len(rabbit_count_list))
number_of_ticks = len(rabbit_count_list)




print(f'entity quantity : {len(animals) + len(grass)}')
print(f'mean framerate : {fps_sum/number_of_ticks}  fps')







#Population Change Plot
figure, axes = plt.subplots(2, 3, figsize = (18,7))
axes[0,0].plot(ticks, rabbit_count_list)
axes[1,0].plot(ticks, fox_count_list, color = "orange")
axes[0,0].set_title("Rabbit Populations")
axes[1,0].set_title("Fox Populations")

#Speed Change Plot
axes[1,1].plot(ticks, fox_speed_list, color = "orange")
axes[1,1].set_title("Fox Mean Speed Change")
axes[0,1].plot(ticks, rabbit_speed_list)
axes[0,1].set_title("Rabbit Mean Speed Change")


#Detetion Radius Plot
axes[1,2].plot(ticks, fox_detection_radius_list, color = "orange")
axes[1,2].set_title("Fox Detection Radius Change")
axes[0,2].plot(ticks, rabbit_detection_radius_list)
axes[0,2].set_title("Rabbit Detection Radius Change")


plt.show()
