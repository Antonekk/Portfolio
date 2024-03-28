#https://wolnelektury.pl/media/book/txt/orwell-rok-1984.txt


txt_file = ''
with open('orwell-rok-1984.txt', encoding='utf8') as f:
    for line in f:
        txt_file += line.strip()


def compress(text):
    if len(text) == 0:
        return []
    compressed_text = [[text[0],1]]
    for  value in text[1:]:
        if value == compressed_text[-1][0]:
            compressed_text[-1][1]+=1
        else:
            compressed_text.append([value,1])
    return compressed_text


def decompress(compressed_text):
    decompressed_text = ''
    for i in compressed_text:
        decompressed_text += i[0] * i[1]
    return decompressed_text

print(compress(txt_file))
print(decompress(compress(txt_file)))



