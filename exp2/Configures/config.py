import csv
import random
#note, the first five are practices

# get a target - 2 cues dictionary 
def get_target_dict():
    target_dict = []
    raw_dict = []
    with open('./Configures/target_dict.csv', 'r', newline='') as f: 
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    word = raw_dict[0][0]
    current = []
    for i in range(0,len(raw_dict)):
        if raw_dict[i][0] == word:
            current.append(raw_dict[i][1])
        else: 
            target_dict.append({'target':word, 'cues':current})
            current = [raw_dict[i][1]]
            word = raw_dict[i][0]
    target_dict.append({'target':word, 'cues':current})
    return target_dict

# Read in all the target and find corresponding nonwords with the same length 
# Only need to execute once when a new target dictionary is generated
def get_nonword_dict():
    nonword = []
    target = []
    target_all = []
    with open('./Configures/nonword.txt','r') as f:
        rawnonword = f.read().split('\n')
    for i in rawnonword:
        if ((len(i) >5) and (len(i)<13)):
            nonword.append(i)
    with open('./Configures/targets.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            target.append(row[0])
    for i in target:
        nw = random.choice(nonword).upper()
        while (len(nw)!= len(i)):
            nw = random.choice(nonword).upper()
        target_all.append([i,nw])
    with open('./Configures/all_targets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(target_all)
    return True

# return a dictionary with targets & all their cues 
def get_whole_dict():
    whole_dict = []
    with open('./Configures/all_cues.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            whole_dict.append(row[1])
    return whole_dict

# find all the words appear as cues
# will serves to be the list where distractors come from
def get_cue_dict():
    cue_dict = []
    raw_dict = []
    with open('./Configures/all_cues.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    word = raw_dict[0][0]
    current = []
    for i in range(0,len(raw_dict)):
        if raw_dict[i][0] == word:
            current.append(raw_dict[i][1])
        else: 
            cue_dict.append({'target':word, 'cues':current})
            current = [raw_dict[i][1]]
            word = raw_dict[i][0]
    cue_dict.append({'target':word, 'cues':current})
    return cue_dict

def get_config():
    configures = [] 
    with open('./Configures/config_e2.csv', 'r', newline='') as configFile:
        reader = csv.reader(configFile,delimiter=',')
        heading = next(reader) 
        for row in reader:
            this_task = {}
            for i in range(1,4):
                    this_task[heading[i]] = int(row[i])
            configures.append(this_task)
    return configures

def get_target(stim_id,flag):
    raw_dict = []
    with open('./Configures/all_targets.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    return raw_dict[stim_id][flag]

configures = get_config() 

def get_config_cen(stim_id):
    return configures[stim_id]["center_is_prime(0no,1yes)"]

def get_config_sur(stim_id):
    return configures[stim_id]["cloud(-1_distratcor,0_none,1_prime)"]

def get_display_time(stim_id):
    return int(configures[stim_id]["display_time"])


font_type = "Times New Roman"
svg_width = 400
svg_height = 400
trial_num = 108 # added 18 for divisibility
prac_num = 5 
burn_num = prac_num + 12 # this is the cutoff for burn-ins
half = trial_num / 2
burn_in = int((burn_num - prac_num) / 2) # this is the number of burn-ins per half (6)

def get_font_type():
    return font_type

def get_size():
    return [svg_width,svg_height]

# generate the order in which the stimuli will be presented
# the first five is practice trial
def get_order():
    order = list(range(0,prac_num))
    burn_in_1 = randomize_list(list(range(prac_num, prac_num + burn_in)))
    order.extend(burn_in_1)
    burn_in_2 = randomize_list(list(range(prac_num + burn_in, burn_num))) # burn-ins after halfway point
    avail =  list(range(burn_num,trial_num + burn_num))
    for i in range(0,trial_num):
        if i == half:
            order.extend(burn_in_2)
        x = random.choice(avail)
        order.append(x)
        avail.remove(x)
    return order

def get_config_env():
    return [prac_num, trial_num + burn_num]

def randomize_list(list):
    out = []
    for i in range(0, len(list)):
        rand = random.choice(list)
        out.append(rand)
        list.remove(rand)
    return out