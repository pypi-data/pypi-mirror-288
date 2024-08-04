class SinglyLinkedNode[T]:
    def __init__(self, value: T, _next: "SinglyLinkedNode[T] | None" = None) -> None:
        """
        Initialize a SinglyLinkedNode.
        :param value: Value of the node.
        :param _next: Next node.
        """
        self.value = value
        self.next = _next

    def __str__(self) -> str:
        """
        Return a string representation of the node.
        :return: String representation of the node.
        """
        return f"Value: {self.value}"
