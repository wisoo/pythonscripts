import bimserver
import json
import requests
from pprint import pprint
from sqlalchemy_totoriol import SQLDB, DB, IFCObject, IFCObjectEncoder


def getAllProjects(cl): # get all projects from server
	projectsDict = cl.ServiceInterface.getAllProjects(onlyTopLevel=False, onlyActive=False)
	return(projectsDict)

def getProjectsByName(cl, name): # get a projects data by project name on the server
	project = cl.ServiceInterface.getProjectsByName(name = name)
	return(project)

def getProjectRoidByPoid(cl, poid):
	roid = cl.ServiceInterface.getProjectByPoid(poid = poid)["lastRevisionId"]
	return(roid)

def getProjectByPoid(cl, poid):
	project = cl.ServiceInterface.getProjectByPoid(poid = poid) 
	return(project)

def getAvailableClassesInProject(cl, roid): #EEERRRROOOORRRR
	classes = cl.ServiceInterface.getAvailableClasses()
	return(classes)

def getAllObjectsFromProjectsByType(cl, roid, className, packageName="ifc4", flat = False):
	objects = cl.LowLevelInterface.getDataObjectsByType(roid = roid, className = className, packageName = packageName, flat = flat)
	return(objects)

def getDataObjectByOID(cl, roid, oid):
	return cl.LowLevelInterface.getDataObjectByOid(roid=roid, oid=oid)

