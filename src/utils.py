def hh_reformat_response(vacancies) -> list[dict]:
    """
    Переформатирует вакансии с API HH
    :param vacancies: вакансии с API HH
    :return: переформатированные вакансии с API HH
    """
    reformat_vacancies: list = []
    for vacancy in vacancies['items']:
        vacancy_dict: dict = {}
        vacancy_dict['id']: int = vacancy['id']
        vacancy_dict['name']: str = vacancy['name'].lower()
        if vacancy['salary']:
            if vacancy['salary']['from']:
                vacancy_dict['salary_from'] = vacancy['salary']['from']
            else:
                vacancy_dict['salary_from'] = 0
            if vacancy['salary']['to']:
                vacancy_dict['salary_to'] = vacancy['salary']['to']
            else:
                vacancy_dict['salary_to'] = 0
        else:
            vacancy_dict['salary_from'] = 0
            vacancy_dict['salary_to'] = 0
        vacancy_dict['url'] = vacancy['alternate_url']
        if vacancy['snippet']['requirement']:
            vacancy_dict['snippet'] = vacancy['snippet']['requirement'].lower()
        else:
            vacancy_dict['snippet'] = " "
        reformat_vacancies.append(vacancy_dict)
    return reformat_vacancies


def print_vacancies(vacancies, companies):
    for vacancy in vacancies:
        for company in companies:
            if vacancy[1] == company["id"]:
                print(f'''\n{company["name"]}
                          \r{vacancy[2]}
                          \rЗ/п от {vacancy[3]} до {vacancy[4]} рублей
                          \rСсылка {vacancy[5]}''')
