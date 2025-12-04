from .activities import ActivityShortSchema, CreateActivitySchema
from .analytics import (
    DealsFunnelSchema,
    DealsSummarySchema,
    DealStageConversionSchema,
    DealStageFunnelItemSchema,
    DealStatusSummarySchema,
)
from .auth import LoginSchema, RegisterUserSchema
from .contacts import ContactShortSchema, CreateContactSchema, GetContactsByCriteriaSchema
from .deals import CreateDealSchema, DealShortSchema, GetDealsByCriteriaSchema, UpdateDealSchema
from .organizations import UserOrganizationSchema
from .tasks import CreateTaskSchema, GetTasksByCriteriaSchema, TaskShortSchema
