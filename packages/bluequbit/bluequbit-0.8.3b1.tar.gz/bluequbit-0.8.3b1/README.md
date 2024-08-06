![lint and tests](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/lint_and_tests.yml/badge.svg) ![PyPI release status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/release.yml/badge.svg) ![Deploy docs](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/deploy_docs.yml/badge.svg)

# BlueQubit Python SDK

## Quick Start

1. Register on https://app.bluequbit.io and copy the API token.

2. Install Python SDK from PyPI:
```
    pip install bluequbit
```
3. An example of how to run a Qiskit circuit using the SDK:

```
    import qiskit

    import bluequbit

    bq_client = bluequbit.init("<token>")

    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)

    job_result = bq_client.run(qc_qiskit, job_name="testing_1")

    state_vector = job_result.get_statevector() 
    # returns a NumPy array of [0. +0.j 0. +0.j 0.70710677+0.j 0.70710677+0.j]
```

4. An example of how to run a Pennylane circuit using the SDK:

To use the Pennylane plugin, you must have pennylane~=0.37 version installed. It requires
Python 3.9, but we recommend using Python 3.10 . Make sure your Python version is not older
```
    import pennylane as qml
    from pennylane import numpy as np
    
    dev = qml.device('bluequbit.cpu', wires=1, token="<token>")
    
    @qml.qnode(dev)
    def circuit(angle):
        qml.RY(angle, wires=0)
        return qml.probs(wires=0)
    
    
    probabilities = circuit(np.pi / 4)
    # returns a NumPy array of [0.85355339 0.14644661]
```

The packages is tested extensively on Python 3.10.

## Full reference

Please find detailed reference at https://app.bluequbit.io/sdk-docs.

## Questions and Issues

Please submit questions and issues to info@bluequbit.io.
