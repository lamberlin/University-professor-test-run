import numpy as np


class EpsilonGreedyMAB:
    def __init__(self, epsilon, n_arms):
        self.epsilon = epsilon  # Exploration probability
        self.n_arms = n_arms  # Number of arms/models
        self.counts = np.zeros(n_arms)  # Count of selections for each arm
        self.values = np.zeros(n_arms)  # Value estimate for each arm

    def select_arm(self):
        # With probability epsilon, select a random arm
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.n_arms)
        # Otherwise, select the arm with the current highest value
        else:
            return np.argmax(self.values)

    def update(self, chosen_arm, reward):
        # Update counts and compute new value based on received reward
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        # New value is a running average of the rewards for this arm
        new_value = ((n - 1) * value + reward) / n
        self.values[chosen_arm] = new_value


def mab_tune_weights(data, epsilon=0.1):
    mab = EpsilonGreedyMAB(epsilon, 2)

    weights = data[['weight1', 'weight2']].values
    model_scores = data[['Model1', 'Model2']].values
    user_scores = data['User scores'].values

    for i in range(len(data)):
        chosen_arm = mab.select_arm()
        not_chosen_arm = 1 - chosen_arm

        predicted_score_chosen = model_scores[i, chosen_arm]
        predicted_score_not_chosen = model_scores[i, not_chosen_arm]

        if user_scores[i] > 5:
            if predicted_score_chosen > predicted_score_not_chosen:
                reward = 1
            else:
                reward = -1
        else:
            if predicted_score_chosen < predicted_score_not_chosen:
                reward = 1
            else:
                reward = -1

        mab.update(chosen_arm, reward)

    return mab.values


def softmax(x):
    e_x = np.exp(x - np.max(x)) 
    return e_x / e_x.sum()


def cac_weight(data):

    updated_values = mab_tune_weights(data)

    final_weights = softmax(updated_values)

    return final_weights
