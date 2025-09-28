import logging
from domain.unit_of_work import UnitOfWork

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            if exception_type is not None:
                # Произошла ошибка, откатываем транзакцию
                logging.info("An error has occurred. %s", exception_value)
                self.rollback()
            else:
                # Нет ошибок, сохраняем изменения
                self.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

