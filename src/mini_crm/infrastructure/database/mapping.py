from sqlalchemy.orm import registry

from mini_crm.application.contacts.entities import Contact
from mini_crm.infrastructure.database.tables import contacts_table

mapper = registry()

mapper.map_imperatively(Contact, contacts_table)
