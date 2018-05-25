import random as rn
import sys

num_words_to_use = 50000
wordlist_filename = '/Users/faben/Dropbox/Programming/anagrams/dictionary_order.txt'
output_filename = 'list_of_hipes'+str(num_words_to_use)+'.txt'
hipe_length = 3
max_matches_allowed = 3

def fetch_hipes(filename,max_matches_allowed=2,hipe_length=3):
    f = open(filename,'r')
    hipe_length = hipe_length
    count = 0
    hipe_dict = dict()
    for i in range(num_words_to_use):
        line = f.readline()
        word = line.strip()
        for m in range(len(word)-hipe_length+1):
            key = word[m:m+hipe_length]
            if hipe_dict.has_key(key):
                hipe_dict[key].append(word)
            else:
                hipe_dict[key] = [word]
        count += 1
        
    hipes = dict()
    for key in hipe_dict:
        if len(hipe_dict[key]) < max_matches_allowed:
            hipes[key] = hipe_dict[key]

    f.close()
    
    g = open(filename, 'r')
    for line in g:
        word = line.strip()
        for m in range(len(word)-hipe_length+1):
            key = word[m:m+hipe_length]
            if hipes.has_key(key):
                if not word in hipes[key]: hipes[key].append(word)
     
    for key in hipes:
        if len(hipes[key])>2*max_matches_allowed:
            print key, hipes[key]
    print len([hipe for hipe in hipes if len(hipes[hipe]) > 6])


    

    


    return hipes
    
wordlist_filename = '/Users/faben/Dropbox/Programming/anagrams/dictionary_order.txt'

def write_hipes(filename,max_matches_allowed = 3):
    hipes = dict()
    for i in range(2,4):
        hipes.update(fetch_hipes(filename,max_matches_allowed,i))
    f = open(output_filename,'w')
    for hipe in hipes:
        f.write(hipe + ',' + ','.join(hipes[hipe]) + '\n')
    f.close()




def play_hipe(filename):

    hipes = fetch_hipes(filename,3)
    hipe = rn.choice(hipes.keys())
    name = raw_input("""What's your name?""")    
    success = 0
    guess = raw_input("""Hi, %s. Can you think of a word that contains the letters %s in that order?\n""" %(name,hipe))
    guesses = 1
    
    while not success:
        if guess in hipes[hipe]:
            print 'Well done, you got it'
            success = 1
        if guess.lower() == 'no' or guesses >= 3:
            print 'Oh well, the answers were'
            print [x for x in hipes[hipe]]
            print 'better luck next time'
            success = -1
        else:
            guess = raw_input("Sorry, %s, %s is not in my dictionary. Try again\n" %(name,guess))
            guesses +=1
        
    
    
write_hipes(wordlist_filename,4)
#play_hipe(wordlist_filename)   

        

