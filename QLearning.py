### Write all your code for Part 1 within or above this cell.

# Your opponent is always the first player. Your agent is always the second player.

import connect
import random
import operator
import numpy as np
import matplotlib.pyplot as plt


def qLearn(epsilon, alpha, episodes, QTable):
    # Repeat for each episode
    for i in range(episodes):
        epsilon = epsilon * (1 / (len(QTable) + 1))
        env = newEnv()
        env.act(action=opponentMove(env))
        currState = str(env.grid)

        while True:
            env.change_turn()
            availableActions = env.available_actions
            selectedAction = greedyChooseAction(epsilon, availableActions, currState, QTable)
            env.act(action=selectedAction)

            if (env.was_winning_move()):
                reward = 1
                QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                        (alpha) * (reward + maxQ(env.available_actions, str(env.grid), QTable)))
                break
            elif env.grid_is_full():
                reward = 0
                QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                        (alpha) * (reward + maxQ(env.available_actions, str(env.grid), QTable)))
                break
            else:
                env.change_turn()
                env.act(action=opponentMove(env))
                if env.was_winning_move():
                    reward = -1
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                            (alpha) * (reward + maxQ(env.available_actions, str(env.grid), QTable)))
                    break
                elif env.grid_is_full():
                    reward = 0
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                            (alpha) * (reward + maxQ(env.available_actions, str(env.grid), QTable)))
                    break
                else:
                    reward = 0
                    QTable[currState, selectedAction] = ((1 - alpha) * QTable[currState, selectedAction]) + (
                            (alpha) * (reward + maxQ(env.available_actions, str(env.grid), QTable)))
                    currState = str(env.grid)

    return QTable


def greedyChooseAction(epsilon, availableActions, state, QTable):
    if len(availableActions) == 1:
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
        chosenAction = (actionValues[random.randint(1, len(actionValues) - 1)])[0]
    else:
        chosenAction = (actionValues[0])[0]
    return chosenAction


def maxQ(availableActions, state, QTable):
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
    env = connect.Connect(verbose=False)
    env.reset(first_player='x')
    return env


def opponentMove(env):
    availableActions = env.available_actions
    selectedActionIndex = random.randint(0, len(availableActions) - 1)
    selectedAction = availableActions[selectedActionIndex]
    return selectedAction


def playGames(QTable, m):
    env = connect.Connect(verbose=False)
    gamesWon = 0

    for i in range(m):
        env.reset(first_player='x')

        while True:
            env.act(action=opponentMove(env))
            if env.was_winning_move() or env.grid_is_full():
                break

            env.change_turn()

            env.act(action=agentMove(env, QTable))
            if env.was_winning_move():
                gamesWon += 1
                break
            elif env.grid_is_full():
                break
            else:
                env.change_turn()

    return gamesWon / m


def agentMove(env, QTable):
    availableActions = env.available_actions
    state = str(env.grid)

    if len(availableActions) == 1:
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
    chosenAction = (actionValues[0])[0]

    return chosenAction


def plotPerformanceOneAgent(k, n, m):
    scores = []
    optimalQ = dict()

    for i in range(k):
        # Interact with environment n times
        optimalQ = qLearn(0.2, 0.6, n, optimalQ)

        # Play m games & add percentage won to scores list
        scores.append(playGames(optimalQ, m))

    return scores


def plotPerformance(k, n, m, a):
    scores = ()

    for i in range(a):
        scores = scores + (plotPerformanceOneAgent(k, n, m),)

    allScores = np.column_stack(scores)

    averages = []

    for i in range(len(allScores)):
        averages.append(np.mean(allScores[i]))

    # plot graph
    plt.xlabel("Environment Interactions")
    plt.ylabel("Percentage of games won")
    x = np.arange(0, (n * k), n)
    plt.plot(x, averages)

% matplotlib
inline
plotPerformance(20, 1000, 10, 30)
