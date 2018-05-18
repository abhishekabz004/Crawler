import csv

class ipReader:
    url_list = []
    category_title = {}
    category_path = {}

    def initiate(self):
        self.url_list = []
        self.category_path = {}
        self.category_title = {}

    def readFile(self, filename):
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.url_list.append(row[3])
                row[0] = row[0].replace("*", ",")
                self.category_title[row[0]] = row[1]
                self.category_path[row[0]] = row[2]