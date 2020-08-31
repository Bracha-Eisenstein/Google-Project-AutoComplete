#from search import find_sentences
from search_functoins import find_sentences


def normal_form_query(query):
    without_unnecessary_spaces = ' '.join([x for x in query.split(' ') if x != ''])
    only_letter_or_number = ''.join(e for e in without_unnecessary_spaces if e.isalnum() or e == ' ').lower()
    return only_letter_or_number


# def find_matches(query):
#     normal_query = normal_form_query(query)
#     find_sentences(normal_form_query(query))
#     #optional_matches = find_sentences(normal_query)
#     #return optional_matches


def main():
    user_input = input("enter an input for search.\n")
    while True:
        if '#' not in user_input:
            user_input += input(user_input)
        else:
            user_input = input("enter an input for search.\n")
        find_sentences(normal_form_query(user_input))


main()
