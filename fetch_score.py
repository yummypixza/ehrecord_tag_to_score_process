import json

file = open('metadata.json', 'r', encoding='utf-8-sig')
raw_data = {i: json.loads(line) for i, line in enumerate(file)}
# reads overall doujin gallery index.

log = open('event.json', 'r', encoding='utf-8-sig')
log_data = {i: json.loads(line) for i, line in enumerate(log)}
# the user record which write events as page basis.

score_data = {}
multiplier = {}

# how do we sampling from data?
# reads all tags and gids (gallery id on site) from raw_data and import all tags into score_data[tag_name]
# which leads to building a tag index.
# then read gids as active_gid in log_data, if a tag in the active_gid matches as in score_data[tag_name],
# we would give 0.005 credit on active_gid as multiplier.
# so if a user reads pages the score would count as (1+1.005+1.010+1.015...) and so on.

for queue in raw_data:
    tags = raw_data[queue]['metadata']['tags']
    gid = raw_data[queue]['metadata']['gid']
    active_gid = log_data[queue]['event']['gid']
    for tag_name in tags:
        if tag_name not in score_data:
            score_data[tag_name] = 1
        else:
            for active_gid in log_data:
                if active_gid not in multiplier:
                    multiplier[active_gid] = 1
                else:
                    multiplier[active_gid] = multiplier[active_gid] + 0.005
            score_data[tag_name] += multiplier[active_gid]

    print(score_data)
    # prints all tags and their scores respectively.
