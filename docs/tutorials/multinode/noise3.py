import cirq, qsimcirq

print(qsimcirq.qsim_gpu)
# Create a Bell state, |00) + |11)
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='m')
)

# Constructs a noise model that adds depolarizing noise after each gate.
noise = cirq.NoiseModel.from_noise_model_like(cirq.depolarize(p=0.05))

# Use the noise model to create a noisy circuit.
noisy_circuit = cirq.Circuit(noise.noisy_moments(circuit, system_qubits=[q0, q1]))
qsim_options = qsimcirq.QSimOptions(
    max_fused_gate_size=3,
    # ev_noisy_repetitions=1000,
    use_gpu=True,
    gpu_sim_threads=256,
    gpu_state_threads=512,
    gpu_data_blocks=16,
    verbosity=0,
    denormals_are_zeros=True,
)
sim = qsimcirq.QSimSimulator(qsim_options=qsim_options)
result = sim.run(noisy_circuit, repetitions=1000)
# Outputs a histogram dict of result:count pairs.
# Expected result is a bunch of 0s and 3s, with fewer 1s and 2s.
# (For comparison, the noiseless circuit will only have 0s and 3s)
print(result.histogram(key='m'))