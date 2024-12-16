from datetime import datetime


class Report:
    def __init__(self, manager, orders, invoices, paid, margin, revenue, nds) -> None:
        self.date = datetime.now().strftime("%d.%m.%Y")
        self.manager = manager
        self.orders = int(orders)
        self.invoices = int(invoices)
        self.paid_invoices = int(paid)
        self.margin = float(margin)
        self.revenue = float(revenue)
        self.nds = float(nds)
        self.conversion = self.colc_conversion()
        self.conversion_paid = self.colc_conversion_paid()
        self.markup_percentage = self.colc_markup_percentage()

    def colc_conversion(self):
        try:
            return (self.invoices * 100) / self.orders
        except ZeroDivisionError:
            return 0

    def colc_conversion_paid(self):
        try:
            return (self.paid_invoices * 100) / self.invoices
        except ZeroDivisionError:
            return 0

    def colc_markup_percentage(self):
        try:
            return (self.margin * 100) / (self.revenue / float(self.nds))
        except ZeroDivisionError:
            return 0
