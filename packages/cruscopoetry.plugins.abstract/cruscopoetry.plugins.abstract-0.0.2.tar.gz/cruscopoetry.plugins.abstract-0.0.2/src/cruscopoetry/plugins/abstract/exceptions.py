# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.


class CruscoPoetryPluginException(Exception):

	def __init__(self):
		super().__init__()


class PluginIdentifiersException(CruscoPoetryPluginException):

	def __init__(self, plugin_class_name: str):
		super().__init__()
		self.plugin_class_name = plugin_class_name
	
	def __str__(self):
		return "Unspecified name or version of the CruscoPoetry plugin %s"%self.plugin_class_name


class UnserialisableDataException(CruscoPoetryPluginException):

	def __init__(self, plugin_class_name: str, datadict):
		super().__init__()
		self.plugin_class_name = plugin_class_name
		self.datadict = datadict
	
	def __str__(self):
		return "CruscoPoetry plugin %s has tried to save data of the non-json-serializable type %s"%(self.plugin_class_name, str(type(self.datadict)))

