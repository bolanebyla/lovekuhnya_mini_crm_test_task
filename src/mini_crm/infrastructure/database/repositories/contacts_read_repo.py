from sqlalchemy import or_, select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.dtos.pagination import Page
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto
from mini_crm.application.contacts.interfaces import ContactsReadRepo
from mini_crm.infrastructure.database.tables import contacts_table


class ContactsReadRepoImpl(BaseReadOnlyRepository, ContactsReadRepo):
    async def get_page_by_criteria(
        self,
        criteria: GetContactsByCriteriaDto,
    ) -> Page[ContactShortDto]:
        filters = [
            contacts_table.c.organization_id == criteria.current_user.organization_id,
        ]

        if criteria.owner_id:
            filters.append(contacts_table.c.owner_id == criteria.owner_id)

        if criteria.search:
            search_pattern = f"%{criteria.search}%"
            filters.append(
                or_(
                    contacts_table.c.email.ilike(search_pattern),
                    contacts_table.c.name.ilike(search_pattern),
                )
            )

        base_query = (
            select(
                contacts_table.c.id,
                contacts_table.c.name,
                contacts_table.c.email,
                contacts_table.c.phone,
            )
            .where(*filters)
            .order_by(contacts_table.c.id)
        )

        paginated_query = self.query_builder.add_pagination(
            query=base_query,
            paginated_request=criteria,
        )

        db_items = (await self.session.execute(paginated_query)).mappings().all()

        total = await self.get_total_items(
            query=base_query,
        )
        pages = self.get_pages_count(total=total, page_size=criteria.page_size)

        items = [
            ContactShortDto(
                id=db_item.id,
                name=db_item.name,
                email=db_item.email,
                phone=db_item.phone,
            )
            for db_item in db_items
        ]

        return Page(
            items=items,
            page=criteria.page,
            page_size=criteria.page_size,
            total=total,
            pages=pages,
        )
