from ..Simulation import Simulation

simulation = Simulation(
    data_folder='./InowasOptimization/tests/test_data',
    bin_folder='./bin',
    optimization_id='test_optimization_problem',
    simulation_id = 'test_simulaion'
)

objects_data = [
    {
        "id": 0,
        "type": "well",
        "position": {
            "row": {
                "min": 30,
                "max": 150,
                "result": 100
            },
            "col": {
                "min": 30,
                "max": 150,
                "result": 100
            },
            "lay": {
                "min": 0,
                "max": 0,
                "result": 0
            }
        },
        "flux": {
            "0": {
                "min": 720,
                "max": 720,
                "result": 720
            }
        },
        "concentration": {
            "0": {
                "component1": {
                    "min": 0,
                    "max": 0,
                    "result": 0
                }
            }
        }
    },
    {
        "id": 1,
        "type": "well",
        "position": {
            "row": {
                "min": 30,
                "max": 150,
                "result": 110
            },
            "col": {
                "min": 30,
                "max": 150,
                "result": 110
            },
            "lay": {
                "min": 0,
                "max": 0,
                "result": 0
            }
        },
        "flux": {
            "0": {
                "min": 720,
                "max": 720,
                "result": 720
            }
        },
        "concentration": {
            "0": {
                "component1": {
                    "min": 0,
                    "max": 0,
                    "result": 0
                }
            }
        }
    }
]



fitness = simulation.evaluate(objects_data)
print(fitness)