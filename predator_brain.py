import numpy as np
INPUTS = 6
HIDDEN = 8
OUTPUTS = 2
class Brain:
    def __init__(self):
        """
        Neural network formation.
        Architecture: 6 inputs → 8 hidden → 2 outputs
        Total weights: (6*8) + (8*2) = 48 + 16 = 64
        """
        self.w1 = np.random.randn(INPUTS, HIDDEN) * 0.5
        self.w2 = np.random.randn(HIDDEN, OUTPUTS) * 0.5
        self.b1 = np.zeros(HIDDEN)
        self.b2 = np.zeros(OUTPUTS)

    def think(self, inputs):
        """
        Forward propagation.
        inputs: 6 numbers' array
        returns: 2 numbers [turn, speed]
        """
        hidden = np.tanh(inputs @ self.w1 + self.b1)

        output = np.tanh(hidden @ self.w2 + self.b2)
        return output
    
    def copy(self):
        new_brain = Brain()

        new_brain.w1 = self.w1.copy()
        new_brain.w2 = self.w2.copy()
        new_brain.b1 = self.b1.copy()
        new_brain.b2 = self.b2.copy()

        return new_brain

    def mutate(self, rate=0.1, strength=0.2):
        if np.random.rand() < rate:
            self.w1 += np.random.randn(*self.w1.shape) * strength

        if np.random.rand() < rate:
            self.w2 += np.random.randn(*self.w2.shape) * strength

        if np.random.rand() < rate:
            self.b1 += np.random.randn(*self.b1.shape) * strength

        if np.random.rand() < rate:
            self.b2 += np.random.randn(*self.b2.shape) * strength



