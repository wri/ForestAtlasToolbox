# coding=utf-8

import os
import arcpy

subtypes = {"9100100": "Loi",
            "9100200": "Code",
            "9100300": "Arrêté",
            "9200100": "Décret",
            "9200200": "Ordonnance",
            "9200300": "Protocole",
            "9200400": "Programme",
            "9200500": "Circulaire",
            "9200600": "Contrat",
            "9200700": "Convention",
            "9200800": "Cahier des charges",
            "9300100": "Avis publis",
            "9300200": "Rapport",
            "9300300": "Notification",
            "9410100": "Plan d'aménagement",
            "9410200": "Plan de sondage",
            "9410300": "Inventaire",
            "9410301": "Inventaire d'aménagement",
            "9410302": "Inventaire d'exploitation",
            "9410303": "Inventaire de faune",
            "9420000": "Etude",
            "9420100": "Etude d'impact environnemental",
            "9430000": "Note",
            "9430100": "Note de conformité",
            "9440000": "Attestation",
            "9440100": "Attestation de superficie"}

def get_workspace(fc):
    workspace = fc
    desc = arcpy.Describe(workspace)
    while 1 == 1:
        if desc.dataType == "Workspace" or desc.dataType == "Folder":
            return workspace
        else:
            workspace = os.path.dirname(workspace)
            desc = arcpy.Describe(workspace)


def add_attachements(fcs, messages):
    for fc in fcs:
        messages.addMessage("Add attachements to {0}".format(fc))
        arcpy.EnableAttachments_management(fc)
        fc_name = os.path.basename(fc)
        workspace = get_workspace(fc)
        table = os.path.join(workspace, "{0}__ATTACH".format(fc_name))
        add_metadata_fields(table, messages)

        messages.addMessage("Enable editor tracking")
        arcpy.EnableEditorTracking_management(table, "created_user", "created_date", "last_edited_user", "last_edited_date", "ADD_FIELDS")

def add_metadata_fields(table, messages):
    messages.addMessage("Add fields")
    arcpy.AddField_management(table, "type_", "LONG", field_alias="Type de document")
    arcpy.AddField_management(table, "desc_type", "TEXT", field_length=50, field_alias="Description")
    arcpy.AddField_management(table, "doc_titre", "TEXT", field_length=255, field_alias="Titre du document")
    arcpy.AddField_management(table, "doc_ref", "TEXT", field_length=255, field_alias="Référence du document")
    arcpy.AddField_management(table, "date_doc", "DATE", field_alias="Date du document")
    arcpy.AddField_management(table, "auteur", "TEXT", field_length=255, field_alias="Auteur")

    # Set subtype field
    messages.addMessage("Set subtype field")
    arcpy.SetSubtypeField_management(table, "type_")

    # add subtypes and default value for description for each subtype
    messages.addMessage("Set subtype default values")
    for subtype in subtypes:
        arcpy.AddSubtype_management(table, subtype, subtypes[subtype])
        arcpy.AssignDefaultToField_management(table, "desc_type", subtypes[subtype], subtype)

    # Set Default Subtype...
    messages.addMessage("Set default subtype")
    arcpy.SetDefaultSubtype_management(table, "9200100")


def add_missing_metadata_fields(gdb, messages):

    arcpy.env.workspace = gdb

    tableList = arcpy.ListTables()
    for table in tableList:
        if table[-6:] == 'ATTACH':
            fieldlist = arcpy.ListFields(table)
            if not "type_" in fieldlist:
                #add new fields
                messages.addMessage("Add fields")
                try:
                    arcpy.AddField_management(table, "type_", "LONG", field_alias="Type de document")
                except: pass
                try:
                    arcpy.AddField_management(table, "desc_type", "TEXT", field_length=50, field_alias="Description")
                except: pass
                try:
                    arcpy.AddField_management(table, "doc_titre", "TEXT", field_length=255, field_alias="Titre du document")
                except: pass
                try:
                    arcpy.AddField_management(table, "doc_ref", "TEXT", field_length=255, field_alias="Référence du document")
                except: pass
                try:
                    arcpy.AddField_management(table, "date_doc", "DATE", field_alias="Date du document")
                except: pass
                try:
                    arcpy.AddField_management(table, "auteur", "TEXT", field_length=255, field_alias="Auteur")
                except: pass

                # Set subtype field
                messages.addMessage("Set subtype field")
                arcpy.SetSubtypeField_management(table, "type_")

                # add subtypes and default value for description for each subtype
                messages.addMessage("Set subtype default values")
                for subtype in subtypes:
                    try:
                        arcpy.AddSubtype_management(table, subtype, subtypes[subtype])
                    except: pass
                    arcpy.AssignDefaultToField_management(table, "desc_type", subtypes[subtype], subtype)

                # Set Default Subtype...
                messages.addMessage("Set default subtype")
                arcpy.SetDefaultSubtype_management(table, "9200100")

                messages.addMessage("Enable editor tracking")
                try:
                    arcpy.EnableEditorTracking_management(table, "created_user", "created_date", "last_edited_user", "last_edited_date", "ADD_FIELDS")
                except: pass