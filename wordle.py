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
    if not set(word).isdisjoint(set(greys)):
        return False

    if set(word) & set(yellows) != set(yellows):
        return False

    for idx in greens:
        if word[idx] != greens[idx]:
            return False

    return True

# . -> grey
# x -> yellow
# # -> green
def parse_response(word, resp):
    greys = []
    yellows = []
    greens = {}

    for idx, c in enumerate(word):
        if resp[idx] == '.':
            greys.append(c)
        elif resp[idx] == 'x':
            yellows.append(c)
        elif resp[idx] == '#':
            greens[idx] = c
        else:
            print("Bad response string")

    return [greys, yellows, greens]

if __name__ == '__main__':
    words = initial_words()
    
    while True:
        counts = character_count(words)
        ranking = sorted(words, key=lambda word: score(word, counts), reverse=True)

        blacklist = set()

        choice = None
        for offer in ranking:
            if offer not in blacklist:
                print(f"try: {offer}")
                resp = input("> ")

                if len(resp) > 0:
                    choice = offer
                    break
                else:
                    blacklist.add(offer)

        parsed = parse_response(choice, resp)
        words = list(filter(lambda w: compatible(w, *parsed), words))