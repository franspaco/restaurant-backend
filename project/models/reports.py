from project.db import get_db
from datetime import datetime, timedelta

class InventoryReport:
    @staticmethod
    def pie_chart_report(days=1):
        pipeline = [
            {'$match':{
                'checkout_time':{
                    '$gt': datetime.now() - timedelta(days=days)
                }
            }},
            {'$group':{
                '_id': '$material_name',
                'count':{ '$sum':1},
                'total': { '$sum': '$cost'}
            }},
            {'$project':{
                '_id':0,
                'name':'$_id',
                'count':1,
                'total':1
            }}
        ]
        cursor = get_db().inventory_log.aggregate(pipeline)
        return [doc for doc in cursor]

class TabReport:
    @staticmethod
    def client_pie_chart_report(customer_id):
        pipeline = [
            {'$match':{
                'customers.id':customer_id
            }},
            {'$unwind':'$orders'},
            {'$group':{
                '_id':'$orders.category',
                'value':{ '$sum': 1}
            }},
            {'$project':{
                '_id':0,
                'name':'$_id',
                'value':1
            }}
        ]
        cursor = get_db().tab_log.aggregate(pipeline)
        return [doc for doc in cursor]

