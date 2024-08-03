import typing
import contextlib

# Import abstract types
from collections.abc import Sequence

# Import the abstract object
from rednest.nested import Nested, NESTED_TYPES


class Array(typing.MutableSequence[typing.Any], Nested):

    # Type globals
    DEFAULT = []

    def _make_subpath(self, index: int) -> str:
        # Create and return a subpath
        return f"{self._subpath}[{index}]"

    def __getitem__(self, index: typing.Union[int, slice]) -> typing.Union[typing.Any, typing.List[typing.Any]]:
        # If a slice is provided, return a list of items
        if isinstance(index, slice):
            # Create a list with all of the requested items
            return [self[item_index] for item_index in range(*index.indices(len(self)))]
        elif isinstance(index, int):
            # Return using subvalue
            return self._fetch_value(self._make_subpath(index), IndexError(index))

        # Input type error
        raise TypeError("Array index must be an int or a slice")

    def __setitem__(self, index: typing.Union[int, slice], value: typing.Union[typing.Any, typing.Sequence[typing.Any]]) -> None:
        # If a slice is provided, splice the list
        if isinstance(index, slice):
            # Fetch slice parameters
            start, stop, step = index.indices(len(self))

            # If the step is more then 1, the value length must match the indice count
            if step > 1 and len(value) != len(range(start, stop, step)):
                raise ValueError(f"Attempted to assign sequence of incompatible size {len(value)}")

            # Create an iterator for the value
            iterator = iter(value)

            # Insert all of the items from the value
            for subindex, subvalue in zip(range(start, stop, step), iterator):
                self[subindex] = subvalue

            # If the step is exactly 1, then we want to insert new values
            if step == 1:
                # Loop over remaining items and insert them
                for counter, subvalue in enumerate(iterator):
                    self.insert(stop + counter, subvalue)
        elif isinstance(index, int):
            # Set using subvalue
            self._update_value(self._make_subpath(index), value)

    def __delitem__(self, index: typing.Union[int, slice]) -> None:
        # If a slice is provided, splice the list
        if isinstance(index, slice):
            # Delete all required items
            for counter, subindex in enumerate(range(*index.indices(len(self)))):
                del self[subindex - counter]
        elif isinstance(index, int):
            # Delete the item from the database
            self._delete_value(self._make_subpath(index), IndexError(index))

    def __len__(self) -> int:
        # Fetch the object length
        object_length: typing.List[int] = self._json.arrlen(self._absolute_name, self._subpath)

        # If object length is an empty list, raise a KeyError
        if not object_length:
            raise KeyError(self._subpath)

        # Untuple the result
        object_length_value, = object_length

        # Return the object length
        return object_length_value

    def __repr__(self) -> str:
        # Format the data like a dictionary
        return "[%s]" % ", ".join(repr(item) for item in self)

    def __eq__(self, other: typing.Any) -> bool:
        # Make sure the other item is a sequence
        if not isinstance(other, Sequence):
            return False

        # Make sure lengths are the same
        if len(self) != len(other):
            return False

        # Loop and check all items
        for index in range(len(self)):
            # Compare items
            if self[index] != other[index]:
                return False

        # Items match
        return True

    def insert(self, index: int, value: typing.Any) -> None:
        # Insert new array item
        self._json.arrinsert(self._absolute_name, self._subpath, index, value)

    def copy(self) -> typing.List[typing.Any]:
        # Create initial bunch
        output = list()

        # Loop over keys
        for value in self:
            # Try copying the value
            with contextlib.suppress(AttributeError):
                value = value.copy()

            # Update the bunch
            output.append(value)

        # Return the created output
        return output


# Registry object type
NESTED_TYPES["array"] = (Array, list)
