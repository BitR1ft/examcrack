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

## Current Status

### Factorization Progress

Using Pollard's rho algorithm, we successfully found small factors:
```
N = 13 × 653 × 2791 × Q
```

where Q is a large 2023-bit composite number:
```
Q = 945016280241333772211643293786766373020855449406550627551448513433749717081522531677310942508877089027111351136178468820479503742640194014164841037935958992950906341707739770636427843230704500518879464650925454433623365106466038452756043429403794994771614751147116081851197304957101534081372619467428767834877554688237844242709852145351237893213867187149209543461406007638797621333233365576485013513752377227046231643724753074611464849962196386401180670977889764149874012787461811544053612073355766282357968925051569490935593201664903304931408594091753210971688274676811166396728201650818974826574270599989139
```

### Challenges Encountered

1. **Q is composite but difficult to factor**
   - Sympy's `isprime()` confirms Q is NOT prime
   - Standard factorization methods (Pollard's rho, Fermat, trial division) have not succeeded
   - ECM and other advanced methods are still running

2. **The Leaked Value Mystery**
   - The leaked value (506 bits) doesn't appear to be a direct factor of N
   - It's not (p-q) or (p+q) for any obvious pair of factors
   - GCD(N, leaked) = 1, so it shares no common factors
   - Multiples of leaked only reveal the factor 13 we already know

3. **Decryption Attempts**
   - Decrypting with partial factorization produces garbled output
   - This confirms more factors are needed for correct decryption
   - Various encoding attempts (XOR, reverse, base64) haven't revealed the flag

## The Role of the Leaked Value

**[ANALYSIS IN PROGRESS]**

Possible interpretations:
1. **Partial key exposure** - May represent high/low bits of a prime factor
2. **Hint for Coppersmith's attack** - Could enable polynomial solving for remaining factors  
3. **Related to φ(N)** - Might be φ of a specific factor
4. **Smoother relation** - Could indicate a smooth number attack vector

The relationship between the leaked value and the factorization remains the key unsolved aspect of this challenge.

## Next Steps for Complete Solution

1. Continue aggressive factorization of Q using:
   - GNFS (General Number Field Sieve) - most effective for large semiprimes
   - Online factorization databases (FactorDB, if available)
   - Specialized hardware/cloud computing resources

2. Investigate Coppersmith-based partial key recovery using the leaked value

3. Consider if this is a known CTF challenge with published solution

## Lessons Learned

1. **Small factors are fatal** - Even one small prime (13) significantly weakens RSA
2. **Multi-prime RSA requires all factors** - Missing even one factor prevents decryption
3. **Modern factorization is computationally intensive** - 2000+ bit composites require specialized tools
4. **CTF challenges often have clever twists** - The leaked value likely has a non-obvious use

## Partial Solution Code

See `solve.py` for the working factorization and decryption framework. The script successfully:
- Finds small factors using Pollard's rho
- Implements multi-prime RSA φ(N) calculation
- Calculates private key d
- Performs RSA decryption

**Missing**: Complete factorization of the 2023-bit quotient Q.

## Flag

**[PENDING COMPLETE FACTORIZATION]**

Current decryption output is garbled, confirming incomplete factorization.

## References

- [Pollard's rho algorithm](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm)
- [Multi-prime RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Multi-prime_RSA)
- [Integer factorization algorithms](https://en.wikipedia.org/wiki/Integer_factorization)
- [Coppersmith's attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack)
