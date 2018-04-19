# Your opponent is always the first player. Your agent is always the second player.

import connect
import random
import operator


QTable = dict()


def qLearn(epsilon, alpha, episodes):
    # Repeat for each episode
    for i in range(episodes):
        env = newEnv()
        env.act(action=agentMove(env))
        currState = str(env.grid)

        while True:
            env.change_turn()
            availableActions = env.available_actions
            selectedAction = greedyChooseAction(epsilon, availableActions, currState)
            env.act(action=selectedAction)

            if (env.was_winning_move()):
                reward = 1
                QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                            (alpha) * (reward + maxQ(env.available_actions, str(env.grid))))
                break
            elif env.grid_is_full():
                reward = 0
                QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                            (alpha) * (reward + maxQ(env.available_actions, str(env.grid))))
                break
            else:
                env.change_turn()
                env.act(action=agentMove(env))
                if env.was_winning_move():
                    reward = -1
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                                (alpha) * (reward + maxQ(env.available_actions, str(env.grid))))
                    break
                elif env.grid_is_full():
                    reward = 0
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                                (alpha) * (reward + maxQ(env.available_actions, str(env.grid))))
                    break
                else:
                    reward = 0
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                                (alpha) * (reward + maxQ(env.available_actions, str(env.grid))))
                    currState = str(env.grid)


def greedyChooseAction(epsilon, availableActions, state):
    if (len(availableActions) == 1):
        return availableActions[0]

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
        chosenAction = (actionValues[random.randint(1, len(actionValues)-1)])[0]
    else:
        chosenAction = (actionValues[0])[0]
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

    if (len(actionValues) == 0):
        return 0
    else:
        # Pick the value of the best action
        bestActionValue = (actionValues[0])[1]

        return bestActionValue


def newEnv():
    env = connect.Connect(verbose=True)
    env.reset(first_player='x')
    return env


def agentMove(env):
    availableActions = env.available_actions
    selectedActionIndex = random.randint(0,len(availableActions)-1)
    selectedAction = availableActions[selectedActionIndex]
    return selectedAction


qLearn(0.2, 0.6, 1000)