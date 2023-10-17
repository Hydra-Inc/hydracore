import base64
import json
import sys
import tempfile
import traceback

from typing import Dict, Optional

from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.model.map import maybe_map_info, maybe_template
from hydracore.heroes3.model.template import TemplateList
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.trainer.main import get_trainer
from hydracore.heroes3.trainer.base import Difficulty


def error(code: str, message: str, sys_message: Optional[str] = None):
    d = {'error': code, 'message': message}
    if sys_message:
        d['sys_message'] = sys_message
    print(json.dumps(d))
    sys.exit(0)


def ok(data: Dict):
    print(json.dumps({'error': False, 'data': data}))
    sys.exit(0)


def run_trainer(data):
    result = {}
    try:
        try:
            sgf = Heroes3SaveGameFile(data['savegame_location'])
        except Exception as e:
            error('bad_file', 'Not a Heroes 3 save game file format', str(e))

        try:
            heroes3sg = savegame(sgf)
        except Exception as e:
            error(
                'bad_version', 'This is a savegame file of Heroes3 not supported version', str(e))

        try:
            heroes3sg.unpack()
        except Exception as e:
            error(
                'unpacking_failure', 'Error during unpacking file - something got wrong', str(e))

        if maybe_template(heroes3sg.title, heroes3sg.description, heroes3sg.map_file_location):
            templates = TemplateList()
            tpl = templates.identify_template(
                heroes3sg.title, heroes3sg.description, heroes3sg.map_file_location)
            if tpl:
                pass
            else:
                error('bad_map', 'Template not identified')
        else:
            error('bad_map', 'A Random Generated Map is required')

        if not data['difficulty'] in [diff.name for diff in Difficulty]:
            error('bad_difficulty', 'Difficulty required')

        heroes = [hero for hero in heroes3sg.heroes() if hero.Hired]
        trainer = get_trainer(data['trainer'], date=heroes3sg.date,
                              heroes=heroes, difficulty=Difficulty[data['difficulty']])

        if trainer is None:
            error(
                'unsupported_trainer', 'Trainer for this savegame is currently unsupported')

        try:
            trainer.check()
            if getattr(trainer, 'supported_templates', False):
                if not tpl.fullid() in trainer.supported_templates():
                    error('unsupported_template',
                          "Trainer doesn't support this template")
        except Exception as e:
            error('trainer_failure', "Can't apply trainer on this savegame", str(e) + traceback.format_exc())

        mapinfo = maybe_map_info(heroes3sg.title, heroes3sg.description)
        trainer.SetMapTerrainInfo(mapinfo)
        try:
            trainer.run()
        except Exception as e:
            error('training_failed',
                  "Something wrong during training happened", str(e))

        heroes3sg.pack()
        
        with tempfile.NamedTemporaryFile() as f:
            heroes3sg.file.save(f.name)
            with open(f.name, 'rb') as f:
                data = f.read()

        # data = heroes3sg.file.binary_data
        flow = json.dumps(trainer.Random.pack())

        result['message'] = 'success'
        result['data'] = base64.b64encode(data).decode()
        result['flow'] = flow

        ok(result)
    except Exception as e:
        error('system_failure', 'Unkown flow error', str(e) + traceback.format_exc())
        


def main():
    try:
        if len(sys.argv)==1:
            data = input()
            input_data = json.loads(data)
        else:
            data = base64.b64decode(sys.argv[1])
            input_data = json.loads(data)
            # input_data['savegame'] = input()      # hack using input
        if not 'action' in input_data:
            error('system_failure', 'no action')
        action = input_data['action']
    except Exception as e:
        error('system_failure', 'json decode failed', str(e))

    if action == 'trainer':
        run_trainer(input_data)
    else:
        error('system_failure', 'bad action')


if __name__ == "__main__":
    main()
