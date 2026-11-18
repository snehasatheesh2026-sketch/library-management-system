
import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class LibraryTransaction(Document):

    def validate(self):

        # Validate only before submission
        if self.docstatus == 0:

            member = frappe.get_doc("Library Member", self.member)

            if member.membership_status != "Active":
                frappe.throw("Only active members can issue books")

            if getdate(self.due_date) < getdate(self.transaction_date):
                frappe.throw("Due Date cannot be before Transaction Date")

            if not self.books:
                frappe.throw("Please add at least one book")

            for row in self.books:

                book = frappe.get_doc("Library Book", row.book)

                if row.quantity <= 0:
                    frappe.throw("Book quantity must be greater than zero")

                if row.quantity > book.available_copies:
                    frappe.throw(
                        f"Not enough copies available for {book.book_title}"
                    )

    def on_submit(self):

        # Reduce available copies when a book is issued
        for row in self.books:

            book = frappe.get_doc("Library Book", row.book)

            book.db_set(
                "available_copies",
                book.available_copies - row.quantity
            )

    def on_update_after_submit(self):

        old_doc = self.get_doc_before_save()

        if not old_doc:
            return

        # Prevent changing books or quantities after submission
        old_books = sorted(
            (row.book, row.quantity) for row in old_doc.books
        )

        new_books = sorted(
            (row.book, row.quantity) for row in self.books
        )

        if old_books != new_books:
            frappe.throw(
                "Books and quantities cannot be changed after submission"
            )

        # Prevent changing Returned back to Issued
        if old_doc.status == "Returned" and self.status != "Returned":
            frappe.throw(
                "A returned transaction cannot be changed back"
            )

        # Restore copies only once
        if old_doc.status == "Issued" and self.status == "Returned":

            for row in self.books:

                book = frappe.get_doc("Library Book", row.book)

                book.db_set(
                    "available_copies",
                    book.available_copies + row.quantity
                )

    def on_cancel(self):

        # Restore copies when an issued transaction is cancelled
        if self.status == "Issued":

            for row in self.books:

                book = frappe.get_doc("Library Book", row.book)

                book.db_set(
                    "available_copies",
                    book.available_copies + row.quantity
                )
