import random
from math import sqrt

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    if sum(x) == 0:
        return 0
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)

def compute_avg_wealth(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    return sum(x) / N

class CommuteModel(Model):
    """This agent-based model seeks to demonstrate the effect of spatial
    inequality on the way agents commute."""

    def __init__(self, N, initial_wealth, cost_per_pixel, pt_cost, cost_to_move, pt_aval, width, height, city_pos):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # place commute agents
        for unique_id in range(self.num_agents):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
            if self.grid.is_cell_empty(pos):
                a = CommuteAgent(unique_id, self, pos, city_pos, initial_wealth, cost_per_pixel, pt_cost, cost_to_move, pt_aval)
                self.schedule.add(a)
                self.grid.place_agent(a, pos)

        self.grid.place_agent(CityAgent(city_pos), city_pos)
        self.ginicollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )
        self.avgcollector = DataCollector(
            model_reporters={"Average Income": compute_avg_wealth},
            agent_reporters={"Wealth": "wealth"}
        )
        self.ginicollector.collect(self)
        self.avgcollector.collect(self)

        self.running = True

    def step(self):
        self.schedule.step()
        # collect data
        self.ginicollector.collect(self)
        self.avgcollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()

class CommuteAgent(Agent):
    """An agent that follows behaviour shown in the README.md."""

    def __init__(self, unique_id, model, pos, city_pos, initial_wealth, cost_per_pixel, pt_cost, cost_to_move, pt_aval):
        super().__init__(unique_id, model)
        self.city_pos = city_pos
        self.pos = pos
        self.dis_city = sqrt((city_pos[0]-pos[0])**2+(city_pos[1]-pos[1])**2)
        self.wealth = initial_wealth
        self.type = 'agent'
        self.pt_cost = pt_cost
        self.cost_per_pixel = cost_per_pixel
        self.cost_to_move = cost_to_move
        self.pt_aval = pt_aval

    def move(self):
        if self.wealth >= self.cost_to_move + 5:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            new_position = (0, 0)
            for pos in possible_steps:
                if sqrt((pos[0]-self.city_pos[0])**2+(pos[1]-self.city_pos[1])**2) < sqrt((new_position[0]-self.city_pos[0])**2 + (new_position[1]-self.city_pos[1])**2):
                    if self.model.grid.is_cell_empty(pos):
                        new_position = pos
            self.model.grid.move_agent(self, new_position)
            self.wealth -= self.cost_to_move

    def commute(self):
        cost_of_carcommute = int(self.dis_city*self.cost_per_pixel)
        # commute by PT
        if random.random() <= self.pt_avaliablity() and self.pt_cost <= cost_of_carcommute:
            if self.wealth >= self.pt_cost:
                self.wealth -= self.pt_cost
                self.wealth += 5
        # commute by car
        else:
            if self.wealth >= cost_of_carcommute:
                self.wealth -= cost_of_carcommute
                self.wealth += 5

    def pt_avaliablity(self):
        total_distance = sqrt(self.city_pos[0]**2 + self.city_pos[1]**2)
        prob_pt = self.pt_aval * 1 - (self.dis_city) / total_distance
        if prob_pt >= 1:
            return 1

        return prob_pt

    def step(self):
        self.commute()
        self.move()
        # cost of living
        self.wealth -= 1

class CityAgent(Agent):
    """An agent representing the city centre."""
    def __init__(self, city_pos):
        self.pos = city_pos
        self.type = 'city'
