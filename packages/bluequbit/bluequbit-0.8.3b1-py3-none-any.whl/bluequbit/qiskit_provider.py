from __future__ import annotations

from typing import TYPE_CHECKING

from qiskit.quantum_info import Statevector
from qiskit.result import Result
from qiskit.result.models import ExperimentResult, ExperimentResultData

import bluequbit

from . import job_metadata_constants

if TYPE_CHECKING:
    from qiskit import QuantumCircuit


class BlueQubitQiskitJob:
    def __init__(self, job_id: str, backend: BlueQubitBackend, jobs):
        super().__init__()
        self.job_id = job_id
        self.backend = backend
        jobs = jobs if isinstance(jobs, list) else [jobs]
        self.jobs = jobs

    def result(self):
        experiment_results: list[ExperimentResult] = []

        for job in self.jobs:
            finished = job
            if self.backend.device != "local":
                finished = self.backend.bq.wait(job.job_id)

            data = ExperimentResultData(
                counts=finished.get_counts(),
                statevector=(
                    Statevector(finished.get_statevector()).data
                    if job.num_qubits <= job_metadata_constants.MAX_QUBITS_WITH_STATEVEC
                    else None
                ),
            )
            experiment_results.append(
                ExperimentResult(
                    shots=job.shots,
                    success=True,
                    status=job.run_status,
                    data=data,
                )
            )
        first_job = self.jobs[0]
        return Result(
            backend_name=f"bluequbit_{first_job.device}",
            backend_version=bluequbit.__version__,
            job_id=first_job.job_id,
            qobj_id=0,
            # TODO this is too restricted
            success=first_job.run_status == "COMPLETED",
            results=experiment_results,
            status=first_job.run_status,
        )


class BlueQubitBackend:
    def __init__(self, bq=None, device="cpu"):
        super().__init__()
        if bq is None:
            bq = bluequbit.init()
        self.bq = bq
        self.device = device

    def run(
        self,
        run_input: QuantumCircuit | list[QuantumCircuit],
    ):
        jobs = self.bq.run(run_input, device=self.device, asynchronous=True)
        return BlueQubitQiskitJob(None, self, jobs)


class BlueQubitProvider:
    """A Qiskit provider for accessing BlueQubit backend.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    """

    def __init__(self, api_token: str | None = None):
        super().__init__()
        self.bq = bluequbit.init(api_token=api_token)

    def get_backend(self, device: str = "cpu"):
        """
        :param device: device for which to run the circuit. Can be one of
                       ``"cpu"`` | ``"gpu"`` | ``"quantum"`` | ``"local"``
        """
        return BlueQubitBackend(bq=self.bq, device=device)
