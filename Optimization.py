import os
import shutil
import random
import json
import uuid
import numpy as np
from mystic.solvers import NelderMeadSimplexSolver
from mystic.monitors import Monitor
from mystic.termination import CandidateRelativeTolerance as CRT
from sklearn.cluster import KMeans
from deap import base
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools
import copy
import pika

class OptimizationBase(object):
    """
    Optimization algorithm class

    """

    def __init__(self, request_data, response_channel, response_queue, data_folder, rabbit_host,
                 rabbit_port, rabbit_vhost, rabbit_user, rabbit_password, simulation_request_queue, simulation_response_queue):

        self.response_queue = response_queue
        self.response_channel = response_channel
        self.host = rabbit_host
        self.port = int(rabbit_port)
        self.login = rabbit_user
        self.password = rabbit_password
        self.virtualhost = rabbit_vhost
        self.request_data = request_data
        
        self._progress_log = []
        self._iter_count = 0

        
        
        try:
            self.optimization_id = self.request_data['optimization']['id']
        except KeyError:
            self.optimization_id = str(uuid.uuid4())

        self.data_dir = os.path.join(
            os.path.realpath(data_folder),
            str(self.optimization_id)
        )
        self.config_file = os.path.join(
            self.data_dir,
            'config.json'
        )
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        with open(self.config_file, 'w') as f:
            json.dump(self.request_data, f)
        
        self.var_template = copy.deepcopy(self.request_data['optimization']['objects'])

        self.weights = [i["weight"] for i in self.request_data["optimization"]["objectives"]]
        
        self.var_map, self.bounds, self.initial_values = self.read_optimitation_data()

        # Rabbit stuf
        self.simulation_request_queue = simulation_request_queue
        self.simulation_response_queue = simulation_response_queue+str(self.optimization_id)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.virtualhost,
                credentials=pika.PlainCredentials(self.login, self.password),
            )
        )

        self.simulation_request_channel = self.connection.channel()
        print('Declaring simulation request queue: '+self.simulation_request_queue)
        self.simulation_request_channel.queue_declare(
            queue=self.simulation_request_queue,
            durable=True,
            auto_delete=False
        )
        
        self.simulation_response_channel = self.connection.channel()
        print('Declaring simulation response queue: '+simulation_response_queue)
        self.simulation_response_channel.queue_declare(
            queue=self.simulation_response_queue,
            durable=True
        )
    
    def clean(self):
        print('Deleting simulation response queue...')
        self.simulation_response_channel.queue_delete(
            self.simulation_response_queue
        )
        print('Closing connection...')
        self.connection.close()

        print('Deleting optimization temp folder...')
        shutil.rmtree(self.data_dir)


    def send_simulation_jobs(self, individual, ind_id):

        print(" [x] Requesting fitness for individual {}".format(individual))
        print(" Publishing simulation job for individual {} to the queue: {}"\
        .format(individual, self.simulation_request_queue))

        objects_data = self.apply_individual(
            individual = individual
        )

        request_data = {
            'ind_id': ind_id,
            'simulation_id': str(uuid.uuid4()),
            'objects_data': objects_data,
            'optimization_id': self.optimization_id
        }
        request_data = json.dumps(request_data).encode()

        self.simulation_request_channel.basic_publish(
            exchange='',
            routing_key=self.simulation_request_queue,
            body=request_data,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )
        return

    def apply_individual(self, individual):
        """Write individual values to variable template and return the filled template"""    
        for ind_value, keys in zip(individual, self.var_map):
            if keys[1] == 'concentration':
                for object_ in self.var_template:
                    if object_['id'] == keys[0]:
                        object_[keys[1]][keys[2]][keys[3]]['result'] = ind_value
                        break
            else:
                for object_ in self.var_template:
                    if object_['id'] == keys[0]:
                        object_[keys[1]][keys[2]]['result'] = ind_value
                        break
                    
        
        return self.var_template

    def read_optimitation_data(self):
        """
        Example of variables template, where values are fixed ones and Nones are optimized:
        
        Example of variables map and variables boundries:
        var_map = [(0, flux, 0), (0, concentration, 0),(0, position, row),(0, position, col)]
        var_bounds = [(0, 10), (0, 1),(0, 30),(0, 30)]
        """

        var_map = []
        var_bounds = []
        initial_values = []

        for object_ in self.var_template:
            for parameter, value in object_.items():
                if parameter == 'position':
                    for axis, axis_data in value.items():
                        if axis_data['min'] != axis_data['max']:
                            var_map.append((object_['id'], 'position', axis))
                            var_bounds.append((axis_data['min'], axis_data['max']))
                            object_['position'][axis]['result'] = None
                            initial_values.append(axis_data.get('initial'))
                        else:
                            object_['position'][axis]['result'] = axis_data['min']
                            

                elif parameter == 'flux':
                    for period, period_data in value.items():
                        if period_data['min'] != period_data['max']:
                            var_map.append((object_['id'], 'flux', period))
                            var_bounds.append((period_data['min'], period_data['max']))
                            object_['flux'][period]['result'] = None
                            initial_values.append(period_data.get('initial'))
                        else:
                            object_['flux'][period]['result'] = period_data['min']
                        
                
                elif parameter == 'concentration':
                    for period, period_data in value.items():
                        for component, component_data in period_data.items():
                            if component_data['min'] != component_data['max']:
                                var_map.append((object_['id'], parameter, period, component))
                                var_bounds.append((component_data['min'], component_data['max']))
                                object_[parameter][period][component]['result'] = None
                                initial_values.append(component_data.get('initial'))
                            else:
                                object_[parameter][period][component]['result'] = component_data['min']
                    

        return var_map, var_bounds, initial_values


