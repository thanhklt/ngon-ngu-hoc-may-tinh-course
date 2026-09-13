import re
import numpy as np
from functools import cmp_to_key
from viet_char import vietnamese_chars

def compare_string(text1: str, text2: str) -> int:
    """
        Nhận 2 chuỗi, trả về số dương nếu chuỗi 1 lớn hơn chuỗi 2, trả về số âm nếu chuỗi 1 nhỏ hơn chuỗi 2, còn lại trả về 0
    """
    len_text1 = len(text1)
    len_text2 = len(text2)
    for i in range(min(len_text1, len_text2)):
        c1 = text1[i].lower()
        c2 = text2[i].lower()
        idx1 = vietnamese_chars.index(c1) if c1 in vietnamese_chars else ord(c1)
        idx2 = vietnamese_chars.index(c2) if c2 in vietnamese_chars else ord(c2)
        if idx1 < idx2:
            return -1
        elif idx1 > idx2:
            return 1
    return len_text1 - len_text2

def generate_vector(text: str) -> list:
    """
        Nhận text trả về biểu diễn vector
    """
    tokens = re.findall(r"\w+", text)
    vector = []
    for word in vocabulary:
        vector.append(tokens.count(word))
    return vector

def build_freq(cleaned_segment: list) -> dict:
    segment_freq = {}
    for w in cleaned_segment:
        segment_freq[w] = segment_freq.get(w,0) + 1
    return segment_freq

def count_text_content_word(document: list, word: str) -> int:
    '''Trả về số lượng text chứa word'''
    cnt = 0
    for text in document:
        tokens = re.findall(r"\w+", text)
        if word in tokens:
            cnt += 1
    return cnt



# dataset
TOTAL_TEXT = 2
text1 = "Nam sống ở thành phố, đang học đại học, quen Lan ở trường, Lan rất thích học tin học và Nam hay học bài ở thư viện."
text2 = "Nam mới mua một cuốn sách mới. Nam rất thích đọc sách. Nam có nhiều cuốn sách rất hay."

text1 = text1.lower()
text2 = text2.lower()


documents = [text1, text2]

# Tách từ cho toàn bộ documents
word_segment = []
for document in documents:
    word_segment.extend(re.findall(r"\w+", document))

# Build vocabulary
unique_word = set(word_segment)
vocabulary = sorted(unique_word, key=cmp_to_key(compare_string))

# Generate vector
v1 = generate_vector(text1)
v2 = generate_vector(text2)
print(f"Vector 1: {v1}")
print(f"Vector 2: {v2}")

# Tính TF
tf1 = []
tf2 = []
len1 = len(re.findall(r"\w+", text1))
len2 = len(re.findall(r"\w+", text2))

for value in v1:
    tf1.append(round(value / len1, 2))
for value in v2:
    tf2.append(round(value / len2, 2))

print(f"TF 1: {tf1}")
print(f"TF 2: {tf2}")

# Tính IDF cho từng từ trong vocabulary
idf = []
for word in vocabulary:
    df = count_text_content_word(documents, word)
    idf.append(round(np.log(TOTAL_TEXT / df + 1), 2))

print(f"IDF: {idf}")

# Tính TF-IDF
tf_idf1 = []
tf_idf2 = []
for tf, idf_val in zip(tf1, idf):
    tf_idf1.append(round(tf * idf_val, 2))
for tf, idf_val in zip(tf2, idf):
    tf_idf2.append(round(tf * idf_val, 2))

print(f"TF-IDF 1: {tf_idf1}")
print(f"TF-IDF 2: {tf_idf2}")
    