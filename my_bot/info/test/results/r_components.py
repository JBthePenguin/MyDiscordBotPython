# ### Component Embed
# BASE_RESULT -> {footer, color, type, timestamp, desription}
BASE_RESULT = {
    'footer': {'text': 'Member since'}, 'color': 0,
    'timestamp': '2020-04-27T13:00:00+00:00', 'type': 'rich',
    'description': "A human actually offline.", }


def get_embed_dict(title, obj_id, values):
    """Return an embed dict for components infos.
    -> {title, author, fields} and updated with base result."""
    tups_name_val = [
        ('Roles', values[0]),
        ('Channels allowed to view', values[1])]
    fields = []
    for name_val in tups_name_val:
        fields.append(
            {'inline': False, 'name': name_val[0], 'value': name_val[1]})
    embed_dict = {
        'title': title,
        'author': {
            'name': f"id: {obj_id}",
            'icon_url': 'https://url.com/avatar.png'},
        'fields': fields}
    embed_dict.update(BASE_RESULT)
    if obj_id == 0:
        embed_dict['description'] += " He's the owner."
    return embed_dict


# COMPONENTS RESULTS -> InfoComponentsCommandsTest expected results
C_RESULTS = {
    'id': get_embed_dict('Jean-Pierre', 0, ('@everyone - admin', 'All')),
    'name': get_embed_dict('Joe', 2, (
        '@everyone - staff',
        'info point - meeting room - reception - shop - snack - studio')),
    'no_id': 'Member with id 12 not founded.',
    'no_name': 'Member with name Tom not founded.'}
