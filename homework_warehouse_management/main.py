from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    warehouse_service = WarehouseService(product_repo, order_repo)
    with SqlAlchemyUnitOfWork(session) as uow:
        new_product = warehouse_service.create_product(name="test1", quantity=1, price=100)
        uow.commit()
        print(f"create product: {new_product}")

        new_order = warehouse_service.create_order(products=[product_repo.get(1)])
        uow.commit()
        print(f"create order: {new_order}")

        new_order = warehouse_service.create_order(products=product_repo.list()[::2])
        uow.commit()
        print(f"create order: {new_order}")

        print("All orders:", *order_repo.list(), sep="\n")

if __name__ == "__main__":
    main()
