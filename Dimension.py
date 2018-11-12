class Dimension:

    def __init__(self,name,size,arr_index):

        self.name = name
        self.size = size
        self.arr_index = arr_index

        self.coords = [None for _ in range(size)]

        # List of 'units'
        for i in range(size):
            self.coords[i] = name + str(i)
