import random

def random_page(max):
    """
    Returns a random page number given max pages.
    """
    return random.randint(1, max)

def weighted_random(d):
    """
    Returns a random channel, weighted towards the beginning.
    """
    # Sum of weights in the dictionary
    weight_sum = sum(d.values())

    r = random.randint(1, weight_sum)
    for k, v in d.items():
        r -= v
        if r <= 0:
            return k
