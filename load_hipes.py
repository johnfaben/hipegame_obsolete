import sys
from app import app, db
from app.models import Hipe, Answer

filename = sys.argv[1]

f = open(filename,'r')

for line in f: 
    words = line.strip().split(',')
    print words
    hipe = Hipe(words[0])
    for word in words[1:]:
        answer = Answer(word)
        hipe.answers.append(answer)
        db.session.add(answer)
    db.session.add(hipe)
    db.session.commit()

    
    

