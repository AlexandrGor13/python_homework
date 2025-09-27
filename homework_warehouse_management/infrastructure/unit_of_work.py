from domain.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            if exception_type is not None:
                # Произошла ошибка, откатываем транзакцию
                self.session.rollback()
            else:
                # Нет ошибок, сохраняем изменения
                self.session.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
