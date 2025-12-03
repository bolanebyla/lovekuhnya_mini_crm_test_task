from commons.app_errors import AppError


class OrganizationMemberNotFoundByOrganizationIdAndUserId(AppError):
    message_template = (
        'Участник организации не найден по id организации "{organization_id}" '
        'и id пользователя "{user_id}"'
    )
    code = "organizations.organization_member_not_found_by_organization_id_and_user_id"
