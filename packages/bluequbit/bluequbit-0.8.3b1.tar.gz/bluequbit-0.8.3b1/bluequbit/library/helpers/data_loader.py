# Copyright 2023 Bluequbit Inc.
#
# All Rights Reserved
#
# NOTICE: All information contained herein is, and remains the property of Bluequbit Inc.
# and its suppliers, if any. The intellectual and technical concepts contained herein are
# proprietary to Bluequbit Inc. and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden unless
# prior written permission is obtained from Bluequbit Inc.
#
# This file is part of a proprietary software product and is not to be copied, modified,
# redistributed, or used in any way without the express written permission of Bluequbit Inc.


import pennylane as qml
from pennylane import numpy as np
from pennylane_lightning.lightning_gpu.lightning_gpu import _gpu_dtype
from tqdm.notebook import trange

complex_dtype = np.complex64
real_dtype = np.float32


class AdamOptim:
    def __init__(self, eta=0.03, beta1=0.9, beta2=0.999, epsilon=1e-8):
        super().__init__()
        self.m, self.v = 0, 0
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.eta = eta
        self.t = 1

    def step(self, grad):
        ## dw, db are from current minibatch
        ## momentum beta 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        ## rms beta 2
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad**2)
        ## bias correction
        m_corr = self.m / (1 - self.beta1**self.t)
        v_corr = self.v / (1 - self.beta2**self.t)
        self.t += 1
        ## update weights and biases
        return self.eta * (m_corr / (np.sqrt(v_corr) + self.epsilon))


def _get_circuit_info(circuit):
    # todo: assert circuit is qnode
    params_dummy = np.zeros(1000000, requires_grad=True)
    specs = qml.specs(circuit)(params_dummy)
    num_params = specs[
        "num_trainable_params"
    ]  # one way to get number of params from a circuit
    num_wires = specs["resources"].num_wires
    return num_wires, num_params


def load_data(
    target_probs: np.ndarray,
    circuit: qml.QNode,
    seed: int = 0,
    loss_type: str = "kl-divergence",  # noqa: ARG001
    num_epochs: int = 1000,
    params_init=None,
    eta=0.03,
) -> dict:
    r"""Run QCBM training to find an approximation to the target_distribution"""
    num_wires, num_params = _get_circuit_info(circuit)

    def adjoint_kl(params):
        dev_bra = qml.device("lightning.gpu", wires=num_wires, c_dtype=complex_dtype)
        dev_ket = qml.device("lightning.gpu", wires=num_wires, c_dtype=complex_dtype)
        dev_gpu = qml.device("lightning.gpu", wires=num_wires, c_dtype=complex_dtype)
        # tic = time.time()
        ket = circuit(params)
        ops = circuit.qtape.operations
        loss = np.sum(target_probs * np.log(target_probs / (np.abs(ket) ** 2)))
        # print("circuit_eval", time.time() - tic)
        bra = target_probs / ket.conj()
        bra_norm = np.linalg.norm(bra)
        bra /= bra_norm
        dev_bra.syncH2D(bra)
        # This line is important to convert NumPy array to PL tensor, so that
        # syncH2D is fast.
        ket = np.asarray(ket)
        dev_ket.syncH2D(ket)
        grads = []
        for op in reversed(ops):
            adj_op = qml.adjoint(op)
            dev_ket.apply([adj_op])
            if op.num_params != 0:
                du = qml.operation.operation_derivative(op)
                # Is this necessary for performance? It may change the result
                # du.requires_grad = False
                _qu = qml.QubitUnitary(du, op.wires)
                use_async = False
                dev_gpu._gpu_state.DeviceToDevice(  # noqa: SLF001
                    dev_ket._gpu_state,  # noqa: SLF001
                    use_async,
                )
                dev_gpu.apply([_qu])
                dm = (
                    -2
                    * bra_norm
                    * dev_gpu._gpu_state.dotWithBraReal(  # noqa: SLF001
                        dev_bra._gpu_state  # noqa: SLF001
                    )
                )
                # A more reliable way to reset _gpu_state
                # TODO raise a bug report to Pennylane
                dev_gpu._gpu_state = _gpu_dtype(complex_dtype)(  # noqa: SLF001
                    dev_gpu._num_local_wires  # noqa: SLF001
                )
                grads.append(dm)
            dev_bra.apply([adj_op])
        return grads[::-1], loss, ket

    np.random.seed(seed)
    best_x, best_loss = None, np.inf
    eps = 0.02
    if params_init is None:
        x = np.random.rand(num_params, requires_grad=True).astype(real_dtype)
    else:
        x = eps * np.random.rand(num_params, requires_grad=True).astype(real_dtype)
        x[: len(params_init)] = params_init

    print(f"starting training with qubits: {num_wires} params: {num_params}")
    print(qml.specs(circuit)(x)["resources"])
    #     print(qml.draw(circuit_gpu)(x))
    opt = AdamOptim(eta=eta)
    for epoch in trange(num_epochs):
        grad, loss, pred_state = adjoint_kl(x)
        grad = np.array(grad).astype(real_dtype)
        if loss < best_loss:
            best_loss = loss
            if best_loss < 5:
                l1_loss = np.sum(np.abs(target_probs - np.abs(pred_state) ** 2))
                print(f"NEW* best_loss: {best_loss}: L1_loss: {l1_loss}")
            best_x = x.copy()
        x -= opt.step(grad)
        print(f"epoch: {epoch} \t loss: {loss}", flush=True)
    return best_x, best_loss
