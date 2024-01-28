class SAW:
    def __init__(self, data, weights):
        self.data = data
        self.weights = weights
        self.num_alternatives = len(data)
        self.num_criteria = len(weights)

    def calculate_scores(self):
        scores = []

        for alternative in self.data:
            if len(alternative) != self.num_criteria:
                raise ValueError("Number of criteria weights and alternative values must match.")
            
            score = sum(alternative[i] * self.weights[i] for i in range(self.num_criteria))
            scores.append(score)

        return scores

# x_matrix = [[4,5,10],[3,10,6],[3,20,2],[2,15,5]] 
# alt_names = ["A", "B", "C", "D"]
# result1=mcdm.rank(x_matrix, alt_names=alt_names, n_method="Linear2", w_method="CRITIC", s_method="SAW")
# print(result1)
