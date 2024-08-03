from cdswjoblauncher.contract import CdswApp
from cdswjoblauncher.core.context import CdswLauncherContext
from cdswjoblauncher.core.error import CdswLauncherException
from cdswjoblauncher.core.module import ModuleUtils, ClassResolver


class MainCommandHandler:
    def __init__(self, ctx: CdswLauncherContext):
        self.ctx = ctx
        self.executor = None
        self._cluster = None

        if not self.ctx:
            raise CdswLauncherException("No context is received")

    def initial_setup(self, package_name):
        module_name = package_name.replace("-", "")
        ModuleUtils.import_or_install(module_name, package_name)
        resolver = ClassResolver(module_name, CdswApp)
        app = resolver.resolve()



