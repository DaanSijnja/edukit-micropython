import json

class card:
    def __init__(self,card_index,card_type,card_text,blank_spaces):
        self.card_index = card_index
        self.card_type = card_type
        self.card_text = card_text
        self.blank_spaces = blank_spaces

card_list = [
    #ready cards -1 => -8
    card(-1,0,"HELL YEAH!",-1),
    card(-2,0,"Yes I'm ready",-1),
    card(-3,0,"Yes Bitch",-1),
    card(-4,0,"Aye I am content to playeth this game",-1),
    card(-5,0,"Game Start!",-1),
    card(-6,0,"I was born ready",-1),   
    card(-7,0,"Ready? yeah sure",-1),
    card(-8,0,"I am the definition of ready, bitch",-1),
    #unready cards -9 => -16
    card(-9,0,"FUCK NO!",-1),
    card(-10,0,"No I'm not ready",-1),
    card(-11,0,"Wait wait! I have stuff to do",-1),
    card(-12,0,"Nah ah",-1),
    card(-13,0,"I dont think so",-1),
    card(-14,0,"I got other things to do",-1),   
    card(-15,0,"No.............",-1),
    card(-16,0,"NOOO, NOOOO, NO NO NO NO",-1),
    #are you ready black card and host ready card
    card(-1,1,"Are you ready to play?",1),
    card(-2,1,"Looks like everyone is ready!",1),
    #host start game card
    card(-22,0,"Start the game",-1)



]


card_dict = {}
card_dict["white_cards"] = []
card_dict["black_cards"] = []

for item in card_list:
    if(item.card_type == 0):
        card_dict["white_cards"].append(item.__dict__)
    else:
        card_dict["black_cards"].append(item.__dict__)

with open('data.json', 'w') as f:
    json.dump(card_dict, f,indent=4)

print(json.dumps(card_dict,indent=4))