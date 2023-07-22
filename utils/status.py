from statemachine import StateMachine, State


class StatusControl(StateMachine):
    draft = State(initial=True)
    open = State()
    paid = State(final=True)
    void = State(final=True)
    uncollectible = State()

    add_to_order = draft.to(open)
    receive_payment = (
        uncollectible.to(open) |
        open.to(open, unless="payments_enough")
    )
    complete_order = open.to(paid, validators="order_close_validator")
    cancel_order = (uncollectible.to(void) | draft.to(void) | open.to(void))
    suspend_order = open.to(uncollectible)
    reopen_order = uncollectible.to(open)

    def __init__(self):
        self.order_total = 0
        self.payments = []
        super(StatusControl, self).__init__()

    def before_add_to_order(self, amount):
        self.order_total += amount

    def payments_enough(self, amount):
        return sum(self.payments) + amount >= self.order_total

    def before_receive_payment(self, amount):
        self.payments.append(amount)
        return self.payments

    def order_close_validator(self):
        total_payments = sum(self.payments)
        if total_payments < self.order_total:
            raise ValueError("Amount payed is not enough")

    def on_enter_open(self):
        self.payment_received = False
