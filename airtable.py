from pyairtable import Api
import os

api = Api(os.environ["AIRTABLE_API_KEY"])
table = api.table("appSBKTKW43QcbpRf", "tblYS5wjMHpRd0WNa")
table.all()
# table.create({"Name": "Bob"})
# table.update("recwAcQdqwe21asdf", {"Name": "Robert"})
# table.delete("recwAcQdqwe21asdf")
