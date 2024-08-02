
import malac.hd
from malac.models.fhir import r4 as supermod

class PythonGenerator(supermod.StructureDefinition, malac.hd.ConvertMaster):
    def __init__(self, id=None, meta=None, implicitRules=None, language=None, text=None, contained=None, extension=None, modifierExtension=None, url=None, identifier=None, version=None, name=None, title=None, status=None, experimental=None, date=None, publisher=None, contact=None, description=None, useContext=None, jurisdiction=None, purpose=None, copyright=None, keyword=None, fhirVersion=None, mapping=None, kind=None, abstract=None, context=None, contextInvariant=None, type_=None, baseDefinition=None, derivation=None, snapshot=None, differential=None, **kwargs_):
        super(PythonGenerator, self).__init__(id, meta, implicitRules, language, text, contained, extension, modifierExtension, url, identifier, version, name, title, status, experimental, date, publisher, contact, description, useContext, jurisdiction, purpose, copyright, keyword, fhirVersion, mapping, kind, abstract, context, contextInvariant, type_, baseDefinition, derivation, snapshot, differential,  **kwargs_)

    def convert(self, input, o_module):
        pass

supermod.StructureDefinition.subclass = PythonGenerator
