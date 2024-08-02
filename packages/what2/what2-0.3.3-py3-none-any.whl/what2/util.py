from  numbers import Real

def clamp[T: Real | float](lower: T, val: T, upper: T) -> T:
    return sorted((lower, val, upper))[1]
