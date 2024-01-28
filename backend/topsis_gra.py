import numpy as np

class TOPSIS_GRA:
    def __init__(self, matrix, weights, is_benefit):
        self.matrix = np.array(matrix)
        self.weights = np.array(weights)
        self.is_benefit = np.array(is_benefit)

    def normalize_matrix(self):
        normalized_matrix = self.matrix / np.sqrt(np.sum(self.matrix ** 2, axis=0))
        return normalized_matrix

    def calculate_gra(self):
        normalized_matrix = self.normalize_matrix()
        
        ideal_solution = np.max(normalized_matrix, axis=0) if self.is_benefit.any() else np.min(normalized_matrix, axis=0)

        # Calculate the absolute deviations from the ideal solution
        absolute_deviations = np.abs(normalized_matrix - ideal_solution)

        # Calculate the grey relational coefficients
        grey_relational_coefficients = np.exp(-0.5 * np.sum(self.weights * absolute_deviations, axis=1))

        # Calculate the relative closeness to the ideal solution
        relative_closeness = grey_relational_coefficients / np.sum(grey_relational_coefficients)

        # Rank the alternatives based on the relative closeness
        rankings = np.argsort(relative_closeness)[::-1] + 1

        return rankings.tolist()
