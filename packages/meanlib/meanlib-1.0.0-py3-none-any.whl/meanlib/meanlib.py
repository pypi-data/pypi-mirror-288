import numpy as np

def weighted_mean(values, weights):
    """
    Calculates the weighted mean of a list of values.

    This function converts the input lists of values and weights into NumPy arrays and then computes the weighted mean.
    The weighted mean is the sum of the values, each multiplied by their corresponding weight, divided by the total sum of the weights.

    Args:
        values: A list or array-like structure containing the values for which the weighted mean is to be calculated.
        weights: A list or array-like structure containing the weights associated with each value.

    Returns:
        The calculated weighted mean (float or complex).

    Raises:
        TypeError: If `values` or `weights` are not list or array-like.
        ValueError: If `values` and `weights` do not have the same length.
        ZeroDivisionError: If the total of `values` is zero.
    """
    values = np.asarray(values)
    weights = np.asarray(weights)
    return np.average(values, weights=weights)

class SimpleMean():
    def __init__(self):
        """
        Initializes a SimpleMean object.

        This function initializes the sum and count attributes to 0.
        """
        self._sum = 0
        self.count = 0 

    def update(self, number: int | float | complex):
        """
        Updates the mean with a new value.

        This function adds the new value to the sum and increments the count.
        It then returns the updated mean.

        Args:
            number (int | float | complex): The new value to be added to the mean.

        Returns:
            The updated mean (float or complex or None).

        Raises:
            TypeError: If the value is not of a compatible type.
        """
        self._sum += number
        self.count += 1
        return self.get_mean()

    def get_mean(self):
        """
        Returns the current mean.

        This function calculates the mean by dividing the sum by the count.
        If the count is 0, it returns None.

        Returns:
            The current mean (float or complex), or None if the count is 0.
        """
        return self._sum / self.count if self.count > 0 else None
    
class Mean():
    def __init__(self, max_size=None):
        """
        Initializes a Mean object.

        This function initializes the array attribute to an empty list.
        It also initializes the max_size attribute to the given value, or None if no value is given.

        Args:
            max_size (int | str, optional): The maximum number of values to store in the array. If None, there is no limit.

        Raises:
            ValueError: If the max_size is not an integer or a string of an integer.
        """
        self.array = []
        if max_size is not None:
            self.max_size = int(max_size)
        else:
            self.max_size = None
    
    def update(self, number: int | float | complex):
        """
        Updates the mean with a new value.

        This function appends the new value to the array.
        If the maximum number of values is reached, it removes the oldest values to maintain the limit.
        It then returns the updated mean.

        Args:
            number (int | float | complex): The new value to be added to the mean.

        Returns:
            The updated mean (float or complex or None).

        Raises:
            TypeError: If the input number is not an int, float, or complex.
        """
        self.array.append(number)
        if self.max_size and len(self.array) > self.max_size:
            self.array.pop(0)
        return self.get_mean()
    
    def update_list(self, _list: list | tuple):
        """
        Updates the mean with a list of values.

        This function appends the list of values to the array.
        If the maximum number of values is reached, it removes the oldest values to maintain the limit.
        It then returns the updated mean.

        Args:
            _list (list | tuple): The list of values to be added to the mean.

        Returns:
            The updated mean (float or complex or None).
        
        Raises:
            TypeError: If an element in the _list is not of the correct type.
            TypeError: If the _list is not a list or tuple.
        """
        if _list:
            self.array.extend(_list)
            if self.max_size and len(self.array) > self.max_size:
                self.array = self.array[-self.max_size:]
        return self.get_mean()

    def get_mean(self):
        """
        Returns the current mean.

        This function calculates the mean of the values in the array.
        If the array is empty, it returns None.

        Returns:
            The current mean (float or complex), or None if the array is empty.
        """
        return sum(self.array) / len(self.array) if len(self.array) > 0 else None
