from pyairtable import Api
from os import environ
from dotenv import load_dotenv
import pandas as pd

class AirtableInterface():
    def __init__(self, api_key):
        self.api = Api(api_key)
        self.table = self.api.table("appSBKTKW43QcbpRf", "tblYS5wjMHpRd0WNa")

    def get_pd_dataframe(self):
        return pd.DataFrame.from_records((r['fields'] for r in self.table.all()))

    def persist_in_airtable(self, json_payload):
        self.table.create(json_payload)

if __name__ == "__main__":
    load_dotenv()
    airt = AirtableInterface(environ["AIRTABLE_API_KEY"])
    print(airt.get_pd_dataframe())


# table.create({"Name": "Bob"})
# table.update("recwAcQdqwe21asdf", {"Name": "Robert"})
# table.delete("recwAcQdqwe21asdf")
