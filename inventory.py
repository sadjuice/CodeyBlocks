class Item():
    def __init__(self):
        self.itemID = 0
        self.status = 0 #PLACEHOLDER value
    def getItemID(self):
        return self.itemID
    def setItemID(self, ID):
        self.itemID = ID

class Inventory():
    def __init__(self):
        self.ItemList = {}

    def addItem(self, itemID, quantity):
        if itemID in self.ItemList.keys():
            self.ItemList[itemID] += quantity
        else:
            self.ItemList[itemID] = quantity

    def grabList(self): return self.ItemList
