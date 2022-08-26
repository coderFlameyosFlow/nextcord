class BaseCooldownError(Exception):
    """The base of cooldown errors, mandatory for most cooldowns"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = self.__doc__

    def __str__(self):
        return self.message

class ApplicationOnCooldown(BaseCooldownError):
    """
    This `Application Command` is currently on cooldown.
    Attributes
    ==========
    func: Application
        The `Application Command` which is currently rate-limited
    cooldown: Cooldown
        The :class:`ApplicationCooldown` which applies to the current cooldown
    resets_at: datetime.datetime
        The exact datetime this cooldown resets.
    """

    def __init__(
        self,
        func: Callable,
        cooldown: Cooldown,
        resets_at: datetime.datetime,
    ) -> None:
        self.func: Callable = func
        self.cooldown: Cooldown = cooldown
        self.resets_at: datetime.datetime = resets_at
        super().__init__(
            "This function is being rate-limited. "
            f"Please try again in {self.retry_after} seconds."
        )

    @property
    def retry_after(self) -> float:
        """How many seconds before you can retry the `Application Command`"""
        now = datetime.datetime.now()
        gap: datetime.timedelta = self.resets_at - now
        return gap.seconds
