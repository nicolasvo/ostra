from flask import Flask, jsonify, request

app = Flask(__name__)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('api/res/ostra-dd1177d64769.json', scope)
client = gspread.authorize(creds)

sheet = client.open("dictionary").sheet1


class Translator():

    def __init__(self, sheet):
        self.sheet = sheet
        self.map_language = {index + 1: language for index, language in enumerate(sheet.row_values(1))}
        self.to_languages = [{"language": language, "index": index} for index, language in self.map_language.items()]

    def show(self):
        list_all = self.sheet.get_all_records()
        return list_all

    def get_next_row(self):
        list_all = self.sheet.get_all_records()
        return len(list_all)

    def translate(self, row, col, word, from_language, to_language):
        content = f'=GOOGLETRANSLATE("{word}", "{from_language}", "{to_language["language"]}")'
        self.sheet.update_cell(row, col, word)
        self.sheet.update_cell(row, to_language["index"], content)

    def translate_row(self, row, col, word):
        from_language = self.map_language[col]
        to_languages = [elt for elt in self.to_languages if elt["language"] != from_language]
        for to_language in to_languages:
            self.translate(row, col, word, from_language, to_language)

    def insert_(self, col, word):
        row = self.get_next_row() + 2
        self.translate_row(row, col, word)

    def delete(self, row, col):
        self.sheet.update_cell(row, col, "")

    def delete_row_(self, row):
        self.sheet.delete_row(row)

translator = Translator(sheet)

@app.route("/")
def hello_world():
    print(translator.show())
    return jsonify(translator.show())

@app.route('/words', methods=['POST'])
def insert():
    body = request.get_json()
    map_parameter = ["word", "col"]
    parameters = {parameter: body[parameter] for parameter in map_parameter}
    translator.insert_(int(parameters["col"]), parameters["word"])
    return "", 201

# transactions = [
#     Income('Salary', 5000),
#     Income('Dividends', 200),
#     Expense('pizza', 50),
#     Expense('Rock Concert', 100)
# ]
#
#
# @app.route('/incomes')
# def get_incomes():
#     schema = IncomeSchema(many=True)
#     incomes = schema.dump(
#         filter(lambda t: t.type == TransactionType.INCOME, transactions)
#     )
#     return jsonify(incomes.data)
#
#
# @app.route('/incomes', methods=['POST'])
# def add_income():
#     income = IncomeSchema().load(request.get_json())
#     transactions.append(income.data)
#     return "", 204
#
#
# @app.route('/expenses')
# def get_expenses():
#     schema = ExpenseSchema(many=True)
#     expenses = schema.dump(
#         filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
#     )
#     return jsonify(expenses.data)
#
#
# @app.route('/expenses', methods=['POST'])
# def add_expense():
#     expense = ExpenseSchema().load(request.get_json())
#     transactions.append(expense.data)
#     return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)