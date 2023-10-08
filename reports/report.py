from datetime import datetime

class Report:
    def __init__(self, manager, orders, invoices, paid, margin, revenue, nds) -> None:
        self.date = datetime.now().strftime('%d.%m.%Y')
        self.manager = manager
        self.orders = int(orders)
        self.invoices = int(invoices)
        self.paid_invoices = int(paid)
        self.margin = float(margin)
        self.revenue = float(revenue)
        self.nds = float(nds)
        self.conversion = (self.invoices * 100) / self.orders
        self.conversion_paid = (self.paid_invoices * 100) / self.invoices
        self.markup_percentage = (self.margin * 100) / (self.revenue / float(nds))

