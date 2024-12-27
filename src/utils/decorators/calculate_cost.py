from functools import wraps
from typing import Callable
def calculate_costs(func:Callable): 
    @wraps(func)  
    def wrapper(*args, **kwargs):
          request = kwargs.get('request')
          distance = request.distance if request and hasattr(request, 'distance') else 1
          weight = request.weight if request and hasattr(request, 'weight') else 1
          cost = distance * weight * 0.5
          result = func(*args, **kwargs)
          return f"{result} | Estimated cost: ${cost:.2f}"
    return wrapper 