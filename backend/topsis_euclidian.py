import numpy as np

class TopsisEuclidian:
    def __init__(self, matrix, weights, is_benefit):
        self.matrix = matrix
        self.weights = weights
        self.is_benefit = is_benefit

    def normalize_matrix(self):
        return self.matrix / np.sqrt(np.sum(self.matrix**2, axis=0))

    def calculate_weighted_matrix(self):
        normalized_matrix = self.normalize_matrix()
        return normalized_matrix * self.weights

    def calculate_ideal_solution(self):
        weighted_matrix = self.calculate_weighted_matrix()
        return np.max(weighted_matrix, axis=0) if self.is_benefit.any() else np.min(weighted_matrix, axis=0)

    def calculate_negative_ideal_solution(self):
        weighted_matrix = self.calculate_weighted_matrix()
        return np.min(weighted_matrix, axis=0) if self.is_benefit.any() else np.max(weighted_matrix, axis=0)

    def calculate_distances_to_ideal(self):
        weighted_matrix = self.calculate_weighted_matrix()
        ideal_solution = self.calculate_ideal_solution()
        return np.sqrt(np.sum((weighted_matrix - ideal_solution)**2, axis=1))

    def calculate_distances_to_negative_ideal(self):
        weighted_matrix = self.calculate_weighted_matrix()
        negative_ideal_solution = self.calculate_negative_ideal_solution()
        return np.sqrt(np.sum((weighted_matrix - negative_ideal_solution)**2, axis=1))

    def calculate_relative_closeness(self):
        distance_to_ideal = self.calculate_distances_to_ideal()
        distance_to_negative_ideal = self.calculate_distances_to_negative_ideal()
        return distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)

    def topsis_euc(self):
        relative_closeness = self.calculate_relative_closeness()
        rankings = np.argsort(relative_closeness)[::-1] + 1
        return rankings.tolist()


