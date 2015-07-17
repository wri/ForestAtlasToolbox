import arcpy
import os


def get_table_list(domain_gdb):
    arcpy.env.workspace = domain_gdb
    return arcpy.ListTables()


def get_table_alias(table):
    desc = arcpy.Describe(table)
    return desc.aliasName


def load_domains(in_gdb, domain_gdb, lang, messages):
    desc = "desc_%s" % lang
    domains = get_table_list(domain_gdb)

    for domain in domains:
        messages.addMessage("Update domain %s" % domain)
        table_name = os.path.join(domain_gdb, domain)
        alias = get_table_alias(table_name)
        arcpy.TableToDomain_management(table_name, "code", desc, in_gdb, domain, alias, "REPLACE")


def update_dataset_alias(in_gdb, alias_table, lang, messages):
    cursor = arcpy.SearchCursor(alias_table)
    dataset_field = "feature_class"
    alias_field = "alias_%s" % lang

    for row in cursor:
        dataset = row.getValue(dataset_field)
        messages.addMessage("Update dataset %s" % dataset)
        ds_path = os.path.join(in_gdb, dataset)
        if arcpy.Exists(ds_path):
            alias = row.getValue(alias_field)

            if alias != '' and alias is not None:
                arcpy.AlterAliasName(ds_path, alias)
        else:
            messages.addMessage("Dataset %s does not exist" % dataset)


def update_field_alias(in_gdb, alias_table, lang, messages):
    cursor = arcpy.SearchCursor(alias_table)
    dataset_field = "feature_class"
    field_field = "field"
    alias_field = "alias_%s" % lang

    for row in cursor:
        dataset = row.getValue(dataset_field)
        ds_path = os.path.join(in_gdb, dataset)

        field = row.getValue(field_field)
        alias = row.getValue(alias_field)

        if alias != '' and alias is not None:
            messages.addMessage("Update %s, %s" % (dataset, field))
            messages.addMessage(alias)
            if arcpy.Exists(ds_path):
                field_list = arcpy.ListFields(ds_path)
                for f in field_list:
                    if f.name == field and f.name.lower() not in \
                            ["shape", "globalid", "shape_area", "shape_length", "shape.starea()", "shape.stlength()"]:

                        arcpy.AlterField_management(ds_path, field, new_field_alias=alias)
                        #f.aliasName = alias
            else:
                messages.addMessage("Dataset %s does not exist" % dataset)

def update_subtype(in_gdb, subtype_table, lang, messages):
    cursor = arcpy.SearchCursor(subtype_table)
    dataset_field = "feature_class"
    subtype_field = "subtype"
    desc_field = "desc_%s" % lang
    #default_field = "default"

    for row in cursor:
        dataset = row.getValue(dataset_field)
        ds_path = os.path.join(in_gdb, dataset)
        subtype = row.getValue(subtype_field)
        desc = row.getValue(desc_field)
        #default = row.getValue(default_field)
        messages.addMessage("Update suptype %s" % subtype)
        if arcpy.Exists(ds_path):
            if desc != '' and desc is not None:
                arcpy.RemoveSubtype_management(ds_path, subtype)
                try:
                    arcpy.SetSubtypeField_management(ds_path, "type_")
                except:
                    pass
                arcpy.AddSubtype_management(ds_path, subtype, desc)
                #if default:
                #    arcpy.SetDefaultSubtype_management(ds_path, subtype)
        else:
            messages.addMessage("Dataset %s does not exist" % dataset)

