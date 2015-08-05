import arcpy
import xml
import xml.etree.ElementTree as ET
import os
import settings
import cgi


def get_datatype(fc):
    # get datatype
    desc = arcpy.Describe(fc)
    return desc.dataType


def copy_metadata(fc, output):
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    xslt = os.path.join(installDir, r"Metadata\Stylesheets\gpTools\exact copy of.xslt")
    arcpy.XSLTransform_conversion(fc, xslt, output)
    


def export_metadata(fc, output_file, translator="ISO"):
    #Directory containing ArcGIS Install files
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    #Path to XML schema for FGDC
    if translator == 'FGDC':
        translator = os.path.join(installDir, "Metadata/Translator/ARCGIS2FGDC.xml")
    elif translator == 'ISO':
        translator = os.path.join(installDir, "Metadata/Translator/ARCGIS2ISO19139.xml")
    #Export your metadata
    arcpy.ExportMetadata_conversion(fc, translator, output_file)


def import_metadata(fc, metadata, format="ARCGIS"):
    if format == "ARCGIS":
        import_type = "FROM_ARCGIS"
    elif format == "ESRI":
        import_type = "FROM_ESRIISO"
    elif format == "FGDC":
        import_type = "FROM_FGDC"
    elif format == "ISO":
        import_type = "FROM_ISO_19139"
    arcpy.ImportMetadata_conversion(metadata, import_type, fc)


def get_metadata_file(fc):
    data_type = get_datatype(fc)
    if data_type == "FeatureClass" or data_type == "Table":
        sets = settings.get_settings()
        if os.path.exists(sets['paths']['scratch_workspace']):
            temp_folder = sets['paths']['scratch_workspace']
        else:
            temp_folder = arcpy.env.scratchFolder
        out_file = os.path.join(temp_folder, os.path.basename(fc) + ".xml")
        copy_metadata(fc, out_file)
        return out_file

    elif data_type == "ShapeFile":
        return fc + ".xml"

def get_metadata_elements_by_key(metadata, e):
    tree = ET.parse(metadata)
    root = tree.getroot()

    elements = []

    for element in root.iter(e):
		try:
			elements.append(element.text.encode('ascii', 'replace'))
		except AttributeError:
			pass
    return elements


def get_metadata_element_by_etree(metadata, e_tree):
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[0] = root
    for e in e_tree:
        i += 1
        d[i] = d[i-1].find(e)
        if i == len(e_tree):
			try:
				text = d[i].text.encode('ascii', 'replace')
			except AttributeError:
				text = ""
			return text

def get_metadata_elements_by_etree(metadata, e_tree):
    elements = []
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[i] = [root]
    for e in e_tree:
        i += 1
        d[i] = []
        for p in d[i-1]:
            d[i] = d[i] + p.findall(e)
        for j in range(len(d[i])):
            if i == len(e_tree):
				try:
					elements.append(d[i][j].text.encode('ascii', 'replace'))
				except AttributeError:
					pass
    return elements


def remove_metadata_elements_by_etree(metadata, e_tree):
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[i] = [root]
    for e in e_tree:
        i += 1
        d[i] = []
        for p in d[i-1]:
            d[i] = d[i] + p.findall(e)
        if i == len(e_tree):
            for j in range(len(d[i])):
                p.remove(d[i][j])
    tree.write(metadata)
    return metadata


def update_metadata_element(metadata, e_tree, e_text):
    done = False

    while not done:
        d = {}
        tree = ET.parse(metadata)
        root = tree.getroot()
        i = 0
        d[0] = root

        for e in e_tree:
            i += 1
            d[i] = d[i-1].find(e)
            if i == len(e_tree):
                try:
                    d[i].text = e_text #cgi.escape(e_text)
                except AttributeError:
                    child = ET.Element(e)
                    child.text = e_text
                    d[i-1].append(child)
                done = True
            elif d[i] is None:
                child = ET.Element(e)
                d[i-1].append(child)
                break
        tree.write(metadata)
    return metadata


def update_metadata_element_attribute(metadata, e_tree, e_attri, e_attri_value):
    done = False

    while not done:
        d = {}
        tree = ET.parse(metadata)
        root = tree.getroot()
        i = 0
        d[0] = root
        for e in e_tree:
            i += 1
            if d[i-1].find(e) is None and i != len(e_tree):
                child = ET.Element(e)
                d[i-1].append(child)
                break
            else:
                d[i] = d[i-1].find(e)
                if i == len(e_tree):
                    try:
                        d[i].attributes[e_attri].value = e_attri_value
                    except AttributeError:
                        child = ET.Element(e)
                        child.set(e_attri, e_attri_value)
                        d[i-1].append(child)

        tree.write(metadata)
    return metadata


def update_metadata_element_and_attribute(metadata, e_tree, e_text, attributs):
    done = False

    while not done:
        d = {}
        tree = ET.parse(metadata)
        root = tree.getroot()
        i = 0
        d[0] = root

        for e in e_tree:
            i += 1
            d[i] = d[i-1].find(e)
            if i == len(e_tree):
                try:
                    d[i].text = e_text #cgi.escape(e_text)
                except AttributeError:
                    child = ET.Element(e)
                    child.text = e_text
                    if e in attributs.keys():
                        for attrib in attributs[e]:
                            child.set(attrib, attributs[e][attrib])
                    d[i-1].append(child)

                done = True
            elif d[i] is None:
                child = ET.Element(e)
                if e in attributs.keys():
                    for attrib in attributs[e]:
                        child.set(attrib, attributs[e][attrib])
                d[i-1].append(child)
                break
            else:
                if e in attributs.keys():
                    for attrib in attributs[e]:
                        d[i].set(attrib, attributs[e][attrib])
        tree.write(metadata)
    return metadata


def update_metadata_elements(metadata, e_tree, e_text_list):
    done = False


    while not done:
        rm = False
        d = {}
        tree = ET.parse(metadata)
        root = tree.getroot()
        i = 0
        d[i] = [root]
        for e in e_tree:
            i += 1
            d[i] = []
            for p in d[i-1]:
                d[i] = d[i] + p.findall(e)
                if i == len(e_tree):
                    for j in range(len(d[i])):
                        try:
                            p.remove(d[i][j])
                            rm = True
                        except ValueError:
                            pass

        tree.write(metadata)
        if not rm:
            d = {}
            tree = ET.parse(metadata)
            root = tree.getroot()
            i = 0
            d[i] = [root]
            for e in e_tree:
                i += 1
                d[i] = []
                for p in d[i-1]:
                    d[i] = d[i] + p.findall(e)
                if i == len(e_tree):
                    for e_text in e_text_list:
                        child = ET.Element(e)
                        child.text = e_text
                        p.append(child)
                        done = True
            tree.write(metadata)
    return metadata

