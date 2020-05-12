import gym

import matplotlib.pyplot as plt
import numpy as np

env = gym.make("MountainCar-v0")

LEARNING_RATE = 0.1

DISCOUNT = 0.95
EPISODES = 10000
SHOW_EVERY = 50
STATS_EVERY = 10

# Discretization granularity of the state space
DISCRETE_OS_SIZE = [20, 20]
discrete_os_win_size = (
    env.observation_space.high - env.observation_space.low
) / DISCRETE_OS_SIZE

# Exploration vs exploitation settings
epsilon = 1
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))


# Define Q-table based on the chosen discretization
q_table = np.random.uniform(
    low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n])
)

# For stats
ep_rewards = []
aggr_ep_rewards = {"ep": [], "avg": [], "max": [], "min": []}

for episode in range(EPISODES + 1):

    episode_reward = 0

    discrete_state = get_discrete_state(env.reset())
    done = False

    if episode % SHOW_EVERY == 0:
        render = True
        print(episode)
    else:
        render = False

    while not done:

        # Balance between exploration and exploitation
        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(q_table[discrete_state])
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)

        new_state, reward, done, _ = env.step(action)

        # Update current reward
        episode_reward += reward

        new_discrete_state = get_discrete_state(new_state)

        if render:
            env.render()

        # If simulation did not end yet after last step - update Q table
        if not done:

            # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_discrete_state])

            # Current Q value (for current state and performed action)
            current_q = q_table[discrete_state + (action,)]

            # And here's our equation for a new Q value for current state and action
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (
                reward + DISCOUNT * max_future_q
            )

            # Update Q table with new Q value
            q_table[discrete_state + (action,)] = new_q

        # Simulation ended (for any reson) - if goal position is achived
        elif new_state[0] >= env.goal_position:
            q_table[discrete_state + (action,)] = 0

        discrete_state = new_discrete_state

    # Decaying is being done every episode if episode number is within decaying range
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value

    ep_rewards.append(episode_reward)
    if episode % STATS_EVERY == 0:
        average_reward = sum(ep_rewards[-STATS_EVERY:]) / STATS_EVERY
        aggr_ep_rewards["ep"].append(episode)
        aggr_ep_rewards["avg"].append(average_reward)
        aggr_ep_rewards["max"].append(max(ep_rewards[-STATS_EVERY:]))
        aggr_ep_rewards["min"].append(min(ep_rewards[-STATS_EVERY:]))
        print(
            f"Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}"
        )

    # if episode % 100 == 0:
    #     np.save(f"mountaincar_qtables/{episode}-qtable.npy", q_table)

plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["avg"], label="average rewards")
plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["max"], label="max rewards")
plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["min"], label="min rewards")
plt.legend(loc=4)
plt.savefig("mountaincar.png")

env.close()