def subtypes_to_table(in_gdb, out_gdb, out_table, messages):

    arcpy.CreateTable_management(out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management(out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management(out_table_path, "subtype", "TEXT")
    arcpy.AddField_management(out_table_path, "desc_fr", "TEXT")
    arcpy.AddField_management(out_table_path, "desc_en", "TEXT")
    arcpy.AddField_management(out_table_path, "desc_es", "TEXT")

    cursor = arcpy.InsertCursor(out_table_path)

    arcpy.env.workspace = in_gdb

    tables = arcpy.ListTables()

    datasets = arcpy.ListDatasets()

    for table in tables:
        messages.addMessage("Adding subtypes for %s" % table)
        table_path = os.path.join(in_gdb, table)
        subtypes = arcpy.da.ListSubtypes(table_path)

        for st in subtypes:
            messages.addMessage("Adding subtypes for %s" % table)
            row = cursor.newRow()
            row.setValue("feature_class", table)
            row.setValue("subtype", st)
            row.setValue("desc_fr", subtypes[st]["Name"])
            cursor.insertRow(row)

    for dataset in datasets:
        ds_path = os.path.join(in_gdb, dataset)
        arcpy.env.workspace = ds_path
        feature_classes = arcpy.ListFeatureClasses()
        for fc in feature_classes:
            messages.addMessage("Adding fields for %s" % fc)
            fc_path = os.path.join(ds_path, fc)

            subtypes = arcpy.da.ListSubtypes(fc_path)

            for st in subtypes:
                row = cursor.newRow()
                row.setValue("feature_class", r"%s\%s" % (dataset, fc))
                row.setValue("subtype", st)
                row.setValue("desc_fr", subtypes[st]["Name"])
                cursor.insertRow(row)


def field_list_to_table(in_gdb, out_gdb, out_table, messages):

    arcpy.CreateTable_management(out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management(out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management(out_table_path, "field", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_fr", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_en", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_es", "TEXT")

    cursor = arcpy.InsertCursor(out_table_path)

    arcpy.env.workspace = in_gdb

    tables = arcpy.ListTables()

    datasets = arcpy.ListDatasets()

    for table in tables:
        messages.addMessage("Adding fields for %s" % table)
        table_path = os.path.join(in_gdb, table)
        field_list = arcpy.ListFields(table_path)
        for f in field_list:
            row = cursor.newRow()
            row.setValue("feature_class", table)
            row.setValue("field", f.name)
            row.setValue("alias_fr", f.aliasName)
            cursor.insertRow(row)

    for dataset in datasets:
        ds_path = os.path.join(in_gdb, dataset)
        arcpy.env.workspace = ds_path
        feature_classes = arcpy.ListFeatureClasses()
        for fc in feature_classes:
            messages.addMessage("Adding fields for %s" % fc)
            fc_path = os.path.join(ds_path, fc)
            field_list = arcpy.ListFields(fc_path)
            for f in field_list:
                row = cursor.newRow()
                row.setValue("feature_class", r"%s\%s" % (dataset, fc))
                row.setValue("field", f.name)
                row.setValue("alias_fr", f.aliasName)
                cursor.insertRow(row)


def datasets_to_table(in_gdb, out_gdb, out_table, messages):

    arcpy.CreateTable_management(out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management(out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_fr", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_en", "TEXT")
    arcpy.AddField_management(out_table_path, "alias_es", "TEXT")

    cursor = arcpy.InsertCursor(out_table_path)

    arcpy.env.workspace = in_gdb

    tables = arcpy.ListTables()

    datasets = arcpy.ListDatasets()

    for table in tables:
        messages.addMessage("Adding alias for %s" % table)
        table_path = os.path.join(in_gdb, table)

        alias = get_table_alias(table_path)

        row = cursor.newRow()
        row.setValue("feature_class", table)
        row.setValue("alias_fr", alias)
        cursor.insertRow(row)

    for dataset in datasets:
        ds_path = os.path.join(in_gdb, dataset)
        arcpy.env.workspace = ds_path
        feature_classes = arcpy.ListFeatureClasses()
        for fc in feature_classes:
            messages.addMessage("Adding alias for %s" % fc)
            fc_path = os.path.join(ds_path, fc)
            alias = get_table_alias(fc_path)
            row = cursor.newRow()
            row.setValue("feature_class", r"%s\%s" % (dataset, fc))
            row.setValue("alias_fr", alias)
            cursor.insertRow(row)
