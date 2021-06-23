from enum import Enum

age_dict = dict(
    age1=18,
    age2=45,
)

age_group = Enum('age', age_dict)