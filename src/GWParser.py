from queue import Queue

class GWParser:
    def loadQueue(filePath):
        queue = Queue()
        with open(filePath) as file:
            for line in file:
                input = line.lower().split()
                queue.put(tuple(input))
        return queue

    def printQueue(queue):
        while queue.qsize():
            print(queue.get())


# path = "..\Scripts\slime.txt"
# parser = GWParser
# parser.printQueue(parser.loadQueue(path))