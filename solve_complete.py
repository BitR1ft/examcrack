#!/usr/bin/env python3
"""
Complete RSA CTF Solution with all known factors
Uses subprocess to call GMP-ECM for advanced factorization
"""

import subprocess
import sys
import time

# RSA parameters
N = 22390080779485592556922250019387804535942150970844073301900331787634631863119379957001661021363380586024454793087898089891387965794121846098610731578768051292228240821906795129994986967668592359189206861201981955879497231171113449387419933008134804648329919204363640756967965655690310269581611117145276843129419092839926907835831742199525663805099619277821604722112856796378496643926410150697178551693618809412583730042210185921401439785719476581529507000164275626160370860296762421089141876077991426018884603789492900583269331672813019358175572606688496385156804982574476926393235539344322155952084051897152072510061
e = 65537
c = 515741699087830912913381962935999944090188098989378685089710137950832957242423048641086497479658097172768378250103827103582847789350975331525539298548164304678656335955679820562003929131634384724203896876428070239757063396270101134844560394925012488394713467526082495857714715764587748453676889785631476995757208147450894559213580873301770833617358533788948483679785333699700630613595987464592937472090519016330451804888285774458504042393224162116921381050699066533437689087784166239019944866027801062840667266649270029453685077890042928106906836040829963

# Known factors from Pollard's rho and ECM
known_factors = [
    13,
    653,
    2791,
    1223766773213688200839,  # Found via ECM
]

# Remaining cofactor to factor
cofactor = N
for f in known_factors:
    cofactor = cofactor // f

print(f"Known factors: {known_factors}")
print(f"Remaining cofactor ({len(str(cofactor))} digits): {cofactor}")
print(f"Cofactor bit length: {cofactor.bit_length()}")
print()

# Try to factor the remaining cofactor using ECM
print("Attempting to factor remaining cofactor using GMP-ECM...")
print("(This may take several minutes...)")
print()

try:
    # Run ECM with moderate parameters
    proc = subprocess.Popen(
        ['ecm', '-c', '200', '100000000'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    stdout, _ = proc.communicate(input=str(cofactor), timeout=600)
    
    # Parse output for found factors
    additional_factors = []
    for line in stdout.split('\n'):
        if 'Found prime factor' in line or 'Found probable prime factor' in line:
            parts = line.split(':')
            if len(parts) > 1:
                factor_str = parts[-1].strip()
                try:
                    factor = int(factor_str)
                    additional_factors.append(factor)
                    print(f"✓ Found factor: {factor}")
                except:
                    pass
    
    if additional_factors:
        known_factors.extend(additional_factors)
        # Update cofactor
        for f in additional_factors:
            cofactor = cofactor // f
        print(f"\nRemaining cofactor: {cofactor}")
        
except subprocess.TimeoutExpired:
    print("ECM timed out after 10 minutes")
except FileNotFoundError:
    print("GMP-ECM not found - install with: sudo apt-get install gmp-ecm")
except Exception as e:
    print(f"Error running ECM: {e}")

# Check if factorization is complete
if cofactor == 1:
    print("\n✓✓✓ COMPLETE FACTORIZATION!")
    all_factors = known_factors
elif cofactor > 1:
    print(f"\n⚠ Factorization incomplete - treating remaining {len(str(cofactor))}-digit number as prime")
    all_factors = known_factors + [cofactor]
    
print(f"\nAll factors of N:")
for i, f in enumerate(all_factors):
    if f < 1000000:
        print(f"  {i+1}. {f}")
    else:
        print(f"  {i+1}. {f} ({len(str(f))} digits)")

# Calculate phi(N) for multi-prime RSA
phi = 1
for f in all_factors:
    phi *= (f - 1)

# Calculate private key d
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

gcd_val, x, y = extended_gcd(e, phi)
if gcd_val != 1:
    print(f"\n✗ Error: gcd(e, phi) = {gcd_val} (should be 1)")
    sys.exit(1)

d = x % phi

print(f"\n✓ Private key d calculated")

# Decrypt
print(f"✓ Decrypting message...")
m = pow(c, d, N)
msg_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')

print(f"\n{'='*70}")
print("🚩 DECRYPTED MESSAGE 🚩")
print(f"{'='*70}")

# Try multiple decoding strategies
decoded = False

# Strategy 1: Direct UTF-8 decode
try:
    text = msg_bytes.decode('utf-8')
    if '{' in text or 'flag' in text.lower() or sum(1 for c in text if c.isprintable()) > len(text) * 0.8:
        print(text)
        decoded = True
except:
    pass

# Strategy 2: Skip padding bytes
if not decoded:
    for skip in range(min(50, len(msg_bytes))):
        try:
            text = msg_bytes[skip:].decode('utf-8')
            if '{' in text or (len(text) > 20 and sum(1 for c in text[:50] if c.isprintable()) > 40):
                print(text)
                decoded = True
                break
        except:
            continue

# Strategy 3: Show raw bytes if can't decode
if not decoded:
    print(f"Raw bytes ({len(msg_bytes)} bytes):")
    print(msg_bytes[:200])
    print("\nTrying ASCII/Latin-1:")
    print(msg_bytes.decode('latin-1', errors='ignore'))
    
print(f"{'='*70}")
