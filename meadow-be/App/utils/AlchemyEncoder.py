import decimal

from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import datetime

# 自定义JSON编码器函数
# def datetime_encoder(obj):
#     if isinstance(obj, datetime):
#         print("--obj time:",obj)
#         return obj.strftime("%Y-%m-%d%H:%M:%S")
#         #return obj.isoformat()
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if field == "query" or field =="query_class" or field =="registry":
                    continue
                if isinstance(data, datetime):
                    data = data.strftime("%Y-%m-%d %H:%M:%S")
                # if isinstance(data, datetime.date):
                #     data = str(data)
                if isinstance(data, decimal.Decimal):
                    # result = round(data, 2)
                    # data = str(data)
                    data = "{:.2f}".format(data)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    #json.dumps(data,cls=MyJsonEncoder)
                    #print("field:",field,"--obj data:", data)
                    fields[field] = data
                except TypeError:
                    # print("---error--field:",field,"data:",data,"type:",type(data))
                    # fields[field] = None
                    fields[field] = str(data)
                    # data = str(data)
            # a json-encodable dict
            return fields
