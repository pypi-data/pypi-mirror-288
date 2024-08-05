# This file is part of Cruscopoetry.
# 
# Cruscopoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cruscopoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cruscopoetry. If not, see <http://www.gnu.org/licenses/>.


class SubscriptableSetException(Exception):

	def __init__(self):
		super().__init__()
		

class NotIndexableException(SubscriptableSetException):

	def __init__(self, obj):
		self.obj = obj
		
	def __str__(self):
		return "The item '%s' is not an integer or does not have an __index__ method."%str(obj)


class SubscriptableSet(set):
	"""This set can contains only integer values or objects which have an __index__ method. It is subscriptable: the subscription operator used with an integer value num will return that item 
	of the set whose value (if it's an integer) or whose value as returned by its __index__ method equals num."""

	def _is_indexable(self, item) -> bool:
		if type(item) == int:
			return True
		index_method = getattr(item, "__index__", None)
		return callable(index_method)
		
	def _check_is_indexable(self, item):
		if not self._is_indexable(item):
			raise NotIndexableException(item)
			
	def __getitem__(self, index: int) -> object:
		"""Returns the item of the set whose index is ``index``, else None"""

		if type(index) != int:
			try:
				index = int(index)
			except TypeError:
				raise
		
		for item in self:
			if int(item) == index:
				return item
		return None
		
	def is_index_unique(self, item) -> bool:
		"""Returns True if there is not element in the set that has the same index value of ``item``."""

		#since we have already checked that item is indexable, we can just use it in __getitem__ and check that the returned value is different from None:
		return self.__getitem__(item) == None
					
	def __new__(cls, *args, **kwargs):
		obj = set.__new__(cls, *args, **kwargs)
		for item in obj:
			self._check_is_indexable(item)
		return obj
	
	def add(self, new_item) -> bool:
		"""Adds a new item to the set. If the item is not indexable, it raises a NotIndexableException. If the item is indexable, but there is another item in the set with the same index value, 
		it does nothing and returns False. Otherwise, it successfully adds the item and returns True"""
		self._check_is_indexable(new_item)
		if not self.is_index_unique(new_item):
			return False
		super().add(new_item)
		return True
		
	def pop(self, index) -> object:
		"""Searchs an item in the set by its index. If no item is found, returns None and nothing happens; if it is found, it is removed from the set and returned by the function."""
		item = self.__getitem__(index)

		#the method discard ensures us that if item == None (and therefore doesn't exist in the set) no modification will be applied and no error will be raised:
		self.discard(item)						

		return item
		
	@property
	def indexes(self):
		"""Returns the indexes of all the items in the set, sorted by increasing value"""
		indexes = [int(item) for item in self]
		indexes = sorted(indexes)
		return tuple(indexes)
		
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
