import arcpy
import os
#import sys


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
        ds_path = os.path.join(in_gdb, dataset)
        alias = row.getValue(alias_field)

        if alias != '' and alias is not None:
            arcpy.AlterAliasName(ds_path, alias)


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
            field_list = arcpy.ListFields (ds_path)
            for f in field_list:
                if f.name == field:
                    f.aliasName = alias


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

        if desc != '' and desc is not None:
            arcpy.RemoveSubtype_management(ds_path, subtype)
            arcpy.AddSubtype_management(ds_path, subtype, desc)
            #if default:
            #    arcpy.SetDefaultSubtype_management(ds_path, subtype)


def subtypes_to_table(in_gdb, out_gdb, out_table, messages):

    arcpy.CreateTable_management (out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management (out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management (out_table_path, "subtype", "TEXT")
    arcpy.AddField_management (out_table_path, "desc_fr", "TEXT")
    arcpy.AddField_management (out_table_path, "desc_en", "TEXT")
    arcpy.AddField_management (out_table_path, "desc_es", "TEXT")

    cursor = arcpy.InsertCursor (out_table_path)

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

    arcpy.CreateTable_management (out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management (out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management (out_table_path, "field", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_fr", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_en", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_es", "TEXT")

    cursor = arcpy.InsertCursor (out_table_path)

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

    arcpy.CreateTable_management (out_gdb, out_table)
    out_table_path = os.path.join(out_gdb, out_table)
    arcpy.AddField_management (out_table_path, "feature_class", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_fr", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_en", "TEXT")
    arcpy.AddField_management (out_table_path, "alias_es", "TEXT")

    cursor = arcpy.InsertCursor (out_table_path)

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



class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Tranlate GDB"
        self.alias = "Translate GDB"

        # List of tool classes associated with this toolbox
        self.tools = [UpdateDomain, UpdateFieldAlias, UpdateDatasetAlias, UpdateSubtypeDesc, WriteDataSetsToTable, WriteFieldsToTable, WriteSubtypesToTable]


class UpdateDomain(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Domains"
        self.description = "Update domains using a predefines list"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Domain GDB",
            name="domain_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param2.filter.type = "ValueList"
        param2.filter.list = ["fr", "en", "es"]

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        domain_gdb = parameters[1].valueAsText
        lang = parameters[2].valueAsText

        load_domains(in_gdb, domain_gdb, lang, messages)
        return

class UpdateFieldAlias(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Field Alias"
        self.description = "Update field alias using a predefines list"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Alias table",
            name="alias_table",
            datatype="DETable",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param2.filter.type = "ValueList"
        param2.filter.list = ["fr", "en", "es"]

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        alias_table = parameters[1].valueAsText
        lang = parameters[2].valueAsText

        update_field_alias(in_gdb, alias_table, lang, messages)
        return


class UpdateDatasetAlias(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Dataset Alias"
        self.description = "Update dataset alias using a predefines list"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Alias table",
            name="alias_table",
            datatype="DETable",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param2.filter.type = "ValueList"
        param2.filter.list = ["fr", "en", "es"]

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        alias_table = parameters[1].valueAsText
        lang = parameters[2].valueAsText

        update_dataset_alias(in_gdb, alias_table, lang, messages)
        return


class UpdateSubtypeDesc(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Subtype Description"
        self.description = "Update subtype description using a predefines list"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Subtype table",
            name="alias_table",
            datatype="DETable",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param2.filter.type = "ValueList"
        param2.filter.list = ["fr", "en", "es"]

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        subtype_table = parameters[1].valueAsText
        lang = parameters[2].valueAsText

        update_subtype(in_gdb, subtype_table, lang, messages)
        return


class WriteFieldsToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Write Fields to Table"
        self.description = "Write fields and field aliases to a table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Output GDB",
            name="out_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Output Table name",
            name="out_table",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        out_gdb = parameters[1].valueAsText
        out_table = parameters[2].valueAsText

        field_list_to_table(in_gdb, out_gdb, out_table, messages)
        return


class WriteDataSetsToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Write Datasets to Table"
        self.description = "Write dataset aliases to a table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Output GDB",
            name="out_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Output Table name",
            name="out_table",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        out_gdb = parameters[1].valueAsText
        out_table = parameters[2].valueAsText

        datasets_to_table(in_gdb, out_gdb, out_table, messages)
        return


class WriteSubtypesToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Write Subtypes to Table"
        self.description = "Write subtype descriptions to a table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Output GDB",
            name="out_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Output Table name",
            name="out_table",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_gdb = parameters[0].valueAsText
        out_gdb = parameters[1].valueAsText
        out_table = parameters[2].valueAsText

        subtypes_to_table(in_gdb, out_gdb, out_table, messages)
        return