# Copyright (c) 2026, Sneha and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class TransactionBook(Document):
# 	pass



import frappe
from frappe.model.document import Document


class TransactionBook(Document):

    def validate(self):
        if not self.book:
            frappe.throw("Please select a book")

        if self.quantity <= 0:
            frappe.throw("Book quantity must be greater than zero")
