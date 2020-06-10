import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import pickle

# E=English, C=Consonant, W=wowel, N=number, O=Other, S=subcript, D=Diacritic, NS=no_space(same E)
# roll up to: NS, C, W, S, D
# consonant and independent vowels
KHCONST = set(u'កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ')
KHVOWEL = set(u'឴឵ាិីឹឺុូួើឿៀេែៃោៅ\u17c6\u17c7\u17c8')
# subscript, diacritics
KHSUB = set(u'្')
KHDIAC = set(u"\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0") #MUUSIKATOAN, TRIISAP, BANTOC,ROBAT,
KHSYM = set('៕។៛ៗ៚៙៘,.? ') # add space
KHNUMBER = set(u'០១២៣៤៥៦៧៨៩0123456789') # remove 0123456789
# lunar date:  U+19E0 to U+19FF ᧠...᧿
KHLUNAR = set('᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿')

def get_type(chr):
    EN = set(u'abcdefghijklmnopqrstuvwxyz0123456789')
    NS = 'NS'
    if chr.lower() in EN: return NS
    if chr in KHCONST: return "C"
    if chr in KHVOWEL: return "W"
    if chr in KHNUMBER: return NS
    if chr in KHSUB: return "S"
    if chr in KHDIAC: return "D"
    return NS

# non-khmer character that we should not separate like number
# multiple characters are false
def is_no_space(k):
    NS = 'NS'
    if get_type(k[0])==NS: return True
    return False

def kcc_type(k):
    if len(k)==1: return get_type(k)
    else: return "K" + str(len(k))

# list of constants needed for KCC and feature generation

def is_khmer_char(ch):
    if (ch >= '\u1780') and (ch <= '\u17ff'): return True
    if ch in KHSYM: return True
    if ch in KHLUNAR: return True
    return False

def is_start_of_kcc(ch):
    if is_khmer_char(ch):
        if ch in KHCONST: return True
        if ch in KHSYM: return True
        if ch in KHNUMBER: return True
        if ch in KHLUNAR: return True
        return False
    return True

# kcc base - must surround space with \u200b using cleanupstr()
def seg_kcc(str_sentence):
    segs = []
    cur = ""
    sentence = str_sentence
    #for phr in str_sentence.split(): #no longer split by space, use 200b
    #    print("phr: '", phr,"'")
    for word in sentence.split('\u200b'):
      #print("PHR:[%s] len:%d" %(phr, len(phr)))
      for i,c in enumerate(word):
          #print(i," c:", c)
          cur += c
          nextchar = word[i+1] if (i+1 < len(word)) else ""
          
          # cluster non-khmer chars together
          if not is_khmer_char(c) and nextchar != " " and nextchar != "" and not is_khmer_char(nextchar): 
            continue
          # cluster number together
          if c in KHNUMBER and nextchar in KHNUMBER: 
            continue
            
          # cluster non-khmer together
          # non-khmer character has no cluster
          if not is_khmer_char(c) or nextchar==" " or nextchar=="":
              segs.append(cur)
              cur=""
          elif is_start_of_kcc(nextchar) and not (c in KHSUB):
              segs.append(cur)
              cur="" 
        # add space back after split
        #segs.append(" ")   
    return segs # [:-1] # trim last space

