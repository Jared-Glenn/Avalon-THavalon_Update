import pdb
import copy
import os
import random
import shutil
import sys

# get_role_descriptions - this is called when information files are generated.
def get_role_description(role):
    return {
        'Tristan' : 'The person you see is also Good and is aware that you are Good.\nYou and Iseult are collectively a valid Assassination target.',
        'Iseult' : 'The person you see is also Good and is aware that you are Good.\nYou and Tristan are collectively a valid Assassination target.',
        'Merlin' : 'You know which people have Evil roles, but not who has any specific role.\nYou are a valid Assassination target.',
        'Percival' : 'You know which people have the Merlin and Morgana roles, but not who has each.',
        'Lancelot' : 'You may play Reversal cards while on missions.\nYou appear Evil to Merlin.',
        'Arthur' : 'You know which Good roles are in the game, but not who has any given role.\nIf two missions have Failed, and less than two missions have Succeeded, you may declare as Arthur.\nAfter declaring, your vote on team proposals is counted twice, but you are unable to be on mission teams until the 5th mission.\nAfter declaring, you are immune to any effect that can forcibly change your vote.',
        'Titania' : 'You appear as Evil to all players with Evil roles (except Colgrevance).',
        'Nimue' : 'You know which Good and Evil roles are in the game, but not who has any given role.\nYou are a valid Assassination target.',
        'Galahad' : 'After two quests have failed, you can declare as Galahad.\nAfter declaring, all other players must close their eyes and hold their fists in front of them.\nYou can name two Good roles (such as Merlin, Arthur, or Lancelot), one at a time.\nIf one of the players is that role, they must raise their thumb to indicate who they are.\nAfter this phase, play resumes normally.',
        'Guinevere' : 'You know two \"rumors\" about other players, but (with the exception of Arthur) nothing about their roles.\n\nThese rumors give you a glimpse at somebody else\'s character information, telling you who they know something about, but not what roles they are.\n\nFor instance, you if you heard a rumor about Player A seeing Player B, it might mean Player A is Merlin seeing an Evil player, or it might mean they are both Evil and can see each other.',
        'Gawain' : 'You can see two pairs of players.\nOne pair of players are against each other (Good and Evil or Pelinor and the Questing Beast), and the other pair are on the same side (Evil and Evil or Good and Good).',

        'Mordred' : 'You are hidden from all Good roles that could reveal that information.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Morgana' : 'You appear like Merlin to Percival.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Maelagant' : 'You may play Reversal cards while on missions.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Agravaine' : 'You must play Fail cards while on missions.\nIf you are on a mission that Succeeds, you may declare as Agravaine to cause it to Fail instead.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Colgrevance' : 'You know not only who else is Evil, but what role each other Evil player possesses.\nEvil players know that there is a Colgrevance, but do not know that it is you or even that you are Evil.',

        'Pelinor' : 'You are Neutral in this battle and have no allies in this game.\n\nYour nemesis is The Questing Beast, who is also Neutral.\n\nCARDS YOU CAN PLAY:\n> \"Success\"\n> \"Reversal\"\n\nTO WIN:\n> The Fifth Quest must occur and you must be on it.\n> Do one of the following:\n>>> Go on the Fifth Quest if The Questing Beast is NOT present.\n>>> Defeat The Questing Beast by declaring as Pelinor on the Fifth Quest while the Questing Beast IS present.\n>>> You MUST declare BEFORE the cards are read.\n>>> Beware, though! If The Questing Beast is not on the Fifth Quest when you declare as Pelinor, you lose and The Questing Beast wins instead.\n\nABOUT THE QUESTING BEAST:\n> The Questing Beast can see who you are.\n> The Questing Beast must play a \"The Questing Beast Was Here\" card at least once to win, but may play a \"Reversal\" card once per game.\n> If The Questing Beast does not play a \"The Questing Beast Was Here\" card at least once before the Fifth Quest, you automatically win by attending the Fifth Quest, even if The Questing Beast is present.',
        'The Questing Beast' : 'You are Neutral in this battle and have no allies in this game.\n\nYour nemesis is Pelinor, who is also Neutral.\n\nCARDS YOU CAN PLAY:\n> \"The Questing Beast Was Here.\"\n> \"Reversal\" (Only Once Per Game)\n\n\nTO WIN:\n> The Fifth Quest Must Occur.\n> You must play at least one \"The Questing Beast Was Here\" card.\n> Complete one of the following two options:\n>>> Go on the Fifth Quest undetected.\n>>> Trick Pelinor into declaring while you are NOT on the Fifth Quest.\n\nABOUT PELINOR:\n> Pelinor cannot see you, though you can see him.\n>Pelinor also wants to reach the Fifth Quest and must go on it to win.\n> Beware! If Pelinor suspects you are on the Fifth Quest, he may declare as Pelinor, causing you to lose. (If Pelinor declares incorrectly, you automatically win and Pelinor loses.)\n> If niether you nor Pelinor are on the Fifth Quest, you both lose.',
}.get(role,'ERROR: No description available.')