def getStringAttribute(name, oid, poid, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.getStringAttribute(tid=tid, oid=oid, attributeName=name)

	# commit or abort
	cl.LowLevelInterface.abortTransaction(tid=tid)
	return(res)

def setStringAttribute(name, oid, poid, newValue, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.setStringAttribute(tid=tid, oid=oid, attributeName=name, value=newValue)

	# commit or abort
	cl.LowLevelInterface.commitTransaction(tid=tid, comment="changed String Attribute " + name)
	return(res)

def getReference(name, oid, poid, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.getReference(tid=tid, oid=oid, referenceName=name)

	# commit or abort
	cl.LowLevelInterface.abortTransaction(tid=tid)
	return(res)

def getIntAttribute(name, oid, poid, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.getIntegerAttribute(tid=tid, oid=oid, attributeName=name)

	# commit or abort
	cl.LowLevelInterface.abortTransaction(tid=tid)
	return(res)

def setIntAttribute(name, oid, poid, newValue, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.setIntAttribute(tid=tid, oid=oid, attributeName=name, value=newValue)

	# commit or abort
	cl.LowLevelInterface.commitTransaction(tid=tid, comment="changed int Attribute " + name)
	return(res)

def getDoubleAttribute(name, oid, poid, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.getDoubleAttribute(tid=tid, oid=oid, attributeName=name)

	# commit or abort
	cl.LowLevelInterface.abortTransaction(tid=tid)
	return(res)

def setDoubleAttribute(name, oid, poid, newValue, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.setDoubleAttribute(tid=tid, oid=oid, attributeName=name, value=newValue)

	# commit or abort
	cl.LowLevelInterface.commitTransaction(tid=tid, comment="changed int Attribute " + name)
	return(res)

def getLongAttribute(name, oid, poid, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.getLongAttribute(tid=tid, oid=oid, attributeName=name)

	# commit or abort
	cl.LowLevelInterface.abortTransaction(tid=tid)
	return(res)

def setLongAttribute(name, oid, poid, newValue, cl):
	# create transaction
	tid = cl.LowLevelInterface.startTransaction(poid=poid)

	# request
	res = cl.LowLevelInterface.setLongAttribute(tid=tid, oid=oid, attributeName=name, value=newValue)

	# commit or abort
	cl.LowLevelInterface.commitTransaction(tid=tid, comment="changed Long Attribute " + name)
	return(res)

def changeAttrValue(name, oid, poid, newValue, cl):
	if isinstance(newValue, str):
		oldValue = getStringAttribute(name, oid, poid, cl)
		if oldValue == newValue :
			return
		else :
			setStringAttribute(name, oid, poid, newValue, cl)
	elif isinstance(newValue, long):
		oldValue = getLongAttribute(name, oid, poid, cl)
		if oldValue == newValue :
			return
		else :
			setLongAttribute(name, oid, poid, newValue, cl)
	elif isinstance(newValue, int):
		oldValue = getIntAttribute(name, oid, poid, cl)
		if oldValue == newValue :
			return
		else :
			setIntAttribute(name, oid, poid, newValue, cl)
	else :
		raise Exception("typeError: value to change is not str nor int nor long")

def getValueByFieldname(collection, fieldName):
	# check type of collection

	# if the collection is a dict, 
	# get dict["fieldName"]
	# and return (fetch the object)

	# if the collection is a list
	# it means that it's a list of dicts
	# either i iterate on the list and return the first occurrence of what we're looking for
	# or, i iterate and return a collection of all the values corresponding to the fieldname...

	# error handling
	pass

def getNestedProperties(cl, roid, hasPropertiesDict, nestedPropertyObjectName):
	properties = []
	propertyOids = []
	filteredProperties = []
	temp = {}
	for value in hasPropertiesDict["values"]:
		propertyOids.append(value["oid"])
	
	for oid in propertyOids:
		properties.append(getDataObjectByOID(cl, roid, oid))
	
	for propertyObj in properties:
		temp = {}
		tempName = None
		tempVal = None
		for prop in propertyObj["values"]:	
			if prop["__type"] == "SSimpleDataValue":
				if prop["fieldName"] == "Name":
					tempName = prop["stringValue"]
				elif prop["fieldName"] == "NominalValue":
					tempVal = prop["stringValue"]

		if tempName != None and tempVal != None and tempVal != "":
			temp['name'] = tempName + ' ' + nestedPropertyObjectName
			temp['value'] = tempVal
			filteredProperties.append(temp)
		else:
			if tempName != None or tempVal != None:
				print("getNestedProperties: tempName != None or tempVal != None", tempName, tempVal)
	return filteredProperties

def getNestedQuantities(cl, roid, hasQuantitiesDict, nestedQuantityObjectName):
	quantities = []
	quantityOids = []
	filteredQuantities = []
	temp = {}
	for value in hasQuantitiesDict["values"]:
		quantityOids.append(value["oid"])
	
	for oid in quantityOids:
		quantities.append(getDataObjectByOID(cl, roid, oid))
	
	for quantityObj in quantities:
		temp = {}
		tempName = None
		tempVal = None
		for quanti in quantityObj["values"]:	
			if quanti["__type"] == "SSimpleDataValue":
				if quanti["fieldName"] == "Name":
					tempName = quanti["stringValue"]
				elif quanti["fieldName"] == "NominalValue":
					tempVal = quanti["stringValue"]

		if tempName != None and tempVal != None and tempVal != "":
			print("ONE GOT AWAAAAAAAAAAAAY")
			temp['name'] = tempName + ' ' + nestedQuantityObjectName
			temp['value'] = tempVal
			filteredQuantities.append(temp)
		else:
			if tempName != None or tempVal != None:
				print("getNestedQuantities: tempName != None or tempVal != None", tempName, tempVal)
	return filteredQuantities

def getObjectsDict(cl, projectName, roid=0):
	i = 1
	project = getProjectsByName(cl, projectName)
	roid = project[0]["lastRevisionId"]
	poid = project[0]["oid"]
	print("ROID = ", roid)
	print("POID = ", poid)
	res = dict()
	print("START 		getAllObjectsFromProjectsByType")
	objectsDict = getAllObjectsFromProjectsByType(cl, roid, "IfcBuildingElementProxy")
	print("END 		getAllObjectsFromProjectsByType")
	print(objectsDict)
	return objectsDict

def getAllLayers(cl, roid):
	edid = 0
	extendedDataOids = []
	objectsToCheck = {}
	

	temp = {}
	for extendedData in cl.ServiceInterface.getAllExtendedDataOfRevision(roid=roid):
		extendedDataOids.append(extendedData["oid"])
	for extendedDataOid in extendedDataOids:
		extendedData = cl.ServiceInterface.getExtendedData(oid=extendedDataOid)
		if (extendedData["title"] == "Geometry generation report (application/json)"):
			edid = extendedData["oid"]
			break
	print("get: " + cl.url + "/download?token=" + cl.token + "&action=extendeddata&edid=" + str(edid))
	token = "88063b2518ca2e2020229ed4647e7410bd03debab7cf5df0027b0c47531c58c8002a3d24be7358c8b0f7adcb1c311a72"
	token = cl.token
	payload = {'token': token, 'action': 'extendeddata', 'edid': edid}
	test = requests.get(cl.url.replace("json", "download", 1), params=payload)
	print(test.url)
	print(test.status_code)
	response = test.json()
	for job in response["jobs"]:
		for obj in job["objects"]:
			temp[obj['oid']] = getDataObjectByOID(cl, roid, obj['oid'])
			objectsToCheck[obj['oid']] = {}
			for value in temp[obj['oid']]["values"]:
				if value["fieldName"] in ["Name", "GlobalId", "Tag"]:
					objectsToCheck[obj['oid']][value["fieldName"]] = value["stringValue"]

	# go rthrough all objs
	print("il y a ", len(temp), " objets")
	for k,v in temp.items():
		propertySetOidsDict = {}
		propertySetOidsDict["quantities"] = []
		propertySetOidsDict["properties"] = []
		
		for value in v["values"]:
			if value["fieldName"] == "IsDefinedBy":
				for value2 in value["values"]:
					for value3 in getDataObjectByOID(cl, roid, value2["oid"])["values"]:
						if value3["fieldName"] == "RelatingPropertyDefinition" and value3["typeName"] == "IfcElementQuantity":
							propertySetOidsDict["quantities"].append(value3["oid"])
						elif value3["fieldName"] == "RelatingPropertyDefinition" and value3["typeName"] == "IfcPropertySet":
							propertySetOidsDict["properties"].append(value3["oid"])

		objectsToCheck[k]["PropertySetOidsDict"] = propertySetOidsDict
		print("done")

	for k,v in objectsToCheck.items():
		v["propertyDict"] = {}
		v["propertyDict"]["unfilteredProperties"] = []
		v["propertyDict"]["unfilteredQuantities"] = []

		for propertySetOid in v["PropertySetOidsDict"]["properties"]:
			temp = getDataObjectByOID(cl, roid, propertySetOid)["values"]
			name = ""
			for prop in temp:
				if prop["fieldName"] == "Name":
					name = prop["stringValue"]
				if prop["fieldName"] == "HasProperties":
					propOids = [i["oid"] for i in prop["values"]]
			v["propertyDict"]["unfilteredProperties"].append({name : propOids})

		for propertySetOid in v["PropertySetOidsDict"]["quantities"]:
			temp = getDataObjectByOID(cl, roid, propertySetOid)["values"]
			name = ""
			for prop in temp:
				if prop["fieldName"] == "Name":
					name = prop["stringValue"]
				if prop["fieldName"] == "Quantities":
					propOids = [i["oid"] for i in prop["values"]]
			v["propertyDict"]["unfilteredQuantities"].append({name : propOids})


	for k,v in objectsToCheck.items():
		v["propertyDict"]["properties"] = []
		v["propertyDict"]["quantities"] = []
		del(v["PropertySetOidsDict"])
		for propertyGroup in v["propertyDict"]["unfilteredProperties"]:
			for groupName, oids in propertyGroup.items():
				propGroup = {'name': groupName, 'children': []}
				for oid in oids:
					children = []
					propList = getDataObjectByOID(cl, roid, oid)
					if propList["type"] == "IfcPropertySingleValue":
						#print(propList["type"])
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] == "NominalValue":
								tempVal = prop["stringValue"]
						children.append({'name': tempName, 'value': tempVal})

					elif propList["type"] == "IfcComplexProperty":
						#print(propList["type"])
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] == "HasProperties":
								tempVal = getNestedProperties(cl, roid, prop, tempName)
						children.append({'name': tempName, 'children': tempVal})
					elif propList["type"] == "IfcPropertyEnumeratedValue":
						#print(propList["type"])
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] == "EnumerationValues":
								tempVal = prop["values"][0]["stringValue"]
						children.append({'name': tempName, 'value': tempVal})
					else:
						#print("unexpected prop type in props: ")
						#pprint(propList)
						pass
					propGroup["children"].extend(children)
			v["propertyDict"]["properties"].append(propGroup)
		
		for propertyGroup in v["propertyDict"]["unfilteredQuantities"]:
			for groupName, oids in propertyGroup.items():
				propGroup = {'name': groupName, 'children': []}
				children = []
				for oid in oids:
					children = []
					propList = getDataObjectByOID(cl, roid, oid)
					if propList["type"] in ["IfcQuantityLength", "IfcQuantityArea", "IfcQuantityVolume"]:
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] in ["LengthValue", "AreaValue", "VolumeValue"]:
								tempVal = prop["stringValue"]
						children.append({'name': tempName, 'value': tempVal})
					elif propList["type"] == "IfcPhysicalComplexQuantity":
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] == "HasQuantities":
								tempVal = getNestedQuantities(cl, roid, prop, tempName)
								pprint(tempVal)
						if tempVal != []:
							children.append({'name': tempName, 'children': tempVal})
					elif propList["type"] == "IfcQuantityCount":
						for prop in propList["values"]:
							if prop["fieldName"] == "Name":
								tempName = prop["stringValue"]
							elif prop["fieldName"] == "CountValue":
								tempVal = prop["stringValue"]
						children.append({'name': tempName, 'value': tempVal})
					propGroup["children"].extend(children)
			if propGroup['children'] != []:
				v["propertyDict"]["quantities"].append(propGroup)
		del(v["propertyDict"]["unfilteredProperties"])	
		del(v["propertyDict"]["unfilteredQuantities"])
	return(objectsToCheck)

def pushObjectsToDB(allObjectsAndPropsDict):
	i = 0
	for k,v in allObjectsAndPropsDict.items():
		i = i+1
		print(i)
		oid = k
		ifcId = v["GlobalId"]
		name = v["Name"]
		calque = None
		for propertyGroup in v["propertyDict"]["properties"]:
			if propertyGroup['name'] == "DefinitionParSection":
				print("defparsec")
				for property in propertyGroup["children"]:
					if property['name'] == "SectionNature" :
						SectionNature = property['value']
					elif property['name'] == "sectionAnnexePiece" :
						sectionAnnexePiece = property['value']
					elif property['name'] == "sectionAppartement" :
						sectionAppartement = property['value']
					elif property['name'] == "sectionBatiment" :
						sectionBatiment = property['value']
					elif property['name'] == "sectionEtage" :
						sectionEtage = property['value']
					elif property['name'] == "sectionPiece" :
						sectionPiece = property['value']
			if propertyGroup['name'] == "ArchiCADProperties":
				for property in propertyGroup["children"]:
					if property['name'] == "Calque":

						if property['value'] != "":
							print("value not none: ", property['value'])
							calque = property['value']
						else:
							print('it is None')
							calque = None

		ifcObject = IFCObject(	oid=oid,
                        		ifcId=ifcId,
                        		name=name,
                        		SectionNature=SectionNature,
                        		sectionAnnexePiece=sectionAnnexePiece,
                        		sectionAppartement=sectionAppartement,
                        		sectionBatiment=sectionBatiment,
                        		sectionEtage=sectionEtage,
                        		sectionPiece=sectionPiece,
                        		calque = calque,
                        		properties=v["propertyDict"])
		if ifcObject.calque == None:
			print('ifcdict calque : ', ifcObject.__dict__['calque'])
		result = requests.post('http://localhost:3000/ifcObject/'+oid, json=ifcObject.__dict__)
	print('\n')


def main():
	server_address = "http://46.105.124.137:8080/bimserver"
	username = "wacim.yassine@syscobat.com"
	password = "admin"
	
	client = bimserver.api(server_address, username, password)
	projectName = "essai ifc4 zones"
	project = getProjectsByName(client, projectName)
	roid = project[0]["lastRevisionId"]
	poid = project[0]["oid"]
	print("ROID = ", roid)
	print("POID = ", poid)

	#########################################################################
	#	uncomment this if you want to create json from bimserver project
	#########################################################################
	#res = getAllLayers(client, roid)
	#with open('result.json', 'w', encoding='utf-8') as fp:
	#	json.dump(res, fp, indent=2, ensure_ascii=False, sort_keys=True)




	#########################################################################
	#	uncomment this if you want to upload to DB using the BIMAPI
	#########################################################################
	with open('result.json', 'r', encoding='utf-8') as fp:
		res = json.load(fp)
	pushObjectsToDB(res)


	# changeColorOfObject(client, 563807247, roid, poid)

	
	#
	#

if __name__ == '__main__':
	main()