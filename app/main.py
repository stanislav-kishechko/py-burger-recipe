from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """Base validator class using descriptor protocol."""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store the attribute name with underscore prefix."""
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        """Return the attribute value."""
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        """Set the attribute value after validation."""
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Abstract method for value validation."""
        pass


class Number(Validator):
    """Validator for numeric values within a range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        """
        Initialize Number validator.

        Args:
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        """
        Validate that value is an integer within the allowed range.

        Args:
            value: Value to validate

        Raises:
            TypeError: If value is not an integer
            ValueError: If value is outside the allowed range
        """
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    """Validator for values that must be one of specific options."""

    def __init__(self, *options: str) -> None:
        """
        Initialize OneOf validator.

        Args:
            *options: Allowed values
        """
        self.options = options

    def validate(self, value: Any) -> None:
        """
        Validate that value is one of the allowed options.

        Args:
            value: Value to validate

        Raises:
            ValueError: If value is not in the allowed options
        """
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    """Class representing a burger recipe with validated ingredients."""

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str
    ) -> None:
        """
        Initialize a burger recipe with validated ingredients.

        Args:
            buns: Number of buns (2-3)
            cheese: Number of cheese slices (0-2)
            tomatoes: Number of tomatoes (0-3)
            cutlets: Number of cutlets (1-3)
            eggs: Number of eggs (0-2)
            sauce: Type of sauce ('ketchup', 'mayo', or 'burger')
        """
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

    def __repr__(self) -> str:
        """Return string representation of the burger recipe."""
        return (
            f"BurgerRecipe(buns={self.buns}, cheese={self.cheese}, "
            f"tomatoes={self.tomatoes}, cutlets={self.cutlets}, "
            f"eggs={self.eggs}, sauce='{self.sauce}')"
        )
