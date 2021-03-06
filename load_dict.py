import csv
import sys
import re

class Dict:
    rex_er = r'(.*)(e|es|ons|ez|ent|iez|ier|iez)$'
    rexes_er = [r'(.*){}$'.format(ending) for ending in ['e', 'es', 'ons', 'ez', 'ent', 'iez', 'ier', 'ant']]

    rex_ir = r'(.*)(is|it|issons|issez|issent|i|ie)$'
    rexes_ir = [r'(.*){}$'.format(ending) for ending in ['is','it','issons','issez','issent','i','ie','ait']]

    rex_re = r'(.*)(e|es|ais|ait|ions|iez|aient|erai|eras|era|erons|erez|eront|ai|as|a|s|d|ons|ez|ent)$'
    rexes_re = [r'(.*){}$'.format(ending) for ending in [
      'e','es','ais','ait','ions','iez','aient','erai','eras','era','erons','erez','eront','ai','as','a',
      's','d','ons','ez','ent', 'ant']
      ]
    def __init__(self, path_to_csv):
        self.dict = self.load_csv_dict(path_to_csv) 
        self.words = self.get_words()
        self.verb_tuples = [
                (Dict.rex_er, 'er'),
                (Dict.rex_ir, 'ir'),
                (Dict.rex_re, 're')
                ]
        self.recursion = 10

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
        if re.findall(r', -.*, -', word):
            return None
        #print("DEBUG:", word)
        def _format_w_d(word, defi):
            return "{} | {}".format(word.upper(), defi)

        def match_v_ending(word, rexs, ending):
            ms = [re.match(rex, word) for rex in rexes]
            hits = [m.groups()[0]+ending for m in ms if m]
            #print("VERB HITS:", hits, "ENDING=", ending)
            for hit in hits:
                defi = self.dict.get(hit, None)
                if defi:
                    return _format_w_d(hit, defi)
                else:
                    hit = hit+' 1'
                    defi = self.dict.get(hit, None)
                    if defi:
                        return _format_w_d(hit, defi)
            return None


        rex_gen = r'(.*)(??|??e)$'
        def _base_word(word, rex, ending):
            matches = re.match(rex, word)
            if matches:
                base = matches.groups(0)[0]
                _word = base+'??, -{}{}'.format(base[-1], ending)
                #print("FOUND", _word)
                if base:
                    defi = self.lookup(_word)
                    if 'No definition' in defi:
                        return None
                    else:
                        return _format_w_d(_word, defi)

        definition =  self.dict.get(word, None)
        if definition:
            return "{} | {}".format(word, definition)
        else:
            for rexes, ending in zip([Dict.rexes_er, Dict.rexes_ir, Dict.rexes_re],['er','ir','re']):
                defi = match_v_ending(word, rexes, ending)
                if defi:
                    return defi

            if word.endswith('??'):
                alt_verb = word[:-1]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
                else:
                    alt_gender = word+', -s??e'
                    definition = self.dict.get(alt_gender)
                    if definition:
                        return "{} | {}".format(alt_gender.upper(), definition)
                    alt_gender = word+', -l??e'
                    definition = self.dict.get(alt_gender)
                    if definition:
                        return "{} | {}".format(alt_gender.upper(), definition)
            elif word.endswith('di'):
                alt_verb = word[:-2]+'dir'
                definition = self.dict.get(alt_verb, None)
                if definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('??e'):
                alt_verb = word[:-2]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition and 'No def' not in definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
                alt_verb = word[:-3]+'er'
                definition = self.dict.get(alt_verb, None)
                if definition and 'No def' not in definition:
                    return "{} | {}".format(alt_verb.upper(), definition)
                if word.endswith('l??e'):
                    gender_word = word[:-1]+', -l??e'
                    definition = self.dict.get(gender_word, None)
                    if definition:
                        return "{} | {}".format(gender_word.upper(), definition)
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
                definition = self.dict.get(alt_plural, None)
                if definition:
                    return "{} | {}".format(alt_plural.upper(), definition)
                else:
                    alt_verb = word[:-1]+'r'
                    definition = self.dict.get(alt_verb, None)
                    if definition:
                        return "{} | {}".format(alt_verb.upper(), definition)
            elif word.endswith('u'):
                gender_word = word+', -rue'
                definition = self.dict.get(gender_word, None)
                if definition:
                    return "{} | {}".format(gender_word.upper(), definition)
            elif word.endswith('le'):
                ir_verb = word[:-1]+'ir'
                definition = self.dict.get(ir_verb, None)
                if definition:
                    return "{} | {}".format(ir_verb.upper(), definition)
            elif word.endswith('in'):
                ir_verb = word+'er'
                definition = self.dict.get(ir_verb, None)
                if definition:
                    return "{} | {}".format(ir_verb.upper(), definition)

        if not definition and word.endswith('??'):
            definition = self.lookup(word+', -'+word[-2:]+'e') 
        if not definition and word.endswith('??e'):
            print("\n<"+word+">\n")
            definition = self.lookup(word[:-1]+', -'+word[-3:]) 
        if not definition and word.endswith('s'):
            definition = self.lookup(word[:-1])
        if not definition and word.endswith('x'):
            definition = self.lookup(word[:-1])
        if not definition:
            definition = self.dict.get(word+' 1')

        return "{} | {}".format(word.upper(), definition) if definition else "No definition found for {}".format(word)

    
