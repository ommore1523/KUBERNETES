
from flask_appbuilder.api import BaseApi, expose, request
from . import appbuilder
from .models import db_obj

class ExampleApi(BaseApi):
    route_base = ''
    @expose('/home', methods=['GET'])
    def home(self):
        try:
            db_obj.create_table_if_not_exists()
            records = db_obj.read_db_records()
            host_info = db_obj.get_host_info()
            return self.response(200, message={"data":records,"hosts":host_info})
        except Exception as err:
            print(err)
            return self.response_500(message=str(err))
    
    @expose('/add', methods=['POST'])
    def add(self):
        try:
            db_obj.create_table_if_not_exists()
            value = request.form['value']
            db_obj.add_record(value)
            records = db_obj.read_db_records()
            host_info = db_obj.get_host_info()
            return self.response(200, message={"data":records,"hosts":host_info})
        except Exception as err:
            print(err)
            return self.response_500(message=str(err))

    @expose('/delete',methods=['POST'])
    def delete(self):
        try:
            db_obj.create_table_if_not_exists()
            id = request.form['id']
            db_obj.delete_record(int(id))
            records = db_obj.read_db_records()
            host_info = db_obj.get_host_info()
            return self.response(200, message={"data":records,"hosts":host_info})
        except Exception as err:
            print("\ndskadksa",err)
            return self.response_500( message=err)
        
appbuilder.add_api(ExampleApi)
