import random

def roll_dice(num_dice, dice_size):
    """
    Simulates rolling a number of dice of a certain size.
    
    Args:
    num_dice (int): The number of dice to roll.
    dice_size (int): The number of sides on each die.
    
    Returns:
    list: A list of individual results from rolling the dice.
    """
    results = []
    for _ in range(num_dice):
        result = random.randint(1, dice_size)
        results.append(result)
        
    return results if len(results) > 1 else None