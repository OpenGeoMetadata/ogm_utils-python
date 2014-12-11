__author__ = 'chrissbarnett'

import xml.etree.ElementTree as ET


def get_metadata_type(xml_string):
    doc = get_doc(xml_string)
    root_tag = doc.getroot().tag.lower()

    if is_iso_root(root_tag):
        metadata_type = "ISO19139"

    elif is_fgdc_root(root_tag):
        metadata_type = "FGDC"

    else:
        raise Exception("Unknown metadata type")

    return metadata_type, doc


def is_iso_root(root_tag):
    return "md_metadata" in root_tag or "mi_metadata" in root_tag


def is_fgdc_root(root_tag):
    if "metadata" in root_tag:
        return not is_iso_root(root_tag)


def get_doc(xml_string):
    try:
        parser = ET.XMLParser(encoding="utf-8")
        el = ET.XML(xml_string, parser=parser)
        tree = ET.ElementTree(element=el)

        return tree
    except UnicodeEncodeError, e:
        print e
        print xml_string
        raise e
    except ET.ParseError as e:
        print e.message
        print xml_string
        raise e



'''

eventually, we'll want to add in resource locations, source info

for item in objs:

    try:
        root = ET.fromstring(value)
        origin = root.findtext("idinfo/citation/citeinfo/origin")
        print origin
    except UnicodeEncodeError, e:
        print layerId
        print e
    except ET.ParseError, e1:
        print layerId
        print e1
'''