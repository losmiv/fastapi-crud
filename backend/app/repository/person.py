from math import ceil
from sqlalchemy import update, delete, or_, text, func, column
from sqlalchemy.sql import select
from config import db, commit_rollback
from models import Person
from schema import PersonCreate, PageResponse


class PersonRepository:

    @staticmethod
    async def create_person(create_form: PersonCreate):
        db.add(Person(
            name=create_form.name,
            sex=create_form.sex,
            birth_date=create_form.birth_date,
            birth_place=create_form.birth_place,
            country=create_form.country
        ))
        await commit_rollback()

    @staticmethod
    async def get_by_id(person_id: int):
        """ retrieve person data by id """
        query = select(Person).where(Person.id == person_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update(person_id: int, update_form: PersonCreate):
        """ update person data """
        query = update(Person) \
            .where(Person.id == person_id) \
            .values(**update_form.dict()) \
            .execution_options(synchronize_session="fetch")

        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(person_id: int):
        """ delete person data by id """
        query = delete(Person).where(Person.id == person_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(
            page: int = 1,
            limit: int = 10,
            columns: str = None,
            sort: str = None,
            filter: str = None
    ):
        query = select(from_obj=Person, columns="*")

        # select columns dynamically
        if columns is not None and columns != "all":
            # we need column format data like this --> [column(id),column(name),column(sex)...]

            query = select(from_obj=Person, columns=convert_columns(columns))

        # select filter dynamically
        # filter_example = "name*John-age*25-city*New York*Los Angeles"
        if filter is not None and filter != "null":

            # convert string to dict format
            # criteria = {'name': 'John', 'age': '25', 'city': 'New York', 'Los Angeles'}
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?

            for attr, value in criteria.items():
                # _attr = Person.name (Person.age, Person.city)
                _attr = getattr(Person, attr)

                # filter format
                # search = '%John%', '%25%', '%New York%', '%Los Angeles%'
                search = "%{}%".format(value)

                # criteria list
                # criteria_list = [Person.name.like('%John%'), Person.age.like('%25%'),
                # Person.city.like('%New York%'), Person.city.like('%Los Angeles%')]
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # select sort dynamically
        if sort is not None and sort != "null":
            # we need sort format data like this --> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # count query
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # pagination
        query = (query.offset(offset_page * limit).limit(limit))

        total_record = (await db.execute(count_query)).scalar() or 0

        total_page = ceil(total_record / limit)

        result = (await db.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )


def convert_sort(sort):
    """
    # separate string using split('-')
    split_sort = sort.split('-')
    # join to list with ','
    new_sort = ','.join(split_sort)
    """
    return ','.join(sort.split('-'))


def convert_columns(columns):
    """
    # seperate string using split ('-')
    new_columns = columns.split('-')

    # add to list with column format
    column_list = []
    for data in new_columns:
        column_list.append(data)

    # we use lambda function to make code simple

    """

    return list(map(lambda x: column(x), columns.split('-')))
