from textblob import TextBlob
import re


def get_wanted_noun(type_list, term_list):
    if len(type_list) < 2:
        return term_list[0]
    elif len(type_list) == 2:
        if type_list == ["noun", "noun"]:
            return term_list[-1]
        elif ("else" in type_list) and ("noun" in type_list):
            return term_list[type_list.index("noun")]
        elif type_list == ["else", "else"]:
            return term_list[0]
        else:
            raise ValueError("No noun found!")
    else:
        if type_list == ["noun", "else", "noun"]:
            return term_list[0]
        elif "noun" not in type_list:
            raise ValueError("No noun found!")
        else:
            return term_list[-1]


def get_types(terms):
    blob = TextBlob(terms)
    type_list = ["noun" if re.search("^NN", t) else "else" for n, t in blob.tags]
    return type_list


def get_meaningful_term(terms):
    """
    If terms can't be matched to ontology, simplify.

    Approach: use textblob to obtain word type. Simply based on heuristics of order (preferred terms: in capslock):

    Heuristics: "noun NOUN", "NOUN verb", "NOUN or noun", "NOUN of noun", "noun NOUN", "noun NOUN", "noun NOUN"

    examples = [
        "test Name",
        "date Performed",
        "laboratory Or Kit",
        "Number of Results",
        "data source",
        "material type",
        "collection site",
        "clinical information",
        "short Histological Findings",
    ]

    """
    term_list = terms.split("_")
    terms_processed = terms.replace("_", " ")
    print(term_list)
    type_list = get_types(terms_processed)
    return get_wanted_noun(type_list, term_list)
