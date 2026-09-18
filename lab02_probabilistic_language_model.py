
corpus = "Tôi thích học toán. Tôi thích học lập trình. Tôi học lập trình rất nhiều. Toán và lập trình là hai môn tôi yêu thích."
stopwords = ['đang', 'rất']

def count_freq(pattern: str, texts:str) -> int:
    cnt = 0
    for text in texts:
        if pattern in text:
            cnt += 1
    return cnt

# clean corpus.
lower_corpus = corpus.lower()
texts = lower_corpus.split(".")[:-1]
texts = [text.strip() for text in texts if text not in stopwords]
vocabulary = []
for text in texts:
    tokens = text.split()
    for token in tokens:
        vocabulary.append(token)
vocabulary = set(vocabulary)

# create unigram
unigram_table = {}
for word in vocabulary:
    unigram_table[word] = count_freq(word, texts)

# Create bigram
bigram = set()
for text in texts:
    words = text.split()
    for i in range(len(words) - 1):
        candidate = " ".join(words[i:i+2])
        bigram.add(candidate)

bigram_table = {}
for pair in bigram:
    bigram_table[pair] = count_freq(pair, texts)

MAX_TOKEN = 10
user_input = input("Prompt: ").lower()
formatted_input = user_input.split(" ")
formatted_input = [token for token in formatted_input if token not in stopwords]

curr_token = 0
output = formatted_input.copy()

while curr_token < MAX_TOKEN:
    if len(formatted_input) == 0:
        break
    elif len(formatted_input) > 0:
        last_token = output[-1]
        max_prob = -1
        max_word = ""
        for word in vocabulary:
            pair = f"{last_token} {word}"
            probability = bigram_table.get(pair, 0) / unigram_table.get(last_token, 1)
            if probability > max_prob:
                max_prob = probability
                max_word = word
        output.append(max_word)
        curr_token += 1

print(" ".join(output))


