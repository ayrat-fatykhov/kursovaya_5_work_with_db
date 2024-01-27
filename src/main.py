import os
from dotenv import load_dotenv

from src.dbmanager import DBManager
from src.hh_api import HeadHunterAPI
from src.utils import hh_reformat_response, print_vacancies

companies: list[dict] = [{"name": "Сбер", "id": 3529},
                         {"name": "Яндекс", "id": 1740},
                         {"name": "Альфа-Банк", "id": 80},
                         {"name": "VK", "id": 15478},
                         {"name": "Тинькофф", "id": 78638},
                         {"name": "Газпром нефть", "id": 39305},
                         {"name": "ВТБ", "id": 4181},
                         {"name": "СИБУР", "id": 3809},
                         {"name": "Tele2", "id": 4219},
                         {"name": "МТС", "id": 3776}]

# Параметры для подключения к БД
load_dotenv()
host: str = os.getenv('HOST')
database: str = os.getenv('DATABASE')
user: str = 'postgres'
password: str = os.getenv('PASSWORD')


def user_interface():
    print('Добро пожаловать!\nПрограмма собирает самые актуальные вакансии. Это может занять некоторое время...')
    db_commands: DBManager = DBManager(host, database, user, password)
    db_commands.deleted_tables()
    db_commands.create_tables()
    db_commands.filled_companies(companies)
    hh_vacancies: HeadHunterAPI = HeadHunterAPI()
    for company in companies:
        company_vacancies = hh_vacancies.get_response(company["id"])
        reform_vacancies: list[dict] = hh_reformat_response(company_vacancies)
        db_commands.filled_vacancies(company["id"], reform_vacancies)

    count_com_and_vac: tuple = db_commands.get_companies_and_vacancies_count()
    print(f'Собраны по {count_com_and_vac[1]} вакансий от {count_com_and_vac[0]} компаний.')
    user_choice: int = 0
    while user_choice != 5:
        user_choice: int = int(input('''\n1. Вывести список всех вакансий
                    \r2. Вывести среднюю зарплату по вакансиям
                    \r3. Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
                    \r4. Вывести список всех вакансий, в названии которых содержатся ключевое слово, например python
                    \r5. Завершить программу
                    \rНаберите соответствующую цифру: '''))
        if user_choice == 1:
            all_vacancies = db_commands.get_all_vacancies()
            print_vacancies(all_vacancies, companies)
        elif user_choice == 2:
            avg_salary = int(db_commands.get_avg_salary())
            print(f'\nСредняя з/п: {avg_salary} рублей')
        elif user_choice == 3:
            choice_vacancies = db_commands.get_vacancies_with_higher_salary()
            print_vacancies(choice_vacancies, companies)
        elif user_choice == 4:
            user_word = input('Введите ключевое слово: ')
            vac_by_word = db_commands.get_vacancies_with_keyword(user_word)
            if vac_by_word:
                print_vacancies(vac_by_word, companies)
            else:
                print("Увы")
    print("\nУдачи при трудоустройстве!")


if __name__ == '__main__':
    user_interface()
