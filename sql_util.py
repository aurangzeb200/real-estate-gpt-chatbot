import pyodbc
import asyncio

async def run_sql(query: str):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=RealEstateDB;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return results

    except Exception as e:
        print("Error running SQL:", e)  
        return "Nothing"