# testing some text
# t1 = "យោងតាមប្រភពព័ត៌មានបានឱ្យដឹងថា កាលពីពេលថ្មីៗនេះក្រុមចក្រភពអង់គ្លេស Royal Marines ដែលមានមូលដ្ឋាននៅ Gibraltar បានរឹបអូសយកនាវាដឹកប្រេងឆៅរបស់អ៊ីរ៉ង់ដែលធ្វើដំណើរទៅកាន់រោងចក្រចម្រាញ់ប្រេងនៅក្នុងប្រទេសស៊ីរី ដោយក្រុងឡុងដ៍អះអាងថា ការរឹបអូសត្រូវបានគេសំដៅអនុវត្ត៕"
# t2 = "ខែThis is a test. N.B. ខែ? Test?"
# t3 = "នៅរសៀលថ្ងៃទី២២ ខែ កក្កដា ឆ្នាំ២០១៩ ឯកឧត្តម គួច ចំរើន អភិបាលខេត្តព្រះសីហនុ"
# t4 = "This. 11,12 ២២.២២២.២២២,២២"
# t5 = " ក "
# print("kcc:", seg_kcc(t1))
# print("kcc:", seg_kcc(t2))
# print("kcc:", seg_kcc(t3))
# print("kcc:", seg_kcc(t4))
# print("kcc:", seg_kcc(t5))
# only pass in kccs list (without labels)
def kcc_to_features(kccs, i):
    maxi = len(kccs)
    kcc = kccs[i]

    features = {
        'kcc': kcc,
        't': kcc_type(kcc),
        'ns': is_no_space(kcc)
    }
    if i >= 1:
        features.update({
            'kcc[-1]'  : kccs[i-1],
            'kcc[-1]t' : kcc_type(kccs[i-1]),
            'kcc[-1:0]': kccs[i-1] + kccs[i],
            'ns-1' : is_no_space(kccs[i-1])
        })
    else:
        features['BOS'] = True

    if i >= 2:
        features.update({
            'kcc[-2]'   : kccs[i-2],
            'kcc[-2]t'  : kcc_type(kccs[i-2]),
            'kcc[-2:-1]': kccs[i-2] + kccs[i-1],
            'kcc[-2:0]' : kccs[i-2] + kccs[i-1] + kccs[i],
        })
    if i >= 3:
        features.update({
            'kcc[-3]'   : kccs[i-3],
            'kcc[-3]t'  : kcc_type(kccs[i-3]),
            'kcc[-3:0]' : kccs[i-3] + kccs[i-2] + kccs[i-1] + kccs[i],
            'kcc[-3:-1]': kccs[i-3] + kccs[i-2] + kccs[i-1],
            'kcc[-3:-2]': kccs[i-3] + kccs[i-2],
        })

    if i < maxi-1:
        features.update({
            'kcc[+1]'  : kccs[i+1],
            'kcc[+1]t'  : kcc_type(kccs[i+1]),
            'kcc[+1:0]': kccs[i] + kccs[i+1],
            'ns+1' : is_no_space(kccs[i+1])

        })
    else:
        features['EOS'] = True

    if i < maxi-2:
        features.update({
            'kcc[+2]'   : kccs[i+2],
            'kcc[+2]t'   : kcc_type(kccs[i+2]),
            'kcc[+1:+2]': kccs[i+1] + kccs[i+2],
            'kcc[0:+2]' : kccs[i+0] + kccs[i+1] + kccs[i+2],
            'ns+2' : is_no_space(kccs[i+2])
        })
    if i < maxi-3:
        features.update({
            'kcc[+3]'   : kccs[i+3],
            'kcc[+3]t'   : kcc_type(kccs[i+3]),
            'kcc[+2:+3]': kccs[i+2] + kccs[i+3],
            'kcc[+1:+3]': kccs[i+1] + kccs[i+2] + kccs[i+3],
            'kcc[0:+3]' : kccs[i+0] + kccs[i+1] + kccs[i+2] + kccs[i+3],
        })

    return features

def generate_kccs_label_per_phrase(sentence):
    phrases = sentence.split()
    print("prep_kcc_labels -- number of phrases:", len(phrases))
    final_kccs = []
    for phrase in phrases:
        kccs = seg_kcc(phrase)
        labels = [1 if (i==0) else 0 for i, k in enumerate(kccs)]
        final_kccs.extend(list(zip(kccs,labels)))
    return final_kccs

def create_kcc_features(kccs):
    return [kcc_to_features(kccs, i) for i in range(len(kccs))]

