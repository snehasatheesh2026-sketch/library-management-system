
# from frappe.model.document import Document


# class LibraryBook(Document):
# 	pass


import frappe
from frappe.model.document import Document


class LibraryBook(Document):

    def validate(self):
        if not self.book_title:
            frappe.throw("Book Title is required")

        if self.quantity < 0:
            frappe.throw("Quantity cannot be negative")

        if self.available_copies < 0:
            frappe.throw("Available Copies cannot be negative")

        if self.available_copies > self.quantity:
            frappe.throw("Available Copies cannot exceed total Quantity")
