#    Main Author(s): paras singh
#    Main Reviewer(s): Khwahish Vaid, Prabhjot singh



	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice as long as it is a hash table

class HashTable:
    
	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice as long as it is a hash table
 
	def __init__(self, cap = 32):
		self.cap = cap
		self.the_table = [None] * self.cap
		self.length = 0
		self.max_load_factor = 0.70

	def insert(self,key, value):
		
		self.length += 1
		hashed_key = hash(key) % self.cap
		
		while self.the_table[hashed_key] is not None:
			if self.the_table[hashed_key][0] == key:
				self.length -= 1
				return False

			hashed_key = self._hash(hashed_key)

		if self.length / float(self.cap) >= self.max_load_factor:
			self._grow()
		tuple = (key, value)
		self.the_table[hashed_key] = tuple
		return True

	def modify(self, key, value):

		index = hash(key) % self.cap
		record = index
		while self.the_table[index] is not None and index != record - 1:
			if(self.the_table[index][0]==key and self.the_table[index][0] != None):
				self.the_table[index] = (key,value)
				return True

			index = self._hash(index)
		return False

	def remove(self, key):
		
		count = 0

		for item in self.the_table:
			if(item is not None):
				if(item[0] == key):
					self.the_table[count] = None
					self.length -= 1
					return True
			count += 1
		return False

	def search(self, key):
		
		for item in self.the_table:
			if (item is not None):
				if (item[0] == key):
					return item[1]
		return None

	def capacity(self):
		
		return self.cap

	def __len__(self):
		
		if(self.length > self.cap):
			self.length -= 1
		return self.length

	def _grow(self):
		
		self.cap *= 2
		self.length = 1
		old_table = self.the_table
		self.the_table = [None] * self.cap
  
		for tuple in old_table:
			if tuple is not None:
				self.insert(tuple[0],tuple[1])

	def _hash(self, key):
		
		return (key + 1) % self.cap 