# take label in second element from kcc with label
def create_labels_from_kccs(kccs_label):
    return [str(part[1]) for part in kccs_label]

# Create KCC using phrase, but pass in the whole sentence to CRF
def load_model(filename_model):
    return pickle.load(open(filename_model, 'rb'))

def segment_kcc_phrase(crf, sentence):
    complete = ""
    sentence = sentence.replace(u'\u200b','')
    kccs = seg_kcc(sentence)

    #TODO should feed the whole sentence, not phrase, kcc already capture english spaces
    features = create_kcc_features(kccs)
    prediction = crf.predict([features])

    for i, p in enumerate(prediction[0]):
        if p == "1":
            complete += " " + kccs[i]
        else:
            complete += kccs[i]
    complete = complete.strip().replace('\n'," ")
    complete = complete.strip().replace("  "," ")
    return complete

# Testting

# t = "ចំណែកជើងទី២២២២ នឹងត្រូវធ្វើឡើងឯប្រទេសកាតា៕"
# t_correct = "ចំណែក ជើង ទី ២២២២ នឹង ត្រូវ ធ្វើឡើង ឯ ប្រទេស កាតា ៕ "
# skcc = seg_kcc(t)
# print("len kcc:", len(skcc), skcc)
# #featrues = create_kcc_features(skcc)
# print(" seg:", segment_kcc_phrase(t))
# print("corr:", t_correct)
# t = "យោងតាមប្រភពព័ត៌មានបានឱ្យដឹងថា កាលពីពេលថ្មីៗនេះក្រុមចក្រភពអង់គ្លេស Royal Marines ដែលមានមូលដ្ឋាននៅ Gibraltar បានរឹបអូសយកនាវាដឹកប្រេងឆៅរបស់អ៊ីរ៉ង់ដែលធ្វើដំណើរទៅកាន់រោងចក្រចម្រាញ់ប្រេងនៅក្នុងប្រទេសស៊ីរី ដោយក្រុងឡុងដ៍អះអាងថា ការរឹបអូសត្រូវបានគេសំដៅអនុវត្ត"
# t_correct = "យោង តាម ប្រភព ព័ត៌មាន បាន ឱ្យដឹង ថា កាលពី ពេល ថ្មី ៗ នេះ ក្រុម ចក្រភព អង់គ្លេស Royal Marines ដែល មាន មូលដ្ឋាន នៅ Gibraltar បាន រឹបអូស យក នាវា ដឹក ប្រេង ឆៅ របស់ អ៊ីរ៉ង់ ដែល ធ្វើដំណើរ ទៅកាន់ រោងចក្រ ចម្រាញ់ ប្រេង នៅ ក្នុង ប្រទេស ស៊ីរី ដោយ ក្រុង ឡុងដ៍ អះអាង ថា ការរឹបអូស ត្រូវបាន គេ សំដៅ អនុវត្ត "
# print("\n seg:", segment_kcc_phrase(t).strip().replace('  ',' '))
# print("corr:", t_correct)
# t= 'ថ្ងៃ​ទី០២ ខែមករា ឆ្នាំ​២០១៤ '
# t_correct = "ថ្ងៃទី ០២ ខែមករា ឆ្នាំ ២០១៤"
# print("\n seg:", segment_kcc_phrase(t))
# print("corr:", t_correct)
# t = "2019-07-12 03:39:34.540220"
# t_correct = "2019-07-12 03:39:34.540220"
# print("\n seg:", segment_kcc_phrase(t))
# print("corr:", t_correct)
# t = 'តើអ្នកប្រាប់ខ្ញុំបានទេថាពេលណាត្រូវចុះពីឡានក្រុង ? '
# t_correct = 'តើ អ្នក ប្រាប់ ខ្ញុំ បាន ទេ ថា ពេលណា ត្រូវ ចុះ ពី ឡានក្រុង ?'
# print("\n seg:", segment_kcc_phrase(t))
# print("corr:", t_correct)
