import argparse
import os
import pathlib
import psycopg2


def create_db_connection():
    connection = psycopg2.connect(
        database="main",
        user="main",
        password=os.getenv("PGPASSWORD"),
        host=f"{os.getenv('CLOUD_SQL_SOCKET_DIR')}/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}",
        port="",
    )
    return connection


def main() -> int:
    parser = argparse.ArgumentParser(description="This is a new command-line tool")
    parser.add_argument("input_file", help="Path to the input file")
    # args = parser.parse_args()

    # print(f"Input file: {args.input_file}")
    conn = create_db_connection()

    cursor = conn.cursor()
    cursor.execute(
        "select  nspname, proname, pg_get_functiondef(p.oid)   from  pg_proc p, pg_namespace np  where  nspname not like 'pg_%' and np.oid = pronamespace;"
    )
    dump_dir = pathlib.Path(os.getcwd())
    for row in cursor:
        (schema_name, function_name, function_def) = row
        schema_dir = dump_dir / schema_name
        schema_function_dir = schema_dir / "functions"
        schema_function_dir.mkdir(parents=True, exist_ok=True)
        sql_file = schema_function_dir / f"{function_name}.sql"
        sql_file.write_text(function_def)
        print(sql_file)
        print(schema_function_dir)
    return 0
