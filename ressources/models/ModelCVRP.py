# import gurobipy
from gurobipy import Model, GRB, quicksum
from abc import ABC, abstractmethod
import numpy as np

class ModelCVRP(ABC):
    def __init__(self):
        self.xcords = []
        self.ycords = []
        self.capacity = []
        self.isOptimized = False

    @abstractmethod
    def readFromData(self, data):
        pass

    def initModel(self, capacityPerVehicle = 40):
        customersNumber = len(self.xcords)
        N = [i for i in range (1, customersNumber)] #Customer's list
        V = [0] + N #Nodes list
        self.A = [(i,j) for i in V for j in V if i!=j] #Arcs (routes)
        c = {(i,j): np.hypot(self.xcords[i]-self.xcords[j], self.ycords[i]-self.ycords[j]) for i,j in self.A} #Euclidean distance between arcs
        Q = capacityPerVehicle #Capacity of vehicules
        print('Capacity per vehicle : ' + str(Q))
        q = {i: self.capacity[i] for i in N} #Amount to be delivred for each customers

        #Instantiate GurobiPy's Model CVRP
        self.modelGurobi = Model('CVRP')
        self.modelGurobi.Params.JSONSolDetail = 1
        #Variables
        self.x = self.modelGurobi.addVars(self.A, vtype=GRB.BINARY)
        u = self.modelGurobi.addVars(N, vtype=GRB.CONTINUOUS)

        #Objectives
        self.modelGurobi.modelSense = GRB.MINIMIZE
        self.modelGurobi.setObjective(quicksum(self.x[i,j]*c[i,j] for i,j in self.A))

        #Constraints
        self.modelGurobi.addConstrs(quicksum(self.x[i,j] for j in V if j!=i)==1 for i in N);
        self.modelGurobi.addConstrs(quicksum(self.x[i,j] for i in V if i!=j)==1 for j in N);
        self.modelGurobi.addConstrs((self.x[i,j]==1) >> (u[i]+q[i]==u[j]) 
                        for i,j in self.A if i!=0 and j!=0);
        self.modelGurobi.addConstrs(u[i]>=q[i] for i in N);
        self.modelGurobi.addConstrs(u[i]<=Q for i in N);

        print('Model initialized successfully')

    @abstractmethod
    def optimizeModel(self):
        pass