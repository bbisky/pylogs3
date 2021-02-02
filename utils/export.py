def get_table_order():
    from django.db.models import get_app, get_apps, get_models
    models = get_models()
    tables = []
    for model in models:
        tables.append(model._meta.db_table)
    print ','.join(tables)
    
if __name__=="__main__":
    get_table_order