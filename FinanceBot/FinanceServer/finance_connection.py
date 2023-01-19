import requests


class FinanceServerConfig:
    limit = 5
    base_url = "http://localhost:8000/"
    list_of_accounts = list()
    show_list = list()
    income_list = list()
    expenses_list = list()
    category_sum_list = list()
    category_sum_limit = list()
    category_limit = list()

    # TODO Проверка пользователя и добавление его в базу
    def user_verification(self, user_id: int, user_data: dict):
        user_search_query = requests.get(f"{self.base_url}users/{user_id}/")
        if user_search_query.status_code == 200:
            return FinanceServerConfig()
        else:
            request_to_add_user = requests.post(f"{self.base_url}users/", json=user_data)
            return request_to_add_user.raise_for_status()

    # TODO Создание счета
    def creating_an_account(self, user_data: dict):
        invoice_creation_request = requests.post(f"{self.base_url}accounts/", json=user_data)
        invoice_creation_request.close()
        return invoice_creation_request.raise_for_status()

    # TODO Удаление счета
    def account_deletion(self, account_deletion):
        account_deletion_request = requests.delete(f"{self.base_url}/accounts/{account_deletion}/")
        return account_deletion_request.raise_for_status()

    # TODO Вывод счета/баланса
    def show_all_accounts(self, user_id):
        self.list_of_accounts.clear()
        invoice_search_query = requests.get(f"{self.base_url}account/{user_id}/")
        json_data = invoice_search_query.json()
        if not json_data['results']:
            return f"Создайте счёт."
        else:
            for json_list in json_data['results']:
                currency = json_list['currency']
                account_name = json_list['account_name']
                amount_check = json_list['amount_check']
                conclusion = str(f"{account_name}: {amount_check} {currency}")
                self.list_of_accounts.append(conclusion)
            return '\n'.join(self.list_of_accounts)

    # TODO Список счетов
    def show_list_of_accounts(self, user_id):
        self.show_list.clear()
        invoice_search_query = requests.get(f"{self.base_url}account/{user_id}/")
        json_data = invoice_search_query.json()
        if not json_data:
            return self.show_list.clear()
        else:
            for json_list in json_data['results']:
                account_id = json_list['id']
                account_name = json_list['account_name']
                conclusion = str(f"{account_id}. {account_name}")
                self.show_list.append(conclusion)
            return self.show_list

    # TODO Добавление дохода
    def adding_income(self, data_user: dict):
        request_to_add_income = requests.post(f"{self.base_url}incomes/", json=data_user)
        return request_to_add_income.raise_for_status()

    # TODO Добавление расхода
    def adding_an_expense(self, data_user: dict):
        request_to_add_an_expense = requests.post(f"{self.base_url}expenses/", json=data_user)
        if request_to_add_an_expense.status_code == 400:
            return f"Расход превышает сумму счёта!"
        else:
            return f"Расход добавлен!"

    # TODO Список аналитики по доходам
    def revenue_analytics(self, account_id):
        self.income_list.clear()
        income_request = requests.get(f"{self.base_url}income/{account_id}/")
        json_data = income_request.json()
        if not json_data:
            return self.income_list.clear()
        else:
            for json_list in json_data['results']:
                source_of_income = json_list['source_of_income']
                amount_income = json_list['amount_income']
                date = '-'.join(json_list['date'].split('-')[::-1])
                conclusion = str(f"Источник дохода: {source_of_income}\nСумма: {amount_income}\nДата: {date}")
                self.income_list.append(conclusion)
            return '\n\n'.join(self.income_list)

    def income_pagination(self, account_id, page=0):
        query_params = dict(limit=self.limit, offset=page)
        income_request = requests.get(f"{self.base_url}income/{account_id}/", params=query_params)
        income_request.raise_for_status()
        return income_request.json()

    # TODO Список аналитики по расходам
    def cost_analytics(self, account_id):
        self.expenses_list.clear()
        flow_request = requests.get(f"{self.base_url}expense/{account_id}/")
        json_data = flow_request.json()
        if not json_data:
            return self.expenses_list.clear()
        else:
            for json_list in json_data['results']:
                category = json_list['category']
                title = json_list['title']
                date = '-'.join(json_list['date'].split('-')[::-1])
                amount_expenses = json_list['amount_expenses']
                conclusion = str(f"Категория: {category}\nНаименование: {title}\nЦена: {amount_expenses}\nДата: {date}")
                self.expenses_list.append(conclusion)
            return '\n\n'.join(self.expenses_list)

    def cost_pagination(self, account_id, page=0):
        query_params = dict(limit=self.limit, offset=page)
        flow_request = requests.get(f"{self.base_url}expense/{account_id}/", params=query_params)
        flow_request.raise_for_status()
        return flow_request.json()

    # TODO Лимиты
    def category_amount(self, account_id, category):
        self.category_sum_list.clear()
        category_query = requests.get(f"{self.base_url}expense_categ/{account_id}/{category}/")
        json_data = category_query.json()
        if not json_data:
            return 0
        for json_list in json_data['results']:
            amount_expenses = float(json_list['amount_expenses'])
            self.category_sum_list.append(amount_expenses)
        sum_result = (sum(self.category_sum_list))
        sum_result = round(sum_result, 2)
        return sum_result

    # Добавление лимита
    def adding_limits(self, data_user):
        request_to_add_limits = requests.post(f"{self.base_url}category_limits/", json=data_user)
        return request_to_add_limits.raise_for_status()

    def amount_category_limit(self, account_id, name_category):
        self.category_sum_limit.clear()
        category_limit_query = requests.get(f"{self.base_url}limit_categ/{account_id}/{name_category}/")
        json_data = category_limit_query.json()
        if not json_data['results']:
            return self.category_sum_limit.clear()
        for json_list in json_data['results']:
            amount_limit = float(json_list['amount_limit'])
            self.category_sum_limit.append(amount_limit)
        sum_result_list = sum(self.category_sum_limit)
        sum_result_list = round(sum_result_list, 2)
        return sum_result_list

    # Список лимитов
    def list_of_limits(self, account_id):
        self.category_limit.clear()
        list_of_limits = requests.get(f"{self.base_url}limit_account/{account_id}/")
        json_data = list_of_limits.json()
        if not json_data:
            pass
        for json_list in json_data['results']:
            id = json_list['id']
            name_category = json_list['name_category']
            amount_limit = json_list['amount_limit']
            conclusion = str(f"{id}, {name_category}: {amount_limit}")
            self.category_limit.append(conclusion)
        return self.category_limit

    # Удаление лимита
    def limit_deletion(self, limit_deletion):
        limit_deletion_request = requests.delete(f"{self.base_url}/category_limits/{limit_deletion}/")
        self.category_limit.clear()
        self.category_sum_limit.clear()
        return limit_deletion_request.raise_for_status()






finance_server = FinanceServerConfig()
