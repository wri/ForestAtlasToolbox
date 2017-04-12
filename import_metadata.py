import arcpy
import arcpy_metadata
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import arcrest
from arcresthelper import securityhandlerhelper


def open_spreadsheet(country, gid):

    # specify oauth2client credentials
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    spreadsheet_file = os.path.join(dir_name, 'spreadsheet.json')

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(spreadsheet_file, scope)

    # authorize oauth2client credentials
    gc = gspread.authorize(credentials)

    # open the metadata entry spreadsheet
    # wks = gc.open("Metadata Forest Atlas (french/ spanish)").sheet1

    sh = gc.open_by_key(gid)

    wks = sh.worksheet(country)

    gdocAsLists = wks.get_all_values()

    return gdocAsLists


def gdoc_lists_to_layer_dict(inGdocAsLists):

    # Create emtpy metadata dictionary
    md = {}

    # Pull the header row from the Google doc
    headerRow = inGdocAsLists[0]

    # Iterate over the remaining data rows
    for dataRow in inGdocAsLists[1:]:

        # Build a dictionary for each row with the column title
        # as the key and the value of that row as the value
        rowAsDict = {k: v for (k, v) in zip(headerRow, dataRow)}

        # Grab the technical title (what we know the layer as)
        layerName = rowAsDict['technical_title']

        # Add that as a key to the larger md dictionary
        md[layerName] = {}

        # For all the
        for key, value in rowAsDict.iteritems():
            try:
                #mdItemName = lkpColName_to_mdName[key]
                #md[layerName][mdItemName] = value
                md[layerName][key] = value

            # If the field isn't in our metadata lookup, ignore it
            except:
                pass

    return md


def update_metadata(gdb, country, gid, agol, username, password, messages):

    if agol:
        config = {'username': username, 'password': password, 'security_type': 'Portal'}
        token = securityhandlerhelper.securityhandlerhelper(config)
        admin = arcrest.manageorg.Administration(securityHandler=token.securityhandler)

    desc = arcpy.Describe(gdb)
    if desc.workspaceFactoryProgID == "esriDataSourcesGDB.SdeWorkspaceFactory.1":
        database = desc.connectionProperties.database
        try:
            user = desc.connectionProperties.user
        except:
            user = "DBO"
        db_prefix = "{}.{}.".format(database, user)
    else:
        db_prefix = ""



    gdocAsLists = open_spreadsheet(country, gid)
    md = gdoc_lists_to_layer_dict(gdocAsLists)
    for dataset in md.keys():
        messages.addMessage(dataset)
        d = dataset.split('\\')
        if len(d) == 1:
            if db_prefix != "":
                ds = os.path.join(gdb, "{}{}".format(db_prefix, d[0]))
            else:
                ds = os.path.join(gdb, d[0])
        elif len(d) == 2:
            if db_prefix != "":
                ds = os.path.join(gdb, "{}{}".format(db_prefix, d[0]), "{}{}".format(db_prefix, d[1]))
            else:
                ds = os.path.join(gdb, d[0], d[1])
        else:
            ds = os.path.join(gdb, dataset)

        if len(dataset) > 0:
            try:

                metadata = arcpy_metadata.MetadataEditor(ds)
                messages.addMessage("Update metadata for %s" % ds)

                metadata.title = md[dataset]["title"]
                metadata.purpose = md[dataset]["summary"]
                metadata.abstract = md[dataset]["description"]
                metadata.language = md[dataset]["language"]
                metadata.tags = md[dataset]["tags"].split(",")
                metadata.place_keywords = md[dataset]["place_keywords"].split(",")
                metadata.extent_description = md[dataset]["extent_description"]
                metadata.temporal_extent_description = md[dataset]["temporal_extent_description"]
                # metadata.scale_resolution = md[dataset]["scale_description"]
                # metadata.min_scale = md[dataset]["scale_min"]
                # metadata.max_scale = md[dataset]["scale_max"]
                metadata.update_frequency_description = md[dataset]["update_freq_desc"]
                metadata.credits = md[dataset]["credits"]
                metadata.citation = md[dataset]["citation"]
                metadata.license = md[dataset]["license"]
                metadata.limitation = md[dataset]["limitation"]
                metadata.source = md[dataset]["source"]
                metadata.point_of_contact.contact_name = md[dataset]["contact_wri_name"]
                metadata.point_of_contact.organization = md[dataset]["contact_wri_org"]
                metadata.point_of_contact.position = md[dataset]["contact_wri_pos"]
                metadata.point_of_contact.address = md[dataset]["contact_wri_address"]
                metadata.point_of_contact.city = md[dataset]["contact_wri_city"]
                metadata.point_of_contact.state = md[dataset]["contact_wri_state"]
                metadata.point_of_contact.zip = md[dataset]["contact_wri_postalcode"]
                metadata.point_of_contact.email = md[dataset]["contact_wri_email"]
                metadata.point_of_contact.country = md[dataset]["contact_wri_country"]
                metadata.point_of_contact.phone_nb = md[dataset]["contact_wri_phone"]
                metadata.maintenance_contact.contact_name = md[dataset]["contact_tec_name"]
                metadata.maintenance_contact.organization = md[dataset]["contact_tec_org"]
                metadata.maintenance_contact.position = md[dataset]["contact_tec_pos"]
                metadata.maintenance_contact.address = md[dataset]["contact_tec_address"]
                metadata.maintenance_contact.city = md[dataset]["contact_tec_city"]
                metadata.maintenance_contact.state = md[dataset]["contact_tec_state"]
                metadata.maintenance_contact.zip = md[dataset]["contact_tec_postalcode"]
                metadata.maintenance_contact.email = md[dataset]["contact_tec_email"]
                metadata.maintenance_contact.country = md[dataset]["contact_tec_country"]
                metadata.maintenance_contact.phone_nb = md[dataset]["contact_tec_phone"]
                metadata.citation_contact.contact_name = md[dataset]["contact_own_name"]
                metadata.citation_contact.organization = md[dataset]["contact_own_org"]
                metadata.citation_contact.position = md[dataset]["contact_own_pos"]
                metadata.citation_contact.address = md[dataset]["contact_own_address"]
                metadata.citation_contact.city = md[dataset]["contact_own_city"]
                metadata.citation_contact.state = md[dataset]["contact_own_state"]
                metadata.citation_contact.zip = md[dataset]["contact_own_postalcode"]
                metadata.citation_contact.email = md[dataset]["contact_own_email"]
                metadata.citation_contact.country = md[dataset]["contact_own_country"]
                metadata.citation_contact.phone_nb = md[dataset]["contact_own_phone"]

                metadata.rm_gp_history()
                metadata.save()

                if len(md[dataset]["arcgis_online_id"]) and agol:
                    item = admin.content.getItem(itemId=md[dataset]["arcgis_online_id"])
                    item.updateMetadata(metadata.metadata_file)

                metadata.finish()

            except IOError:
                messages.addMessage("Skip metadata for %s" % ds)

