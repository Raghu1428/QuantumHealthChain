
from qiskit import QuantumCircuit, Aer, transpile, assemble
from numpy.random import randint
import numpy as np

np.random.seed(seed=0)
n = 100

def sample_bits(bits, selection):
    sample = []
    for i in selection:
        # use np.mod to make sure the
        # bit we sample is always in 
        # the list range
        i = np.mod(i, len(bits))
        # pop(i) removes the element of the
        # list at index 'i'
        sample.append(bits.pop(i))
    return sample
#function to validate key
def checkKey(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits

#function to check key for authentication by measuring each bit in the key
def measureKey(message, bases):
    backend = Aer.get_backend('aer_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0: # measuring in Z-basis
            message[q].measure(0,0)
        if bases[q] == 1: # measuring in X-basis
            message[q].h(0)
            message[q].measure(0,0)
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements

#generate quantum latice authentication key
def generateKey(bits, bases):
    key = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass 
            else:
                qc.x(0)
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        key.append(qc)
    return key

def getUserID(name):
    uid = np.zeros(100)
    for i in range(len(name)):
        uid[i] = 1
    return np.asarray(uid)

#comparing exchnage keys between two users for authentication
def exchangeKeys(user1, user2):
    alice_bits = getUserID(user1)
    alice_bases =  np.zeros(100)
    auth_key = generateKey(alice_bits, alice_bases)
    bob_bases = getUserID(user2)
    auth_key = measureKey(auth_key, bob_bases)
    alice_key = checkKey(alice_bases, bob_bases, alice_bits)
    bob_key = checkKey(alice_bases, bob_bases, auth_key)
    return alice_key == bob_key




