from commons.app_errors import AppError
from commons.app_errors.errors import ForbiddenError


class DealStatusCannotBeWonWithZeroAmount(AppError):
    message_template = (
        'Сделка с id "{id_}" не может иметь статус "won", если сумма сделки равна нулю'
    )
    code = "deals.deal_status_cannot_be_won_with_zero_amount"


class RollingBackDealStageIsProhibited(ForbiddenError):
    message_template = 'Откат стадии назад запрещен для сделки с id "{id_}"'
    code = "deals.rolling_back_deal_stage_is_prohibited"
