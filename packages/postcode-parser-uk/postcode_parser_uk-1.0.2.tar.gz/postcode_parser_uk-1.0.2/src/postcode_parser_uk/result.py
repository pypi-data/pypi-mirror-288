from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """
    Represents the result of a process, which can either be successful or failed.

    Attributes:
        is_valid (bool): Indicates if the process was successful.
        value (Optional[T]): The value that was validated or parsed.
        error (Optional[Exception]): The error encountered during the process, if any.

    Methods:
        success(value: Optional[T] = None) -> Result[T]: Create a successful result.
        failure(error: Optional[Exception] = None) -> Result[T]: Create a failed result.
        raise_if_invalid() -> None: Raise the error if the result is not valid.
    """

    is_valid: bool
    value: Optional[T] = None
    error: Optional[Exception] = None

    @property
    def is_failure(self) -> bool:
        """
        Check if the result is a failure.

        Returns:
            bool: True if the result is a failure, False otherwise.
        """
        return not self.is_valid

    @staticmethod
    def success(value: Optional[T] = None) -> "Result[T]":
        """
        Create a successful result.

        Args:
            value (Optional[T]): The value associated with the successful result.

        Returns:
            Result[T]: A result indicating success.
        """
        return Result(is_valid=True, value=value)

    @staticmethod
    def failure(error: Optional[Exception] = None) -> "Result[T]":
        """
        Create a failed result.

        Args:
            error (Optional[Exception]): The error associated with the failed result.

        Returns:
            Result[T]: A result indicating failure.
        """
        return Result(is_valid=False, error=error)

    def raise_if_invalid(self) -> None:
        """
        Raise the error if the result is not valid.

        Raises:
            Exception: The error associated with the failed result if the result is not valid.
        """
        if not self.is_valid and self.error:
            raise self.error
