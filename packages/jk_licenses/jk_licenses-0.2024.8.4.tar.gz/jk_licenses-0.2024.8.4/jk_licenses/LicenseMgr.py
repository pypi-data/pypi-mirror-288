

import os
import typing

import jk_json

from .License import License
from .VariableDef import VariableDef





class LicenseMgr(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, licenseDirs:typing.Union[list,tuple] = None):
		if licenseDirs is None:
			licenseDirs = []
			licenseDirs.append(os.path.join(os.path.dirname(__file__), "licenses"))
		else:
			assert isinstance(licenseDirs, (tuple,list))
			for _dir in licenseDirs:
				assert isinstance(_dir, str)

		# ----

		self.__licenseDirs:typing.Tuple[str] = tuple(licenseDirs)
		self.__licenses:typing.Dict[str,License] = None
		self.__licensesByMainID:typing.Dict[str,License] = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dirPaths(self) -> typing.Tuple[str]:
		return self.__licenseDirs
	#

	@property
	def allLicenseIDs(self) -> typing.Sequence[str]:
		if self.__licenses is None:
			self.scan()
		return sorted(self.__licenses.keys())
	#

	@property
	def mainLicenseIDs(self) -> typing.Sequence[str]:
		if self.__licensesByMainID is None:
			self.scan()
		return sorted(self.__licensesByMainID.keys())
	#

	@property
	def licenses(self) -> typing.Generator[License,License,License]:
		if self.__licensesByMainID is None:
			self.scan()
		mainLicenseIDs = [ l.licenseID for l in self.__licenses.values() ]
		for licenseID in sorted(self.__licensesByMainID.keys()):
			yield self.__licensesByMainID[licenseID]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __loadLicense(self, fullPath:str):
		assert isinstance(fullPath, str)

		# ----

		licenseRawFilePath = fullPath[:-5] + ".txt"
		if not os.path.isfile(licenseRawFilePath):
			licenseRawFilePath = None

		jLicenseInfo = jk_json.loadFromFile(fullPath)

		if "identifiers" in jLicenseInfo:
			identifiers = jLicenseInfo["identifiers"]
		else:
			identifiers = []
		if "identifier" in jLicenseInfo:
			mainIdentifier = jLicenseInfo["identifier"]
			identifiers.insert(0, mainIdentifier)
		mainIdentifier = identifiers[0]

		name = jLicenseInfo["name"]

		url = jLicenseInfo.get("url")

		classifier = jLicenseInfo.get("classifier")

		variableDefs = {}
		if "variables" in jLicenseInfo:
			for jVarDefs in jLicenseInfo["variables"]:
				varName = jVarDefs["name"]
				varType = jVarDefs.get("type", "str")
				assert varType in [ "bool", "str", "int", "str|int", "int|str", ]
				varDescr = jVarDefs.get("description")
				variableDefs[varName] = VariableDef(varName, varType, varDescr)

		# ----

		lic = License(mainIdentifier, identifiers, name, url, classifier, licenseRawFilePath, variableDefs)

		self.__licensesByMainID[lic.licenseID] = lic
		self.__licenses[lic.licenseID] = lic
		for licenseID in lic.licenseIDs:
			self.__licenses[licenseID] = lic
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def scan(self):
		self.__licenses = {}
		self.__licensesByMainID = {}
		for dirPath in self.__licenseDirs:
			if os.path.isdir(dirPath):
				for entry in os.listdir(dirPath):
					if entry.endswith(".json") or entry.endswith(".jsonc"):
						fullPath = os.path.join(dirPath, entry)
						self.__loadLicense(fullPath)
	#

	def getLicense(self, identifier:str):
		if self.__licenses is None:
			self.scan()
		return self.__licenses[identifier]
	#

	def createLicenseMap(self) -> typing.Dict[str,list]:
		if self.__licenses is None:
			self.scan()
		ret = {}
		for license in self.__licensesByMainID.values():
			licenseIDSet = []
			for licenseID in license.licenseIDs:
				if licenseID == license.licenseID:
					continue
				licenseIDSet.append(licenseID)
			ret[license.licenseID] = licenseIDSet
		return ret
	#

	def createAlternativeLicenseIDMap(self) -> typing.Dict[str,str]:
		if self.__licenses is None:
			self.scan()
		ret = {}
		for license in self.__licensesByMainID.values():
			for licenseID in license.licenseIDs:
				if licenseID == license.licenseID:
					continue
				ret[licenseID] = license.licenseID
		return ret
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#









