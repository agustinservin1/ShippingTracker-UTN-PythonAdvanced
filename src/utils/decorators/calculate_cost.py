def calculate_costs(func): 
    def wrapper(*args, **kwargs):
         distance = kwargs.get('distance', 1)
         weight = kwargs.get('weight', 1) 
         cost = distance * weight * 0.5
         result = func(*args, **kwargs)
         return f"{result} | Estimated cost: ${cost:.2f}"
    return wrapper 