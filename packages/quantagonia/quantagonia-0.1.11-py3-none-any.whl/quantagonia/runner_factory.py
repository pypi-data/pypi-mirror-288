from quantagonia.enums import HybridSolverServers, HybridSolverConnectionType
from quantagonia.cloud.cloud_runner import CloudRunner
from quantagonia.runner import Runner
from quantagonia.parameters import HybridSolverParameters


_local_is_there__ = None
try:
    from quantagonia.local.local_runner import LocalRunner
    _local_is_there__ = True
except ModuleNotFoundError:
    _local_is_there__ = False


class RunnerSuppresExitWrapper(Runner):

    def __init__(self, runner):
        self.runner = runner

    def solve(self, problem_file: str, params: HybridSolverParameters = None, **kwargs):
        try:
            return self.runner.solve(problem_file, params, **kwargs)
        except SystemExit as e:
            raise Exception(e)

    def solveBatched(self, problem_files: list, params: list = [], **kwargs):
        try:
            return self.runner.solveBatched(problem_files, params, **kwargs)
        except SystemExit as e:
            raise Exception(e)

    async def solveAsync(self, problem_file: str, params: HybridSolverParameters = None, **kwargs):
        try:
            return self.runner.solve(problem_file, spec, **kwargs)
        except SystemExit as e:
            raise Exception(e)

    async def solveBatchedAsync(self, problem_files: list, params: list = [], **kwargs):
        try:
            return self.runner.solve(problem_files, specs, **kwargs)
        except SystemExit as e:
            raise Exception(e)


class RunnerFactory:
    """
    Creates a Runner instance based on specifications.
    The Runner is used to submit problem instances for solving.
    """

    @classmethod
    def getRunner(
            cls,
            connection : HybridSolverConnectionType,
            api_key : str = None,
            server : HybridSolverServers = HybridSolverServers.PROD,
            suppress_output : bool = False,
            suppress_exitonfailure : bool = False):
        """
        Creates and returns a Runner instance based on the provided connection type and optional parameters.

        Args:
            connection: A HybridSolverConnectionType enum value representing the type of connection to use.
            api_key: A string containing the Quantagonia API key. Default is None.
            server: A HybridSolverServers enum value representing the server to use for cloud connections. Default is HybridSolverServers.PROD.
            suppress_output: A boolean indicating whether to suppress the output when running a job. Default is False.

        Returns:
            A Runner instance based on the provided connection type and optional parameters.

        Raises:
            RuntimeError: If unable to instantiate Quantagonia runner.
    """

        runner = None
        if connection == HybridSolverConnectionType.CLOUD:
            if api_key is None or api_key == "":
                raise RuntimeError("No API key given.")
            runner = CloudRunner(api_key, server, suppress_output)
        elif connection == HybridSolverConnectionType.LOCAL:
            if _local_is_there__:
                runner = LocalRunner(suppress_output)
            else:
                raise RuntimeError("LocalRunner not supported in packaged version!")
        else:
            raise RuntimeError("Unable to instantiate Quantagonia runner.")

        if suppress_exitonfailure:
            return RunnerSuppresExitWrapper(runner)
        else:
            return runner
