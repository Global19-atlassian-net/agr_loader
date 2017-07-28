from files import *

import re

class SOExt:
    @staticmethod
    def get_data():
        path = "tmp";
        S3File("mod-datadumps/data", "so.obo", path).download()
        so_data = TXTFile(path + "/so.obo").get_data()

        so_dataset = {}

        creating_term = None

        for line in so_data:
            line = line.strip()

            if line == "[Term]":
                creating_term = True
            elif creating_term:
                key = (line.split(":")[0]).strip()
                value = ("".join(":".join(line.split(":")[1:]))).strip()

                if key == "id":
                    creating_term = value
                    so_dataset[creating_term] = {}
                else:
                    if key == "synonym":
                        if value.split(" ")[-2] == "EXACT":
                            value = (" ".join(value.split(" ")[:-2]))[1:-1]
                        else:
                            continue
                    if key == "def":
                        m = re.search('\"(.+)\"', value)
                        value = m.group(1)

                    if key in so_dataset[creating_term]:
                        so_dataset[creating_term][key].append(value)
                    else:
                        so_dataset[creating_term][key] = [value]

        return so_dataset