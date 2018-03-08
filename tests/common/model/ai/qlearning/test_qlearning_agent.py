from services.common.model.ai.qlearning.qlearning_agent import QLearningAgent
from services.common.model.ai.qlearning import rewarding
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

        agent = QLearningAgent(states, actions)

        actual = QLearningAgent.from_binarys(agent.to_binarys())
        expected = agent
        self.assertEqual(expected, actual, "Binary serialization error")

        for i in range(iterations):

            curr_state = random.choice(states)

            reward = agent.get_reward(curr_state)

            agent.learn(reward, curr_state)

            action = agent.get_action(curr_state)

            agent.save_experience(curr_state, action)

        actual = QLearningAgent.from_binarys(agent.to_binarys())
        expected = agent
        self.assertEqual(expected, actual, "Binary serialization error")

    def test_learning(self):
        """
        Test the learning loop.
        :return: None
        """
        try:
            states = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            actions = [-1, 0, 1]
            alpha = 0.5
            gamma = 0.5
            epsilon = 0.1
            rewarding_function = rewarding.reward_naive

            iterations = 100

            agent = QLearningAgent(states, actions, alpha, gamma, epsilon, rewarding_function)

            for i in range(iterations):

                curr_state = random.choice(states)

                reward = agent.get_reward(curr_state)

                agent.learn(reward, curr_state)

                action = agent.get_action(curr_state)

                agent.save_experience(curr_state, action)
        except Exception as exc:
            self.fail("Error during learning loop: {}".format(exc))


if __name__ == "__main__":
    unittest.main()
