import docker
import os

class DockerManager(object):
    
    _simulation_server_command = 'python /Simulation/SimulationServer.py'
    _optimization_server_command = 'python /Optimization/OptimizationManager.py'

    def __init__(self, configuration):
        self.configuration = configuration
        self.client = docker.from_env()
        self.optimization_containers = []
        self.simulation_containers = []

        self.optimization_image = self.configuration['OPTIMIZATION_IMAGE']
        self.simulation_image = self.configuration['SIMULATION_IMAGE']
    
        self.volumes = {
            os.path.realpath(self.configuration['HOST_TEMP_FOLDER']): {'bind': self.configuration['DOCKER_TEMP_FOLDER'], 'mode': 'rw'},
            os.path.realpath('./Optimization'): {'bind': '/Optimization', 'mode': 'rw'},
            os.path.realpath('./Simulation'): {'bind': '/Simulation', 'mode': 'rw'}
        }
    def get_containers(self, container_type, status='running'):
        if container_type == 'optimization':
            image = self.optimization_image
        elif container_type == 'simulation':
            image = self.simulation_image
        else:
            print('Invald container type - {}'.format(container_type))
            return []

        containers = self.client.containers.list(
            filters={
                'ancestor': image,
                'status': status
            }
        )
        return containers
    
    def count_simulation_containers(self, status='running'):
        containers = self.get_containers('simulation', status)
        return len(containers)

    def count_optimization_containers(self, status='running'):
        containers = self.get_containers('optimization', status)
        return len(containers)
    
    def run_optimization_container(self, number):
        for _ in range(number):
            container = self.client.containers.run(
                self.optimization_image,
                command=self._optimization_server_command,
                environment=self.configuration,
                volumes=self.volumes,
                detach=True
            )
            self.optimization_containers.append(container)
        return

    def run_simulation_container(self, number):
        for _ in range(number):
            container = self.client.containers.run(
                self.simulation_image,
                command=self._simulation_server_command,
                environment=self.configuration,
                volumes=self.volumes,
                detach=True
            )
            self.simulation_containers.append(container)
        
    
    def stop_all_simulation_containers(self, remove=True):
        containers = self.get_containers('simulation', 'running')
        print('Total {} Simulation containers running'.format(len(containers)))
        for container in containers:
            self.stop_container(container)
            if remove:
                self.remove_container(container)

        return
    
    def stop_all_optimization_containers(self, remove=True):
        containers = self.get_containers('optimization', 'running')
        print('Total {} Optimization containers running'.format(len(containers)))
        for container in containers:
            self.stop_container(container)
            if remove:
                self.remove_container(container)

        return
    
    def stop_own_simulation_containers(self, remove=True):
        containers = self.simulation_containers
        print('{} own Simulation containers running'.format(len(containers)))
        for container in containers:
            self.stop_container(container)
            if remove:
                self.remove_container(container)
        return
    
    def stop_own_optimization_containers(self, remove=True):

        containers = self.optimization_containers
        print('{} own Optimization containers running'.format(len(containers)))
        
        for container in containers:
            self.stop_container(container)
            if remove:
                self.remove_container(container)

        return
    
    def remove_exited_containers(self):
        containers = self.client.containers.list(
            filters={
                'status': 'exited'
            }
        )
        for container in containers:
            container.remove()

    
    def clean(self):
        self.stop_own_optimization_containers(remove=True)
        self.stop_own_simulation_containers(remove=True)
        self.optimization_containers = []
        self.simulation_containers = []
    
    def clean_all(self):
        self.stop_all_optimization_containers(remove=True)
        self.stop_all_simulation_containers(remove=True)
        self.optimization_containers = []
        self.simulation_containers = []
    
    @staticmethod
    def stop_container(container):
        try:
            container.stop()
            print('Stoped container {}'.format(container.id))
        except:
            print('Could not stop container {}'.format(container.id))
            pass
        return
    
    @staticmethod
    def remove_container(container):
        try:
            container.remove()
            print('Removed container {}'.format(container.id))
        except:
            print('Could not remove container {}'.format(container.id))
            pass
        return