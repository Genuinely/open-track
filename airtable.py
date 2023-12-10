from pyairtable import Api
from os import environ
from dotenv import load_dotenv
import pandas as pd

class AirtableInterface():
    def __init__(self, api_key, base_id, table_key):
        self.api = Api(api_key)
        self.table = self.api.table(environ["AIRTABLE_BASE_ID"], "Snapshots")

    def get_pd_dataframe(self):
        return pd.DataFrame.from_records((r['fields'] for r in self.table.all()))

    def persist_json_in_airtable(self, json_payload):
        self.table.create(json_payload)

if __name__ == "__main__":
    load_dotenv()
    airt = AirtableInterface(environ["AIRTABLE_API_KEY"], environ['AIRTABLE_BASE_ID'], environ['AIRTABLE_TABLE_KEY'])
    print(airt.get_pd_dataframe())

    # with open("data.json", "r") as f:
    #     for line in f.readlines():
    #         airt.persist_json_in_airtable(line)
    #         print(line)

    # table.create({"Name": "Bob"})



# table.create({"Name": "Bob"})
# table.update("recwAcQdqwe21asdf", {"Name": "Robert"})
# table.delete("recwAcQdqwe21asdf")
