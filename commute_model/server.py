from mesa.visualization.ModularVisualization import ModularServer
from .model import CommuteModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
    if agent.type == 'city':
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["Shape"] = "circle"

        return portrayal

    if agent.wealth >= 0 and agent.wealth < 5:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.wealth >= 5 and agent.wealth < 10:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2

    return portrayal

grid = CanvasGrid(agent_portrayal, 200, 200, 1000, 1000)
chart = ChartModule([
    {"Label": "Gini", "Color": "#0000FF"}],
    data_collector_name='datacollector'
)

model_params = {
    "N": UserSettableParameter('slider', "Number of agents", 100, 2, 200, 1,
                               description="Choose how many agents to include in the model"),
    "width": 200,
    "height": 200,
    "city_pos": (100, 100)

}

server = ModularServer(CommuteModel, [grid, chart], "Commute Model", model_params)
server.port = 8521
