#-- Eco-Sim :- Evolution Simmulator ---
from abc import ABC, abstractmethod
import random
#-- Class Organism Base class --
class Organism(ABC):
    def __init__(self, name, species, energy=10):
        self.name = name
        self.species = species
        self.__energy = energy   # private

    # Getter
    @property
    def energy(self):
        return self.__energy

    # Setter
    @energy.setter
    def energy(self, value):
        if value >= 0:
            self.__energy = value

    def is_alive(self):
        return self.__energy > 0

    def change_energy(self, amount):
        self.__energy += amount
        if self.__energy < 0:
            self.__energy = 0

    # Abstraction
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def act(self, world):
        pass


# -------- Plant derived from Organism -----
class Plant(Organism):
    def __init__(self, name):
        super().__init__(name, "Plant", 5)

    def move(self):
        print(f"{self.name} can't move ")

    def act(self, world):
        self.move()   # call once here
        self.change_energy(2)
        print(f"{self.name} grows. Energy: {self.energy}")


# -------- Animal derived from Organism -----
class Animal(Organism):
    def __init__(self, name, species):
        super().__init__(name, species, 10)

    def move(self):
        print(f"{self.name} is moving ")
        self.change_energy(-1)

    def act(self, world):
        self.move()


# -------- Herbivore derived from Animal ------
class Herbivore(Animal):
    def __init__(self, name):
        super().__init__(name, "Herbivore")

    def act(self, world):
        self.move()

        plants = [p for p in world.organisms if isinstance(p, Plant) and p.is_alive()]

        if plants:
            plant = random.choice(plants)
            plant.change_energy(-3)
            self.change_energy(+4)
            print(f"{self.name} eats {plant.name} ")
        else:
            print(f"{self.name} found no plants.")

        print(f"{self.name} Energy: {self.energy}")


# -------- Carnivore derived from Animal ------
class Carnivore(Animal):
    def __init__(self, name):
        super().__init__(name, "Carnivore")

    def act(self, world):
        self.move()

        herbivores = [h for h in world.organisms if isinstance(h, Herbivore) and h.is_alive()]

        if herbivores:
            prey = random.choice(herbivores)
            prey.change_energy(-5)
            self.change_energy(+6)
            print(f"{self.name} eats {prey.name} ")
        else:
            print(f"{self.name} found no prey.")

        print(f"{self.name} Energy: {self.energy}")


# Interaction 
class World:
    def __init__(self):
        self.organisms = []

    def add(self, organism):
        self.organisms.append(organism)

    def simulate(self, turns):
        for turn in range(turns):
            print(f"\n--- Turn {turn + 1} ---")

            for organism in self.organisms:
                if organism.is_alive():
                    organism.act(self)
            dead = [o for o in self.organisms if not o.is_alive()]
            for d in dead:
                print(f"{d.name} ({d.species}) died!")
            # Remove dead organisms
            self.organisms = [o for o in self.organisms if o.is_alive()]

world = World()

world.add(Plant("Grass"))
world.add(Plant("Tree"))
world.add(Herbivore("Deer"))
world.add(Carnivore("Lion"))

n = int(input("No. of Turns: "))
world.simulate(n)