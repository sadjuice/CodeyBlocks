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

    def isEmpty(self):
        if len(self.ItemList) == 0:
            return True
        else:
            return False

    def inInv(self, itemID):
        if itemID in self.ItemList.keys():
            return True
        else:
            return False

    def addItem(self, itemID, quantity):
        if self.inInv(itemID):
            self.ItemList[itemID] += quantity
        else:
            self.ItemList[itemID] = quantity

    def removeItem(self, itemID, quantity):
        if self.inInv(itemID):
            if self.ItemList[itemID] == 0 or self.ItemList[itemID] - quantity == 0:
                del self.ItemList[itemID]
            else:
                self.ItemList[itemID] -= quantity


    def grabList(self): return self.ItemList

