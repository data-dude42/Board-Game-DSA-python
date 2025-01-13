# Copy over your a1_partc.py file here

#    Main Reviewer(s): Paras Singh, Prabhjot Singh



class Stack:

	def __init__(self, cap=10):
		self.cap = cap
		self.stack = [None] * cap
		self.size = 0


# This function returns capacity.
	def capacity(self):
		return self.cap

# This function doubles the size of the stack and copy the original list to a new list
	def resize(self):
		new_stack = [None] * self.cap * 2
		for i in range(self.cap):
			new_stack[i] = self.stack[i]
		self.stack = new_stack
		self.cap *= 2

	# This function adds data to the "top" of the Stack without returning anything
	def push(self, data):
		# the size exceeds the capacity, resize it first
		if self.size == self.cap:
			self.resize()
  		# push the coming data into the top of the stack
		self.stack[self.size] = data
		self.size += 1

# This function removes the newest value from the Stack and returns the removed data
# IndexError raises if the stack is empty
	def pop(self):
		if self.is_empty():
			raise IndexError('pop() used on empty stack')
		# removed = self.get_top() will cause error
		removed = self.stack[self.size - 1]
		self.stack[self.size - 1] = None
		self.size -= 1
		return removed

# This function returns the newest value (value at "top") from the Stack without removing it.
	def get_top(self):
		if self.is_empty():
			return None
		return self.stack[self.size - 1]

# This function returns True if Stack is empty, False otherwise.
	def is_empty(self):
		return self.size == 0

# This function returns the number of values in the Stack.
	def __len__(self):
		
		return self.size


class Queue:

	def __init__(self, cap=10):
		self.my_queue = [None] * cap
		self.cap = cap
		self.size = 0
		# front and back is useful in circular manner
		self.front = 0
		self.back = 0

# This function returns capacity.
	def capacity(self):
		return self.cap

# The function doubles the size of the queue and copy all values
	def resize(self):
		new_queue = [None] * self.cap * 2
		# Copy current values to new_queue using circular manner
		for i in range(self.size):
			new_queue[i] = self.my_queue[(self.front + i) % self.cap]
		self.my_queue = new_queue
		self.cap *= 2
		self.front = 0
		# Move the back index
		self.back = self.size

# The function does not return anything.
	def enqueue(self, data):
		# resize the queue if adding data will exceed the capacity
		if self.size == self.cap:
			self.resize()
		# Adding the coming data to the end of the queue
		self.my_queue[self.back] = data
		self.back = (self.back + 1) % self.cap
		# self.my_queue[(self.size + self.front) % self.cap] = data
		self.size += 1

# Function returns value removed.
	def dequeue(self):
		# If the function is called on an empty Queue, raise the IndexError with this statement
		if self.is_empty():
			raise IndexError('dequeue() used on empty queue')
			
# remove the oldest value and move the front to the next index
		removed = self.my_queue[self.front]
		self.my_queue[self.front] = None
		# Remove the front one forward
		self.front = (self.front + 1) % self.cap
		self.size -= 1
		return removed

# Function returns None if Queue is empty.
	def get_front(self):
		return self.my_queue[self.front]

# This function returns True if Queue is empty, False otherwise.
	def is_empty(self):
		return self.size == 0

# This function returns the number of values in the Queue.
	def __len__(self):
		"""
		# return len(self.my_queue)
		count = 0
		for e in self.my_queue:
			if e is None:
				break
			count += 1
		return count
		"""
		return self.size

class Deque:
	def __init__(self, cap=10):
		self.my_deque = [None] * cap
		self.cap = cap
		self.front = 0 
		self.back = 0
		self.size = 0

# This function returns capacity
	def capacity(self):
		return self.cap

# This function doubles the size of the deque and copy all values
	def resize(self):
		new_cap = self.cap * 2
		new_deque = [None] * new_cap
		for i in range(self.size):
			new_deque[i] = self.my_deque[(self.front + i) % self.cap]
		self.my_deque = new_deque
		self.front = 0
		self.back = self.size
		self.cap = new_cap

# This function adds data to the "front" of the Deque.
	def push_front(self, data):
		if self.size == self.cap:
			self.resize()
		self.front = (self.front - 1) % self.cap
		self.my_deque[self.front] = data
		self.size += 1

# Function does not return anything.
	def push_back(self, data):
		if self.size == self.cap:
			self.resize()
		# Adding the data to the back index
		self.my_deque[self.back] = data
		# Move the back index in one further
		self.back = (self.back + 1) % self.cap
		# Increasing the size
		self.size += 1

# Function returns value removed.
	def pop_front(self):
		# If the function is called on an empty Deque, raise the IndexError
		if self.is_empty():
			raise IndexError('pop_front() used on empty deque')
		# Get the front value
		removed = self.my_deque[self.front]
		# Setting to None excludes it
		self.my_deque[self.front] = None
		# Move the front to the next index
		self.front = (self.front + 1) % self.cap
		# Decrease the size
		self.size -= 1
		return removed

# This function removes the value from the "back" of the Deque.
	def pop_back(self):
		if self.is_empty():
			raise IndexError('pop_back() used on empty deque')

		# Get the back value and excludes it
		self.back = (self.back - 1) % self.cap
		removed = self.my_deque[self.back]
		self.my_deque[self.back] = None

		# Reducing the size
		self.size -= 1

		return removed

# This function returns the value from the "front" of the Deque without removing it.
	def get_front(self):
		# Return None if the deque is empty
		if self.is_empty():
			return None
		return self.my_deque[self.front]

# This function returns the value from the "back" of the Deque without removing it.
	def get_back(self):
		# Return None if the deque is empty
		if self.is_empty():
			return None
		return self.my_deque[(self.back - 1) % self.cap]

# This function returns True if Deque is empty, False otherwise.
	def is_empty(self):
		return self.size == 0

# This function returns the number of values in the Deque.
	def __len__(self):
		"""
		count = 0
		for e in self.my_deque:
			if e is None:
				break
			count += 1
		return count
		"""
		return self.size

# This function returns the k'th value from the "front" of the Deque without removing it.
	def __getitem__(self, k):
		if k < 0 or k > self.size - 1:
			raise IndexError('Index out of range')
		return self.my_deque[(self.front + k) % self.cap]
