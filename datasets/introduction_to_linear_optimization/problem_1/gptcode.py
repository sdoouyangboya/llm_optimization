
import json
from gurobipy import Model, GRB

# Step 1: Read Data
with open('data.json', 'r') as file:
    data = json.load(file)

available = data['available']
requirements = data['requirements']
prices = data['prices']

# Step 2: Create a model
model = Model()

# Step 3: Create variables
x = model.addVars(len(prices), lb=0, vtype=GRB.CONTINUOUS)

# Step 4: Set objective
model.setObjective(sum(prices[j]*x[j] for j in range(len(prices))), GRB.MAXIMIZE)

# Step 5: Add constraints
for i in range(len(available)):
    model.addConstr(sum(requirements[j][i]*x[j] for j in range(len(prices))) <= available[i])

# Step 6: Optimize model
model.optimize()

# Step 7: Retrieve results
amount = [x[j].x for j in range(len(prices))]

# Step 8: Save results
with open('output.json', 'w') as file:
    json.dump({"amount": amount}, file, indent=4)
