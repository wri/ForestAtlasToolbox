import arcpy
import import_metadata
import translate
import attachements_metadata


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
                      WriteDataSetsToTable,
                      WriteFieldsToTable,
                      WriteSubtypesToTable,
                      ImportMetadata,
                      AddAttachementMetadata]


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

        translate.load_domains(in_gdb, domain_gdb, lang, messages)
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

        translate.update_subtype(in_gdb, subtype_table, lang, messages)
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

        translate.field_list_to_table(in_gdb, out_gdb, out_table, messages)
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

        translate.datasets_to_table(in_gdb, out_gdb, out_table, messages)
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

        translate.subtypes_to_table(in_gdb, out_gdb, out_table, messages)
        return



class ImportMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Import Metadata"
        self.description = "Imports metadata from a Google spreadsheet"
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
            displayName="Country",
            name="country",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param1.filter.type = "ValueList"
        param1.filter.list = ["COG", "COD", "CAF", "CMR", "GAB", "GNQ"]

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
        country = parameters[1].valueAsText
        lang = parameters[2].valueAsText

        import_metadata.update_metadata(in_gdb, country, lang, messages)
        return

class AddAttachementMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add document metadata fields"
        self.description = "Add document metadata fields"
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

        params = [param0]

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

        attachements_metadata.add_metadata_fields(in_gdb, messages)
        return