# get_role_information: this is called to populate information files
# blank roles:
# - Lancelot: no information
# - Arthur: no information
# - Guinevere: too complicated to generate here
# - Colgrevance: name, role (evil has an update later to inform them about the presence of Colgrevance)
def get_role_information(my_player,players):
    return {
        'Tristan' : ['{} is Iseult.'.format(player.name) for player in players if player.role == 'Iseult'],
        'Iseult' : ['{} is Tristan.'.format(player.name) for player in players if player.role == 'Tristan'],
        'Merlin' : ['{} is Evil'.format(player.name) for player in players if (player.team == 'Evil' and player.role != 'Mordred') or player.role == 'Lancelot'],
        'Percival' : ['{} is Merlin or Morgana.'.format(player.name) for player in players if player.role == 'Merlin' or player.role == 'Morgana'],
        'Lancelot' : [],
        'Arthur' : ['{}'.format(player.role) for player in players if player.team == 'Good' and player.role != 'Arthur'],
        'Titania' : [],
        'Nimue' : ['{}'.format(player.role) for player in players if player.role != 'Nimue'],
        'Galahad' : [],
        'Guinevere' : [str(get_rumors(my_player, players))],
        'Gawain' : [str(get_relationships(my_player, players))],

        'Mordred' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Morgana' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Maelagant' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Agravaine' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Colgrevance' : ['{} is {}.'.format(player.name, player.role) for player in players if player.team == 'Evil' and player != my_player],

        'Pelinor' : [],
        'The Questing Beast' : ['{} is Pelinor.'.format(player.name) for player in players if player.role == 'Pelinor'],
    }.get(my_player.role,[])

def get_rumors(my_player, players):
    rumors = []

    # Generate rumors about Merlin
    merlin_player = None
    is_Merlin = 0
    for player in players:
        if player.role == 'Merlin':
            merlin_player = player.name
            is_Merlin = 1
    if is_Merlin == 1:
        for player in players:
            if (player.team == 'Evil' and player.role != 'Mordred') or player.role == "Lancelot":
                player_of_evil = player.name
                rumors.append('{} sees {}'.format(merlin_player, player_of_evil))

    # Generate rumors about Percival
    percival_player = None
    is_Percival = 0
    for player in players:
        if player.role == 'Percival':
            percival_player = player.name
            is_Percival = 1
    if is_Percival == 1:
        for player in players:
            if player.role == 'Merlin' or player.role == 'Morgana':
                seer = player.name
                rumors.append('{} sees {}'.format(percival_player, seer))

    # Generate rumor about the Lovers
    tristan_player = None
    iseult_player = None
    is_Lovers = 0
    for player in players:
        if player.role == 'Tristan':
            tristan_player = player.name
            is_Lovers += 1
        elif player.role == 'Iseult':
            iseult_player = player.name
            is_Lovers += 1
    if is_Lovers == 2:
        rumors.append('{} sees {}'.format(tristan_player, iseult_player))
        rumors.append('{} sees {}'.format(iseult_player, tristan_player))

    # Generate rumor about Evil players
    for player in players:
        if player.team == 'Evil' and player.role != 'Mordred':
            for player_two in players:
                if (player_two.team == 'Evil' and player_two.role != 'Mordred' and player_two.role != 'Colgrevance' and player_two != player) or (player_two.role == 'Titania' and player_two != player):
                    rumors.append('{} sees {}'.format(player.name, player_two.name))

    # Generate rumor about Arthur
    is_Arthur = 0
    for player in players:
        if player.role == 'Arthur':
            is_Arthur = 1
    if is_Arthur == 1:
        for player in players:
            if player.team == 'Good' and player.role != 'Arthur' and player.role != 'Guinevere':
                rumors.append('King Arthur sees {}'.format(player.role))

    # Generate rumor about The Questing Beast
    questing_player = None
    is_Questing = 0
    for player in players:
        if player.role == 'The Questing Beast':
            questing_player = player
            is_Questing = 1
    if is_Questing == 1:
        for player in players:
            if player.role == 'Pelinor':
                rumors.append(f'{questing_player} sees {player}.')

    rumor_one = random.choice(rumors)
    rumor_two = random.choice(rumors)
    while rumor_one == rumor_two:
            rumor_two = random.choice(rumors)
    return rumor_one + '\n' + rumor_two

