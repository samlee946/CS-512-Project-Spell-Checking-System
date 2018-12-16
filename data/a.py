import numpy as np
freq = []
f = open('freq.txt', 'r')
freq = f.readlines()
f.close()
freq_list = [str.split() for str in freq]
f = open('en.txt', 'r')
en = f.readlines()
f.close()
freq_list = np.array(freq_list)
freq_dict = dict(zip(freq_list[:, 0], freq_list[:, 1]))
f = open('en1.txt', 'w')
for word in en:
    word = word.strip()
    if word in freq_dict:
        f.write('%s %s\n' % (word, freq_dict[word]))
    elif word.lower() in freq_dict:
        f.write('%s %s\n' % (word.lower(), freq_dict[word.lower()]))
    else:
        f.write('%s 99999\n' % word)
