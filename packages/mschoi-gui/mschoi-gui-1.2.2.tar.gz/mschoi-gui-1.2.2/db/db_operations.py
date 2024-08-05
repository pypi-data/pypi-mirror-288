
import pandas as pd
from .db_connect import make_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List


# select문 실행
def select_to_dataframe(db_name:str, query:str, params=None):
    '''
    select문 실행 결과를 데이터 프레임으로
    '''
    engine = make_engine(db_name)

    with engine.connect() as connection:
        if params:
            result = connection.execute(text(query), params)
        else:
            result = connection.execute(text(query))

        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df



# 저장 프로시져를 실행만 시키기
def execute_procedure(db_name:str, query:str, params ):
    '''
    저장 프로시져 실행
    '''
    engine = make_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result= session.execute(text(query), params)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
    finally:
        session.close()
    return result


# 프로시져 실행 결과값을 반환
def procedure_to_dataframe(db_name:str, query:str, params ):
    '''
    프로시져 실행 결과 데이터 프레임으로 가져옴
    '''

    engine = make_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    result_proxy = session.execute(text(query), params)
    result_set = result_proxy.fetchall()

    df = pd.DataFrame(result_set,  columns=result_proxy.keys() )
    session.commit()

    return df



# update, delete, truncate 수행
def execute_to_commit(db_name:str, query:str):
    """update, delete, truncate 수행"""
    engine = make_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.execute(text(query))
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()

    finally:
        session.close()
    return 


# insert문을 반복적으로 수행
def execute_insert_queries(db_name:str, insert_queries: List[str]) -> None:
    '''
    insert문을 리스트로 받아와 반복해서 수행
    '''
    engine = make_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        for query in insert_queries:
            session.execute(query)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()

    finally:
        session.close()



