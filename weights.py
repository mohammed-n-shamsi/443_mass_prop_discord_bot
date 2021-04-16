""" Perform computation on weights """
import json
import secrets
import discord

client = discord.Client()
TOKEN = secrets.TOKEN

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
        if group == comp['group']:
            weight_sum = weight_sum + comp['weight']
    return weight_sum


def build_all_weights():
    """ Builds weight string to send to discord """
    weight_str = "Weight of all components \n"
    weight_str = weight_str + "----------- \n"
    for comp in weight_store:
        if comp['group'] != 'invalid':
            weight_str = weight_str + comp['component']
            weight_str = weight_str + ' '
            weight_str = weight_str + str(comp['weight'])
            weight_str = weight_str + '\n'
    weight_str = weight_str + "---------- \n"
    weight_str = weight_str + "MTOW - " + str(total_weight())
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
    msg = "Commands: |$List all weights| & "
    msg = msg + "|$Change weight: component weight| \n"
    msg = msg + "Components are: \n"
    for comp in weight_store:
        if comp['group'] != 'invalid':
            msg = msg + comp['component']
            msg = msg + '\n'
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
    if message.content.startswith('$List all weights'):
        msg = build_all_weights()
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
    client.run(TOKEN)


if __name__ == '__main__':
    main()
