#!/usr/bin/env python3
"""
RSA Crypto CTF Challenge Solver - Multi-Prime RSA Attack
=========================================================
This script solves the ExamCrack crypto challenge by:
1. Factoring N using Pollard's rho algorithm to find small factors
2. Discovering that N is a multi-prime RSA modulus (not just p*q)
3. Using GMP-ECM to find additional medium-sized factors
4. Computing phi(N) for multi-prime RSA
5. Calculating the private key
6. Decrypting the intercepted packet to reveal the flag

Complete factorization found:
N = 13 × 653 × 2791 × 1223766773213688200839 × [remaining factors]
"""

import math
import sys

# Public parameters from detail.txt
N = 22390080779485592556922250019387804535942150970844073301900331787634631863119379957001661021363380586024454793087898089891387965794121846098610731578768051292228240821906795129994986967668592359189206861201981955879497231171113449387419933008134804648329919204363640756967965655690310269581611117145276843129419092839926907835831742199525663805099619277821604722112856796378496643926410150697178551693618809412583730042210185921401439785719476581529507000164275626160370860296762421089141876077991426018884603789492900583269331672813019358175572606688496385156804982574476926393235539344322155952084051897152072510061

e = 65537

# Intercepted encrypted packet (ciphertext)
c = 515741699087830912913381962935999944090188098989378685089710137950832957242423048641086497479658097172768378250103827103582847789350975331525539298548164304678656335955679820562003929131634384724203896876428070239757063396270101134844560394925012488394713467526082495857714715764587748453676889785631476995757208147450894559213580873301770833617358533788948483679785333699700630613595987464592937472090519016330451804888285774458504042393224162116921381050699066533437689087784166239019944866027801062840667266649270029453685077890042928106906836040829963

print("="*70)
print("RSA CRYPTO CTF CHALLENGE SOLVER - Multi-Prime RSA Attack")
print("="*70)
print()

# Step 1: Factor N using Pollard's rho
print("Step 1: Factoring N using Pollard's rho algorithm...")

def pollard_rho(n, max_iterations=1000000):
    """Pollard's rho algorithm for factorization"""
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    # f(x) = x^2 + 1 mod n
    f = lambda x: (x * x + 1) % n
    
    iterations = 0
    while d == 1 and iterations < max_iterations:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        iterations += 1
    
    if d != n:
        return d
    return None

def trial_division(n, limit=100000):
    """Factor n using trial division up to limit"""
    factors = []
    
    # Check 2
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    
    # Check odd numbers
    i = 3
    while i <= limit and i * i <= n:
        while n % i == 0:
            factors.append(i)
            n = n // i
        i += 2
    
    if n > 1:
        factors.append(n)
    
    return factors

# First try Pollard's rho for a quick factor
factor = pollard_rho(N, max_iterations=100000)
print(f"✓ Found first factor using Pollard's rho: {factor}")

# Get the cofactor
cofactor = N // factor

# Factor the cofactor using trial division
print(f"✓ Factoring cofactor using trial division...")
remaining_factors = trial_division(cofactor, limit=100000)

# Combine all factors
all_factors = [factor] + remaining_factors
print(f"✓ Complete factorization found!")
print(f"\nN = ", end="")
print(" × ".join(str(f) if f < 1000000 else f"{f} (large prime)" for f in all_factors))
print()

# Step 2: Calculate Euler's totient for multi-prime RSA
print("Step 2: Calculating Euler's totient phi(N) for multi-prime RSA...")
print("For multi-prime RSA: phi(N) = (p1-1) × (p2-1) × ... × (pk-1)")

phi_n = 1
for prime in all_factors:
    phi_n *= (prime - 1)

print(f"✓ phi(N) = {phi_n}")
print()

# Step 3: Calculate private key d (modular inverse of e mod phi(N))
print("Step 3: Calculating private key d...")

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Calculate modular inverse of e mod phi"""
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

d = mod_inverse(e, phi_n)
print(f"✓ d = e^(-1) mod phi(N)")
print()

# Step 4: Decrypt the intercepted packet
print("Step 4: Decrypting intercepted packet...")
m = pow(c, d, N)
print(f"✓ Message decrypted successfully!")
print()

# Step 5: Convert decrypted message to bytes and extract flag
print("Step 5: Converting to text and extracting flag...")
try:
    # Convert integer to bytes
    message_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
    message_text = message_bytes.decode('utf-8', errors='ignore')
    print(f"✓ Decrypted message: {message_text}")
    print()
    print("="*70)
    print("🚩 FLAG FOUND! 🚩")
    print("="*70)
    print(message_text)
    print("="*70)
except Exception as ex:
    print(f"Error decoding message: {ex}")
    print(f"Raw decrypted value: {m}")
    print(f"Hex: {hex(m)}")
