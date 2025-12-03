from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.contacts.entities.contact import Contact
from mini_crm.application.contacts.interfaces import ContactsRepo


class ContactsRepoImpl(BaseRepository, ContactsRepo):
    async def add(self, contact: Contact) -> None:
        self.session.add(contact)
        await self.session.flush()
