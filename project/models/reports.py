from project.db import get_db, load_kv
from datetime import datetime, timedelta

class InventoryReport:
    @staticmethod
    def filter_time_material(days, steps=[]):
        return [
            {'$match':{
                'checkout_time':{
                    '$gt': datetime.now() - timedelta(days=days)
                }
            }},
            {'$group':{
                '_id': '$material_name',
                'count':{ '$sum':1},
                'total': { '$sum': '$cost'}
            }}
        ] + steps
    @staticmethod
    def usage_pie_chart_report(days=1):
        pipeline = InventoryReport.filter_time_material(days, [
            {'$project':{
                '_id':0,
                'name':'$_id',
                'value':'$count'
            }}
        ])
        cursor = get_db().inventory_log.aggregate(pipeline)
        return [doc for doc in cursor]

    @staticmethod
    def expense_pie_chart_report(days=1):
        pipeline =  InventoryReport.filter_time_material(days, [
            {'$project':{
                '_id':0,
                'name':'$_id',
                'value':'$total'
            }}
        ])
        cursor = get_db().inventory_log.aggregate(pipeline)
        return [doc for doc in cursor]

class TabReport:
    @staticmethod
    def customer_pie_chart_report(customer_id):
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
    
    @staticmethod
    def tables_report(days=1):
        pipeline = [
            {'$match':{
                'close_time':{
                    '$gt': datetime.now() - timedelta(days=days)
                }
            }},
            {'$unwind':'$orders'},
            {'$group':{
                '_id':'$table',
                'Y':{'$sum':'$orders.cost'}
            }},
            {'$project':{
                '_id':0,
                'X':'$_id',
                'Y':1
            }}
        ]
        cursor = get_db().tab_log.aggregate(pipeline)
        tables = load_kv('tables')
        data = {doc['X']:doc['Y'] for doc in cursor}
        return [{'X':X, 'Y':(data[X] if X in data else 0)} for X in range(1, tables+1)]

    @staticmethod
    def waiter_report(days=1):
        pipeline = [
            {'$match':{
                'close_time':{
                    '$gt': datetime.now() - timedelta(days=days)
                }
            }},
            {'$unwind':'$orders'},
            {'$group':{
                '_id':{'id':'$waiter.id', 'name':'$waiter.name'},
                'value':{'$sum':'$orders.cost'}
            }},
            {'$project':{
                '_id':0,
                'name':'$_id.name',
                'value':1
            }}
        ]
        cursor = get_db().tab_log.aggregate(pipeline)
        return [doc for doc in cursor]