class NSGA(OptimizationBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._hypervolume_ref_point = None
        self._diversity_ref_point = None
    
    def run(self):

        ngen = self.request_data['optimization']['parameters']['ngen']
        pop_size = self.request_data['optimization']['parameters']['pop_size']
        mutpb = self.request_data['optimization']['parameters']['mutpb']
        cxpb = self.request_data['optimization']['parameters']['cxpb']
        mu = pop_size
        eta = self.request_data['optimization']['parameters']['eta']
        indpb = self.request_data['optimization']['parameters']['indpb']
        ncls = self.request_data['optimization']['parameters']['ncls']
        qbound = self.request_data['optimization']['parameters']['qbound']
        # diversity_flg = self.request_data['optimization']['parameters']['diversity_flg']
        diversity_flg = False

        creator.create(
            "Fitnessmulti", base.Fitness,
            weights=self.weights
        )
        creator.create("Individual", list, fitness=creator.Fitnessmulti)
        self.toolbox = base.Toolbox()
        self.toolbox.register("candidate", self.make_candidate, self.bounds)
        self.toolbox.register(
            "mutate", tools.mutPolynomialBounded,
            low=[i[0] for i in self.bounds], up=[i[1] for i in self.bounds],
            eta=eta, indpb=indpb
        )
        self.toolbox.register(
            "mate", tools.cxSimulatedBinaryBounded,
            low=[i[0] for i in self.bounds], up=[i[1] for i in self.bounds],
            eta=eta
        )
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.candidate)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("select", tools.selNSGA2)

        pop = self.toolbox.population(n=mu)
        pop = self.evaluate_population(pop=pop)
        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        pop = self.toolbox.select(pop, len(pop))
        # response = self.callback(pop=pop, final=False)

        # Begin the generational process
        for gen in range(1, ngen):
            offspring = self.generate_offspring(pop, cxpb, mutpb, mu)
            offspring = self.evaluate_population(pop=offspring)
            combined_pop = pop + offspring

            if diversity_flg:
                pop = self.check_diversity(combined_pop, ncls, qbound, mu)
            else:
                pop = self.toolbox.select(combined_pop, mu)
    
            self.calculate_hypervolume(pop)
    
            print('Generating response for iteration No. {}'.format(gen))
            response = self.callback(pop=pop, final=gen==ngen-1)

        return

    def callback(self, pop, final, status_code=200):
        """
        Generate response json of the NSGA algorithm
        """
        self._iter_count += 1
        response = {}
        response['status_code'] = status_code
        response['solutions'] = []
        for individual in pop:
            response['solutions'].append(
                {
                    'fitness': list(individual.fitness.values),
                    'variables': list(individual),
                    'objects': self.apply_individual(individual)
                }
            )
        response['progess_log'] = self._progress_log
        response['iteration'] = self._iter_count
        response['final'] = final
        
        response = json.dumps(response).encode()

        self.response_channel.basic_publish(
            exchange='',
            routing_key=self.response_queue,
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )

        return response

    def generate_offspring(self, pop, cxpb, mutpb, mu):
        # Vary population. Taken from def varOr()
        offspring = []
        for _ in range(mu):
            op_choice = random.random()
            if op_choice < cxpb:            # Apply crossover
                ind1, ind2 = map(self.toolbox.clone, random.sample(pop, 2))
                ind1, ind2 = self.toolbox.mate(ind1, ind2)
                del ind1.fitness.values
                offspring.append(ind1)
            elif op_choice < cxpb + mutpb:  # Apply mutation
                ind = self.toolbox.clone(random.choice(pop))
                ind, = self.toolbox.mutate(ind)
                del ind.fitness.values
                offspring.append(ind)
            else:                           # Apply reproduction
                offspring.append(random.choice(pop))
        
        return offspring
    
    def check_diversity(self, pop, ncls, qbound, mu):

        Q_diversity, cluster_labels = self.project_and_cluster(n_clasters=ncls, pop=pop)
        if self._diversity_ref_point is None:
            self._diversity_ref_point = qbound * Q_diversity
    
        print('Performing clustering and diversity calculation...'.format(gen))
        
        if Q_diversity < Q_diversity_bound:
            print(' Q diversity index {} lower than boundary {}. Diversity will be enhanced...'.format(
                Q_diversity, self._diversity_ref_point
            ))

            pop = self.diversity_enhanced_selection(
                pop=pop, cluster_labels=cluster_labels,
                mu=mu, selection_method=self.toolbox.select
            )
        else:
            pop = self.toolbox.select(pop, mu)
        
        self._diversity_ref_point = qbound * Q_diversity

        return pop
    
    def calculate_hypervolume(self, pop):

        print('Calculating hypervolume...')

        if self._hypervolume_ref_point is None:
            print('Calculating hypervolume reference point...')
            worst_values = []
            fitness_array = np.array([i.fitness.values for i in pop])
            maxs = np.max(fitness_array, 0)
            mins = np.min(fitness_array, 0)
            for i, weight in enumerate(self.weights):
                if weight <= 0:
                    worst_values.append(maxs[i])
                else:
                    worst_values.append(mins[i])
            self._hypervolume_ref_point = np.array(worst_values)


        hv = hypervolume(pop, self._hypervolume_ref_point)
        self._progress_log.append(hv)
        print('Hypervolume of the generation: {}'.format(self._progress_log[-1]))
        

    def evaluate_population(self, pop):

        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        print('Initial fitnesses:')
        print([ind.fitness.values for ind in pop])

        results = {}
        for _id, ind in enumerate(invalid_ind):
            self.send_simulation_jobs(
                ind, _id
            )

        consumer_tag = str(uuid.uuid4())
        def consumer_callback(channel, method, properties, body):
            content = json.loads(body.decode())
            results[content['ind_id']] = content['fitness']
            if len(results) == len(invalid_ind):
                print('Fetched all results from the simulation response queue: '+self.simulation_response_queue)
                self.simulation_response_channel.basic_cancel(
                    consumer_tag=consumer_tag
                )
            return

        print('Consuming results from the simulation response queue: '+self.simulation_response_queue)
        self.simulation_response_channel.basic_consume(
            consumer_callback=consumer_callback,
            queue=self.simulation_response_queue,
            no_ack=True,
            exclusive=False,
            consumer_tag=consumer_tag
        )
        self.simulation_response_channel.start_consuming()

        for _id, ind in enumerate(invalid_ind):
            ind.fitness.values = results[_id]

        print('Result fitnesses:')
        print([ind.fitness.values for ind in pop])

        return pop
    
    @staticmethod
    def make_candidate(bounds):
        """Generates random initial individual"""
        return [
            random.randint(value[0], value[1]) for value in bounds
        ]

    @staticmethod
    def project_and_cluster(n_clasters, pop):
        # Implementation of the Project And Cluster algorithm proposed by Syndhya et al.
        fitnesses = np.array([ind.fitness.values for ind in pop])
        fitnesses_reprojected = np.zeros(fitnesses.shape)
        maximals = np.max(fitnesses, axis=0)
        ws = maximals ** -1
        for i, fitness in enumerate(fitnesses):
            fitnesses_reprojected[i] = ((1-np.dot(ws, fitness))/np.dot(ws, ws)) * ws + fitness

        #Applying K-means clustering
        kmeans = KMeans(n_clusters=n_clasters, random_state=0).fit(fitnesses_reprojected)
        cluster_labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        #Calculating cluster diversity index
        Q_diversity = 0
        for cluster_label, centroid in zip(np.unique(cluster_labels), centroids):
            cluster_inds = [i for i, j in zip(pop, cluster_labels) if j == cluster_label]
            # print('Cluster inds of cluster '+str(cluster))
            # print(cluster_inds)
            sum_of_distances = 0
            for ind in cluster_inds:
                sum_of_distances += np.linalg.norm(centroid - ind.fitness.values)
            Q_diversity += sum_of_distances / len(cluster_inds)

        return Q_diversity, cluster_labels

    @staticmethod
    def diversity_enhanced_selection(pop, cluster_labels, mu, selection_method):
        # Returns population with enhanced deversity
        diverse_pop = []
        cluster_pop_sorted = {}

        for cluster in np.unique(cluster_labels):
            cluster_inds = [i for i, j in zip(pop, cluster_labels) if j == cluster]
            cluster_pop_sorted[cluster] = selection_method(cluster_inds, len(cluster_inds))

        rank = 0
        while len(diverse_pop) < mu:
            for p in cluster_pop_sorted.values():
                try:
                    diverse_pop.append(p[rank])
                except IndexError:
                    pass
                if len(diverse_pop) == mu:
                    return diverse_pop
            rank += 1

        return diverse_pop

    # @staticmethod
    # def scalarization(fitness, reference_point, z_max, z_min):
    #     # Achevement Based Scalarization of a multidimensional fitness
    #     p = 10e-6 # augmentation coefficient
    #     w = [] # weight factors
    #     for i, j in zip(z_max, z_min):
    #         w.append(1 / (i - j))
        
    #     vector = []

    #     for i, j, k in zip(fitness, reference_point, w):
    #         vector.append(
    #             k * (i - j)
    #         )
    #     vector_augemnted = [i + p * sum(vector) for i in vector]
    #     scalar = max(vector_augemnted)

    #     return scalar


