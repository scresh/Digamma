from re import sub
from itertools import combinations


def generate_snippet(text, searched_words):
    text_words = sub(r'([^\s\w]|_)', ' ', text).lower().split(' ')

    searched_word_indexes = pick_searched_word_indexes(searched_words, text_words)
    snippet_word_indexes = get_adjacent_words_indexes(text_words, searched_word_indexes, 256)
    snippet_word_index_group = group_indexes(snippet_word_indexes)

    pieces = []

    for group in snippet_word_index_group:
        pieces.append('')
        for word_index in range(group[0], group[-1] + 1):

            start_index = len(' '.join(text_words[:word_index]))
            stop_index = start_index + len(text_words[word_index]) + 1

            if text_words[word_index] in searched_words:
                pieces[-1] += f'<b>{text[start_index:stop_index]}</b>'
            else:
                pieces[-1] += text[start_index:stop_index]
        pieces[-1] = pieces[-1].strip()

    return ' … '.join(pieces)


def pick_searched_word_indexes(searched_words, text_words):
    picked_searched_word_indexes = set()

    if len(searched_words) > 1:
        searched_word_distances = get_searched_word_distances(searched_words, text_words)

        while len(picked_searched_word_indexes) < len(searched_words):
            word_a, word_b = get_min_distance_pair(searched_word_distances)

            delete_word_pair(searched_word_distances, (word_a, word_b))

            picked_searched_word_indexes.add(word_a['index'])
            picked_searched_word_indexes.add(word_b['index'])
    else:
        picked_searched_word_indexes.add(
            get_all_searched_word_indexes(searched_words, text_words)[searched_words[0]][0]
        )

    return sorted(picked_searched_word_indexes)


def get_all_searched_word_indexes(searched_words, text_words):
    all_searched_word_indexes = {}
    for word in searched_words:
        all_searched_word_indexes[word] = [index for index, value in enumerate(text_words) if value == word]

    return all_searched_word_indexes


def get_searched_word_distances(searched_words, text_words):
    all_searched_word_indexes = get_all_searched_word_indexes(searched_words, text_words)
    searched_word_pairs = list(combinations(searched_words, 2))

    searched_word_distances = {}

    for (word_a, word_b) in searched_word_pairs:
        searched_word_distances[(word_a, word_b)] = []
        for a_index in all_searched_word_indexes[word_a]:
            for b_index in all_searched_word_indexes[word_b]:
                first_index, second_index = sorted((a_index, b_index))
                distance = len(' '.join(text_words[first_index + 1:second_index]))
                searched_word_distances[(word_a, word_b)].append((distance, (a_index, b_index)))

    return searched_word_distances


def get_min_distance_pair(word_distances):
    min_distance_dict = {}

    for word_pair in word_distances:
        min_distance_dict[word_pair] = sorted(word_distances[word_pair], key=lambda x: x[0])[0]

    min_distance = sorted(list(min_distance_dict.items()), key=lambda x: x[1][0])[0]
    word_a, word_b = min_distance[0]
    a_index, b_index = min_distance[1][1]

    return {'value': word_a, 'index': a_index}, {'value': word_b, 'index': b_index}


def delete_word_pair(searched_word_distances, del_words):
    del searched_word_distances[tuple(map(lambda x: x['value'], del_words))]

    for word_pair in searched_word_distances:
        for word in del_words:
            if word['value'] in word_pair:
                word_index = word_pair.index(word['value'])

                i = 0
                while i < len(searched_word_distances[word_pair]):
                    if searched_word_distances[word_pair][i][1][word_index] != word['index']:
                        del searched_word_distances[word_pair][i]
                        continue
                    i += 1


def get_adjacent_words_indexes(text_words, word_indexes, max_snippet_len):
    right = {'shift': 1, 'range condition': lambda x: word_indexes[x] < len(text_words) - 1}
    left = {'shift': -1, 'range condition': lambda x: word_indexes[x] > 0}

    new_indexes_added = True
    while new_indexes_added:
        new_indexes_added = False
        iteration_indexes = []

        for i in range(len(word_indexes)):
            for direction in (left, right):
                if direction['range condition'](i) and word_indexes[i] + direction['shift'] not in word_indexes:
                    new_snippet_indexes = set(word_indexes + iteration_indexes + [word_indexes[i] + direction['shift']])
                    new_snippet_len = len(' '.join(map(lambda x: text_words[x], new_snippet_indexes)))

                    if new_snippet_len < max_snippet_len:
                        new_indexes_added = True
                        iteration_indexes = [*set(iteration_indexes + [word_indexes[i] + direction['shift']])]

        word_indexes = sorted(word_indexes + iteration_indexes)
    return word_indexes


def group_indexes(index_list):
    index_group = [[index_list[0]]]
    for i in range(1, len(index_list)):
        if index_list[i] == index_list[i - 1] + 1:
            index_group[-1].append(index_list[i])
        else:
            index_group.append([index_list[i]])
    return index_group

