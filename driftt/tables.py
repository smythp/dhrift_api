from piccolo.table import Table
from piccolo.columns import Varchar, Boolean, UUID, Date, ForeignKey, Timestamp, Text
import enum


class DrifttUser(Table):
    # id = UUID()
    first_name = Varchar()
    last_name = Varchar()
    username = Varchar()    
    password = Varchar(secret=True)
    confirmed = Boolean
    email = Varchar()
    last_modified = Timestamp()


class Site(Table):
    display_name = Varchar()
    institution = Varchar()
    admin = ForeignKey(references=DrifttUser)
    domain = Varchar()
    created = Timestamp()
    last_modified = Timestamp()


class ResourceType(str, enum.Enum):
    workshop = 'workshop'
    guide = 'guide'
    insight = 'insight'
    other = 'other'


class Resource(Table):
    title = Varchar()
    author = ForeignKey(references=DrifttUser)
    content = Text()
    type = Varchar(choices=ResourceType)
