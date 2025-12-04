from sqlalchemy.orm import registry

from mini_crm.application.activities.entities import Activity
from mini_crm.application.contacts.entities import Contact
from mini_crm.application.deals.entities import Deal
from mini_crm.application.tasks.entities import Task
from mini_crm.infrastructure.database.tables import (
    activities_table,
    contacts_table,
    deals_table,
    tasks_table,
)

mapper = registry()

mapper.map_imperatively(Contact, contacts_table)
mapper.map_imperatively(Deal, deals_table)
mapper.map_imperatively(Task, tasks_table)
mapper.map_imperatively(Activity, activities_table)
