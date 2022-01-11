import csv
import sys
import re

class Dict:
    def __init__(self, path_to_csv):
        self.dict = self.load_csv_dict(path_to_csv) 
        self.words = self.get_words()

    def load_csv_dict(self, _path):
        with open(_path, 'r') as source:
            reader = csv.DictReader(source)
            self.dict = {row['WORD']:row['DEF'] for row in reader}
        assert self.dict, "Nothing loaded to self.dict!"
        assert isinstance(self.dict, dict), "self.dict should be a dict type! but got {}".format(type(self.dict))
        return self.dict

    def get_words(self):
        return self.dict.keys()

    def startswith(self, letters):
        return [word for word in self.get_words() if word.startswith(letters)]

    def lookup(self, word):
        definition =  self.dict.get(word, None)
        def _format_w_d(word, defi):
            return "{} | {}".format(word.upper(), defi)

        rex_er = r'(.*)(e|es|ons|ez|ent|iez|ier)$'
        rex_ir = r'(.*)(is|it|issons|issez|issent)$'
        rex_re = r'(.*)(s|d|ons|ez|ent)$'
        def _verb(word, rex, ending):
            matches = re.match(rex, word)
            if matches:
                base = matches.groups(0)[0]
                _word = base+ending
                print("FOUND", _word)
                if base:
                    defi = self.lookup(_word)
                    if 'No definition' in defi:
                        return None
                    else:
                        return _format_w_d(_word, defi)
                

        rex_gen = r'(.*)(é|ée)$'
        def _base_word(word, rex, ending):
            matches = re.match(rex, word)
            if matches:
                base = matches.groups(0)[0]
                _word = base+'é, -{}{}'.format(base[-1], ending)
                print("FOUND", _word)
                if base:
                    defi = self.lookup(_word)
                    if 'No definition' in defi:
                        return None
                    else:
                        return _format_w_d(_word, defi)

        if definition:
            return "{} | {}".format(word, definition)
        else:
            defi = _verb(word, rex_er, 'er')
            if defi:
                return defi
            defi = _verb(word, rex_ir, 'ir')
            if defi:
                return defi
            defi = _verb(word, rex_re, 're')
            if defi:
                return defi
            #defi = _base_word(word, rex_gen, 'ée')
            #if defi:
            #    return defi

            if word.endswith('é'):
                alt_verb = word[:-1]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
                else:
                    alt_gender = word+', -sée'
                    definition = self.dict.get(alt_gender)
                    if definition:
                        return "{} | {}".format(alt_gender.upper(), definition)
            elif word.endswith('di'):
                alt_verb = word[:-2]+'dir'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('ée'):
                alt_verb = word[:-2]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('aient'):
                alt_verb = word[:-5]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('ait'):
                alt_verb = word[:-3]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('ais'):
                alt_verb = word[:-3]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('chant'):
                alt_verb = word+', -chante'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('teux'):
                alt_verb = word+', -teuse'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('is'):
                alt_verb = word[:-1]+'r'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('s'):
                alt_plural = word[:-1]
                definition = self.dict.get(alt_plural)
                if definition:
                    return "{} | {}".format(alt_plural.upper(), definition)
                else:
                    alt_verb = word[:-1]+'r'
                    definition = self.dict.get(alt_verb, None)
                    if definition:
                        return "{} | {}".format(alt_verb.upper(), definition)
        
        if not definition and word.endswith('s'):
            definition = self.lookup(word[:-1])
        if not definition and word.endswith('x'):
            definition = self.lookup(word[:-1])
        if not definition:
            definition = self.dict.get(word+' 1')

        return definition if definition else "No definition found for {}".format(word)

    
#======================= TESTS ===================================

test_path = 'dictionary/translate_dict.csv'
dd = Dict(test_path)

def test_lookup_basic():
    defi = dd.lookup('talus')
    assert "embankment" in defi

def test_lookup_negative():
    defi = dd.lookup("zzzyg")
    assert "No definition found for zzzyg" in defi

def test_lookup_re_verb_tense():
    defi = dd.lookup("crevé")
    assert "CREVER" in defi
    defi = dd.lookup("arpentaient")
    assert "ARPENTER" in defi
    defi = dd.lookup("brouillait")
    assert "brouiller".upper() in defi
    defi = dd.lookup("reculais")
    assert "reculer".upper() in defi
    defi = dd.lookup("transpires")
    assert "transpirer".upper() in defi
    defi = dd.lookup("accrochée")
    assert "accrocher".upper() in defi

def test_lookup_ir_verb_tense():
    defi = dd.lookup("accroupis")
    assert "accroupir".upper() in defi
    defi = dd.lookup("bondi")
    assert "bondir".upper() in defi

def test_lookup_er_verb_tense():
    defi = dd.lookup("égariez")
    assert "égarer".upper() in defi

def test_lookup_plurals():
    defi = dd.lookup("billes")
    assert "marble" in defi

def test_lookup_gender():
    defi = dd.lookup("sensé")
    assert "sensé, -sée".upper() in defi
    defi = dd.lookup("hérissés")
    assert "hérisser".upper() in defi

def test_lookup_ant_gender():
    defi = dd.lookup("alléchant")
    assert "alléchant, -chante".upper() in defi

def test_lookup_ieux_gender():
    defi = dd.lookup("miteux")
    assert "miteux, -teuse".upper() in defi

if __name__ == "__main__":

    DICT = 'dictionary/translate_dict.csv'

    tdict = Dict(DICT)

    print(tdict.lookup('talus'))