def get_relationships(my_player, players):

    # Assign teams
    good_team = []
    evil_team = []
    neutral_team = []
    for player in players:
        if player.team == 'Good' and player.role != 'Gawain':
            good_team.append(player)
        if player.team == 'Evil' and player.role != 'Mordred':
            evil_team.append(player)
        if player.team == 'Neutral':
            neutral_team.append(player)
    valid_players = good_team + evil_team + neutral_team

    # Choose random Opposing Team players
    opposition = None
    opposing_player = random.choice(valid_players)
    if opposing_player.team == 'Good':
            opposition = opposing_player.name + ' opposes ' + (random.choice(evil_team)).name
    elif opposing_player.team == 'Evil':
            opposition = opposing_player.name + ' opposes ' + (random.choice(good_team)).name
    elif opposing_player.role == 'Pelinor':
            for player in players:
                if player.role == 'The Questing Beast':
                    opposition = opposing_player.name + ' opposes ' + player.name
    elif opposing_player.role == 'The Questing Beast':
            for player in players:
                if player.role == 'Pelinor':
                    opposition = opposing_player.name + ' opposes ' + player.name

    # Choose random Collaborator players
    # Random choice of good or evil team (else good would be much more likely)
    # while loop to prevent collaborators from being the same player
    collaboration = None
    player_one = "1"
    player_two = "1"
    random_team = random.choice(['Good','Evil'])
    while player_one == player_two:
        if random_team == 'Good':
            player_one = (random.choice(good_team)).name
            player_two = (random.choice(good_team)).name
        elif random_team == 'Evil':
            player_one = (random.choice(evil_team)).name
            player_two = (random.choice(evil_team)).name

    collaboration = player_one + ' is collaborating with ' + player_two

    return opposition + '\n' + collaboration

# Oberoning Merlin (save for later)
#if player_of_role.get('Merlin'):
#    merlin_player = '{}'.format(player.name) for player in players if player.role == 'Merlin'
#    nonevil_list = []
#    for player in players:
#        if player.team != 'Evil' and player.role != "Lancelot" and player.role != "Merlin:
#            nonevil_list.append(player.name)
#    random_nonevil = random.sample(nonevil_list,1)[0]
#    rumors['merlin_rumor'] = [merlin_player + ' sees {}'.format(player.name) for player in players if (player.team == 'Evil' and player.role != 'Mordred') or player.role == 'Lancelot' or player.name == random_nonevil]


class Player():
    # Players have the following traits
    # name: the name of the player as fed into system arguments
    # role: the role the player possesses
    # team: whether the player is on good or evil's team
    # type: information or ability
    # seen: a list of what they will see
    # modifier: the random modifier this player has [NOT CURRENTLY UTILIZED]
    def __init__(self, name):
        self.name = name
        self.role = None
        self.team = None
        self.modifier = None
        self.info = []
        self.is_assassin = False

    def set_role(self, role):
        self.role = role

    def set_team(self, team):
        self.team = team

    def add_info(self, info):
        self.info += info

    def erase_info(self, info):
        self.info = []

    def generate_info(self, players):
        pass

