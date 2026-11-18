# # Copyright (c) 2026, Sneha and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class LibraryMember(Document):
# 	pass



import frappe
from frappe.model.document import Document


class LibraryMember(Document):

    def validate(self):
        if not self.member_name:
            frappe.throw("Member Name is required")

        if not self.email:
            frappe.throw("Email is required")

        if "@" not in self.email:
            frappe.throw("Please enter a valid email address")
