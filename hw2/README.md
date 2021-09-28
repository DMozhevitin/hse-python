## Homework 2

### Запустить сервер:

```
uvicorn api:app --reload
```

### Запустить тесты:

```
python3 -m unittest tests.integration.account_service_test tests.unit.account_service_test tests.unit.payment_comission_service_test
```

### Немного пояснений:

В проекте есть некоторые сущности (`User`) и сервисы (`user_service`), испольщующиеся только в API. Они не покрыты тестами и написаны скорее как задел для развития проекта в последующих дз.
