from pyairtable import Api
from os import environ
from dotenv import load_dotenv
import pandas as pd

def get_pd_dataframe():
    api = Api(environ["AIRTABLE_API_KEY"])
    table = api.table("appSBKTKW43QcbpRf", "tblYS5wjMHpRd0WNa")
    data = table.all()
    return pd.DataFrame.from_records((r['fields'] for r in data))

if __name__ == "__main__":
    load_dotenv()
    print(get_pd_dataframe())


# table.create({"Name": "Bob"})
# table.update("recwAcQdqwe21asdf", {"Name": "Robert"})
# table.delete("recwAcQdqwe21asdf")
