from icecream import ic
from pydantic import BaseModel, EmailStr
from datetime import datetime
from my_right_hand.models.enums import (
    RelationshipTypes,
    TaskTypes,
    FrequencyPeriod,
    ThreeTier,
    Critera,
)


class Relation(BaseModel):
    name: str
    type: RelationshipTypes


class Person(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    relationships: list[Relation]


class Task(BaseModel):
    name: str
    type: TaskTypes
    description: str
    deadline: datetime
    frequency: int
    frequency_period: FrequencyPeriod
    urgency: ThreeTier
    importance: ThreeTier


class Assignment(BaseModel):
    task: Task
    criteria: Critera
    source: Person
    target: Person


if __name__ == "__main__":
    person = Person(
        first_name="Bejan",
        last_name="Sadeghian",
        email="bejan.sadeghian@gmail.com",
        phone="123-456-7890",
        relationships=[
            Relation(
                name="Me",
                type="self",
            )
        ],
    )
    task = Task(
        name="name of task",
        description="desc of task",
        type="personal",
        deadline=datetime(2024, 12, 23),
        frequency=1,
        frequency_period="one_time",
        urgency="low",
        importance="low",
    )
    assignment = Assignment(
        task=task,
        source=person,
        target=person,
    )
    ic(assignment)
