import csv
class TOCSV:

    node = None
    edge = None
    weight = None

    def __init__(self, node, edge, weight):
        self.node = node
        self.edge = edge
        self.weight = weight
    
    def getCsvFile(self):
        with open('partition.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            for i in range(0, len(self.node)):
                filewriter.writerow([self.node[i], self.edge[i], self.weight[i]])
