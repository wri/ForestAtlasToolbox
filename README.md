# translate_gdb

Translate geodatabase domains, dataset aliases, field aliases and subtypes with this python toolbox. 

# Requirements

Uses the ArcPy python module, so you must have ArcGIS Installed 

# Usage

This Python toolbox helps you to translate domains, datasets aliases, field aliases and subtypes in your geodatabase.
The tool currently supports French, English and Spanish with French as the default language. However, you can use any language instead.

## Translate dataset or field aliases and subtypes

1. Create an empty file or personal geodatabase
2. Open the "Write Dataset/ Fields/ Subtypes to Table" tool
    - Input GDB: Select your geodatabase you want to translate
    - Output GDB: Select the newly created file or personal geodatabase (you can reuse the same database of other translations)
    - Output Table name: Pick any name you want (ie myGDB_datasets, myGDB_fields, myGDB_subtypes)
3. Click OK. The tool will write all your dataset aliases, field aliases or subtype descriptions to the new table
4. Open the output table. You will see the current aliases/ descriptions next to the the actual name or code.
5. Update or translate aliases/ description as needed in the corresponding language collumn.
6. Make sure your edits got saved.
7. Open the "Update Dataset Aliases/ Field Aliases/ Subtype Description" tool
    - Input GDB: Select your geodatabase you want to translate
    - Alias table/ subtype table: Select the table which contains the translation
    - Language: Select the language column you want to use. 
8. Click OK. The tool will update aliases or description using the values in the selected column. 

HINT: You cannot translate subtypes if the feature class is part of a relationship class. Remove the relationship class first.
HINT: The tool selects the language based on the language suffix of the column (fr = French, en = English, es = Spanish). You can use any other language instead, just make sure you pick the right column.

## Translate domains

The first part is a manual process, and not yet scripted

1. Create an empty file or personal geodatabase
2. Use the "Domain To Table" from ArcToolbox tool and export your domains
    - Input Workspace: The geodatabase you want to translate
    - Domain Name: The domain you want to export
    - Output Table: Make sure you pick the same name as you actual domain
    - Code Field: Always name this field "code"
    - Field Description: Always name this field "desc_en" or "desc_fr" or "desc_es"
3. Repeat for every Domain you want to translate
4. Open each table and create a new column for the translation. Call the column "desc_en" or "desc_fr" or "desc_es"
5. Translate your domains
6. Open the "Update domain" tool
    - Input GDB: The geodatabase you want to translate
    - Domain GDB: The geodatabase with the translated domains
    - Language: Select the language column you want to use.
7. Click OK. The tool will update alias description using the values in the selected column. 

