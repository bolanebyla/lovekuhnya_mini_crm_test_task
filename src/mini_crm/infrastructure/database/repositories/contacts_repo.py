from commons.db.sqlalchemy import BaseRepository
from commons.entities import EntityId
from mini_crm.application.contacts.entities.contact import Contact
from mini_crm.application.contacts.interfaces import ContactsRepo


class ContactsRepoImpl(BaseRepository, ContactsRepo):
    async def add(self, contact: Contact) -> None:
        self.session.add(contact)
        await self.session.flush()

    async def get_by_id(self, id_: EntityId) -> Contact | None:
        return await self.session.get(Contact, id_)
