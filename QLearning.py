# Your opponent is always the first player. Your agent is always the second player.

import connect
import random
import operator


QTable = dict()


def qLearn(epsilon, alpha, episodes):
    # Repeat for each episode
    for _ in range(episodes):
        env = newEnv()
        currState = env.grid

        while (not env.grid_is_full()) and (not env.was_winning_move()):
            availableActions = env.available_actions
            selectedAction = greedyChooseAction(epsilon, availableActions, currState)
            env.act(action=selectedAction)
            reward = 1 if (env.was_winning_move()) else 0
            env = agentMove(env)
            QTable[currState, selectedAction] = ((1-alpha) * QTable[currState, selectedAction]) + ((alpha) * (reward + maxQ(env.available_actions, env.grid)))
            currState = env.grid


def greedyChooseAction(epsilon, availableActions, state):
    # Create sorted list of pairs of type (action, value)
    actionValues = []

    for action in availableActions:
        QValue = QTable.get((state, action), 0)
        actionValues.append((action, QValue))
        # If the default value is used, this means this state/action pair doesn't exist in the QTable, so add it
        if QValue == 0:
            QTable[(state, action)] = 0

    # Sort this list based on the value of the action, in descending order
    actionValues.sort(key=operator.itemgetter(1), reverse=True)

    # Pick the best action, or on occasion, another random action
    if random.random() < epsilon:
        chosenAction = actionValues[random.randint(1, len(actionValues)-1)][0]
    else:
        chosenAction = actionValues[0][0]
    return chosenAction


def maxQ(availableActions, state):
    # Create sorted list of pairs of type (action, value)
    actionValues = []
    for action in availableActions:
        QValue = QTable.get((state, action), 0)
        actionValues.append((action, QValue))
        # If the default value is used, this means this state/action pair doesn't exist in the QTable, so add it
        if QValue == 0:
            QTable[(state, action)] = 0

    # Sort this list based on the value of the action, in descending order
    actionValues.sort(key=operator.itemgetter(1), reverse=True)

    # Pick the value of the best action
    bestActionValue = actionValues[0][1]

    return bestActionValue


def newEnv():
    env = connect.Connect(verbose=True)
    env.reset(first_player='x')
    env = agentMove(env)
    return env


def agentMove(env):
    availableActions = env.available_actions
    selectedActionIndex = random.randint(0,len(availableActions)-1)
    selectedAction = availableActions[selectedActionIndex]
    env.act(action=selectedAction)
    env.change_turn()
    return env


qLearn(0.2, 0.1, 10)