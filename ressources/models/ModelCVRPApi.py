from ressources.models.ModelCVRP import ModelCVRP

class ModelCVRPApi(ModelCVRP):

    def readFromData(self, data):
        self.xcords = data['xcords']
        self.ycords = data['ycords']
        self.capacity = data['capacity']

    def setParameters(self, parameters):
        if 'gap' in parameters and parameters['gap'] > 0:
            self.modelGurobi.Params.MIPGap = parameters['gap']
        if 'time_limit' in parameters and parameters['time_limit'] > 0:
            self.modelGurobi.Params.TimeLimit = parameters['time_limit']
        if 'iterations_limit' in parameters and parameters['iterations_limit'] > 0:
            self.modelGurobi.Params.IterationLimit = parameters['iterations_limit']

    def optimizeModel(self, parameters):
        self.setParameters(parameters)
        self.modelGurobi.optimize()
        self.isOptimized = True
    
    #Serialize Class
    def toJson(self):
        return {
            "xcords": self.xcords,
            "ycords": self.ycords,
            "capacity": self.capacity,
        }
    
    #Get routes solution
    def getRoutesFromSolution(self):
        if(self.isOptimized):
            routes = [a for a in self.A if self.x[a].x > 0.99]
            tailleRoutes = len(routes)
            routes_final = [[routes[0]]]
            del routes[0]
            i = 0
            j = 0
            indice = 0
            while self.calculateLen(routes_final) != tailleRoutes:
                #Cas où la taille de la route est = à 0
                if(len(routes_final[i]) == 0):
                    if(routes[indice][0] == 0):
                        routes_final[i].append(routes[indice])
                        del routes[indice]
                elif routes[indice][0] == routes_final[i][j][1]:
                    routes_final[i].append(routes[indice])
                    j+=1
                    if routes[indice][1] == 0 and len(routes) > 1:
                        routes_final.append([])
                        i+=1
                        j=0
                    del routes[indice]
                indice += 1
                if (indice >= len(routes)):
                    indice = 0
            return routes_final


        else:
            return

    def calculateLen(self, routes_final):
        lenList = 0
        for i in range(len(routes_final)):
            for i in range(len(routes_final[i])):
                lenList += 1 
        return lenList