def get_player_info(player_names):
    num_players = len(player_names)
    if len(player_names) != num_players:
        print('ERROR: Duplicate player names.')
        exit(1)

    # create player objects
    players = []
    for i in range(0, len(player_names)):
        player = Player(player_names[i])
        players.append(player)

    # number of good and evil roles
    num_neutral = 0
    if num_players < 7:
        num_evil = 2
    elif num_players < 9:
        num_evil = 3
    elif num_players == 9:
        num_evil = 4
    else:
        if random.choice([True, False, False]):
            num_evil = 3
            num_neutral = 2
        else:
            num_evil = 4
    num_good = num_players - num_evil - num_neutral

    # establish available roles
    good_roles = ['Merlin', 'Percival', 'Guinevere', 'Tristan', 'Iseult', 'Lancelot', 'Galahad',]
    evil_roles = ['Mordred', 'Morgana', 'Maelagant']
    neutral_roles = []

    # additional roles for player-count
    # 5 only
    if num_players < 6:
        good_roles.append('Nimue')

    # 7 plus
    if num_players > 6:
        good_roles.append('Arthur')
        good_roles.append('Gawain')
        good_roles.append('Titania')

    # 8 plus
    if num_players > 7:
        evil_roles.append('Agravaine')

    # 10 only
    if num_players == 10:
        evil_roles.append('Colgrevance')
        neutral_roles.append('Pelinor')
        neutral_roles.append('The Questing Beast')

    good_roles_in_game = random.sample(good_roles, num_good)
    evil_roles_in_game = random.sample(evil_roles, num_evil)
    neutral_roles_in_game = []
    if num_neutral > 0:
        neutral_roles_in_game.append('Pelinor')
        neutral_roles_in_game.append('The Questing Beast')

    # lone lovers are rerolled
    # 50% chance to reroll one lone lover
    # 50% chance to reroll another role into a lover
    if sum(gr in ['Tristan','Iseult'] for gr in good_roles_in_game) == 1 and num_good > 1:
        if 'Tristan' in good_roles_in_game:
            good_roles_in_game.remove('Tristan')
        if 'Iseult' in good_roles_in_game:
            good_roles_in_game.remove('Iseult')

        if random.choice([True, False]):
            # replacing the lone lover
            ##### ISSUE FOUND!!!! ############### Problem occurs when Lover is removed and replaced!
            available_roles = good_roles
            not_available = good_roles_in_game + ['Tristan'] + ['Iseult']
            for role in not_available:
                available_roles.remove(role)
            # DecrecationWarning issue. Found solution at https://stackoverflow.com/questions/70426576/get-random-number-from-set-deprecation
            good_roles_in_game.append(random.choice(available_roles))
        else:
            # upgradng to pair of lovers
            rerolled = random.choice(good_roles_in_game)
            good_roles_in_game.remove(rerolled)
            good_roles_in_game.append('Tristan')
            good_roles_in_game.append('Iseult')

    # roles after validation
    #print(good_roles_in_game)
    #print(evil_roles_in_game)

    # role assignment
    random.shuffle(players)
    neutral_players = []
    good_players = players[:num_good]
    if num_neutral == 0:
        evil_players = players[num_good:]
    else:
        evil_players = players[num_good:-2]
        neutral_players.append(players[-1])
        neutral_players.append(players[-2])

    player_of_role = dict()

    for gp in good_players:
        new_role = good_roles_in_game.pop()
        gp.set_role(new_role)
        gp.set_team('Good')
        player_of_role[new_role] = gp

    # if there is at least one evil, first evil player becomes assassin
    if len(evil_players) > 0:
        evil_players[0].is_assassin = True

    for ep in evil_players:
        new_role = evil_roles_in_game.pop()
        ep.set_role(new_role)
        ep.set_team('Evil')
        player_of_role[new_role] = ep

    for np in neutral_players:
        new_role = neutral_roles_in_game.pop()
        np.set_role(new_role)
        np.set_team('Neutral')
        player_of_role[new_role] = np

    for p in players:
        p.add_info(get_role_information(p,players))
        random.shuffle(p.info)
        # print(p.name,p.role,p.team,p.info)

    # Informing Evil about Colgrevance
    for ep in evil_players:
        if ep.role != 'Colgrevance' and player_of_role.get('Colgrevance'):
            ep.add_info(['Colgrevance lurks in the shadows. (There is another Evil that you do not see.)'])
        if ep.role != 'Colgrevance' and player_of_role.get('Titania'):
            ep.add_info(['Titania has infiltrated your ranks. (One of the people you see is not Evil.)'])
        if ep.is_assassin:
            ep.add_info(['You are the Assassin.'])

    # delete and recreate game directory
    if os.path.isdir("game"):
        shutil.rmtree("game")
    os.mkdir("game")

    bar= '----------------------------------------\n'
    for player in players:
        player.string= bar+'You are '+player.role+' ['+player.team+']\n'+bar+get_role_description(player.role)+'\n'+bar+'\n'.join(player.info)+'\n'+bar
        player_file = "game/{}".format(player.name)
        with open(player_file,"w") as file:
            file.write(player.string)

    first_player = random.sample(players,1)[0]
    with open("game/start", "w") as file:
        file.write("The player proposing the first mission is {}.".format(first_player.name))
        #file.write("\n" + second_mission_starter + " is the starting player of the 2nd round.\n")

    with open("game/DoNotOpen", "w") as file:
        file.write("Player -> Role\n\n GOOD TEAM:\n")
        for gp in good_players:
            file.write("{} -> {}\n".format(gp.name, gp.role))
        file.write("\nEVIL TEAM:\n")
        for ep in evil_players:
            file.write("{} -> {}\n".format(ep.name,ep.role))
        if len(neutral_players) > 0:
            file.write("\nNEUTRAL TEAM:\n")
            for np in neutral_players:
                file.write("{} -> {}\n".format(np.name,np.role))

if __name__ == "__main__":
    if not (6 <= len(sys.argv) <= 11):
        print("Invalid number of players")
        exit(1)

    players = sys.argv[1:]
    num_players = len(players)
    players = set(players) # use as a set to avoid duplicate players
    players = list(players) # convert to list
    random.shuffle(players) # ensure random order, though set should already do that
    if len(players) != num_players:
        print("No duplicate player names")
        exit(1)

    get_player_info(players)
