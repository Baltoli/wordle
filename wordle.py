#!/usr/bin/env python3

from collections import Counter

def initial_words():
    with open('/usr/share/dict/words') as f:
        return list({w.rstrip('\n').lower() for w in f.readlines() if len(w) == 6})

def character_count(words):
    count = Counter()
    for word in words:
        count += Counter(word)
    return count

def score(word, counts):
    return sum([counts[c] for c in set(word)])

def compatible(word, greys, yellows, greens):
    if not set(yellows) <= set(word):
        return False

    for idx in greens:
        if word[idx] != greens[idx]:
            return False

    for idx in greys:
        if word[idx] in greens.values():
            if word[idx] == greys[idx]:
                return False
        else:
            if word[idx] in greys.values():
                return False

    return True

# . -> grey
# x -> yellow
# # -> green
def parse_response(word, resp):
    greys = {}
    yellows = []
    greens = {}

    for idx, c in enumerate(word):
        if resp[idx] == '.':
            greys[idx] = c
        elif resp[idx] == 'x':
            yellows.append(c)
        elif resp[idx] == '#':
            greens[idx] = c
        else:
            print("Bad response string")

    return [greys, yellows, greens]

if __name__ == '__main__':
    words = initial_words()
    
    blacklist = set()

    while True:
        counts = character_count(words)
        ranking = sorted(words, key=lambda word: score(word, counts), reverse=True)

        choice = None
        for offer in ranking:
            print(f"try: {offer}")
            resp = input("> ")

            blacklist.add(offer)

            if len(resp) > 0:
                choice = offer
                break

        parsed = parse_response(choice, resp)
        words = list(filter(lambda w: compatible(w, *parsed) and w not in blacklist, words))
