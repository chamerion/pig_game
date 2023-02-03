import numpy as np

PRNG = np.random.default_rng()

def binomial(prng=PRNG):
    return prng.binomial(n=20, p=.1) + 1

def poisson(prng=PRNG):
    return prng.poisson(lam=3) + 1

default_rv = binomial

def play_random(score=None, player_on_the_move=0, rv=default_rv, prng=PRNG):
    '''Random simulation of the game.
    
    Parameters
    ----------
    score: seq of 2 integers, default = [0, 0]
        The current score of both players.
    
    player_on_the_move: int
        Index of player on the move (0 or 1).
    
    rv: parameterless function
        Returns the number of PC rolls.
        
    prng: numpy.random.Generator
        Random generator
    '''

    if score is None:
        score = [0, 0]
    else:
        # Copy so as not to modify an existing score.
        score = list(score)

    random_rolls = prng.integers(low=1, high=7, size=10000)

    i = 0

    while True:
        if score[0] >= 100:
            return 0
        elif score[1] >= 100:
            return 1
        
        number_of_rolls = 2 * rv() # The player has 2 dice
        rolls = random_rolls[i:i + number_of_rolls]
        i += number_of_rolls

        # If no 1 has been drawn.
        if (rolls != 1).all():
            score[player_on_the_move] += rolls.sum()
        
        player_on_the_move = 1 - player_on_the_move
        

def assesment(number_of_rolls, 
              score,
              player_on_the_move, 
              n=1000,
              rv=default_rv,
              prng=PRNG):
    '''Assesment of the move with MC method.
    
    Parameters
    ----------
    number_of_rolls: int
        Planned number of rolls.
        
    score: seq of 2 integers, default = [0, 0]
        The current score of both players.
    
    player_on_the_move: int
        Index of player on the move (0 or 1).
        
    n: int, default=1000
        Number of simulations.
    
    rv: parameterless function
        Returns the number of PC rolls.
        
    prng: numpy.random.Generator
        Random generator
    '''
    
    ct = 0

    for _ in range(n):
        score_ = list(score)
        rolls = prng.integers(low=1, high=7, size=2 * number_of_rolls)
        
        if (rolls != 1).all():
            score_[player_on_the_move] += rolls.sum()
        
        ct += play_random(score=score_,
                          rv=rv,
                          player_on_the_move=1 - player_on_the_move,
                          prng=prng)

    return 1 - ct/n if player_on_the_move == 0 else ct/n


def human_on_the_move(score, player):
    rolls = []
    turn_total = sum(rolls)
    while True:
        print(f'\nYou have {turn_total}/{score[player]}. PC has {score[1 - player]}.')
        print('Choose:\n\t1. Roll\n\t2. Break')
        decision = input()
        if decision.strip()[0] == '2':
            score[player] += turn_total
            return False
        else:
            rolls.extend(np.random.randint(low=1, high=7, size=2))
            print(' '.join(map(str, rolls)))
            if 1 not in rolls:
                turn_total = sum(rolls)
                if turn_total + score[player] >= 100:
                    return True
            else:
                return False


def pc_on_the_move(score, player):
    number_of_rolls = 1
    move_assesment = assesment(number_of_rolls,
                               player_on_the_move=player,
                               score=score,
                               n=5000)

    while True:
        print(f'Checking number of rolls: {number_of_rolls + 1}.')
        one_more_roll_assesment = assesment(number_of_rolls + 1,
                                             player_on_the_move=player,
                                             score=score,
                                             n=5000)

        if one_more_roll_assesment < move_assesment:
            break
        
        move_assesment = one_more_roll_assesment
        number_of_rolls += 1

    print(f'Chosen number of rolls {number_of_rolls}.')

    rolls = np.random.randint(low=1, high=7, size=2 * number_of_rolls)
    
    if 1 not in rolls:
        score[player] += rolls.sum()
        if score[player] >= 100:
            return True
    else:
        return False


PLAYERS = {0: 'HUMAN', 1: 'PC'}
SCORE = [0, 0]
player = 0

while True:
    if PLAYERS[player] == 'HUMAN':
        won = human_on_the_move(SCORE, player)
        if won:
            print('Human')
            break
    else:
        won = pc_on_the_move(SCORE, player)
        if won:
            print('PC')
            break
    player = 1 - player
