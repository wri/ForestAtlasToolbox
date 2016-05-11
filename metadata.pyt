import arcpy
import import_metadata



class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Import metadata"
        self.alias = "Import metadata"

        # List of tool classes associated with this toolbox
        self.tools = [ImportMetadata]

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


