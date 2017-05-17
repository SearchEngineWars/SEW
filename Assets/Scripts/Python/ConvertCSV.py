#!/usr/bin/python

import sys, getopt, os, os.path, datetime, re, glob
from getopt import getopt

# Writes the output usage to the console with corresponding parameters.
def usage():
    print ("Usage: \t./ConvertCSV.py [-f --file] csv_to_covert [-a --all]" \
        "[-s --steps] num_levels_down_to_check [-o --outputDir] output_directory" \
        " [-d --dataloader] dataloader_path_and_name")


# Gets all CSV files from sub-directories of the provided directory
# @param dir the base directory to search down from
def get_csv_files(dir):
    files = []

    for dirpath,_,filenames in os.walk(dir):
        for filename in [f for f in filenames if f.endswith(".csv")]:
            files.append([dirpath, filename])
    return files


# Converts file from csv to JSON and generates the appropriate DTO for the class object.
# @param infile the path - file array pair to the input file
# @param outDir the output directory for the converted file
def convert_file(infile, outDir, dtoDir):
    fileContent = []
    trimmedContent = []
    columns = []
    adjustedCols = []
    with open(os.path.join(infile[0], infile[1]), "r") as fobj:
        text = fobj.readline()
        columns = text.replace("\n", "").split(',')
        regexStr = "^"
        for i in range(len(columns)):
            regexStr += "([\"].*[\"|]|[^,]*),"
        regexStr = regexStr[:-1]
        regexStr += "$"
        pattern = re.compile(regexStr)
        for column in columns: adjustedCols.append(re.sub("\\s", "", column))

        content = fobj.readlines()
        for line in content:
            fileContent.append(pattern.search(line.replace("\n", "")).groups())

    write_json(infile[1], outDir, adjustedCols, fileContent)
    write_dto(dtoDir, infile[0], infile[1], adjustedCols)


# Writes the data collected from the file to an output directory in a JSON format
# @param path to write the converted file to
# @param filename the name of the origional file
# @param outputDir the output directory for the file data
# @param data the data to insert into the JSON from the file
def write_json(filename, outputDir, headers, data):
    with open(outputDir + filename.replace(".csv", ".json"), "w") as targetFile:
        for entry in data:
            targetFile.write("{ \"" + filename.replace(".csv", "") + "\" : { ")
            writeString = ""
            for i in range(len(headers)):
                writeString += ("\"" + headers[i] + "\" : \"" + entry[i].replace("\"", "") + "\",")
            targetFile.write(writeString[:-1])
            targetFile.write("}}\n")
        targetFile.close()


# Writes the class that uses the provided CSV file set
# @param dtoDir is the data transfer object directory for stored objects
# @param filename the name of the file being read in
def write_dto(dtoDir, inputDir, filename, headers):
    with open(dtoDir + filename[:-4] + ".cs", "w") as dtoFile:
        dtoFile.write("/* \n")
        dtoFile.write(" * Automatically generated class due to the potential radical changes that may occur. \n")
        dtoFile.write(" * This file was generated from: " + inputDir.replace("\\", "/") + "/" + filename + " \n")
        dtoFile.write(" * This allows more radical changes to the provided classes should design require it. \n")
        dtoFile.write(" */\n")
        dtoFile.write("public class " + filename[:-4] + " { \n")
        for field in headers:
            dtoFile.write("\n")
            dtoFile.write("\tprivate string " + field.lower() + ";\n")
            dtoFile.write("\n")
            dtoFile.write("\tpublic string get" + field + "() {\n")
            dtoFile.write("\t\treturn " + field.lower() + ";\n")
            dtoFile.write("\t}\n")
            dtoFile.write("\n")
            dtoFile.write("\tpublic void set" + field + "(string " + field.lower() + ") {\n")
            dtoFile.write("\t\tthis." + field.lower() + " = " + field.lower() + ";\n")
            dtoFile.write("\t}\n")
        dtoFile.write("}\n")


# Updates the dataloader with the loaded data structures from the csv files
# @param dataStructureNames headers from the csv files
# @param dataloader file name for the data loader
def updateDataLoader(dataStructureNames, dataloader, dtoDir):
    with open(dataloader, "r") as dataloaderFile:
        text = dataloaderFile.read()
    structTag = "DATA_STRUCTURES"
    readTag = "READ_FILES"
    populateTag = "POPULATE_DATA"
    skip = False
    with open(dataloader, "w") as dlf:
        for line in text.split("\n"):
            if (structTag in line) and (skip is False):
                skip = True;
                dlf.write(line + "\n")
                for header in dataStructureNames:
                    dlf.write("\tList<" + header[1][:-4] + "> list" + header[1][:-4] + "Entries = new List<" + header[1][:-4] + ">();\n")
            elif (structTag in line) and (skip is True):
                skip = False
            elif (readTag in line) and (skip is False):
                skip = True
                dlf.write(line + "\n")
                for header in dataStructureNames:
                    dlf.write("\t\tList<string> " + header[1][:-4].lower() + "Entries = new List<string>(File.ReadAllLines(\"" + dtoDir + header[1][:-4] + ".json\"));\n")
            elif (readTag in line) and (skip is True):
                skip = False
            elif (populateTag in line) and (skip is False):
                skip = True
                dlf.write(line + "\n")
                for header in dataStructureNames:
                    dlf.write("\t\t" + header[1][:-4].lower() + "Entries.ForEach(entry => list" + header[1][:-4] + "Entries.Add(JsonConvert.DeserializeObject<" + header[1][:-4] + ">(entry)));\n")
            elif (populateTag in line) and (skip is True):
                skip = False
            if skip is False:
                dlf.write(line + "\n")


# The main method for execution
def main():
    baseDir = "../.."
    outputDir = '''../../ConvertedCSV/'''
    dtoDir = '''../csharp/dto/column/'''
    dataloader = '''../csharp/dto/loader/DataLoader.cs'''
    selectedFile = ''''''
    all = False
    opts, args = getopt(sys.argv[1:], "hi:o", ["file=", "all=", "outputDir="])

    try:
        for opt, arg in opts:
            if opt in ('-h', "--help"):
                usage()
                sys.exit(0)
            elif opt in ('-f', "--file"):
                selectedFile = arg.stip()
            elif opt in ('-a', "--all"):
                all = True
            elif opt in ('-s', "--steps"):
                pattern = arg.stip()
            elif opt in ('-d', "--dataloader"):
                dataloader = arg.strip()

        files = get_csv_files(baseDir)
        for file in files:
            convert_file(file, outputDir, dtoDir)
        dataStructures = []
        for (dirPath, filename) in files:
            dataStructures.append(filename)
        updateDataLoader(files, dataloader, dtoDir)

    except IOError as ioe:
        print ("Error: ", ioe)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
