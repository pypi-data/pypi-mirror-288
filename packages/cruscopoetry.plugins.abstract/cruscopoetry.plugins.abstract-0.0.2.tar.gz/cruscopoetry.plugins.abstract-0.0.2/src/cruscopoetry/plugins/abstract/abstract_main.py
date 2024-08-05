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
import abc
from .exceptions import PluginIdentifiersException
from cruscopoetry.core.jsonparser import JsonParser
import typing
JsonSerialisable = type(None) | bool | int | str | float | list | dict


class AbstractPlugin(metaclass=abc.ABCMeta):

	PLUGIN_NAME = None
	PLUGIN_VERSION = None
	
	def __call__(self, *args, **kwargs):
		if (self.__class__.PLUGIN_NAME == None or self.__class__.PLUGIN_VERSION == None):
			raise PluginIdentifiersException(self.__class__.__name__)
		super().__call__(self, *args, **kwargs)

	@abc.abstractclassmethod
	def _build_args_parser(cls):
		pass
		
	@classmethod
	def get_plugin_data(cls):
		return "%s-%s"%(cls.PLUGIN_NAME, cls.PLUGIN_VERSION)
	
	@abc.abstractclassmethod
	def main(cls):
		"""The method to call when the plugin is called from shell"""
	
	@classmethod
	def save_data(cls, jparser: JsonParser, datadict: JsonSerialisable):
		if not isinstance(datadict, JsonSerialisable):
			raise UnserialisableDataException(cls.__name__, datadict)
		
		print(datadict)
		
		jparser.plugins[cls.get_plugin_data()] = datadict
		jparser.save()
	
	@classmethod
	def get_data(cls, jparser: JsonParser):
		plugin_key = cls.get_plugin_data()
		if plugin_key not in jparser.plugins:
			jparser.plugins[plugin_key] = {}
		return jparser.plugins[plugin_key]
	
	@classmethod
	def reset(cls, jparser: JsonParser):
		if cls.get_plugin_data() in jparser.plugins:
			del jparser.plugins[cls.get_plugin_data()]
		jparser.save()
