import arcpy

import translate



class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Tranlate GDB"
        self.alias = "Translate GDB"

        # List of tool classes associated with this toolbox
        self.tools = [UpdateDomain,
                      UpdateFieldAlias,
                      UpdateDatasetAlias,
                      UpdateSubtypeDesc,
                      ExportDomainToTable,
                      ExportDataSetsToTable,
                      ExportFieldsToTable,
                      ExportSubtypesToTable]


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
        param2.filter.list = ["fr", "en", "es", "ka"]

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

        translate.load_domains(in_gdb, domain_gdb, lang, messages)
        return


class ExportDomainToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Domains"
        self.description = "Export domains to table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        in_gdb = arcpy.Parameter(
            displayName="Input GDB",
            name="in_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Second parameter
        domain_gdb = arcpy.Parameter(
            displayName="Domain GDB",
            name="domain_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Third parameter
        lang = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        lang.filter.type = "ValueList"
        lang.filter.list = ["fr", "en", "es", "ka"]

        params = [in_gdb, domain_gdb, lang]

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

        translate.export_domains(in_gdb, domain_gdb, lang, messages)
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
        param2.filter.list = ["fr", "en", "es", "ka"]

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

        translate.update_field_alias(in_gdb, alias_table, lang, messages)
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
        param2.filter.list = ["fr", "en", "es", "ka"]

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

        translate.update_dataset_alias(in_gdb, alias_table, lang, messages)
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
        param2.filter.list = ["fr", "en", "es", "ka"]

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

        translate.update_subtype(in_gdb, subtype_table, lang, messages)
        return


class ExportFieldsToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Fields to Table"
        self.description = "Export fields and field aliases to a table"
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

        translate.field_list_to_table(in_gdb, out_gdb, out_table, messages)
        return


class ExportDataSetsToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Datasets to Table"
        self.description = "Export dataset aliases to a table"
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

        translate.datasets_to_table(in_gdb, out_gdb, out_table, messages)
        return


class ExportSubtypesToTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Subtypes to Table"
        self.description = "Export subtype descriptions to a table"
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

        translate.subtypes_to_table(in_gdb, out_gdb, out_table, messages)
        return
