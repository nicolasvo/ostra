from flask import Flask, jsonify, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('api/res/ostra-dd1177d64769.json', scope)
client = gspread.authorize(creds)

sheet = client.open("dictionary").sheet1


class Translator():

    def __init__(self, sheet):
        self.sheet = sheet
        self.map_language = {index + 1: language for index, language in enumerate(sheet.row_values(1))}
        self.to_languages = [{"language": language, "index": index} for index, language in self.map_language.items()]

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
        row = self.get_next_row() + 2
        self.translate_row(row, col, word)

    def delete(self, row, col):
        self.update_(row, col, "")

    def delete_row_(self, row):
        self.sheet.delete_row(row + 1)

translator = Translator(sheet)

@app.route("/")
def hello_world():
    print(translator.show())
    return jsonify(translator.show())

@app.route('/words', methods=['POST'])
def insert():
    body = request.get_json()
    map_parameter = ["col", "word"]
    parameters = {parameter: body[parameter] for parameter in map_parameter}
    parameters = translator.parse_parameter(parameters)
    translator.insert_(**parameters)
    return "", 201

@app.route("/words", methods=["PUT"])
def update():
    body = request.get_json()
    map_parameter = ["row", "col", "word"]
    parameters = {parameter: body[parameter] for parameter in map_parameter}
    parameters = translator.parse_parameter(parameters)

    if parameters["row"] <= 0:
        return "Row must be greater than 0.", 400
    else:
        translator.update_(**parameters)
        return "", 201

@app.route("/words", methods=["DELETE"])
def delete():
    body = request.get_json()
    map_parameter = ["row"]
    parameters = {parameter: body[parameter] for parameter in map_parameter}
    if int(parameters["row"]) <= 0:
        return "Row must be greater than 0.", 400
    else:
        translator.delete_row_(int(parameters["row"]))
        return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)