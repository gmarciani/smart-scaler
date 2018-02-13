from services.common.model.ai.qlearning.agent import SimpleQLearningAgent
from services.common.model.ai.qlearning import rewarding as rewarding_functions
import random
import unittest


class QLearningAgentTestCase(unittest.TestCase):

    def test_binary_serialization(self):
        """
        Test the binary serialization.
        :return: None
        """
        states = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        actions = [-1, 0, 1]

        iterations = 100

        agent = SimpleQLearningAgent(states, actions)

        actual = SimpleQLearningAgent.from_binarys(agent.to_binarys())
        expected = agent
        self.assertEqual(expected, actual, "Binary serialization error")

        for i in range(iterations):

            curr_state = random.choice(states)

            reward = agent.get_reward(curr_state)

            agent.learn(reward, curr_state)

            action = agent.get_action(curr_state)

            agent.save_experience(curr_state, action)

        actual = SimpleQLearningAgent.from_binarys(agent.to_binarys())
        expected = agent
        self.assertEqual(expected, actual, "Binary serialization error")

    def test_learning(self):
        """
        Test the learning loop.
        :return: None
        """
        states = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        actions = [-1, 0, 1]
        alpha = 0.5
        gamma = 0.5
        epsilon = 0.1
        rewarding_function = rewarding_functions.stupid_rewarding_function

        iterations = 100

        agent = SimpleQLearningAgent(states, actions, alpha, gamma, epsilon, rewarding_function)

        for i in range(iterations):

            curr_state = random.choice(states)

            reward = agent.get_reward(curr_state)

            agent.learn(reward, curr_state)

            action = agent.get_action(curr_state)

            agent.save_experience(curr_state, action)


if __name__ == "__main__":
    unittest.main()
