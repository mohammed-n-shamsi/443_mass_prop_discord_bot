""" Perform computation on weights """
import json
import secrets
import discord

client = discord.Client()

with open('weight_store.json', 'r') as f:
    weight_store = json.load(f)


def change_element(component, element, value):
    """
    Changes an element for a specified component with given value
    and updates the json file
    """
    component[element] = value
    with open('weight_store.json', 'w') as file_push:
        json.dump(weight_store, file_push, indent=4)


def change_weight(component, weight):
    """ Changes weight for given component """
    for comp in weight_store:
        if comp['component'] == component:
            change_element(comp, 'weight', weight)


def total_weight():
    """ Returns the weight from each component """
    weight_sum = 0
    for comp in weight_store:
        if comp['group'] != "invalid":
            weight_sum = weight_sum + comp['weight']
    return weight_sum


def group_weight(group):
    """ Returns the weight for each component in a group """
    weight_sum = 0
    for comp in weight_store:
        if determine_group(group, comp['group']):
            weight_sum = weight_sum + comp['weight']
    return weight_sum

def determine_group(requested_group, item_group):
    """ Determines if item group should be in requested group """
    if item_group == "invalid":
        return False
    if item_group == requested_group:
        return True
    if requested_group == "max_weight":
        return True
    if requested_group == "operating_empty_weight" and \
            item_group != "max_weight":
        return True
    return False


def build_weights(group):
    """ Builds weight string to send to discord """
    weight_str = "Weight of "
    weight_str = weight_str + group + '\n'
    weight_str = weight_str + "----------- \n"
    for comp in weight_store:
        if determine_group(group, comp['group']):
            weight_str = weight_str + comp['component']
            weight_str = weight_str + ' '
            weight_str = weight_str + str(comp['weight'])
            weight_str = weight_str + '\n'
    weight_str = weight_str + "---------- \n"
    weight_str = weight_str + group
    weight_str = weight_str + " - " + str(group_weight(group))
    return weight_str


def comp_weight_str(component):
    """ returns weight of a component """
    for comp in weight_store:
        if comp['component'] == component:
            msg = "Weight - "
            msg = msg + component + ' ' + str(comp['weight']) + '\n'
            return msg
    return "Component not found"


def help_string():
    """ Builds help string """
    msg = "Commands: |$List <group>| \n "
    msg = msg + "|$Change weight: component weight| \n"
    msg = msg + "Components are: \n"
    for comp in weight_store:
        if comp['group'] != 'invalid':
            msg = msg + comp['component']
            msg = msg + '\n'
    msg = msg + "Groups are: \n"
    msg = msg + "empty_weight \n"
    msg = msg + "operating_empty_weight \n"
    msg = msg + "max_weight \n"
    return msg


def valid_component(component):
    """ Verifies if given component is valid or not """
    for comp in weight_store:
        if comp['component'] == component:
            return True
    return False


@client.event
async def on_ready():
    """ On ready response """
    print('Mass prop bot has landed')


@client.event
async def on_message(message):
    """ Message Trigger """
    if message.content.startswith('$help'):
        msg = help_string()
        await message.channel.send(msg)
    if message.content.startswith('$List'):
        args = (message.content).split()
        msg = build_weights(args[1])
        await message.channel.send(msg)
    if message.content.startswith('$Change weight:'):
        args = (message.content).split()
        if valid_component(args[2]):
            change_weight(args[2], float(args[3]))
            msg = comp_weight_str(args[2])
        else:
            msg = "Invalid Component"
        await message.channel.send(msg)


def main():
    """ Entry point of program """
    client.run(secrets.TOKEN)


if __name__ == '__main__':
    main()
