
import sys
import json

import malac.hd
from malac.models.fhir import r4 as supermod

class PythonGenerator(supermod.ConceptMap, malac.hd.ConvertMaster):
    from collections import defaultdict
    con_map_6d = None

    def __init__(self, id=None, meta=None, implicitRules=None, language=None, text=None, contained=None, extension=None, modifierExtension=None, url=None, identifier=None, version=None, name=None, title=None, status=None, experimental=None, date=None, publisher=None, contact=None, description=None, useContext=None, jurisdiction=None, purpose=None, copyright=None, sourceUri=None, sourceCanonical=None, targetUri=None, targetCanonical=None, group=None, **kwargs_):
        super(PythonGenerator, self).__init__(id, meta, implicitRules, language, text, contained, extension, modifierExtension, url, identifier, version, name, title, status, experimental, date, publisher, contact, description, useContext, jurisdiction, purpose, copyright, sourceUri, sourceCanonical, targetUri, targetCanonical, group,  **kwargs_)

    # the source param is not beeing handled, because there are no known possbilities of importing/including conceptMaps in other conceptMaps
    def convert(self, silent=True, return_header_and_footer_for_standalone=True, source=".", return_translate_def=True, return_dict_add=True):  # TODO:sbe replace source and return_XXX with context/params, to make more generic
        self.py_code = ""
        if return_header_and_footer_for_standalone:
            self._header_standalone()
        if return_translate_def:
            self._header_translate_def()
        if return_dict_add:
            self.con_map_6d = self.nested_dict(5, list)
            for one_group in self.get_group():
                for one_element in one_group.get_element():
                    for one_target in one_element.get_target():
                        self.con_map_6d \
                            [tmp.get_value() if (tmp := self.get_sourceUri()) or (tmp := self.get_sourceCanonical()) else "%"] \
                            [tmp.get_value() if (tmp := self.get_targetUri()) or (tmp := self.get_targetCanonical()) else "%"] \
                            [tmp.get_value() if (tmp := one_group.get_source()) else "%"] \
                            [tmp.get_value() if (tmp := one_group.get_target()) else "%"] \
                            [tmp.get_value() if (tmp := one_element.get_code()) else "%"] \
                            .append({"equivalence":one_target.get_equivalence().get_value(), 
                                    "concept":{
                                        "system": tmp.get_value() if (tmp := one_group.get_source()) else "", 
                                        "version": "", # TODO version of codesystem out of url?
                                        "code": tmp.get_value() if (tmp := one_target.get_code()) else "",
                                        "display": tmp.get_value() if (tmp := one_target.get_display()) else "",
                                        "userSelected": False},
                                    "source": tmp.get_value() if (tmp := self.get_url()) or (tmp := self.get_id()) else "%"})
                
                if unmapped := one_group.get_unmapped(): # using as many unsafe url characters here, that really should not be used as system id/url or codes of a real codesystem, like [ ] { } | \ ” % ~ # < >
                    tmp_equivalence = "inexact"
                    tmp_code = ""
                    tmp_display = ""
                    tmp_code_lvl = ""
                    if unmapped.get_mode().get_value() == "provided":
                        tmp_code_lvl = "|"
                        tmp_equivalence = "equal"
                        tmp_code = "|" + (tmp.get_value() if (tmp := unmapped.get_code()) else "") 
                    elif unmapped.get_mode().get_value() == "fixed":
                        tmp_code_lvl = "~"
                        tmp_code = "~"+unmapped.get_code().get_value() # must be given if fixed
                        tmp_display = unmapped.get_display().get_value() or ""
                    elif unmapped.get_mode().get_value() == "other-map":
                        #tmp_match = "lambda: translate(url="+unmapped.get_url()+", conceptMapVersion=conceptMapVersion, code=code, system=system, version=version, source=source, coding=coding, codeableConcept=codeableConcept, target=target, targetsystem=targetsystem, reverse=reverse, silent=silent)" # cant access the varibales inside the dict...
                        tmp_code_lvl = "#"
                        tmp_code = "#"+unmapped.get_url().get_value()
                    else:
                        sys.exit(unmapped.get_mode()+" as mode for unmapped is not defined! Please use the modes from https://hl7.org/fhir/R4B/valueset-conceptmap-unmapped-mode.html .")
                    self.con_map_6d \
                        [tmp.get_value() if (tmp := self.get_sourceUri()) or (tmp := self.get_sourceCanonical()) else "%"] \
                        [tmp.get_value() if (tmp := self.get_targetUri()) or (tmp := self.get_targetCanonical()) else "%"] \
                        [tmp.get_value() if (tmp := one_group.get_source()) else "%"] \
                        [tmp.get_value() if (tmp := one_group.get_target()) else "%"] \
                        [tmp_code_lvl] \
                        .append({"equivalence":tmp_equivalence, 
                                "concept":{
                                    "system": "", 
                                    "version": "", # TODO version of codesystem out of url?
                                    "code": tmp_code,
                                    "display": tmp_display,
                                    "userSelected": False},
                                "source": tmp.get_value() if (tmp := self.get_url()) or (tmp := self.get_id()) else "%"})

            self.py_code += "\n"
            j_dump = json.dumps(self.con_map_6d, indent=4)
            # replace all the json lower case bools to python usual pascal case bools
            j_dump = j_dump.replace(": false",": False").replace(": true",": True")
            self.py_code += 'con_map_7d["'+(tmp.get_value() if (tmp := self.get_url()) or (tmp := self.get_id()) else "%")+'"] = ' + j_dump
            
        if return_header_and_footer_for_standalone:
            self._footer_standalone()

        if not silent:
            print("\n%s" % self.py_code)
        
        return self.py_code
        
    # from https://stackoverflow.com/a/39819609/6012216
    def nested_dict(self, n, type): 
        if n == 1:
            return self.defaultdict(type)
        else:
            return self.defaultdict(lambda: self.nested_dict(n-1, type))  

    def _header_standalone(self):
        self.py_code += '''import argparse
import time
import malac.models.fhir.r4 as fhir4
import sys

description_text = "This has been compiled by the MApping LAnguage Compiler for Health Data, short MaLaC-HD. See arguments for more details."

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument(
       '-c', '--code', help="""code --	
The code that is to be translated. If a code is provided, a system must be provided""",
        required=True
    )
    parser.add_argument(
       '-sys', '--system', help="""uri --	
The system for the code that is to be translated""",
        required=True
    )
    parser.add_argument(
       '-ver', '--version', help="""string --	
The version of the system, if one was provided in the source data""",
        required=True
    )
    parser.add_argument(
       '-s', '--source', help="""uri --	
Identifies the value set used when the concept (system/code pair) was chosen. 
May be a logical id, or an absolute or relative location. 
The source value set is an optional parameter because in some cases, the client cannot know what the source value set is. 
However, without a source value set, the server may be unable to safely identify an applicable concept map, 
and would return an error. For this reason, a source value set SHOULD always be provided. 
Note that servers may be able to identify an appropriate concept map without a source value set 
if there is a full mapping for the entire code system in the concept map, or by manual intervention""",
        required=True
    )
    parser.add_argument(
       '-cg', '--coding', help="""Coding --	
A coding to translate""",
        required=True
    )
    parser.add_argument(
       '-cc', '--codeableConcept', help="""CodeableConcept --	
A full codeableConcept to validate. The server can translate any of the coding values (e.g. existing translations) 
as it chooses""",
        required=True
    )
    parser.add_argument(
       '-t', '--target', help="""uri -- 
Identifies the value set in which a translation is sought. May be a logical id, or an absolute or relative location. 
If there's no target specified, the server should return all known translations, along with their source""", 
        required=True
    )
    parser.add_argument(
       '-ts', '--targetsystem', help="""uri -- 
Identifies a target code system in which a mapping is sought. This parameter is an alternative to the target parameter - 
only one is required. Searching for any translation to a target code system irrespective of the context (e.g. target valueset) 
may lead to unsafe results, and it is at the discretion of the server to decide when to support this operation""", 
        required=True
    )
    parser.add_argument(
       '-r', '--reverse', action="store_true", help="""boolean -- True if stated, else False -- 
If this is true, then the operation should return all the codes that might be mapped to this code. 
This parameter reverses the meaning of the source and target parameters""", 
        required=True
    )
    parser.add_argument(
       '-st', '--silent', action="store_true", help="""boolean -- True if stated, else False --
Do not print the converted python mapping to console""", 
        required=True
    )
    return parser
'''

    def _header_translate_def(self): 
        self.py_code += '''
# output
# 1..1 result (boolean)
# 0..1 message with error details for human (string)
# 0..* match with (list)
#   0..1 equivalnce (string from https://hl7.org/fhir/R4B/valueset-concept-map-equivalence.html)
#   0..1 concept
#       0..1 system
#       0..1 version
#       0..1 code
#       0..1 display 
#       0..1 userSelected will always be false, because this is a translation
#   0..1 source (conceptMap url)
# TODO implement reverse
def translate(url=None, conceptMapVersion=None, code=None, system=None, version=None, source=None, coding=None, codeableConcept=None, target=None, targetsystem=None, reverse=None, silent=False)\
              -> dict [bool, str, list[dict[str, dict[str, str, str, str, bool], str]]]:
    start = time.time()
    
    # start validation and recall of translate in simple from
    if codeableConcept:
        if isinstance(codeableConcept, str): 
            codeableConcept = fhir4.parseString(codeableConcept, silent)
        elif isinstance(coding, fhir4.CodeableConcept):
            pass
        else:
            sys.exit("The codeableConcept parameter has to be a string or a CodeableConcept Object (called method as library)!")
        # the first fit will be returned, else the last unfitted value will be returned
        # TODO check translate params
        for one_coding in codeableConcept.get_coding:
            if (ret := translate(url=url, source=source, coding=one_coding, 
                                 target=target, targetsystem=targetsystem, 
                                 reverse=reverse, silent=True))[0]:
                return ret
        else: return ret
        
    elif coding:
        if isinstance(coding, str): 
            coding = fhir4.parseString(coding, silent)
        elif isinstance(coding, fhir4.Coding):
            pass
        else:
            sys.exit("The coding parameter has to be a string or a Coding Object (called method as library)!")
        # TODO check translate params
        return translate(url=url,  source=source, coding=one_coding, 
                         target=target, targetsystem=targetsystem, 
                         reverse=reverse, silent=True)
        
    elif code:
        if not isinstance(code,str): 
            sys.exit("The code parameter has to be a string!")
        
    elif target:
        if not isinstance(code,str): 
            sys.exit("The target parameter has to be a string!")
        
    elif targetsystem:
        if not isinstance(code,str): 
            sys.exit("The targetsystem parameter has to be a string!")
        
    else:
        sys.exit("At least codeableConcept, coding, code, target or targetSystem has to be given!")
    # end validation and recall of translate in simplier from

    # look for any information from the one ore more generated conceptMaps into con_map_7d
    match = []
    unmapped = []
    if url not in con_map_7d.keys():
        print('   #ERROR# ConceptMap with URL "'+ url +'" is not loaded to this compiled conceptMap #ERROR#')
    else:
        for url_lvl in con_map_7d:
            if url_lvl == "%" or url_lvl == str(url or ""):#+str(("/?version=" and conceptMapVersion) or ""):
                for source_lvl in con_map_7d[url_lvl]:
                    if source_lvl == "%" or not source or source_lvl == source:
                        for target_lvl in con_map_7d[url_lvl][source_lvl]:
                            if target_lvl == "%" or not target or target_lvl == target:
                                for system_lvl in con_map_7d[url_lvl][source_lvl][target_lvl]:
                                    if system_lvl == "%" or not system or system_lvl == system:#+str(("/?version=" and version) or ""):
                                        for targetsystem_lvl in con_map_7d[url_lvl][source_lvl][target_lvl][system_lvl]:
                                            if targetsystem_lvl == "%" or not targetsystem or targetsystem_lvl == targetsystem:
                                                for code_lvl in con_map_7d[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl]:
                                                    if code_lvl == "|" or code_lvl == "~" or code_lvl == "#":
                                                        unmapped += con_map_7d[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl][code_lvl]
                                                    if code_lvl == "%" or not code or code_lvl == code:
                                                        match += con_map_7d[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl][code_lvl]                
                                                    
    if not match:
        for one_unmapped in unmapped:
            tmp_system = ""
            tmp_version = ""
            tmp_code = ""
            tmp_display = ""
            # replace all "|" values with to translated code (provided from https://hl7.org/fhir/R4B/conceptmap-definitions.html#ConceptMap.group.unmapped.mode)
            if one_unmapped["concept"]["code"].startswith("|"):
                tmp_system = system
                tmp_version = version
                tmp_code = one_unmapped["concept"]["code"][1:] + code
            # replace all "~" values with fixed code (provided from https://hl7.org/fhir/R4B/conceptmap-definitions.html#ConceptMap.group.unmapped.mode)
            elif one_unmapped["concept"]["code"].startswith("~"):
                tmp_code = one_unmapped["concept"]["code"][1:]
                tmp_display = one_unmapped["concept"]["display"]
            elif one_unmapped["concept"]["code"].startswith("#"):
                # TODO detect recursion like conceptMapA -> conceptMapB -> ConceptMapA -> ...
                return translate(one_unmapped["concept"]["code"][1:], None, code, system, version, source, 
                                 coding, codeableConcept, target, targetsystem, reverse, silent)
            match.append({"equivalence": one_unmapped["equivalence"], 
                          "concept":{
                            "system": tmp_system, 
                            "version": tmp_version, # TODO version of codesystem out of url?
                            "code": tmp_code,
                            "display": tmp_display,
                            "userSelected": False},
                          "source": one_unmapped["source"]})
                
            
    # see if any match is not "unmatched" or "disjoint"
    result = False
    message = ""
    for one_match in match:
        if one_match["equivalence"] != "unmatched" and one_match["equivalence"] != "disjoint":
            result = True 

    if not silent:
        print('Translation in '+str(round(time.time()-start,3))+' seconds for code "'+code+'" with ConceptMap "'+url+'"')
    return {"result": result, "message": message, "match": match}

# The con_map_7d is a seven dimensional dictionary, for quickly finding the fitting translation
# All dimensions except the last are optional, so a explicit NONE value will be used as key and 
# interpreted as the default key, that always will be fitting, no matter what other keys are fitting.
# If a version is included (purely optional), than the version will be added with a blank before to the key
#
# The 0th dimension is mandatory and stating the ConceptMap with its url (including the version).
#
# The 1st dimension is optional and stating the SOURCE valueset (including the version), as one conceptMap can only 
# have a maximum of one SOURCE, this is reserved for MaLaC-HD ability to process multiple ConceptMaps in one output.
#
# The 2nd dimension is optional and stating the TARGET valueset (including the version), as one conceptMap can only 
# have a maximum of one TARGET, this is reserved for MaLaC-HD ability to process multiple ConceptMaps in one output.
#
# The 3th dimension is optional and stating the SYSTEM (including the version) from the source valueset code, as one 
# code could be used in multiple SYSTEMs from the source valueset to translate. 
# Not stating a SYSTEM with a code, is not FHIR compliant and not a whole concept, but still a valid conceptmap.
# As many conceptMaps exists that are worngly using this SYSTEM element as stating the valueset, that should be
# stated in source, this case will still be supported by MaLaC-HD. Having a conceptMap with a source valueset 
# and a different SYSTEM valueset will result in an impossible match and an error will not be recognized by MaLaC-HD.
#
# The 4th dimension is optional and stating the TARGET SYSTEM (including the version) from the target valueset code, as one 
# code could be used in multiple SYSTEMs from the target valueset to translate. 
# Not stating a TARGET SYSTEM with a code, is not FHIR compliant and not a whole concept, but still a valid conceptmap.
# As many conceptMaps exists that are worngly using this TARGET SYSTEM element as stating the target valueset, that should be
# stated in target, this case will still be supported by MaLaC-HD. Having a conceptMap with a target valueset 
# and a different TARGET SYSTEM valueset will result in an impossible match and an error will not be recognized by MaLaC-HD.
#   
# The 5th dimension is optional and stating the CODE from the source valueset, as one conceptMap can have none or 
# multiple CODEs from the source to translate. 
#
# The 6th dimension is NOT optional and stating the TARGET CODE from the target valueset. As one source code could be translated 
# in multiple TARGET CODEs, the whole set have to be returend. 
# For a translation with explicitly no TARGET CODE, because of an quivalence of unmatched or disjoint, NONE will be returned. 
#   
# a minimal example, translating "hi" to "servus": 
# con_map_7d = {"myConMap": {None: {None: {"hi": {None: {None: ["equivalent", "<coding><code>servus</code></coding>", "https://my.concept.map/conceptMap/my"]}}}}}
#
# TODO add a dimension for a specific dependsOn property
# TODO add a solution for the unmapped element
con_map_7d = {}
'''

    def _footer_standalone(self): 
        self.py_code += '''
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    ret = translate(args.code, args.system, args.version, args.source, args.coding, 
    args.codeableConcept, args.target, args.targetsystem, args.reverse, args.silent)'''

supermod.ConceptMap.subclass = PythonGenerator
