from .OptimizationAlgorithm import OptimizationAlgorithm
from components.Component import ComponentTypes as ct, Component, type_to_comp_class_map
import components.ComponentsUtil as comp_util
from random import choice, sample, randrange, random
import numpy as np
from tqdm import tqdm


class TSBMA(OptimizationAlgorithm):
    def __init__(
        self, components, compatibility_graphs, cache_path="res/cache/"
    ) -> None:
        super().__init__(compatibility_graphs)
        self.prohibited_solutions = set()
        self.components_hamming_distances = comp_util.get_components_hamming_distances(
            components, cache_path=cache_path
        )

    def _swap_random_components(
        self,
        individual,
        number_of_components_to_swap: int,
        budget,
        can_change_of_subgraph=False,
    ):
        components_to_swap = sample(
            sorted(individual.values(), key=lambda c: c.component_type),
            number_of_components_to_swap,
        )
        remaining_components = {
            comp for comp in individual.values() if comp not in components_to_swap
        }

        components_in_graphs = (
            remaining_components if can_change_of_subgraph else individual.values()
        )
        graphs_with_components = self.filter_graphs_with_all_component(
            components_in_graphs
        )

        if len(graphs_with_components) == 0:
            return individual

        commom_graphs = set.intersection(*graphs_with_components)

        if can_change_of_subgraph:
            selected_subgraph = choice(tuple(commom_graphs))
        else:
            selected_subgraph = next(iter(commom_graphs))

        new_components = set()
        remaining_budget = budget - self._calculate_individual_price(individual)

        for c in components_to_swap:
            valid_components = tuple(
                filter(
                    lambda c: c.price <= remaining_budget,
                    self.graphs_components[selected_subgraph][c.component_type],
                )
            )

            if len(valid_components) == 0:
                return individual

            selected_component = choice(valid_components)
            new_components.add(selected_component)
            remaining_budget -= selected_component.price

        swaped_individual = {
            c.component_type: c for c in remaining_components | new_components
        }

        return swaped_individual
    

    def _calculate_individual_score(self, individual, components_priorities=None):
        if components_priorities:
            return sum(individual[tp].mark * components_priorities[tp] for tp in ct)
        else:
            return sum(i.mark for i in individual.values())

    def _calculate_individual_price(self, individual):
        return sum(i.price for i in individual.values())

    def _calculate_population_score(self, population: list, components_priorities=None):
        scores = [
            self._calculate_individual_score(individual, components_priorities)
            for individual in population
        ]
        return np.array(scores)

    def _initialize_population(
        self,
        budget,
        individuals_per_graph=5,
        max_swap_iterations=1,
        min_components_to_swap=1,
        max_components_to_swap=2,
        components_priorities=None,
    ):
        population = []

        for _, components in self.graphs_components.items():
            for _ in range(individuals_per_graph):
                individual = {tp: components[tp][0] for tp in ct}

                if (
                    self._calculate_individual_price(individual)
                    > budget
                ):
                    continue

                threshold = (
                    self._calculate_individual_score(individual, components_priorities)
                    * 0.4
                )
                # individual = self.threshold_search(
                #     individual,
                #     threshold,
                #     budget,
                #     max_swap_iterations,
                #     min_components_to_swap,
                #     max_components_to_swap,
                #     False,
                #     components_priorities=components_priorities
                # )

                population.append(individual)

        return np.array(population)

    def calculate_individuals_hamming_distance_on_graph_level(
        self, individual_1, individual_2
    ):
        distance = 0
        for tp in ct:
            ind_1_tp_graphs = self.components_graphs[individual_1[tp]]
            ind_2_tp_graphs = self.components_graphs[individual_2[tp]]

            if len(ind_1_tp_graphs & ind_2_tp_graphs) == 0:
                distance += 1

        return distance

    def calculate_individuals_hamming_distance(self, individual_1, individual_2):
        distance = 0

        for tp in ct:
            distance += self.components_hamming_distances[individual_1[tp]][
                individual_2[tp]
            ]

        return distance

    def calculate_individual_hamming_distances_mean(self, individual, population):
        distances_sum = 0

        for pop_individual in population:
            if individual == pop_individual:
                continue

            distances_sum += self.calculate_individuals_hamming_distance(
                individual, pop_individual
            )

        distances_mean = distances_sum / len(population)

        return distances_mean

    def update_distances(
        self,
        population,
        distances=None,
        leaving_individual=None,
        entering_individual=None,
    ):
        if distances is None:
            distances = [
                self.calculate_individual_hamming_distances_mean(ind, population)
                for ind in population
            ]
            distances = np.array(distances)
        else:
            if leaving_individual is not None:
                for i in range(len(population)):
                    distance_to_leaving_individual = (
                        self.calculate_individuals_hamming_distance(
                            population[i], leaving_individual
                        )
                    )
                    updated_distance = distances[i] - (
                        distance_to_leaving_individual / (len(population) + 1)
                    )
                    distances[i] = updated_distance

            if entering_individual is not None:
                for i in range(len(population)):
                    distance_to_entering_individual = (
                        self.calculate_individuals_hamming_distance(
                            population[i], entering_individual
                        )
                    )
                    updated_distance = distances[i] + (
                        distance_to_entering_individual / (len(population) + 1)
                    )
                    distances[i] = updated_distance

        return distances

    def calculate_individuals_goodness(self, distances, pontuation, beta=0.7):
        d_min = np.min(distances)
        d_max = np.max(distances)

        f_min = np.min(pontuation)
        f_max = np.max(pontuation)

        normalized_f = (pontuation - f_min) / (f_max - f_min)
        normalized_d = (distances - d_min) / (d_max - d_min)

        scores = beta * normalized_f + (1 - beta) * normalized_d

        return scores

    def select_individuals_index(self, population: np.array, marks=None, random_selection=False, n=2):
        if not random_selection:
            return np.argsort(marks)[-n:]
        else:
            return np.random.choice(population.size, size=n, replace=False)

    def crossover(self, parent_1, parent_2, budget):
        commom_graphs_list = []
        commom_graphs_components_types = set()
        new_individual = {}

        for tp in ct:
            comp_1_graphs = self.components_graphs[parent_1[tp]]
            comp_2_graphs = self.components_graphs[parent_2[tp]]

            commom_graphs = comp_1_graphs & comp_2_graphs

            if len(commom_graphs) > 0:
                commom_graphs_components_types.add(tp)
                commom_graphs_list.append(commom_graphs)

        commom_to_all = set.intersection(*commom_graphs_list)

        remaining_budget = budget
        replace_uncommon_components = False

        if len(commom_to_all) > 0:
            selected_graph = choice(tuple(commom_to_all))

            for tp in commom_graphs_components_types:
                comp_1_price = parent_1[tp].price
                comp_2_price = parent_2[tp].price

                if comp_1_price > remaining_budget and comp_2_price > remaining_budget:
                    return choice((parent_1, parent_2))
                elif (
                    comp_1_price <= remaining_budget and comp_2_price > remaining_budget
                ):
                    new_individual[tp] = parent_1[tp]
                elif (
                    comp_1_price > remaining_budget and comp_2_price <= remaining_budget
                ):
                    new_individual[tp] = parent_2[tp]
                else:
                    new_individual[tp] = choice([parent_1[tp], parent_2[tp]])

                remaining_budget = budget - new_individual[tp].price

            for tp in set(ct) - commom_graphs_components_types:
                valid_components = tuple(
                    filter(
                        lambda c: c.price <= remaining_budget,
                        self.graphs_components[selected_graph][tp],
                    )
                )

                if len(valid_components) == 0:
                    replace_uncommon_components = True
                    break

                if not replace_uncommon_components:
                    new_individual[tp] = choice(valid_components)

                remaining_budget = budget - new_individual[tp].price
        else:
            return choice((parent_1, parent_2))

        if replace_uncommon_components:
            for tp in set(ct) - commom_graphs_components_types:
                new_individual[tp] = self.graphs_components[selected_graph][tp][0]

        if self._calculate_individual_price(new_individual) > budget:
            return choice((parent_1, parent_2))

        return new_individual

    def individual_mutation(self, individual, budget, mutation_probability=0.01):
        components_to_swap = np.random.binomial(len(individual), mutation_probability)

        if components_to_swap > 0:
            mutated_individual = self._swap_random_components(
                individual, components_to_swap, budget, True
            )
            return mutated_individual, True

        return individual, False

    def population_mutation(
        self, population, distances, budget, mutation_probability=0.01
    ):
        for i in range(len(population)):
            population[i], has_mutated = self.individual_mutation(
                population[i], budget, mutation_probability
            )

            if has_mutated:
                distances[i] = self.calculate_individual_hamming_distances_mean(
                    population[i], population
                )

    def threshold_search(
        self,
        individual,
        threshold,
        budget,
        max_iterations,
        min_components_to_swap=1,
        max_components_to_swap=2,
        can_change_of_subgraph=True,
        components_priorities=None,
    ):

        best_individual = individual
        best_mark = self._calculate_individual_score(individual, components_priorities)

        current_individual = individual

        i = 0

        while i < max_iterations:
            components_to_swap = randrange(
                min_components_to_swap, max_components_to_swap
            )
            swapped_individual = self._swap_random_components(
                current_individual, components_to_swap, budget, can_change_of_subgraph
            )
            swapped_individual_mark = self._calculate_individual_score(
                swapped_individual, components_priorities
            )
            swapped_individual_key = frozenset(swapped_individual.values())

            if (
                swapped_individual_mark >= threshold
                and swapped_individual_key not in self.prohibited_solutions
            ):
                current_individual = swapped_individual
                self.prohibited_solutions.add(swapped_individual_key)

            if swapped_individual_mark > best_mark:
                best_individual = swapped_individual
                best_mark = swapped_individual_mark
                i = 0
            else:
                i += 1

        return best_individual

    def calculate_best_solution(
        self,
        budget,
        generations,
        individuals_per_graph=5,
        threshold_iterations=5,
        min_components_to_swap=1,
        max_components_to_swap=2,
        components_priorities=None,
        random_parents=False,
        score_beta=0.7
    ):

        self.prohibited_solutions = set()
        print("initializing population...")
        population = self._initialize_population(
            budget,
            individuals_per_graph,
            threshold_iterations,
            min_components_to_swap,
            max_components_to_swap,
            components_priorities=components_priorities
        )
        distances = self.update_distances(population)
        marks = self._calculate_population_score(population, components_priorities)

        best_population_individual_index = np.argmax(marks)
        best_mark = marks[best_population_individual_index]
        best_individual = population[best_population_individual_index]

        for g in range(generations):
            parent_1, parent_2 = population[
                self.select_individuals_index(population, marks, random_parents)
            ]
            temp_individual = self.crossover(parent_1, parent_2, budget)
            temp_individual_mark = self._calculate_individual_score(
                temp_individual, components_priorities
            )

            threshold = temp_individual_mark * 0.5
            
            new_individual = self.threshold_search(
                temp_individual,
                threshold,
                budget,
                threshold_iterations,
                min_components_to_swap,
                max_components_to_swap,
                components_priorities=components_priorities,
            )
            new_individual_mark = self._calculate_individual_score(
                new_individual, components_priorities
            )

            distances = self.update_distances(
                population, distances, entering_individual=new_individual
            )

            population = np.append(population, new_individual)
            distances = np.append(
                distances,
                self.calculate_individual_hamming_distances_mean(
                    new_individual, population
                ),
            )
            marks = np.append(marks, new_individual_mark)

            scores = self.calculate_individuals_goodness(distances, marks, score_beta)
            leaving_individual_index = np.argmin(scores)

            population = np.delete(population, leaving_individual_index)
            distances = np.delete(distances, leaving_individual_index)
            marks = np.delete(marks, leaving_individual_index)

            distances = self.update_distances(
                population, distances, entering_individual=new_individual
            )

            if new_individual_mark > best_mark:
                if leaving_individual_index >= len(population):
                    best_population_individual_index = np.argmax(marks)
                    best_mark = marks[best_population_individual_index]
                    best_individual = population[best_population_individual_index]
                else:
                    best_mark = new_individual_mark
                    best_individual = new_individual

            price = sum([c.price for c in best_individual.values()])
            print(f"gen: {g};\t best mark: {best_mark * 100}; \tprice: {price}")


        ind = [f"{c.component_type.name}: {c.name}\t (price: R$ {c.price}, mark: {c.mark}, link: {c.link})" for c in best_individual.values()]
        print()
        print(*ind, sep="\n")
