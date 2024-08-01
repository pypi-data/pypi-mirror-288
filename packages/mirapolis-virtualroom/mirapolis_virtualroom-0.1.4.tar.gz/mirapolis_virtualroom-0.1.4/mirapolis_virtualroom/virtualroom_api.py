from typing import Optional

from .base_api import BaseAPI
from .models import (
    Measure,
    Person,
    Measures,
    Persons,
    Members,
    Member,
    Tutors,
    Tutor
)


class VirtualRoom(BaseAPI):
    def __init__(
            self,
            base_link: str,
            secret_key: str,
            app_id: str
    ):
        super().__init__(
            base_link,
            secret_key,
            app_id
        )

    async def get_persons(
            self,
            limit: int = 200,
            offset: int = 0
    ) -> Optional[Persons]:
        """
        Получение информации о физических лицах
        :rtype: list[Person]
        :param limit: Количество записей (200 максимально)
        :param offset: Сдвиг страницы
        :return: Sequence of Persons and count
        """
        persons = await self._get(
            route="/service/v2/persons",
            params={
                "limit": limit,
                "offset": offset,
            }
        )
        if persons:
            return Persons(
                [Person(**person) for person in persons['data']],
                persons['count']
            )
        else:
            return None

    async def get_person(self, person_id: int) -> Optional[Person]:
        """
        Получение информации о физическом лице
        :rtype: Person
        :param person_id: идентификатор физического лица
        :return: Person
        """
        person = await self._get(
            route=f"/service/v2/persons/{person_id}"
        )
        if person:
            return Person(**person)
        else:
            return None

    async def get_measures(
            self,
            limit: int = 200,
            offset: int = 0
    ) -> Optional[Measures]:
        """
        Получение информации о мероприятиях
        :param limit: Количество записей (200 максимально)
        :param offset: Сдвиг страницы
        :return: Sequence of Measures and count
        """
        measures = await self._get(
            route="/service/v2/measures",
            params={
                "limit": limit,
                "offset": offset,
            }
        )
        if measures:
            return Measures(
                [Measure(**measure) for measure in measures['data']],
                measures['count']
            )
        else:
            return None

    async def get_measure(self, measure_id: int) -> Optional[Measure]:
        """
        Получение информации о мероприятии
        :rtype: Measure
        :param measure_id: идентификатор мероприятия
        :return: Measure
        """
        measure = await self._get(
            route=f"/service/v2/measures/{measure_id}"
        )
        if measure:
            return Measure(**measure)
        else:
            return None

    async def get_members(
            self,
            measure_id: int,
            limit: int = 200,
            offset: int = 0
    ) -> Optional[Members]:
        """
        Получение информации об участниках мероприятия
        :param measure_id: идентификатор мероприятия
        :param limit: Количество записей (200 максимально)
        :param offset: Сдвиг страницы
        :return: Sequence of Members and count
        """
        members = await self._get(
            route=f"/service/v2/measures/{measure_id}/members",
            params={
                "limit": limit,
                "offset": offset,
            }
        )
        if members:
            return Members(
                [Member(**member) for member in members['data']],
                members['count']
            )
        else:
            return None

    async def get_tutors(
            self,
            measure_id: int,
            limit: int = 200,
            offset: int = 0
    ) -> Optional[Tutors]:
        """
        Получение информации о преподавателях мероприятия
        :param measure_id: идентификатор мероприятия
        :param limit: Количество записей (200 максимально)
        :param offset: Сдвиг страницы
        :return: Sequence of tutors and count
        """
        tutors = await self._get(
            route=f"/service/v2/measures/{measure_id}/tutors",
            params={
                "limit": limit,
                "offset": offset,
            }
        )
        if tutors:
            return Tutors(
                [Tutor(**tutor) for tutor in tutors['data']],
                tutors['count']
            )
        else:
            return None

    async def get_measures_info(self):
        measures_info = await self._get(
            route="/service/v2/measures/info"
        )
        return measures_info

    async def create_measure(
            self,
            measure: Measure,
    ) -> Optional[Measure]:
        """
        Добавление мероприятия
        :param measure: объект мероприятия
        :return: созданное мероприятие
        """
        created_measure = await self._post(
            route="/service/v2/measures",
            data=measure.model_dump(exclude_none=True),
        )
        if created_measure:
            return Measure(**created_measure)

    async def add_tutor_to_measure_by_email(
            self,
            measure_id: int,
            tutor_email: str,
            send_notifications: bool = True,
            add_roles_by_default: bool = True,
            enable_search_by_email: bool = True,
    ):
        """
        Добавление преподавателя мероприятия по E-mail
        :param measure_id: идентификатор мероприятия
        :param tutor_email: e-mail преподавателя
        :return: id физического лица
        """
        data = {
            "sendNotifications": send_notifications,
            "addRolesByDefault": add_roles_by_default,
            "enableSearchByEmail": enable_search_by_email,
        }
        tutor = await self._post(
            route=f"/service/v2/measures/{
                measure_id}/tutors/regbyemail/{tutor_email}",
            data=data
        )
        return tutor

    async def add_tutor_to_measure_by_id(
        self,
        measure_id: int,
        person_id: int,
    ) -> Optional[Tutor]:
        """
        Добавление преподавателя мероприятия по id
        :param measure_id: идентификатор мероприятия
        :param person_id: id физического лицапреподавателя
        :return: Tutor
        """
        tutor = await self._post(
            route=f"/service/v2/measures/{
                measure_id}/tutors/{person_id}",
        )
        if tutor:
            return Tutor(**tutor)

    async def delete_measure(self, measure_id: int) -> Optional[bool]:
        """
        Удаление мероприятия
        :param measure_id: идентификатор мероприятия
        :return: True if success
        """
        measure = await self._delete(
            route=f"/service/v2/measures/{measure_id}"
        )
        if measure:
            return True
        else:
            return False
