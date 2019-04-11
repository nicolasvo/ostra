from flask import Flask, jsonify, request
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

PORT = os.getenv("PORT", "5000")
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class Sheet():

    def __init__(self, name):
        self.name = name
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('api/res/contract.json', scope)
        self.client = gspread.authorize(self.creds)

    @property
    def sheet(self):
        if self.creds.access_token_expired:
            self.client.login()
        return self.client.open(self.name).sheet1

    def map_language(self):
        self.map_language = {index + 1: language for index, language in enumerate(self.sheet.row_values(1))}
        self.to_languages = [{"language": language, "index": index} for index, language in self.map_language.items()]

    def refresh_token(self):
        self.client.login()

    def parse_parameter(self, parameters):
        return {k: int(v) if k in ["row", "col"] else v for k, v in parameters.items()}

    def show(self):
        list_all = self.sheet.get_all_records()
        return list_all

    def get_next_row(self):
        list_all = self.sheet.get_all_records()
        return len(list_all)

    def update_(self, row, col, word):
        self.sheet.update_cell(row + 1, col, word)

    def translate(self, row, col, word, from_language, to_language):
        content = f'=GOOGLETRANSLATE("{word}", "{from_language}", "{to_language["language"]}")'
        self.update_(row, col, word)
        self.update_(row, to_language["index"], content)

    def translate_row(self, row, col, word):
        from_language = self.map_language[col]
        to_languages = [elt for elt in self.to_languages if elt["language"] != from_language]
        for to_language in to_languages:
            self.translate(row, col, word, from_language, to_language)

    def insert_(self, col, word):
        row = self.get_next_row() + 1
        self.translate_row(row, col, word)

    def delete(self, row, col):
        self.update_(row, col, "")

    def delete_row_(self, row):
        self.sheet.delete_row(row + 1)


sheet = Sheet("dictionary")
sheet.map_language()


@app.route("/")
def hello_world():
    print(sheet.show())
    return jsonify(sheet.show())


@app.route('/words', methods=['POST'])
def insert():
    parameters = sheet.parse_parameter(request.get_json())
    sheet.insert_(**parameters)
    return "", 201


@app.route("/words", methods=["PUT"])
def update():
    parameters = sheet.parse_parameter(request.get_json())
    if parameters["row"] <= 0:
        return "Row must be greater than 0.", 400
    else:
        sheet.update_(**parameters)
        return "", 201


@app.route("/words", methods=["DELETE"])
def delete():
    parameters = sheet.parse_parameter(request.get_json())
    if parameters["row"] <= 0:
        return "Row must be greater than 0.", 400
    else:
        sheet.delete_row_(**parameters)
        return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
