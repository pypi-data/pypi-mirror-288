from simplepyds.LinkedList.Node import SinglyLinkedNode
from typing import Any, Callable


class SinglyLinkedList[T]:
    def __init__(self) -> None:
        """
        Initialize a Singly Linked List that only accepts one element type
        Places the cursor before the beginning of the list head
        """
        self.head: SinglyLinkedNode[T] | None = None
        self.length = 0
        self.curr: SinglyLinkedNode[T] | None = None
        self._type: type | None = None

    def __str__(self) -> str:
        """
        Prints the singly linked list
        Does not change the position of the cursor
        :return: A string representation of the list
        """
        old_current = self.curr
        self.curr = self.head
        result = "["
        while self.curr is not None:
            result += f" {self.curr.value},"
            self.next()
        result += " None ]"
        self.curr = old_current
        return result

    def __iter__(self) -> "SinglyLinkedList[T]":
        """
        Creates an iterator for the List
        Sets the cursor position to before the front of the List
        :return: None
        """
        self.curr = None
        return self

    def __next__(self) -> T:
        """
        Get the next element of the List
        :return: Next element
        :raises StopIteration: if the List is empty or the end of the list is reached
        """
        self.next()
        if self.curr is not None:
            return self.curr.value
        else:
            raise StopIteration("List out of bounds: No more values to return")

    def _check_type(self, value: Any) -> None:
        """
        Checks if a given value is the correct type
        :param value: A value to be checked
        :return: None
        :raises TypeError: If the value is not of the correct type
        """
        if self._type is None:
            self._type = type(value)
        else:
            if not isinstance(value, self._type):
                raise TypeError(f"Value {value} is not of type {self._type}")

    def insert_front(self, value: T) -> None:
        """
        Insert value at the front of the list.
        Makes no changes to the cursor position.
        :param value: value to insert
        :raises TypeError: If the value is not of the correct type
        :return: None
        """
        self._check_type(value)
        old_head = self.head
        self.head = SinglyLinkedNode(value, old_head)
        self.length += 1

    def insert_back(self, value: T) -> None:
        """
        Insert value at the back of the list
        :param value: value to insert
        :raises TypeError: If the value is not of the correct type
        :return: None
        """
        self._check_type(value)
        if self.is_empty():
            self.head = SinglyLinkedNode(value)
            self.length += 1
            self.curr = None
            return

        old_current = self.curr
        self.curr = self.head
        if self.curr is not None:
            while self.curr.next is not None:
                self.next()

        if self.curr is not None:
            self.curr.next = SinglyLinkedNode(value)

        self.curr = old_current
        self.length += 1

    def delete_front(self) -> None:
        """
        Delete the first element of the List
        Sets the cursor position to the front of the List
        :return: None
        """
        if not self.is_empty():
            if self.head is not None:
                new_head = self.head.next
                self.head = new_head
                self.length -= 1
                self.curr = self.head

    def delete_back(self) -> None:
        """
        Delete the last element of the list
        Sets the cursor position to the front of the List
        :return: None
        """
        if not self.is_empty():
            self.curr = self.head

            if self.length == 1:
                self.head = None
                self.curr = self.head
                self.length = 0
                return

            if self.curr is not None:
                for i in range(self.length - 2):
                    self.next()

                if self.curr is not None:
                    self.curr.next = None
                    self.length -= 1
                    self.curr = self.head

    def is_empty(self) -> bool:
        """
        Check if the List is empty
        :return: True if the list is empty otherwise False
        """
        if self.head is None:
            return True
        else:
            return False

    def next(self) -> None:
        """
        Move the cursor to the next element of the List
        :return:
        """
        if self.curr is not None:
            self.curr = self.curr.next
        else:
            self.curr = self.head

    def len(self) -> int:
        """
        Gets the length of the List
        :return: length of the List
        """
        return self.length

    def foreach(self, cb: Callable[[T], Any]) -> None:
        """
        Apply a function to each element of the List
        Does not change the cursor position
        :param cb: The function to be applied
        :return: None
        """
        old_current = self.curr
        self.curr = self.head
        while self.curr is not None:
            cb(self.curr.value)
            self.next()
        self.curr = old_current

    def search(self, query: T) -> None:
        """
        Search the list for a particular element.
        Leaves the cursor at the first instance of the query's position in the list.
        If the query value is not found in the list the cursor is not moved
        :param query: The element to be searched
        :return: None
        """
        old_current = self.curr
        self.curr = self.head
        while self.curr is not None:
            if self.curr.value == query:
                return
            else:
                self.next()
        self.curr = old_current

    def get(self, index: int) -> T | None:
        """
        Get the value at the specified index
        Does not change the cursor position.
        :param index: the index whose value will be returned
        :raises IndexError: if the index is out of the bounds of the list.
        :return: The value at the specified index
        """
        if type(index) is not int:
            raise TypeError("<index> must be an integer")

        if self.is_empty():
            return None

        if index > self.len() - 1:
            raise IndexError("Index out of bounds")

        old_current = self.curr
        self.curr = self.head

        for i in range(index):
            self.next()

        if self.curr is not None:
            to_return = self.curr.value
            self.curr = old_current
            return to_return

    def set(self, index: int, new_value: T) -> None:
        """
        Set the value at the specified index.
        Does not change the cursor position.
        :param index: The index whose value will be set
        :param new_value: The new value to be set
        :raises IndexError: If the <index> is out of the bounds of the list.
        :raises TypeError: If the <new_value> is not of the correct type
        :return: None
        """
        if self.is_empty():
            raise RuntimeError("List is empty")

        if not isinstance(index, int):
            raise TypeError("<index> must be an integer")

        if self._type is not None:
            if not isinstance(new_value, self._type):
                raise TypeError(f"<new_value> must be of type {str(self._type)}")

        if index > self.len() - 1:
            raise IndexError("Index out of bounds")

        old_current = self.curr
        self.curr = self.head

        for i in range(index):
            self.next()

        if self.curr is not None:
            self.curr.value = new_value

        self.curr = old_current

    def current(self) -> T | None:
        """
        Get the current element of the list
        :return: The current element
        """
        if self.curr is not None:
            return self.curr.value
        else:
            return None