#======================= TESTS ===================================

test_path = 'dictionary/translate_dict.csv'
dd = Dict(test_path)

def test_lookup_basic():
    defi = dd.lookup('talus')
    assert "embankment" in defi
    defi = dd.lookup('bourru')
    assert "gruff" in defi
    defi = dd.lookup('h??l??e')
    assert "tanned" in defi
    defi = dd.lookup('bond??')
    assert "crammed" in defi
    defi = dd.lookup('bond??e')
    assert "crammed" in defi

def test_lookup_negative():
    defi = dd.lookup("zzzyg")
    assert "No definition found for zzzyg" in defi

def test_lookup_er_verb_tense():
    defi = dd.lookup("crev??")
    assert "CREVER" in defi
    defi = dd.lookup("arpentaient")
    assert "ARPENTER" in defi
    defi = dd.lookup("brouillait")
    assert "brouiller".upper() in defi
    defi = dd.lookup("reculais")
    assert "reculer".upper() in defi
    defi = dd.lookup("transpires")
    assert "transpirer".upper() in defi
    defi = dd.lookup("accroch??e")
    assert "accrocher".upper() in defi
    defi = dd.lookup("bouchant")
    assert "boucher".upper() in defi
    defi = dd.lookup("??gariez")
    assert "??garer".upper() in defi
    defi = dd.lookup("fr??le")
    assert "fr??ler".upper() in defi
    defi = dd.lookup("bouchant")
    assert "boucher 1".upper() in defi
    defi = dd.lookup("taquin")
    assert "taquiner".upper() in defi


def test_lookup_ir_verb_tense():
    defi = dd.lookup("accroupis")
    assert "accroupir".upper() in defi
    defi = dd.lookup("bondi")
    assert "bondir".upper() in defi
    defi = dd.lookup("tenait")
    assert "tenir".upper() in defi
    defi = dd.lookup("tressaille")
    assert "tressaillir".upper() in defi

#def test_lookup_re_verb_tense():
#    defi = dd.lookup("??gariez")
#    assert "??garer".upper() in defi
#    defi = dd.lookup("fr??le")
#    assert "fr??ler".upper() in defi

def test_lookup_plurals():
    defi = dd.lookup("billes")
    assert "marble" in defi

def test_lookup_gender():
    defi = dd.lookup("sens??")
    assert "sens??, -s??e".upper() in defi
    defi = dd.lookup("h??riss??s")
    assert "h??risser".upper() in defi

#def test_lookup_ant_gender():
#    defi = dd.lookup("all??chant")
#    assert "all??chant, -chante".upper() in defi

def test_lookup_ieux_gender():
    defi = dd.lookup("miteux")
    assert "miteux, -teuse".upper() in defi

if __name__ == "__main__":

    DICT = 'dictionary/translate_dict.csv'

    tdict = Dict(DICT)

    print(tdict.lookup('talus'))

