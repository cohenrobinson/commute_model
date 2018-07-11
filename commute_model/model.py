import random
from math import sqrt

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

CITY_POS = (width//2, height//2)

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)

class CommuteModel(Model):
    """This agent-based model seeks to demonstrate the effect of spatial
    inequality on the way agents commute."""

    def __init__(self, N, width=200, height=100, city_pos):
        self.N = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.make_commuteagents()
        self.grid.place_agent(CityAgent(city_pos))
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )
        self.datacollector.collect(self)
        self.running = True

    def make_commuteagents(self):
        for unique_id in range(self.N):
            x = random.randarrange(self.grid.width)
            y = random.randarrange(self.grid.height)
            pos = (x, y)
            if self.grid.is_cell_empty(pos):
                a = CommuteAgent(unique_id, self, pos, city_pos, width, height)
                self.schedule.add(a)
                self.grid.place_agent(a, pos)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()

class CommuteAgent(Agent):
    """An agent that follows behaviour shown in the README.md."""

    def __init(self, unique_id, model, pos, city_pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.dis_city = sqrt((city_pos[0]-pos[0])**2+(city_pos[1]-pos[1])**2)
        self.wealth = 10
        self.type = 'agent'

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.wealth -= 20
    def commute(self, city_pos):
        # commute by PT
        if random.random() <= self.pt_avaliablity(self, city_):
            if self.wealth >= 2:
                self.wealth -= 2
                self.wealth += 5
        # commute by car
        else:
            if self.wealth >= 6:
                self.wealth -= 6
                self.wealth += 5

    def pt_avaliablity(self, city_pos):
        total_distance = sqrt(city_pos[0]**2 + city_pos**2)
        return 1 - self.dis_city / total_distance

class CityAgent(Agent):
    """An agent representing the city centre."""
    def __init__(self, city_pos):
        self.pos = city_pos
        self.type = 'city'
