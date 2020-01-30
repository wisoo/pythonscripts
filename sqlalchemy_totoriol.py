# sqlalchemy totoriol
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pprint import pprint
import json
import requests

Base = declarative_base()

class IFCObjectEncoder(json.JSONEncoder):
    def default(self, object):

        if isinstance(object, IFCObject):

            return object.__dict__

        else:

            # call base class implementation which takes care of

            # raising exceptions for unsupported types

            return json.JSONEncoder.default(self, object)


class IFCObject():
    oid = Column(Integer, primary_key=True)
    ifcId = Column(String)
    name = Column(String)
    SectionNature = Column(String)
    sectionAnnexePiece = Column(String)
    sectionAppartement = Column(String)
    sectionBatiment = Column(String)
    sectionEtage = Column(String)
    sectionPiece = Column(String)
    calque = Column(String)
    properties = Column(String(100000))

    
    def __init__(self):
        self.oid = 0;
        self.ifcId = "err";
        self.name = "err";
        self.SectionNature = "err";
        self.sectionAnnexePiece = "err";
        self.sectionAppartement = "err";
        self.sectionBatiment = "err";
        self.sectionEtage = "err";
        self.sectionPiece = "err";
        self.calque = 'err';
        self.properties = "{}";

    def __init__(self, oid=oid,
                ifcId=ifcId,
                name=name,
                SectionNature=SectionNature,
                sectionAnnexePiece=sectionAnnexePiece,
                sectionAppartement=sectionAppartement,
                sectionBatiment=sectionBatiment,
                sectionEtage=sectionEtage,
                sectionPiece=sectionPiece,
                calque=calque,
                properties=properties):
        self.oid = oid
        self.ifcId = ifcId
        self.name = name
        self.SectionNature = SectionNature
        self.sectionAnnexePiece = sectionAnnexePiece
        self.sectionAppartement = sectionAppartement
        self.sectionBatiment = sectionBatiment
        self.sectionEtage = sectionEtage
        self.sectionPiece = sectionPiece
        self.calque = calque
        self.properties = properties
        # print(self.oid)
        # print(self.ifcId)
        # print(self.name)
        # print(self.SectionNature)
        # print(self.sectionAnnexePiece)
        # print(self.sectionAppartement)
        # print(self.sectionBatiment)
        # print(self.sectionEtage)
        # print(self.sectionPiece)
        # print(self.properties)
    def __repr__(self):
        return "<IFCObject(oid=%d, ifcId=%s, name=%s )>" % (self.oid, self.ifcId, self.name)

class DB():
    def __init__(self, DBAddress, verboseBoolean=True):
        engine = create_engine(DBAddress, echo=verboseBoolean, encoding='U8')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def addOrUpdateToDB(self, ifcObject):
        self.session.merge(ifcObject)

class SQLDB():

    def addOrUpdateToDB(self, ifcObject):
        #payload = { "oid" : json.dumps(ifcObject.oid, ensure_ascii=False), 
        #            "ifcId" : json.dumps(ifcObject.ifcId, ensure_ascii=False),
        #            "name" : json.dumps(ifcObject.name, ensure_ascii=False),
        #            "SectionNature" : json.dumps(ifcObject.SectionNature, ensure_ascii=False),
        #            "sectionAnnexePiece" : json.dumps(ifcObject.sectionAnnexePiece, ensure_ascii=False),
        #            "sectionAppartement" : json.dumps(ifcObject.sectionAppartement, ensure_ascii=False),
        #            "sectionBatiment" : json.dumps(ifcObject.sectionBatiment, ensure_ascii=False),
        #            "sectionEtage" : json.dumps(ifcObject.sectionEtage, ensure_ascii=False),
        #            "sectionPiece" : json.dumps(ifcObject.sectionPiece, ensure_ascii=False)
        #            }
        payload = { "oid" : ifcObject.oid, 
            "ifcId" : ifcObject.ifcId,
            "name" : ifcObject.name,
            "SectionNature" : ifcObject.SectionNature,
            "sectionAnnexePiece" : ifcObject.sectionAnnexePiece,
            "sectionAppartement" : ifcObject.sectionAppartement,
            "sectionBatiment" : ifcObject.sectionBatiment,
            "sectionEtage" : ifcObject.sectionEtage,
            "sectionPiece" : ifcObject.sectionPiece,
            "properties" : ifcObject.properties
            }
        
        test = requests.post("http://46.105.124.137:3000/ifcObject", json=payload)
        print("####################################################################################################################################################################")
        print("####################################################################################################################################################################")
        print("####################################################################################################################################################################")

        print(test.text)
        print(test.request.body)