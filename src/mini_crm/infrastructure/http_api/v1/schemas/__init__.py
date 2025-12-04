from .activities import ActivityShortSchema, CreateActivitySchema
from .analytics import DealsSummarySchema, DealStatusSummarySchema, GetDealsSummaryQuerySchema
from .auth import LoginSchema, RegisterUserSchema
from .contacts import ContactShortSchema, CreateContactSchema, GetContactsByCriteriaSchema
from .deals import CreateDealSchema, UpdateDealSchema
from .organizations import UserOrganizationSchema
from .tasks import CreateTaskSchema, GetTasksByCriteriaSchema, TaskShortSchema
