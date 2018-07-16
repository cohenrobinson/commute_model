# commute_model
Commute Model is an _Agent-Based Model_ (ABM) set at showing **emergent behaviour** of transport inequality. Currently when run in default, the agents of wealth form a high dense neighbourhood in the centre whereas the agents in poverty are sparce in the outskirts. This not only shows emergent behaviour that is common to today's societies, but leaves room to impliment a solution within the model. 

## Model Characteristics
The model starts all agents with some **initial wealth** and randomly distrbutes them around the city. __Further__ distances from the city centre have __less__ avaliability of public transport (PT). Car __commuting__ has a _cost_ per unit distance the agent has to travel to get to the city.
### Agent Behaviour
Agents have the following behaviour:
* A cost of living,
* The ability to **commute** to work,
* Earn an **income** from working,
* Can choose to commute either by _car_ or _PT_,
* If an agent gains __enough__ wealth, then it can move _closer_ to the city.

## Using the model
To __run__ the model, execute _'run.py'_ with python. This will open up a local __mesa__ server with the ABM running in this model.
## Reading the model
On the grid, each agent is represented by a circle; black is the city centre; green is a wealthy agent; yellow is an average agent; red is a poor agent. 

The charts below the model show the Gini coefficent of the model over time and the second chart is average distance at where the agents of a particular wealth bracket are located over time.
