from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)


# below is the function for the gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# this is the mod inverse function
def mod_inverse(e, r):
    for d in range(2, r):
        if (d * e) % r == 1:
            return d
    return None


# this is the function for the generation of all the keys and prime numbers between 10 and 99 then p and q are randomly picked from this list of primes
def generate_keys():
    primes = [i for i in range(10, 100) if all(i % j != 0 for j in range(2, int(i ** 0.5) + 1))]
    p, q = random.sample(primes, 2)
    n = p * q
    r = (p - 1) * (q - 1)

    e = random.choice([x for x in range(2, r) if gcd(x, r) == 1])
    d = mod_inverse(e, r)

    return p, q, n, e, d


# encryption function
def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]


# decryption function
def decrypt(ciphertext, d, n):
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)


# key and message storage
keys = {"p": "", "q": "", "n": "", "e": "", "d": ""}
messages = {"plaintext": "", "ciphertext": "", "decrypted": ""}


@app.route("/", methods=["GET", "POST"])
def index():
    global keys, messages

    if request.method == "POST":
        action = request.form.get("action")

        if action == "generate":
            p, q, n, e, d = generate_keys()
            keys.update({"p": p, "q": q, "n": n, "e": e, "d": d})

        elif action == "encrypt":
            messages["plaintext"] = request.form.get("message")
            if keys["e"] and keys["n"]:
                encrypted = encrypt(messages["plaintext"], keys["e"], keys["n"])
                messages["ciphertext"] = encrypted

        elif action == "decrypt":
            messages["ciphertext"] = request.form.get("ciphertext")
            if keys["d"] and keys["n"] and messages["ciphertext"]:
                decrypted = decrypt(eval(messages["ciphertext"]), keys["d"], keys["n"])
                messages["decrypted"] = decrypted

    return render_template("index.html", **keys, **messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


