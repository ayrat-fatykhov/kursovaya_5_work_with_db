import requests


class HeadHunterAPI:
    """Класс для запросов в API HH"""

    def get_response(self, employer_id: int) -> list[dict]:
        """
        Получает вакансии из API HH
        :param employer_id: иденфикационный номер работодателя
        :return: список ваканский
        """
        params: dict = {
            "employer_id": f'{employer_id}'
        }
        response = requests.get("https://api.hh.ru/vacancies", params)
        return response.json()