class NelderMead(OptimizationBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._best_scalar_fitness = None
        self._best_fitness = None
        self._best_individual = None
    
    def run(self):
        print('Start local optimization...')
        maxf = self.request_data['optimization']['parameters']['maxf']
        xtol = self.request_data['optimization']['parameters']['xtol']
        ftol = self.request_data['optimization']['parameters']['ftol']


        solver = NelderMeadSimplexSolver(len(self.initial_values))
        solver.SetInitialPoints(self.initial_values)

        solver.SetStrictRanges([i[0] for i in self.bounds], [i[1] for i in self.bounds])
        solver.SetEvaluationLimits(evaluations=maxf)
        solver.SetTermination(CRT(xtol=ftol, ftol=ftol))
        # Inverting weights (*-1) to convert problem to minimizing 
        solver.Solve(
            self.evaluate_single_solution,
            ExtraArgs=([weight * -1 for weight in self.weights]),
            callback=self.callback
        )
        solver.enable_signal_handler()

        #Finally
        self.callback(
            individual=solver.Solution(),
            final=True
        )

        return

    def callback(self, individual, final=False, status_code=200):
        """
        Generate response json of the NSGA algorithm
        """
        self._iter_count += 1
        self._progress_log.append(self._best_scalar_fitness*-1)

        response = {}
        response['status_code'] = status_code
        response['solutions'] = [
            {
                'fitness': list(self._best_fitness),
                'variables': list(self._best_individual),
                'objects': self.apply_individual(self._best_individual)
            }
        ]
        response['progess_log'] = self._progress_log
        response['iteration'] = self._iter_count
        response['final'] = final
        
        response = json.dumps(response).encode()

        self.response_channel.basic_publish(
            exchange='',
            routing_key=self.response_queue,
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )

        return
    
    def evaluate_single_solution(self, individual, *weights):
        """Returns scalar fitness if weghts, else vector fitness of a single individual"""

        self.send_simulation_jobs(individual, 0)

        fitness = []
        consumer_tag = str(uuid.uuid4())
        def consumer_callback(channel, method, properties, body):
            content = json.loads(body.decode())
            for i in content['fitness']:
                fitness.append(i)
            print('Fetched result from the simulation response queue: '+self.simulation_response_queue)
            self.simulation_response_channel.basic_cancel(
                consumer_tag=consumer_tag
            )
            return

        print('Consuming results from the simulation response queue: '+self.simulation_response_queue)
        self.simulation_response_channel.basic_consume(
            consumer_callback=consumer_callback,
            queue=self.simulation_response_queue,
            no_ack=True,
            exclusive=False,
            consumer_tag=consumer_tag
        )
        self.simulation_response_channel.start_consuming()

        scalar_fitness = 0
        for value, weight in zip(fitness, weights):
            scalar_fitness += value * weight
        
        if self._best_scalar_fitness is not None and scalar_fitness >= self._best_scalar_fitness:
            return scalar_fitness
        
        else:
            self._best_scalar_fitness = scalar_fitness
            self._best_fitness = fitness
            self._best_individual = individual
        
        return scalar_fitness
    