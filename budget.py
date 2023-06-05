class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []

  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})

  def withdraw(self, amount, description=''):
    if self.check_funds(amount):
      self.ledger.append({'amount': -amount, 'description': description})
      return True
    else:
      return False

  def transfer(self, amount, category):
    if self.check_funds(amount):
        description = f"Transfer to {category.name}"
        withdrawal_successful = self.withdraw(amount, description)
        if withdrawal_successful:
            description = f"Transfer from {self.name}"
            category.deposit(amount, description)
            return True
    return False

  def get_balance(self):
    balance = sum(transaction['amount'] for transaction in self.ledger)
    return balance

  def check_funds(self, amount):
    return amount <= self.get_balance()

  def __str__(self):
    title = f"{self.name.center(30, '*')}\n"
    items = ""
    total = 0

    for item in self.ledger:
      description = item["description"][:23].ljust(23)
      amount = format(item["amount"], ".2f").rjust(7)
      items += f"{description}{amount}\n"
      total += item["amount"]

    total_line = f"Total: {format(total, '.2f')}"

    return title + items + total_line


def create_spend_chart(categories):
  # Step 1: Calculate percentage spent for each category
    category_names = []
    category_withdrawals = []
    total_withdrawals = 0

    for category in categories:
        withdrawals = sum(transaction["amount"] for transaction in category.ledger if transaction["amount"] < 0)
        category_names.append(category.name)
        category_withdrawals.append(withdrawals)
        total_withdrawals += withdrawals

    category_percentages = [withdrawals / total_withdrawals * 100 for withdrawals in category_withdrawals]

    # Step 2: Generate chart lines
    chart_lines = []
    chart_lines.append("Percentage spent by category")

    for percentage in range(100, -10, -10):
        line = f"{percentage:3d}| "
        for category_percentage in category_percentages:
            if category_percentage >= percentage:
                line += "o  "
            else:
                line += "   "
        chart_lines.append(line)

    # Step 3: Generate horizontal line and category names
    horizontal_line = "    " + "-" * (len(category_names) * 3 + 1)

    max_name_length = max(len(name) for name in category_names)
    category_names_lines = []

    for i in range(max_name_length):
        line = "     "
        for name in category_names:
            if i < len(name):
                line += name[i] + "  "
            else:
                line += "   "
        category_names_lines.append(line)

    # Step 4: Combine chart lines, horizontal line, and category names
    chart = "\n".join(chart_lines) + "\n"
    chart += horizontal_line + "\n"
    chart += "\n".join(category_names_lines)

    return chart