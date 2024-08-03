import pygame
from random import uniform, randint

def load_and_resize_image(texture_path, size):
    image = pygame.image.load(texture_path).convert_alpha()
    image = pygame.transform.scale(image, (size, size))
    return image

def paint_image(pygame_image, color):
    color = (color[0], color[1], color[2], 255)
    painted_image = pygame_image.copy()
    painted_image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    return painted_image

class Single_Particle():
    def __init__(self, particle_ID: str, duration: int, position_vector: tuple, velocity_vector: tuple, color: tuple, random_painted_textures: pygame.surface = None) -> None:
        self.ID = particle_ID
        self.duration = duration
        self.end = False
        self.x, self.y = position_vector
        self.velocityX, self.velocityY = velocity_vector
        self.color = color
        self.cycle = 0
        self.cycle_texture = 0
        self.random_painted_textures = random_painted_textures

    def update(self, pygame_surface: pygame.surface, data: list) -> None:
        textures, painted_textures, size, gravity, drag_coefficient, color_state, phase_duration = data

        # counts down the particle duration which acts like a timer

        duration_decrement = False
        if phase_duration == None:
            duration_decrement = True
        else:
            # updates the texture cycle
            self.cycle += 1
            if self.cycle >= phase_duration:
                self.cycle = 0
                self.cycle_texture += 1
            
            if self.cycle_texture >= len(textures):
                self.cycle_texture = 0
                duration_decrement = True

        # declares itself finished with 'self.end'
        if self.duration <= 0:
            self.end = True
            return
        
        if duration_decrement:
            self.duration -= 1
        
        if phase_duration != None and self.duration <= 0:
            self.end = True
            return

        # applies physics to the particles
        self.velocityX += gravity[0]
        self.velocityY += gravity[1]

        self.velocityX -= self.velocityX * drag_coefficient
        self.velocityY -= self.velocityY * drag_coefficient

        self.x += self.velocityX
        self.y += self.velocityY

        # displays the particles in the case of keywords
        if type(textures) == str:
            if textures == "circle":
                pygame.draw.circle(pygame_surface, self.color, (self.x, self.y), size // 2)
            if textures == "square":
                pygame.draw.rect(pygame_surface, self.color, (self.x, self.y, size, size))
        # displays the particle depending on it's color
        else:    
            if color_state == "random":
                image = self.random_painted_textures[self.cycle_texture]
            else:
                image = painted_textures[self.cycle_texture]
            
            pygame_surface.blit(image, (self.x, self.y))

class Particles():
    def __init__(self, surface, FPS) -> None:
        self.pygame_surface = surface
        self.FPS = FPS
        self.particles_data = {}
        self.active_particles = {}
        self.finished_particles = {}

    def add_particle_type(self, particle_ID: str, texture_paths, size: int, gravity_vector: tuple, drag_coefficient: float = 0, color = (255, 255, 255, 255), phase_duration: float = None) -> None:
        # creating the list which will receive all the particle data into the dictionary with the particle_ID as the key
        self.particles_data[particle_ID] = []

        # loading texture into the 'images' variable and coloring the texture and saving it into 'painted_images'
        if type(texture_paths) == str:
            if texture_paths == "circle" or texture_paths == "square":
                images = texture_paths # here the variable 'images' contains a string indicating which shape it shoud have instead of a list of textures
                painted_images = None
                phase_duration = None
            else:
                # loading the singular image and putting it images as a list
                image = load_and_resize_image(texture_paths, size)
                images = [image]
                if color != "random":
                    painted_image = paint_image(image, color)
                    painted_images = [painted_image]
        elif type(texture_paths) == list:
            images = []
            painted_images = []
            # loops over all the texture paths inside the list 'texture_paths', loads, paints and stores the data inside 'images' and 'painted_images'
            for texture_path in texture_paths:
                image = load_and_resize_image(texture_path, size)
                images.append(image)
                if color != "random":
                    painted_image = paint_image(image, color)
                    painted_images.append(painted_image)
        
        # creates a new refference 'painted_images' for the images inside 'images'
        if color == "random":
            painted_images = images

        if drag_coefficient > 1:
            drag_coefficient = 1

        if type(phase_duration) == float:
            if phase_duration <= 0:
                raise ValueError(f"The duration of the phase of the particle cannot be below or equal to 0. Here '{phase_duration}' given")

        # adds the particles data the the dictionary used as the memory
        self.particles_data[particle_ID].append(images)                         # 0
        self.particles_data[particle_ID].append(painted_images)                 # 1
        self.particles_data[particle_ID].append(size)                           # 2
        self.particles_data[particle_ID].append(gravity_vector)                 # 3
        self.particles_data[particle_ID].append(drag_coefficient)               # 4
        self.particles_data[particle_ID].append(color)                          # 5
        self.particles_data[particle_ID].append(phase_duration)                 # 6
        

        self.active_particles[particle_ID] = []

    def new_particles(self, particle_ID: str, number_of_particles: int, duration: int, position_vector: tuple, velocity_vector: tuple = (0, 0), delta: tuple = (0, 0)) -> None:
        # checks if the particle exists inside the dictionary. If not, error
        particle_present = False
        for IDs in self.particles_data.keys():
            if IDs == particle_ID:
                particle_present = True

        if not particle_present:
            raise ValueError(f"The particle with the particle ID: '{particle_ID}' is not defined")

        if duration < 0:
            raise ValueError(f"The particle duration cannot be below 0. Here '{duration}' given")
        elif duration == 0:
            return
                    

        if number_of_particles <= 0:
            number_of_particles = 0

        position_vector_initial = position_vector
        for i in range(number_of_particles):
            # set particle position
            if position_vector_initial[0] <= position_vector_initial[0] + delta[0]:
                x = randint(position_vector_initial[0], position_vector_initial[0] + delta[0])
            else:
                x = randint(position_vector_initial[0] + delta[0], position_vector_initial[0])

            if position_vector_initial[1] <= position_vector_initial[1] + delta[1]:
                y = randint(position_vector_initial[1], position_vector_initial[1] + delta[1])
            else:
                y = randint(position_vector_initial[1] + delta[1], position_vector_initial[1])
            position_vector = (x, y)

            # set particle velocity in case it is random
            velocityX, velocityY = velocity_vector
            if type(velocityX) == tuple:
                velocityX = uniform(velocityX[0], velocityX[1])
            if type(velocityY) == tuple:
                velocityY = uniform(velocityY[0], velocityY[1])
            velocity_vector = (velocityX, velocityY)

            # set particle color in case it is random and create particle
            if self.particles_data[particle_ID][5] == "random":
                particle_color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
                if type(self.particles_data[particle_ID][0]) == str:
                    random_painted_particle_textures = None
                else:
                    random_painted_particle_textures = []
                    for i in range(len(self.particles_data[particle_ID][1])):
                        random_painted_particle_texture = self.particles_data[particle_ID][1][i].copy()
                        random_painted_particle_texture = paint_image(random_painted_particle_texture, particle_color)
                        random_painted_particle_textures.append(random_painted_particle_texture)

                particle = Single_Particle(particle_ID, duration, position_vector, velocity_vector, particle_color, random_painted_particle_textures)
                
            else: # creates particle if color is not random
                particle_color = self.particles_data[particle_ID][5]
                particle = Single_Particle(particle_ID, duration, position_vector, velocity_vector, particle_color)

            # adds the new particle to the list of active particles
            self.active_particles[particle_ID].append(particle)

    def update(self) -> None:
        for particle_type in self.active_particles.keys():
            for particle in self.active_particles[particle_type]:
                # updates the every individual particle
                particle.update(self.pygame_surface, self.particles_data[particle_type])

        # deletes every particle that is finished
        for particle_type in self.active_particles.keys():
            for particle in self.active_particles[particle_type]:
                if particle.end:
                    del self.active_particles[particle_type][self.active_particles[particle_type].index(particle)]

    def get_defined_particles_ID(self) -> list:
        particle_IDs = []
        for particle_ID in self.particles_data.keys():
            particle_IDs.append(particle_ID)
        return particle_IDs
    
    def get_defined_particles_data(self) -> list:
        return self.particles_data
    
    def get_defined_particle_data(self, particle_ID: str) -> list:
        particle_present = False
        for IDs in self.particles_data.keys():
            if IDs == particle_ID:
                particle_present = True

        if not particle_present:
            raise ValueError(f"The particle with the particle ID: '{particle_ID}' is not defined")
        
        return self.particles_data[particle_ID]
    
    def clear_all_particles(self) -> None:
        for particle_type in self.active_particles.keys():
            self.active_particles[particle_type] = []

    def clear_particle_type(self, particle_ID: str) -> None:
        self.active_particles[particle_ID] = []