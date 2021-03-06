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
        portrayal["r"] = 1

        return portrayal

    if agent.wealth >= 10:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    elif agent.wealth >= 3 and agent.wealth < 10:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1

    return portrayal

grid = CanvasGrid(agent_portrayal, 150, 150, 1000, 1000)
gini_chart = ChartModule([
    {"Label": "Gini", "Color": "#0000FF"}],
    data_collector_name='ginicollector'
)
avg_chart = ChartModule([
    {"Label": "Average Wealth", "Color": "#0000FF"}],
    data_collector_name='avgcollector')

model_params = {
    "N": UserSettableParameter('slider', "Number of agents", 200, 2, 400, 1,
                               description="Choose how many agents to include in the model"),
    "initial_wealth": UserSettableParameter('slider', "Initial Wealth", 10, 2, 20, 1),
    "cost_per_pixel": UserSettableParameter('slider', "Cost of Car Travel per Unit", 0.3, 0.1, 1, 0.1),
    "pt_cost": UserSettableParameter('slider', "Cost of PT Travel", 2, 1, 10, 1),
    "cost_to_move": UserSettableParameter('slider', "Cost of Moving/Selling", 30, 10, 60, 1),
    "pt_aval": UserSettableParameter('slider', "Avaliablity of PT over distance", 1, 0.1, 3, 0.1),
    "width": 150,
    "height": 150,
    "city_pos": (75, 75)

}

server = ModularServer(CommuteModel, [grid, gini_chart, avg_chart], "Commute Model", model_params)
server.port = 8521
