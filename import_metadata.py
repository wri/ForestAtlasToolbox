import settings
import metadata
import codecs
import os


def read_meta_dic(f):
    meta_lines = []
    with codecs.open(f, 'r', encoding="utf8") as csvfile:
        #meta = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for row in csvfile:
            meta_lines.append(row.split("\t"))

    meta_attribute = meta_lines[1:len(meta_lines)-1]

    layers = meta_lines[0][3:len(meta_lines[0])-1]

    meta = {}
    i = 0

    for layer in layers:
        meta[layer] = {}
        for att in meta_attribute:
            meta[layer][att[0]] = {"value": att[i+3], "frequency": att[1], "subtype": att[2]}
        i += 1

    return meta


def get_position_in_list(i_list, item):
    return [i for i, x in enumerate(i_list) if x == item]


def update_md_layer(mfile, layer, mkeys, messages):
#m_file, m_dic[layer], m_keys

    #messages.addMessage("Layer %s" % layer)

    for attrib in layer:

        messages.addMessage("Attribute %s" % attrib)

        if layer[attrib]['frequency'] == "single":
            attributes = {}
            a_elmements = []

            if attrib in mkeys["ARCGIS"]['values'].keys():
                if layer[attrib]['subtype'] != "":
                    subtype = layer[attrib]['subtype']
                    for element in mkeys["ARCGIS"]['values'][attrib]:
                        #l = mkeys["ARCGIS"][attrib]
                        pos = get_position_in_list(mkeys["ARCGIS"][attrib], element)
                        e_tree = mkeys["ARCGIS"][attrib][0:pos[0]+1]
                        text = True

                        attributes[attrib] = {}

                        for s_attrib in mkeys["ARCGIS"]['values'][attrib][element][subtype]:

                            value = mkeys["ARCGIS"]['values'][attrib][element][subtype][s_attrib]
                            if s_attrib == "text":
                                text = False
                            else:
                                attributes[attrib][s_attrib] = value
                                a_elmements.append([mfile, e_tree, s_attrib, value])
                                #metadata.update_metadata_element_attribute(mfile, e_tree, s_attrib, value)

                        metadata.update_metadata_element_and_attribute(mfile,
                                                                               mkeys["ARCGIS"][attrib],
                                                                               layer[attrib]['value'].strip('"'),
                                                                               attributes)
                        #if text:
                        #        metadata.update_metadata_element_and_attribute(mfile,
                        #                                                       mkeys["ARCGIS"][attrib],
                        #                                                       layer[attrib]['value'].strip('"'),
                        #                                                       attributes)
                        #else:
                        #    for a_e in a_elmements:
                        #        metadata.update_metadata_element_attribute(a_e[0], a_e[1], a_e[2], a_e[3])
            else:

                metadata.update_metadata_element(mfile, mkeys["ARCGIS"][attrib], layer[attrib]['value'].strip('"'))
        else:
            values = layer[attrib]['value'].split(',')
            striped_values = []
            for value in values:
                striped_values.append(value.strip('"').strip())
            metadata.update_metadata_elements(mfile, mkeys["ARCGIS"][attrib], striped_values)


def import_metadata(gdb, m_dic, messages):
    #r"C:\Users\Thomas.Maschler\Desktop\WRI_metadata_gnq.txt"
    #r"C:\Users\Thomas.Maschler\Desktop\conc.xml"
    m_keys = settings.get_metadata_keys()
    m_dic = read_meta_dic(m_dic)

    for layer in m_dic:
        fc = os.path.join(gdb, layer)
        m_file = metadata.get_metadata_file(fc)
        update_md_layer(m_file, m_dic[layer], m_keys, messages)
        metadata.import_metadata(fc, m_file)
