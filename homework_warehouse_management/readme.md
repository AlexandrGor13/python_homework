### Чистый склад
В проекте реализована бизнес логика и репозиторий для чистого склада с использованием одного из вариантов DDD и Clean Architecture


#### Тестирование
- Для тестирования используется pytest
- Покрытие расчитывается с помощью pytest-cov и составляет для модуля domain 68%

#### Linter
- Для проверки кода используется pylint
- В файле .pylintrc игнорируются некоторые ошибки

#### Примерное работы
В файле main.py приведен пример добавления сущностей "товар" и "заказ" в репозиторий

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
