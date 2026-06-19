from datetime import date


def calculate_total(items, tax, discount):

    subtotal = 0

    for item in items:

        subtotal += item.quantity * item.price

    total = subtotal + tax - discount

    return subtotal, total


def is_overdue(due_date):

    return due_date < date.today()