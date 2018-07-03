import os
import sys
import json
import shutil

from InowasFlopyAdapter.InowasFlopyReadFitness import InowasFlopyReadFitness
from InowasFlopyAdapter.InowasFlopyCalculationAdapter import InowasFlopyCalculationAdapter


class Simulation(object):

    def __init__(self, data_folder, optimization_id, simulation_id):
        # Set model workspace
        self.model_ws = os.path.join(
            os.path.realpath(data_folder),
            str(optimization_id),
            str(simulation_id)
        )
        print('Set model workspace to {}'.format(self.model_ws))
        
        # Set configuration file name
        config_file = os.path.join(
            os.path.realpath(data_folder),
            str(optimization_id),
            'config.json'
        )
        print('Reading configulation file {}'.format(config_file))

        with open(config_file) as f:
            data = json.load(f)
        
        self.simulation_id = simulation_id
        self.flopy_version = data.get('version', '3.2.6')

        self.model_data = data['data']
        self.optimization_data = data['optimization']

        self.model_data['mf']['mf']['modelname'] = 'mf'
        self.model_data['mf']['mf']['model_ws'] = self.model_ws
        self.model_data['mf']['mf']['exe_name'] = self.model_data['mf']['mf']['exe_name']
    
        try:
            self.model_data['mt']['mt']['modelname'] = 'mt'
            self.model_data['mt']['mt']['model_ws'] = self.model_ws
            self.model_data['mt']['mt']['exe_name'] = self.model_data['mt']['mt']['exe_name']
  
        except KeyError:
            pass
    
    def evaluate(self, objects_data):
        """ """
        self.model_data = self.write_spd(self.model_data, objects_data)
        self.optimization_data['objects'] = objects_data

        flopy_adapter = InowasFlopyCalculationAdapter(
            self.flopy_version, self.model_data, self.simulation_id
        )

        fitness = InowasFlopyReadFitness(
            self.optimization_data, flopy_adapter
        )

        print('Deleting model files in: {}'.format(self.model_ws))
        shutil.rmtree(self.model_ws)

        return fitness.get_fitness()
    
    @staticmethod
    def write_spd(model_data, objects_data):
        """Write optimization objects data to model data SPD"""
        for obj in objects_data:
            lay = obj['position']['lay']['result']
            row = obj['position']['row']['result']
            col = obj['position']['col']['result']

            for key, record in obj.items():
                if key == 'flux':
                    #write wel package
                    if not 'wel' in model_data['mf']: 
                        model_data['mf']['wel'] = {}
                        model_data['mf']['packages'].append('wel')
                    if not 'stress_period_data' in model_data['mf']['wel']:
                        model_data["mf"]["wel"]["stress_period_data"] = {}

                    for period, value in record.items():
                        if period in model_data["mf"]["wel"]["stress_period_data"]: 
                            model_data["mf"]["wel"]["stress_period_data"][period].append([lay, row, col, value['result']])
                        else:
                            model_data["mf"]["wel"]["stress_period_data"][period]=[[lay, row, col, value['result']]]
                    
                elif key == 'concentration':
                    #write ssm package
                    dummy_concentration_value = 1.
                    well_itype = 2

                    if not 'ssm' in model_data['mt']: 
                        model_data['mt']['ssm'] = {}
                        model_data['mt']['packages'].append('ssm')
                    if not 'stress_period_data' in model_data['mt']['ssm']:
                        model_data['mt']['ssm']['stress_period_data'] = {}

                    for period, components in record.items():
                        if len(components) > 1:
                            record = [lay, row, col, dummy_concentration_value, well_itype]
                            for value in components.values():
                                record.append(value['result'])
                            
                        else:
                            for value in components.values():
                                record = [lay, row, col, value['result'], well_itype]
                        if period in model_data['mt']['ssm']['stress_period_data']:
                            model_data['mt']['ssm']['stress_period_data'][period].append(record)
                        else:
                            model_data['mt']['ssm']['stress_period_data'][period] = [record]
                    # print(model_data['mt']['ssm']['stress_period_data'])

        return model_data

