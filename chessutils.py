def process_match(id1,id2,result):
    if result == 3:
        result = 1
    elif result == 2:
        result = 0.5
    else:
        result = 0
    old_rating = db.search(ID.id == id1)[0]['rating']
    old_rd = db.search(ID.id == id1)[0]['rd']
    old_vol = db.search(ID.id == id1)[0]['vol']
    op_rating = db.search(ID.id == id2)[0]['rating']
    op_rd = db.search(ID.id == id2)[0]['rd']
    op_vol = db.search(ID.id == id2)[0]['vol']
    temp = Player(old_rating,old_rd,old_vol)
    temp.update_player([op_rating],[op_rd],[result])
    db.update({'rating': temp.rating,'rd': temp.rd,'vol': temp.vol}, ID.id == id1)
    temp = Player(op_rating,op_rd,op_vol)
    if result == 1:
        result = 0
    elif result == 0:
        result = 1
    else:
        result = 0.5
    temp.update_player([old_rating],[old_rd],[result])
    db.update({'rating': temp.rating,'rd': temp.rd,'vol': temp.vol}, ID.id == id2)
def new_player(name):
    db.insert({'name': name, 'rating':1500,'rd':350,'vol':0.06,'id':len(db)})
    return(len(db)-1)