import arcpy
import import_metadata
import arcpy_metadata


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Metadata Toolbox"
        self.alias = "Metadata Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [ImportMetadata, MXDMetadata]


class ImportMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Import Metadata"
        self.description = "Imports metadata from a Google spreadsheet"
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
        country = arcpy.Parameter(
            displayName="Country",
            name="country",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        country.filter.type = "ValueList"
        country.filter.list = ["COG", "COD", "CAF", "CMR", "GAB", "GNQ"]

        # Third parameter
        lang = arcpy.Parameter(
            displayName="Language",
            name="lang",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        lang.filter.type = "ValueList"
        lang.filter.list = ["fr", "en", "es"]

        update_agol = arcpy.Parameter(
            displayName="Update AGOL metadata",
            name="update_agol",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
            category="ArcGIS online")

        username = arcpy.Parameter(
            displayName="AGOL username",
            name="username",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="ArcGIS online")

        password = arcpy.Parameter(
            displayName="AGOL password",
            name="password",
            datatype="GPStringHidden",
            parameterType="Optional",
            direction="Input",
            category="ArcGIS online")

        gid_en = arcpy.Parameter(
            displayName="English",
            name="gid_en",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="Metadata source (Google spreadsheet id)")

        gid_en.value = '1f0ODEaQL2RUV8bv3Y3_Kqwf9eLFL1mZiwLxFWS1SRfY'

        gid_fr = arcpy.Parameter(
            displayName="French",
            name="gid_fr",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Metadata source (Google spreadsheet id)")

        gid_fr.value = '1JoxJKA0oSID4gIOGKKSbqUjBTYA9SAFEN0yz-FUFrhM'

        gid_es = arcpy.Parameter(
            displayName="Spanish",
            name="gid_es",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Metadata source (Google spreadsheet id)")

        gid_es.value = '1JoxJKA0oSID4gIOGKKSbqUjBTYA9SAFEN0yz-FUFrhM'

        params = [in_gdb, country, lang, update_agol, username, password, gid_en, gid_es, gid_fr]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if bool(parameters[3].value):
            parameters[4].enabled = True
            parameters[5].enabled = True
        else:
            parameters[4].enabled = False
            parameters[5].enabled = False

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

        if lang == 'en':
            gid = parameters[6].valueAsText
        elif lang == 'fr':
            gid = parameters[7].valueAsText
        else:
            gid = parameters[8].valueAsText

        agol = bool(parameters[3].value)

        if agol:
            username = parameters[4].valueAsText
            password = parameters[5].valueAsText
        else:
            username = None
            password = None

        import_metadata.update_metadata(in_gdb,  country, gid, agol, username, password, messages)
        return


class MXDMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "MxdMetadata"
        self.description = "Update layer metadata using its data source"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input MXD",
            name="in_gdbs",
            datatype="DEMapDocument",
            parameterType="Required",
            direction="Input")

        #param0.filter.type = "File"
        #param0.filter.list = ["mxd"]
        #param0.value = "CURRENT"

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
        mxd_path = parameters[0].valueAsText

        mxd = arcpy.mapping.MapDocument(mxd_path)

        layers = arcpy.mapping.ListLayers(mxd)

        for l in layers:
            if l.supports("dataSource") and l.supports("description") and l.supports("credits"):
                messages.AddMessage(u"Update {}".format(l.name))
                md = arcpy_metadata.MetadataEditor(l.dataSource)
                l.description = md.abstract
                l.credits = md.credits
        mxd.save()
        #arcpy.RefreshTOC()

        return

