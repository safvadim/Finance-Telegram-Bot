import requests


class FamilyFinanceServerConfig:
    limit = 5
    base_url = "http://localhost:8000/"

    # TODO Проверка пользователя и добавление его в базу
    def user_verification(self, user_id: int):
        family_search_query = requests.get(f"{self.base_url}family_users/{user_id}")
        if family_search_query.status_code == 200:
            return True
        else:
            return False

    def wallet_creation(self, user_data: dict):
        request_to_add_user = requests.post(f"{self.base_url}users/", json=user_data)
        return request_to_add_user.raise_for_status()

    def family_wallet_creation(self, family_data: dict):
        request_to_add_family = requests.post(f"{self.base_url}family_users/", json=family_data)
        request_to_add_family.raise_for_status()
        return f"Добро пожаловать в семейный кошелёк!"

    def search_by_token(self, token, family_data):
        search_request = requests.get(f"{self.base_url}user_token/{token}/")
        if search_request.status_code == 200:
            json_data = search_request.json()
            for json_list in json_data['results']:
                user_id = json_list['user_id']
                family_data['family_user_id'] = user_id
            request_to_add_family = requests.post(f"{self.base_url}family_users/", json=family_data)
            return f"Добро пожаловать в семейный кошелёк!"
        else:
            return f"Такой код не существует"

    # TODO Добавление пользователя
    def adding_a_user(self, user_data):
        request_to_add_a_user = requests.post(f"{self.base_url}family_users/", json=user_data)
        if request_to_add_a_user.status_code == 200:
            return f"Пользователь с таким id уже есть в базе!"
        else:
            return f"Пользователь добавлен!"

    # TODO Счёт
    def show_all_family_accounts(self, user_id):
        family_search_query = requests.get(f"{self.base_url}family_users/{user_id}")
        json_data = family_search_query.json()
        family_user = json_data['family_user_id']
        invoice_search_query = requests.get(f"{self.base_url}account/{family_user}/")
        json_data = invoice_search_query.json()
        if not json_data['results']:
            return f"Создайте счёт."
        else:
            list_of_accounts = list()
            for json_list in json_data['results']:
                currency = json_list['currency']
                account_name = json_list['account_name']
                amount_check = json_list['amount_check']
                conclusion = str(f"{account_name}: {amount_check} {currency}")
                list_of_accounts.append(conclusion)
            return '\n'.join(list_of_accounts)

    # TODO Список счетов
    def show_list_of_accounts(self, user_id):
        family_search_query = requests.get(f"{self.base_url}family_users/{user_id}")
        json_data = family_search_query.json()
        family_user = json_data['family_user_id']
        invoice_search_query = requests.get(f"{self.base_url}account/{family_user}/")
        json_data = invoice_search_query.json()
        if not json_data:
            return json_data
        else:
            show_list = list()
            for json_list in json_data['results']:
                account_id = json_list['id']
                account_name = json_list['account_name']
                conclusion = str(f"{account_id}. {account_name}")
                show_list.append(conclusion)
            return show_list

    # TODO Создание счета
    def creating_an_account(self, user_id, user_data: dict):
        family_search_query = requests.get(f"{self.base_url}family_users/{user_id}")
        json_data = family_search_query.json()
        family_user = json_data['family_user_id']
        user_data['user'] = family_user
        invoice_creation_request = requests.post(f"{self.base_url}accounts/", json=user_data)
        invoice_creation_request.close()
        return invoice_creation_request.raise_for_status()

    # TODO Удаление счета
    def account_deletion(self, account_deletion):
        account_deletion_request = requests.delete(f"{self.base_url}/accounts/{account_deletion}/")
        return account_deletion_request.raise_for_status()

    # TODO Лимиты
    def category_amount(self, account_id, category):
        category_query = requests.get(f"{self.base_url}expense_categ/{account_id}/{category}/")
        json_data = category_query.json()
        if not json_data:
            return None
        else:
            category_sum_list = list()
            for json_list in json_data['results']:
                amount_expenses = float(json_list['amount_expenses'])
                category_sum_list.append(amount_expenses)
            sum_result = (sum(category_sum_list))
            sum_result = round(sum_result, 2)
            return sum_result

    # Добавление лимита
    def adding_limits(self, data_user):
        request_to_add_limits = requests.post(f"{self.base_url}category_limits/", json=data_user)
        return request_to_add_limits.raise_for_status()

    def amount_category_limit(self, account_id, name_category):
        category_limit_query = requests.get(f"{self.base_url}limit_categ/{account_id}/{name_category}/")
        json_data = category_limit_query.json()
        if not json_data['results']:
            return None
        else:
            category_sum_limit = list()
            for json_list in json_data['results']:
                amount_limit = float(json_list['amount_limit'])
                category_sum_limit.append(amount_limit)
            sum_result_list = sum(category_sum_limit)
            sum_result_list = round(sum_result_list, 2)
            return sum_result_list

    # TODO Добавление расхода
    def adding_an_expense(self, data_user: dict):
        request_to_add_an_expense = requests.post(f"{self.base_url}expenses/", json=data_user)
        if request_to_add_an_expense.status_code == 400:
            return f"Расход превышает сумму счёта!"
        else:
            return f"Расход добавлен!"

    # TODO Добавление дохода
    def adding_income(self, data_user: dict):
        request_to_add_income = requests.post(f"{self.base_url}incomes/", json=data_user)
        return request_to_add_income.raise_for_status()

    # TODO Список аналитики по расходам
    def cost_analytics(self, account_id):
        flow_request = requests.get(f"{self.base_url}expense/{account_id}/")
        json_data = flow_request.json()
        if not json_data:
            return json_data
        else:
            expenses_list = list()
            for json_list in json_data['results']:
                category = json_list['category']
                title = json_list['title']
                date = '-'.join(json_list['date'].split('-')[::-1])
                amount_expenses = json_list['amount_expenses']
                conclusion = str(f"Категория: {category}\nНаименование: {title}\nЦена: {amount_expenses}\nДата: {date}")
                expenses_list.append(conclusion)
            return '\n\n'.join(expenses_list)

    def cost_pagination(self, account_id, page=0):
        query_params = dict(limit=self.limit, offset=page)
        flow_request = requests.get(f"{self.base_url}expense/{account_id}/", params=query_params)
        flow_request.raise_for_status()
        return flow_request.json()

    # TODO Список аналитики по доходам
    def revenue_analytics(self, account_id):
        income_request = requests.get(f"{self.base_url}income/{account_id}/")
        json_data = income_request.json()
        if not json_data:
            return json_data
        else:
            income_list = list()
            for json_list in json_data['results']:
                source_of_income = json_list['source_of_income']
                amount_income = json_list['amount_income']
                date = '-'.join(json_list['date'].split('-')[::-1])
                conclusion = str(f"Источник дохода: {source_of_income}\nСумма: {amount_income}\nДата: {date}")
                income_list.append(conclusion)
            return '\n\n'.join(income_list)

    def income_pagination(self, account_id, page=0):
        query_params = dict(limit=self.limit, offset=page)
        income_request = requests.get(f"{self.base_url}income/{account_id}/", params=query_params)
        income_request.raise_for_status()
        return income_request.json()

    # Список лимитов
    def list_of_limits(self, account_id):
        list_of_limits = requests.get(f"{self.base_url}limit_account/{account_id}/")
        json_data = list_of_limits.json()
        if not json_data:
            pass
        else:
            category_limit = list()
            for json_list in json_data['results']:
                id = json_list['id']
                name_category = json_list['name_category']
                amount_limit = json_list['amount_limit']
                conclusion = str(f"{id}, {name_category}: {amount_limit}")
                category_limit.append(conclusion)
            return category_limit

    # Удаление лимита
    def limit_deletion(self, limit_deletion):
        limit_deletion_request = requests.delete(f"{self.base_url}/category_limits/{limit_deletion}/")
        return limit_deletion_request.raise_for_status()


family_finance_server = FamilyFinanceServerConfig()
