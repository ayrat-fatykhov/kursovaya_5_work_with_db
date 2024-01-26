import psycopg2


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.host: str = host
        self.database: str = database
        self.user: str = user
        self.password: str = password

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM companies")
                counter_companies: tuple = cur.fetchone()
                cur.execute("SELECT COUNT(id_vacancy) FROM vacancies GROUP BY id_company")
                counter_vacancies: tuple = cur.fetchone()
        conn.close()
        return counter_companies[0], counter_vacancies[0]

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancies")
                all_vacancies: tuple = cur.fetchall()
        conn.close()
        return all_vacancies

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) FROM vacancies")
                avg_salary: tuple = cur.fetchone()
        conn.close()
        return avg_salary[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) FROM vacancies")
                avg_salary: tuple = cur.fetchone()
                cur.execute(f"SELECT * FROM vacancies WHERE salary_from > {avg_salary[0]}")
                part_vacancies: tuple = cur.fetchall()
        conn.close()
        return part_vacancies

    def get_vacancies_with_keyword(self, user_word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :return:
        """
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancies")
                vacancies: tuple = cur.fetchall()
        conn.close()
        filtered_vacancies: list = []
        for vacancy in vacancies:
            if user_word in vacancy[2]:
                filtered_vacancies.append(vacancy)
                return filtered_vacancies

    def create_tables(self):
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE companies (id_company int PRIMARY KEY, name varchar(255) NOT NULL)")
                cur.execute("""CREATE TABLE vacancies (
                id_vacancy int PRIMARY KEY,
                id_company int REFERENCES companies(id_company) NOT NULL, 
                name varchar(255) NOT NULL, 
                salary_from int, 
                salary_to int, 
                url varchar(100) NOT NULL, 
                description text)""")
        conn.close()

    def filled_companies(self, companies):
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                for company in companies:
                    cur.execute("INSERT INTO companies VALUES (%s, %s)", (company["id"], company["name"]))
        conn.close()

    def filled_vacancies(self, id_company, vacancies):
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)", (
                        vacancy["id"],
                        id_company,
                        vacancy["name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["url"],
                        vacancy["snippet"]))
        conn.close()

    def deleted_tables(self):
        with psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE vacancies")
                cur.execute("DROP TABLE companies")
        conn.close()
