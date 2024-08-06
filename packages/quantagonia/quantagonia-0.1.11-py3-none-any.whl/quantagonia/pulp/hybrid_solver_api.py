import sys, os, os.path
from pulp.apis import LpSolver_CMD, subprocess, PulpSolverError, constants
from enum import Enum
import warnings

from quantagonia.runner import Runner
from quantagonia.parameters import HybridSolverParameters
from quantagonia.parser.solution_parser import SolutionParser

class QQVM_CMD(LpSolver_CMD):
    """The QQVM_CMD solver"""

    name = "QQVM_CMD"

    def __init__(
            self,
            runner : Runner = None,
            params : dict = None,
            keepFiles = False,
            obfuscate: bool = True
    ):
        """
        :param dict params: sets parameters and options for Bolt
        :param bool keepFiles: if True, files are saved in the current directory and not deleted after solving
        :param bool obfuscate: if True, constraints and variable names are obfuscated
        """
        self.runner = runner
        self.params = params
        if self.params is None:
            self.params = HybridSolverParameters()
        self.obfuscate = obfuscate
        LpSolver_CMD.__init__(
            self,
            mip=True,
            path="",
            keepFiles=keepFiles,
        )

    def defaultPath(self):
        return self.executableExtension("qqvm")

    def available(self):
        """True if the solver is available"""
        return self.executable(self.path)

    def actualSolve(self, lp):
        """Solve a well formulated lp problem"""

        if not self.runner:
            raise PulpSolverError("QQVM runner not set.")

        varLP = False # When lp files are written, qqvm-bolt loses the ordering of variables. This results in wrong
        # reading of solutions as the assumed ordering is not present. In order to support varLP=True, one would have to
        # reimplement the readsol method.

        if varLP:
            tmpMps, tmpSol, tmpOptions, tmpLog = self.create_tmp_files(
                lp.name, "lp", "sol", "QQVM", "QQVM_log"
            )
        else:
            tmpMps, tmpSol, tmpOptions, tmpLog = self.create_tmp_files(
                lp.name, "mps", "sol", "QQVM", "QQVM_log"
            )

        if not varLP:
            if lp.sense == constants.LpMaximize:
                # we swap the objectives
                # because it does not handle maximization.

                warnings.warn(
                    "QQVM_CMD solving equivalent minimization form."
                )

                lp += -lp.objective

        lp.checkDuplicateVars()
        lp.checkLengthVars(52)

        # flag for renaming in writeMPS() should be {0,1}
        rename = 1
        if not self.obfuscate:
            rename = 0

        rename_map = {}

        if varLP:
            lp.writeLP(filename=tmpMps)  # , mpsSense=constants.LpMinimize)
        else:
            ret_tpl = lp.writeMPS(filename=tmpMps, rename = rename)  # , mpsSense=constants.LpMinimize)
            rename_map = ret_tpl[1]

        if lp.isMIP():
            if not self.mip:
                warnings.warn("QQVM_CMD cannot solve the relaxation of a problem")

        ########################################################################
        # actual solve operation (local or cloud)
        result, _ = self.runner.solve(tmpMps, self.params)
        ########################################################################

        if not varLP:
            if lp.sense == constants.LpMaximize:
                lp += -lp.objective

        # parse solution
        content = result['solver_log'].splitlines()

        sol_status_key = "Solution Status"
        try:
            sol_status = next(l for l in content if sol_status_key in l).split()[3]
        except:
            raise PulpSolverError("Pulp: Error while executing", self.path)

        has_sol_key = "Best solution found"
        has_sol = True if len([l for l in content if has_sol_key in l]) >= 1 else False

        # map HybridSolver Status to pulp status
        if sol_status.lower() == "optimal":  # optimal
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionOptimal,
            )
        elif sol_status.lower() == "time limit reached" and has_sol:  # feasible
            # Following the PuLP convention
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionIntegerFeasible,
            )
        elif sol_status.lower() == "time limit reached" and not has_sol:  # feasible
            # Following the PuLP convention
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionNoSolutionFound,
            )
        elif sol_status.lower() == "infeasible":  # infeasible
            status, status_sol = (
                constants.LpStatusInfeasible,
                constants.LpSolutionNoSolutionFound,
            )
        elif sol_status.lower() == "unbounded":  # unbounded
            status, status_sol = (
                constants.LpStatusUnbounded,
                constants.LpSolutionNoSolutionFound,
            )
        else:
            raise RuntimeError(f"Uncatched solution status: {sol_status}")

        # remap obfuscated variable names to original variable names
        for orig_name, obfuscated_name in rename_map.items():
            result["solution"][orig_name] = result["solution"].pop(obfuscated_name)

        self.delete_tmp_files(tmpMps, tmpSol, tmpOptions, tmpLog)
        lp.assignStatus(status, status_sol)

        if status == constants.LpStatusOptimal:
            lp.assignVarsVals(result["solution"])

        return status
