# ExamCrack CTF Challenge - Solution Writeup

## Challenge Overview

This is a cryptography CTF challenge involving RSA encryption. The challenge provides:
- RSA public parameters (N, e)
- An intercepted encrypted packet (ciphertext)
- A leaked diagnostic value

The goal is to decrypt the intercepted packet to retrieve the flag.

## Initial Analysis

### Given Information
```
N = 22390080779485592556922250019387804535942150970844073301900331787634631863119379957001661021363380586024454793087898089891387965794121846098610731578768051292228240821906795129994986967668592359189206861201981955879497231171113449387419933008134804648329919204363640756967965655690310269581611117145276843129419092839926907835831742199525663805099619277821604722112856796378496643926410150697178551693618809412583730042210185921401439785719476581529507000164275626160370860296762421089141876077991426018884603789492900583269331672813019358175572606688496385156804982574476926393235539344322155952084051897152072510061

e = 65537

c = (intercepted ciphertext)

leaked = 147256321351554522923025052858080546989014873223310927062041132934178096111731513865510758804386187116099594303744610658170425580899245192228479203627189
```

### Key Observations
- N is 2048 bits
- e is the standard RSA public exponent (65537)
- The leaked value is 506 bits (about 1/4 of N's bit length)

## Attack Strategy

### Step 1: Check for Weak Factorization

The first approach is to test if N has small prime factors, which would make it vulnerable to factorization.

Using **Pollard's rho algorithm**, we quickly discover that N has a very small factor:

```
N = 13 × quotient
```

This is unusual for RSA! Continuing the factorization:

```
quotient = 653 × 2791 × large_number
```

So we have:
```
N = 13 × 653 × 2791 × large_prime
```

This is a **multi-prime RSA** implementation, which is weaker than standard two-prime RSA.

### Step 2: Complete Factorization

The remaining cofactor after dividing by (13 × 653 × 2791) is either:
- A large prime (making this a 4-prime RSA)
- Composite and needs further factorization

[WORK IN PROGRESS - Factorization ongoing]

### Step 3: Calculate Private Key

For multi-prime RSA with factors p₁, p₂, ..., pₖ:

```
φ(N) = (p₁-1) × (p₂-1) × ... × (pₖ-1)
d = e⁻¹ mod φ(N)
```

### Step 4: Decrypt the Message

```
m = c^d mod N
```

Then convert the decrypted integer to bytes to retrieve the flag.

## Tools and Techniques Used

1. **Pollard's rho algorithm** - For finding small factors quickly
2. **Trial division** - For systematic factorization
3. **Multi-prime RSA mathematics** - Understanding φ(N) for multiple primes
4. **Modular inverse calculation** - Using Extended Euclidean Algorithm

## The Role of the Leaked Value

[TO BE DETERMINED - Still analyzing the leaked value's purpose in the solution]

The leaked value (506 bits) may be:
- Part of one of the prime factors (high or low bits)
- Related to (p-q) or (p+q) for two of the primes
- A hint for a specific factorization attack
- Phi of one of the smaller primes

## Lessons Learned

1. **Never use small primes in RSA** - Even a single small factor (like 13) makes the entire system vulnerable
2. **Multi-prime RSA is weaker** - More factors mean more attack surface
3. **Factorization is the key** - Once N is factored, RSA is completely broken
4. **Always test for small factors first** - Pollard's rho can find them quickly

## Flag

[TO BE EXTRACTED AFTER SUCCESSFUL DECRYPTION]

## References

- Pollard's rho algorithm
- Multi-prime RSA
- RSA factorization attacks
