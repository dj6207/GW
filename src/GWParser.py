import os
from queue import Queue

class GWParser:
    def loadQueue(filePath):
        directory = "..\\Images\\"
        images = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                images.append(file.split(".")[0])
        queue = Queue()
        with open(filePath) as file:
            for line in file:
                input = line.lower().split()
                if input[1] in images:
                    queue.put(tuple(input))
                else:
                    raise Exception(f"{input[1]} does not have corresponding image")
        return queue

    def printQueue(queue):
        while queue.qsize():
            print(queue.get())

# path = "..\Scripts\slime.txt"
# parser = GWParser
# parser.printQueue(parser.loadQueue(path))