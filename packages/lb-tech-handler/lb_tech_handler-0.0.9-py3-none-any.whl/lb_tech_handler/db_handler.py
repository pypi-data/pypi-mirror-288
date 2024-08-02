import os
import traceback
from psycopg2 import pool
import psycopg2
import pandas as pd 
import multiprocessing
from lb_tech_handler.common_methods import timed_execution,timeit

from dotenv import load_dotenv

load_dotenv()

CPU_COUNT = os.cpu_count()

LB_DB_HOST_NAME_OR_IP = os.getenv(key='LB_DB_HOST_NAME_OR_IP',default='db.learnbasics.fun')

LB_DB_USER_NAME = os.getenv(key='LB_DB_USER_NAME')

LB_DB_PASSWORD = os.getenv(key='LB_DB_PASSWORD')

LB_DB_PORT = os.getenv(key='LB_DB_PORT',default=7777)

LB_DB_APPLICATION_NAME = os.getenv(key='LB_DB_APPLICATION_NAME',default='LB_DB_UNNAMED_APPLICATION')

LB_DB_DATABASE_NAME = os.getenv(key='LB_DB_DATABASE_NAME',default='lb_db')

LB_DB_MIN_CONN = os.getenv(key='LB_DB_MIN_CONN',default=1)

LB_DB_MAX_CONN = os.getenv(key='LB_DB_MAX_CONN',default=CPU_COUNT)

LB_DB_LOG_FILE_PATH = os.getenv(key='LB_DB_LOG_FILE_PATH',default='db.log') 

db_pool = pool.SimpleConnectionPool(
    minconn = LB_DB_MIN_CONN,
    maxconn = LB_DB_MAX_CONN * 2,
    database = LB_DB_DATABASE_NAME,
    user = LB_DB_USER_NAME,
    password = LB_DB_PASSWORD,
    host = LB_DB_HOST_NAME_OR_IP,
    port = LB_DB_PORT,
    application_name = LB_DB_APPLICATION_NAME
)

def get_dataframe_from_query(query: str,args={}) -> pd.DataFrame:

    """returns the query as pandas dataframe from database
    Args:
    --------
        query (str): query
    
    Returns:
    ---------
        data: pandas dataframe from query
    """
    conn = None

    try:
        conn = db_pool.getconn()
        table = pd.read_sql(query, con=conn, params=args)

    except Exception as e:
        raise

    finally:
        if conn:
            db_pool.putconn(conn)

    return table

def get_dataframe_from_list_of_queries(list_of_queries:list[dict]) -> list[pd.DataFrame]:
    """returns the query as pandas dataframe from database
    Args:
    --------
        query (str): query
    
    Returns:
    ---------
        data: pandas dataframe from query
    """

    try:
        with multiprocessing.Pool(processes=CPU_COUNT) as pool:
            results = pool.starmap(get_dataframe_from_query,[(sub_queries['query'],sub_queries['vars'] ) for sub_queries in list_of_queries])

    except Exception as e:
        raise Exception(e)

  
    return results



def execute_query(query:str,vars={}):

    try:
        conn:psycopg2.extensions.connection = db_pool.getconn()

        cursor = conn.cursor()   
        cursor.execute(query=query,vars=vars)
        conn.commit()
        
        db_pool.putconn(conn=conn)
    except Exception as e:
        db_pool.putconn(conn=conn,close=True)
        raise Exception(e)


def execute_query_and_return_result(query:str,vars={}):
    try:

        conn:psycopg2.extensions.connection = db_pool.getconn()
        
        cursor = conn.cursor()   

        cursor.execute(query=query,vars=vars)

        conn.commit()

        data =  cursor.fetchall()

        db_pool.putconn(conn=conn)

        return data
    except Exception as e:

        db_pool.putconn(conn=conn,close=True)

        raise Exception(e)

def execute_transaction(list_of_queries:list[dict]):

    try:
        conn:psycopg2.extensions.connection = db_pool.getconn()

        cursor = conn.cursor()

        for query in list_of_queries:
            cursor.execute(query=query['query'],vars=query['vars'])
        
        conn.commit()
        
        
        db_pool.putconn(conn=conn)

    except Exception as e:
        conn.rollback()

        db_pool.putconn(conn=conn,close=True)  
        
        raise Exception(e)

def execute_transaction_with_multiprocessing(list_of_queries:list[dict],MAX_PROCESS:int=CPU_COUNT) -> bool:
    sub_queries_list = []

    for i in range(0,len(list_of_queries),MAX_PROCESS):
        sub_queries_list.append(list_of_queries[i:i+MAX_PROCESS])

    with multiprocessing.Pool(processes=MAX_PROCESS) as pool:
        pool.starmap(execute_transaction,[(sub_queries, ) for sub_queries in sub_queries_list])

    return True

    
def get_connection_from_pool():
    return db_pool.getconn()

def put_connection_in_pool(conn):
    db_pool.putconn(conn=conn)

def is_free_connection_in_pool() -> bool:

    return LB_DB_MAX_CONN - len(db_pool._used) > 0

@timed_execution
def test_excution_multi_query(list_of_queries:list[dict]):
    for query in list_of_queries:
        execute_query(query=query['query'],vars=query['vars'])

if __name__ == "__main__":

    list_of_queries = []

    start_time = timeit.default_timer()


    for section_id in range(98,249):

        query = f"select * from school_data.student_detail where section_id = {section_id};"

        list_of_queries.append({
            'query':query,
            'vars':{}
        })
        # df = get_dataframe_from_query(query=query)


        # print(df)
    
    results = get_dataframe_from_list_of_queries(list_of_queries=list_of_queries)

    for each_df in results:
        print(each_df)

    end_time = timeit.default_timer()
    
    execution_time = end_time - start_time
    
    print(f"Execution time for {execution_time} seconds")

    print(type(results))