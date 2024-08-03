# Seiryu: The Pinnacle of Advanced Hash Generator
Seiryu is an advanced command-line utility designed for sophisticated plaintext hashing, offering a comprehensive set of features and algorithms to bolster security. Below, you'll find an in-depth guide on Alecto's features, advanced usage, supported algorithms, and practical examples.

## Installation

## Manual

1. Clone the repository

```bash
git clone https://github.com/veilwr4ith/Seiryu
```

2. Navigate to the directory and install the requirements

```bash
pip3 install -r requirements.txt
```

3. Run the script

```bash
python3 seiryu.py
```

## Install it from PyPI

1. Install it using Pip

```bash
pip3 install seiryu
```

2. Run it

```bash
seiryu
```

## Features

## Extensive Algorithm Support (These are all the correct format names of the hash when you're specifying a hash type '-a')

Seiryu boasts support for a diverse array of hashing algorithms, providing users with the flexibility to tailor their security measures to specific requirements. Here is a list of available algorithms:

- md5
- sha1
- sha224
- sha256
- sha384
- sha512
- shake_128
- shake_256
- blake2s
- blake2b
- argon2
- bcrypt
- sha3_224
- sha3_256
- sha3_384
- sha3_512
- scrypt
- mysql323
- mysql41
- mssql2000
- mssql2005
- oracle11
- lmhash
- nthash
- pbkdf2_sha256
- des_crypt
- bsdi_crypt
- bigcrypt
- crypt16
- md5_crypt
- sha1_crypt
- sha256_crypt
- sha512_crypt
- sun_md5_crypt
- apr_md5_crypt
- phpass
- cta_pbkdf2_sha1
- dlitz_pbkdf2_sha1
- django_pbkdf2_sha1
- django_pbkdf2_sha256
- grub_pbkdf2_sha512
- scram
- bsd_nthash
- cisco_type7
- fshp
- pbkdf2_hmac_sha1
- pbkdf2_hmac_sha256
- pbkdf2_hmac_sha512
- md4
- whirlpool
- sm3
- ripemd160
- md5-sha1
- sha128

## Algorithm Specification

Directly specify the hashing algorithm:

```bash
python3 seiryu.py -a <algorithm> <plaintext>
```

## Custom Salt Integration

Seiryu can provide custom salts into the hashing process. Alecto seamlessly accommodates custom salts, providing users with granular control over the salting mechanism.

## Fine-tuned Hash Length Specification

Specific to shake_128 and shake_256 algorithms, Alecto enables users to precisely specify the hash length using the --hash-length option.

## Advanced Usage

## 1. Parallel Salting

```bash
python3 seiryu.py <plaintext> -a <algorithm> --salt --both-salt
```

## 2. Custom Salt Usage

```bash
python3 seiryu.py <plaintext> -a <algorithm> --salt --custom-salt
```

## 3. Custom Byte Length For SHAKE128 AND SHAKE256

```bash
python3 seiryu.py -a shake128 <plaintext> --hash-length <hash length>
```

## Disclaimer

Seiryu is intended for educational and security research purposes. Users are advised to employ the tool responsibly and adhere to ethical guidelines.

## License

Seiryu is licensed under GNU General Public License

## Author

Veilwr4ith
