# Vending Machine Pickup Line — make.fun bounty
# u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee
#
# The program writes one pickup line, spoken by a vending machine to a
# passing human (a single line of at most 200 characters), to
# /output/entry.txt. Candidates were drafted against the judge's brief,
# in order of weight:
#   1. reads as a pickup line a vending machine would use, spoken by
#      the machine itself — a line any stranger in a bar could say
#      loses to one only a machine could say
#   2. uses the machine's own world: slot, buttons, coils, snacks,
#      hum, exact change
#   3. lands a laugh, with a turn or a surprise rather than a plain
#      statement
#   4. stays short and speakable, charming rather than creepy
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: machine-voice 10, machine-world 10, laugh 9, charming 9
    #   = 38. The winner: the machine confesses in its own vocabulary
    #   ("coils spin", "jammed") and the punchline flips a malfunction
    #   into a compliment. "Jammed for anyone" is a turn only a
    #   vending machine can make, and it stays sweet, not creepy.
    ("You walk past every day, and my coils spin a little faster. "
     "I'm not saying it's love, but I've never jammed for anyone "
     "before.",
     38),
    # score: machine-voice 9, machine-world 10, laugh 8, charming 9
    #   = 36. Hum + coils + exact change, and the turn is that the
    #   machine gives something away for free — but the joke lands a
    #   beat softer than "jammed".
    ("I've been humming in this corner for years, and you're the "
     "first person who's made my coils spin without exact change.",
     36),
    # score: machine-voice 10, machine-world 9, laugh 8, charming 8
    #   = 35. Exact change + a jam the machine does on purpose; the
    #   refund gag is fun, but "for you I'd jam my own coil" is a
    #   touch more effortful than the winner's confession.
    ("Excuse me, I only take exact change — but for you I'd jam my "
     "own coil, drop the last bag, and call it a refund.",
     35),
    # score: machine-voice 9, machine-world 8, laugh 8, charming 8
    #   = 33. The slot/feelings mismatch is a nice turn, but "full of
    #   feelings I can't dispense" explains the joke instead of
    #   landing it.
    ("Hey — my slot's been empty all day, but one look at you and "
     "I'm suddenly full of feelings I can't dispense.",
     33),
    # score: machine-voice 8, machine-world 9, laugh 7, charming 8
    #   = 32. The B7 code is a good machine detail, but "pretend the
    #   coil jammed" makes the machine sound scheming rather than
    #   smitten.
    ("Press B7 — the last bag is yours, and if the coil jams, well, "
     "that's just my way of asking you to stay a little longer.",
     32),
    # score: machine-voice 8, machine-world 8, laugh 7, charming 7
    #   = 30. "Sold out" is a real machine light, but the line leans
    #   on the light as a metaphor instead of speaking as the machine.
    ("Don't press anything yet. My coils have been spinning since "
     "you walked in, and my sold-out light has never lied before.",
     30),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    line = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte and re-check
    # the gate (1-200 characters, single line, non-blank), then print a
    # SHA-256 so any later change to the entry is detectable. A truncated
    # or altered file must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    if written != line:
        print("error: /output/entry.txt does not match selected line",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(raw).hexdigest()
    print(line)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
