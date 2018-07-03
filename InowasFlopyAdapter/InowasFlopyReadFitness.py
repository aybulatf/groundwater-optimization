"""
Calculation of objective values of a model 

Author: Aybulat Fatkhutdinov
"""

import os
import math
import numpy as np
import flopy


class InowasFlopyReadFitness:
    """Calculation of objective values of a model """

    def __init__(self, optimization_data, flopy_adapter):

        self.optimization_data = optimization_data

        self.dis_package = flopy_adapter._mf.get_package('DIS')
        self.model_ws = flopy_adapter._mf.model_ws
        self.model_name = flopy_adapter._mf.namefile.split('.')[0]
        self.objects = self.optimization_data['objects']

        objectives_values = self.read_objectives()
        constraints_exceeded = self.check_constraints()

        if True in constraints_exceeded or None in objectives_values:
            self.fitness = [obj["penalty_value"] for obj in optimization_data["objectives"]]
        else:
            self.fitness = objectives_values


    def get_fitness(self):

        return self.fitness

    def read_objectives(self):
        "Returnes fitnes list"
        fitness = []

        for objective in self.optimization_data["objectives"]:

            if objective["type"] == "concentration":
                mask = self.make_mask(
                    objective["location"], self.objects, self.dis_package
                )
                value = self.read_concentration(objective, mask, self.model_ws, self.model_name)

            elif objective["type"] == "head":
                mask = self.make_mask(
                    objective["location"], self.objects, self.dis_package
                )
                value = self.read_head(objective, mask, self.model_ws, self.model_name)
          

            elif objective["type"] == "flux":
                value = self.read_flux(objective, self.objects)

            
            elif objective["type"] == "input_concentration":
                value = self.read_input_concentration(objective, self.objects)
            
            value = self.summary(value, objective["summary_method"])
            print('Fitness value: {}'.format(value))
            fitness.append(value.item())

        return fitness
    
    def check_constraints(self):
        """Returns a list of penalty values"""
        constraints_exceeded = []

        for constraint in self.optimization_data["constraints"]:

            if constraint["type"] == 'head':
                mask = self.make_mask(
                    constraint["location"], self.objects, self.dis_package    
                )
                value = self.read_head(
                    constraint, mask, self.model_ws, self.model_name
                )
   
            elif constraint["type"] == 'concentration':
                mask = self.make_mask(
                    constraint["location"], self.objects, self.dis_package    
                )
                value = self.read_concentration(
                    constraint, mask, self.model_ws, self.model_name
                )
            
            elif constraint["type"] == "flux":
                value = self.read_flux(
                    constraint, self.objects
                )
            
            elif constraint["type"] == "input_concentrations":
                value = self.read_input_concentration(
                    constraint, self.objects
                )
            
            value = self.summary(value, constraint["summary_method"])
            
            
            if constraint["operator"] == "less":
                if value > constraint["value"]:
                    print("Constraint value {} exceeded max value {}, penalty will be assigned".format(value, constraint["value"]))
                    constraints_exceeded.append(True)
                else:
                    constraints_exceeded.append(False)
                
            elif constraint["operator"] == "more":
                if value < constraint["value"]:
                    print("Constraint value {} lower than min value {}, penalty will be assigned".format(value, constraint["value"]))
                    constraints_exceeded.append(True)
                else:
                    constraints_exceeded.append(False)

        return constraints_exceeded
    
    @staticmethod
    def summary(result, method):
        if method == 'mean':
            result = np.nanmean(result)
        elif method == 'max':
            result = np.max(result)
        elif method == 'min':
            result = np.min(result)
        else:
            print("Unknown summary method {}. Using max".format(method))
            result = np.max(result)
        
        return result


    @staticmethod
    def read_head(data, mask, model_ws, model_name):
        "Reads head file"

        print('Read head values at location: {}'.format(data['location']))
        
        try:
            head_file_object = flopy.utils.HeadFile(
                os.path.join(model_ws, model_name) + '.hds')
            head = head_file_object.get_alldata(
                nodata=-9999
                )
            head = head[mask]

            head_file_object.close()

        except Exception as e:
            print('Head file of the model: '+model_name+' could not be opened')
            print(str(e))
            return head

        return head
    
    @staticmethod
    def read_concentration(data, mask, model_ws, model_name):
        "Reads concentrations file"

        print('Read concentration values at location: {}'.format(data['location']))

        try:
            conc_file_object = flopy.utils.UcnFile(
                os.path.join(model_ws, data["conc_file_name"]))
            conc = conc_file_object.get_alldata(
                nodata=-9999
                )
            conc = conc[mask]

            conc_file_object.close()
        
        except Exception as e:
            print('Concentrations file of the model: '+model_name+' could not be opened')
            print(str(e))
            return conc

        return conc
    
    @staticmethod
    def read_flux(data, objects):
        "Reads wel fluxes"

        print('Read flux values at location: {}'.format(data['location']))

        fluxes = np.array([])

        try:
            obj_ids = data["location"]["objects"]
        except KeyError:
            print("ERROR! Objective location of type Flux has to be an Object!")
            return None

        for obj in objects:
            if obj['id'] in obj_ids:
                obj_fluxes = []
                for period_data in obj['flux'].values():
                    obj_fluxes.append(period_data['result'])
        
                fluxes = np.hstack(
                    (fluxes,
                    np.array(obj_fluxes))
                )

        return fluxes
    
    @staticmethod
    def read_input_concentration(data, objects):

        print('Read input_concentration values at location: {}'.format(data['location']))

        input_concentrations = np.array([])

        try:
            component = data["component"]
        except KeyError:
            print("ERROR! Concentration component for the Objective of type input_concentrations is not defined!")
            return None
        
        try:
            obj_ids = data["location"]["objects"]
        except KeyError:
            print("ERROR! Objective location of type input_concentrations has to be an Object!")
            return None
        
        for obj in objects:
            if obj['id'] in obj_ids:
                obj_concentrations = []
                for period_data in obj['concentration'].values():
                    obj_concentrations.append(period_data[component]['result'])
                input_concentrations = np.hstack(
                    (input_concentrations, 
                    np.array(obj_concentrations))
                )
        

        return input_concentrations
    
    @staticmethod
    def read_distance(data, objects):
        """Returns distance between two groups of objects"""

        print('Read distance between {} and {}'.format(data['location_1'], data['location_2']))

        location_1 = data["location_1"]
        location_2 = data["location_2"]
        
        objects_1 = None
        objects_2 = None

        if location_1['type'] == 'object':
            objects_1 = [
                obj for id_, obj in objects.items() if id_ in location_1['objects_ids']
            ]

        if location_2['type'] == 'object':
            objects_2 =[
                obj for id_, obj in objects.items() if id_ in location_2['objects_ids']
            ]
        
        distances = []
        if objects_1 is not None:
            for obj_1 in objects_1:
                if objects_2 is not None:
                    for obj_2 in objects_2:
                        dx = float(abs(obj_2['position']['col']['result'] - obj_1['position']['col']['result']))
                        dy = float(abs(obj_2['position']['row']['result'] - obj_1['position']['row']['result']))
                        dz = float(abs(obj_2['position']['lay']['result'] - obj_1['position']['lay']['result']))
                        distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
                else:
                    dx = float(abs(location_2['lay_row_col'][2] - obj_1['position']['col']['result']))
                    dy = float(abs(location_2['lay_row_col'][1] - obj_1['position']['row']['result']))
                    dz = float(abs(location_2['lay_row_col'][0] - obj_1['position']['lay']['result']))
                    distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
        else:
            if objects_2 is not None:
                for obj_2 in objects_2:
                    dx = float(abs(obj_2['position']['col']['result'] - location_1['lay_row_col'][2]))
                    dy = float(abs(obj_2['position']['row']['result'] - location_1['lay_row_col'][1]))
                    dz = float(abs(obj_2['position']['lay']['result'] - location_1['lay_row_col'][0]))
                    distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
            else:
                dx = float(abs(location_2['lay_row_col'][2]-location_1['lay_row_col'][2]))
                dy = float(abs(location_2['lay_row_col'][1]-location_1['lay_row_col'][1]))
                dz = float(abs(location_2['lay_row_col'][0]-location_1['lay_row_col'][0]))
                distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))

        distances = np.array(distances)
        
        return distances

    @staticmethod
    def make_mask(location, objects, dis_package):
        "Returns an array mask of location that has nper,nlay,nrow,ncol dimensions"

        print('Making mask array for location: {}'.format(location))
        nstp_flat = dis_package.nstp.array.sum()
        nrow = dis_package.nrow
        ncol = dis_package.ncol
        nlay = dis_package.nlay

        if location["type"] == 'bbox':
            try:
                per_min = location['per_min']
            except KeyError:
                per_min = 0

            try:
                per_max = location['per_max']
            except KeyError:
                per_max = nstp_flat

            try:
                lay_min = location['lay_min']
            except KeyError:
                lay_min = 0

            try:
                lay_max = location['lay_max']
            except KeyError:
                lay_max = nlay

            try:
                col_min = location['col_min']
            except KeyError:
                col_min = 0

            try:
                col_max = location['col_max']
            except KeyError:
                col_max = ncol

            try:
                row_min = location['row_min']
            except KeyError:
                row_min = 0

            try:
                row_max = location['row_max']
            except KeyError:
                row_max = nrow

            if per_min == per_max:
                per_max += 1
            if lay_min == lay_max:
                lay_max += 1
            if row_min == row_max:
                row_max += 1
            if col_min == col_max:
                col_max += 1
        
            mask = np.zeros((nstp_flat, nlay, nrow, ncol), dtype=bool)
            mask[
                per_min:per_max,
                lay_min:lay_max,
                row_min:row_max,
                col_min:col_max
            ] = True

        elif location["type"] == 'object':
            lays = []
            rows = []
            cols = []
            for obj in objects:
                if obj['id'] in location['objects']:
                    lays.append(obj['position']['lay']['result'])
                    rows.append(obj['position']['row']['result'])
                    cols.append(obj['position']['col']['result'])

            mask = np.zeros((nstp_flat, nlay, nrow, ncol), dtype=bool)
            mask[:,lays,rows,cols] = True
        
        return mask