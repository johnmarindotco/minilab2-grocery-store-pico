class Product:
    def __init__(self, sku, name, description, stock):
        self.sku = sku
        self.name = name
        self.description = description
        self.stock = stock

    def line1(self):
        return self.description

    def line2(self):
        return self.name

class PackagedProduct(Product):
    def __init__(self, sku, name, description, stock, manufacturer, msrp):
        super().__init__(sku, name, description, stock)
        self.manufacturer = manufacturer
        self.msrp = msrp

    def line2(self):
        return str(self.msrp)

class BulkProduct(Product):
    pass
