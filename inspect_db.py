import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoviewer.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    query = """
        SELECT lin_eros, lin_cons, lin_aprv, lin_infr, lin_rsgo, lin_mrco
        FROM datos.meta2
        WHERE cod_trm = %s
    """
    cursor.execute(query, ['QR-I-a-01'])
    row = cursor.fetchone()
    print("QueryResult from datos.meta2:")
    if row:
        titles = [
            "lin_eros",
            "lin_cons",
            "lin_aprv",
            "lin_infr",
            "lin_rsgo",
            "lin_mrco"
        ]
        for t, val in zip(titles, row):
            print(f"  {t}: {repr(val)[:60]}")
    else:
        print("No row found!")



