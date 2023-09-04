import copy
import json

import click
import yaspin

import myass.assistant

import mucus.command
import mucus.deezer.page
import mucus.exception
import mucus.history
import mucus.song


class Assistant(myass.assistant.Assistant):
    def __init__(self):
        super().__init__('mucus')
        self.context = {}

    def __call__(self, content):
        params = copy.deepcopy(self.config.flatten())
        self.messages.append({'role': 'user', 'content': content})
        params['messages'].extend(self.messages)
        with yaspin.yaspin(timer=True):
            r = self.api.post('chat/completions', json=params)
        m = r['choices'][0]['message']
        self.messages.append(m)
        params['messages'].append(m)
        while m.get('function_call') is not None:
            fn = m['function_call']['name']
            try:
                f = getattr(self, fn)
            except AttributeError:
                r = None
            else:
                r = f(**json.loads(m['function_call']['arguments']))
            m = {'role': 'function', 'name': fn, 'content': str(r)}
            params['messages'].append(m)
            with yaspin.yaspin(timer=True):
                r = self.api.post('chat/completions', json=params)
            params['messages'].pop()
            m = r['choices'][0]['message']
            self.messages.append(m)
        yield m['content']

    def play_song(self, artist, title):
        client = self.context['client']
        query = f'{artist} {title}'
        search = mucus.deezer.page.Search(client=client, query=query, nb=1)
        song = mucus.song.Song(search.track['data'][0])
        self.context['player'].queue.put(song)
        return str(song)

    def play_songs(self, songs):
        client = self.context['client']
        for song in songs:
            query = ' '.join((song['artist'], song['title']))
            search = mucus.deezer.page.Search(client=client, query=query, nb=1)
            song = mucus.song.Song(search.track['data'][0])
            self.context['player'].queue.put(song)

    def exit(self):
        raise mucus.exception.Exit


class Command(mucus.command.Command):
    def __init__(self):
        self.assistant = Assistant()

    def __call__(self, **kwargs):
        assist = self.assistant
        assist.context.update(**kwargs)
        with mucus.history.History(__name__):
            while True:
                try:
                    inputs = click.prompt(':', prompt_suffix=' ')
                except click.exceptions.Abort:
                    break
                try:
                    for content in assist(inputs):
                        click.echo(content)
                except mucus.exception.Exit:
                    break
