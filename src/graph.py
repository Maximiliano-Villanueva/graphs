import re
from glob import glob
import os
from os import path, sep
from Parser.CodeParser import Parser


class Tm1Graph:

    RULE_DIRECTION_CHAR = '='
    FEEDER_DIRECTION_CHARS = "=>"
    FEEDER_KEYWORD = "feeders;"

    DB_REGEX = '(db\(.*?\));'


    def __init__(self, data_path, parser = None, exclude_regex = None):
        """ basic constructor"""

        #assert path existance
        if not path.exists(data_path):
            raise Exception(data_path + " could not find")
        
        self.exclude = exclude_regex
        self.dataPath = data_path
        self.data = list()
        
        #load filenames from directory
        self.__getData()

        #exclude files if requested
        if exclude_regex is not None:
            self.__exclude()
        
        if parser:
            self.parser = parser
        else:
            self.parser = Parser()
        
            

    def __getData(self):
        """
        get files from directory and store them in list
        """
        for file in glob(os.path.join(self.dataPath,'*.RUX')):
            self.data.append(file)



    def __exclude(self):
        """
        exclude items from list
        """
        pass

    def __readFileContent(self,file_path):
        """
        read content from specific file without comments
        """
        #assert file existance
        if not path.exists(file_path):
            raise Exception(file_path + " could not find")

        content = ""
        lines = []
 
        #open file in read mode and read its contents
        with open(file_path, mode = "r", encoding= "utf-8") as file:

            lines = file.readlines()

            #get rid of comments 
            for line in lines:
                line = line.strip()

                if len(line) < 1:
                    continue
                if line[0] != '#':
                    content +=line+"\n"

        return content

    def _find_string(self, items):
        if isinstance(items, str) :
            return items
        else:
            if isinstance(items, list):
                for i in items:
                    res = self._find_string(i)
                    if isinstance(res, str):
                        return res
            elif isinstance(items, dict):
                for i in items.keys():
                    i = items[i]
                    res = self._find_string(i)
                    if isinstance(res, str):
                        return res

    def getNodesAndEdges(self, data):
        edges_green = list()
        edges_red = list()
        nodes = list()

        for d in data.keys():
            if not (d in nodes):
                nodes.append(d)
            for ge in data[d]["GREEN_EDGES"]:
                if not (ge in nodes):
                    nodes.append(ge)
                edges_green.append((d,ge))

            for re in data[d]["RED_EDGES"]:
                if not (re in nodes):
                    nodes.append(re)
                edges_red.append((d,re))

        return nodes, edges_green, edges_red

            
            
        pass
    def parseContent(self):
        """
        parse content from files
        return : dict
        """
        #assert number of files
        if len(self.data) < 1 :
            raise Exception("No files found")

        cubes = dict()

        for file in self.data:
            content = self.__readFileContent(file)
            content = content.lower()
            #skip exmpty strings
            if content == '':
                continue
                        
            #get cube name
            cube_name = file.split(os.sep)[-1].split('.')[0]

            #create entry in cube dict if it does not exist
            if cube_name not in cubes.keys():
                cubes[cube_name] = {"FEEDERS_IN" : [], "FEEDERS_OUT" : [], "RULES" : [], "DIMENSIONS" : [], "RED_EDGES" : [], "GREEN_EDGES" : []}

            content= content.split(self.FEEDER_KEYWORD)
            
            #split rules from freeders
            content_rules = content[0]
            content_feeders = content[1]
            
            #find all matches for rules and feeders
            rules = re.findall(self.DB_REGEX, content_rules, flags=re.I|re.M)
            feeders = re.findall(self.DB_REGEX, content_feeders, flags=re.I|re.M)

            #parse feeders
            for feeder in feeders:
                #cubes[cube_name]["FEEDERS_OUT"].append(cstring)
                content = self.parser.parse(feeder)
                cubes[cube_name]["FEEDERS_OUT"].append(content)
                func_name = list(content[0].keys())[0]

                pos_str = self._find_string(content)
                
                cubes[cube_name]["RED_EDGES"].append(pos_str.strip("'"))
                


            #parse rules
            for rule in rules:
                #cubes[cube_name]["RULES"].append(cstring)
                content = self.parser.parse(rule)
                cubes[cube_name]["RULES"].append(content)

                func_name = list(content[0].keys())[0]
        
                pos_str = self._find_string(content)
                
                cubes[cube_name]["GREEN_EDGES"].append(pos_str.strip("'"))
            
        return cubes











                
                    
                
            


            


        
    