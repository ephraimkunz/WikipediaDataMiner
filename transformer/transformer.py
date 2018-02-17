import json
import os
import glob
import csv

class Transformer():
    def __init__(self, input_path, output_path, transformation):
        """ 
        input_path: path to directory containing raw scrape data. Ex: ../articles/. If just one file is desired to 
        be transformed (for testing), you can pass the path to that file instead.

        output_path: path to file (to be created) that will contain output CSV. Ex: ./dumb_count_output.csv

        transformation: function that applies transform. Will be called many times, with a raw data object argument 
        and a count (for debugging / logging in the transform function).
        Should return a dict of key, value mappings. This dict will be converted to a CSV with column title = key and 
        column value = value. 
        
        For example, I might be passed {"content": "This is the content", "pageid": 12345}. If I 
        am counting words in the page, I would return {"pageid": 12345, "word_count": 4}. This would result in CSV of 
        the form: 

        pageid,word_count
        12345,4
        ...

        Pageid should always be passed back out of the transformation to allow later joining of many transformations.
        Each item passed out of the transformation should have the same keys.
        """

        self.input_path = input_path
        self.output_path = output_path
        self.transformation = transformation

        # Check for valid paths
        if not os.path.exists(self.input_path):
            raise ValueError("Input path {} does not exist".format(self.input_path))

        if not self.output_path.endswith(".csv"):
            raise ValueError("Output path {} should have a .csv extension".format(self.output_path))

    def get_file_list(self):
        """ Returns an array of filenames to transform """
        # If this is a directory, enumerate all data file names in it.
        if os.path.isdir(self.input_path):
            filenames = []
            if not self.input_path.endswith("/"):
                self.input_path += "/"

            for filename in glob.glob(self.input_path + "controversial*.json"):
                filenames.append(filename)

            for filename in glob.glob(self.input_path + "normal*.json"):
                filenames.append(filename)

            return filenames

        # If this is a file, return just the filename.
        if os.path.isfile(self.input_path):
            return [self.input_path]

        raise ValueError("Unknown input file_path: {}".format(self.input_path))

    def dump_transformed(self, array):
        """ Dumps the output of the transformation into a CSV named output_path """
        if not os.path.exists(os.path.dirname(self.output_path)):
            os.makedirs(os.path.dirname(self.output_path))


        with open(self.output_path, 'w') as f:
            # pageid must come first
            orig_keys = list(array[0].keys())
            orig_keys.remove("pageid")
            keys = ["pageid"]
            keys.extend(orig_keys)

            w = csv.DictWriter(f, keys)
            w.writeheader()
            w.writerows(array)

    def run(self):
        """ Runs the transform, passing a raw data object and the count to the transformation function 
        for each raw data object """

        file_list = self.get_file_list()
        transformed = []
        count = 0

        for file in file_list:
            with open(file, "r") as f:
                text = f.read()
                items = json.loads(text)
                articles = items["articles"]

                for article in articles:
                    trans = self.transformation(article, count)
                    transformed.append(trans)
                    count += 1

        self.dump_transformed(transformed)