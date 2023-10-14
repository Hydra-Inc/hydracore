from typing import Iterator, Optional
from functools import partial

from hydracore.heroes3.model.game import VERSIONS
from hydracore.heroes3.model.arch import Slot
from hydracore.heroes3.model.town import Towns


def model_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('model', help='Heroes 3 model print and debug')
    p.set_defaults(main=model_main)

    p.add_argument('version', choices=VERSIONS.keys(),
                   action='store',
                   help='version of the game')

    p.add_argument('category', choices=['artifacts', 'creatures', 'skills', 
                                        'spells', 'towns', 'heroclasses', 'hero',
                                        'templates'],
                   action='store',
                   help="what category you want to see")

    p.add_argument('--filter', type=str, action='store',
                   help="filter list by substring in name")

    p.add_argument('--level', type=int, action='store',
                   help="filter list by level (for creatures and spells only)")

    p.add_argument('--by-town', choices=[x.name for x in Towns('hota').All()],
                   help="filter creatures by town")

    p.add_argument('--upgraded', choices=['0', '1', '2'],
                   help="filter creatures by upgrade: 0 - un-upgraded, 1 - upgraded, 2 - second time upgrade")

    p.add_argument('--art-category', choices=['treasure', 'minor', 'major', 'relic', 'combination', 'scroll'],
                   help="filter artifacts by category")

    slots = [str(x).replace('Slot.', '') for x in Slot]
    p.add_argument('--art-slot', choices=slots,
                   help="filter artifacts by slots it fits")

    p.add_argument('--magic-school', choices=['Air', 'Earth', 'Fire', 'Water', 'Special'],
                   help="filter speels by magic school")


def filter_by_name(iter: Iterator, sub: Optional[str] = None) -> Iterator:
    for x in iter:
        if sub is not None:
            if isinstance(x, str):
                if not sub in x:
                    continue
            else:
                if not sub in x.name:
                    continue
        yield x


def model_main(cmdargs):

    from hydracore.heroes3.model.artifact import Artifacts
    from hydracore.heroes3.model.creature import Creatures
    from hydracore.heroes3.model.skill import Skills
    from hydracore.heroes3.model.spell import Spells
    from hydracore.heroes3.model.town import Towns

    ver = cmdargs.version
    filt = partial(filter_by_name, sub=(
        cmdargs.filter if cmdargs.filter else None))

    if cmdargs.category == 'artifacts':
        it = Artifacts(ver).All()
        if cmdargs.art_category == 'treasure':
            it = Artifacts(ver).Treasure()
        if cmdargs.art_category == 'minor':
            it = Artifacts(ver).Minor()
        if cmdargs.art_category == 'major':
            it = Artifacts(ver).Major()
        if cmdargs.art_category == 'relic':
            it = Artifacts(ver).Relic()
        if cmdargs.art_category == 'combination':
            it = Artifacts(ver).Combination()
        if cmdargs.art_category == 'scroll':
            it = Artifacts(ver).Scroll()
        if cmdargs.art_slot:
            it = Artifacts(ver).Slot(it, cmdargs.art_slot)

        Artifacts(ver).dump(filt(it))

    if cmdargs.category == 'creatures':
        it = Creatures(ver).All()
        if cmdargs.by_town:
            it = Creatures(ver).Town(cmdargs.by_town)
        if cmdargs.level:
            it = Creatures(ver).Level(cmdargs.level, it)
        if cmdargs.upgraded:
            it = Creatures(ver).Upg(int(cmdargs.upgraded), it)

        Creatures(ver).dump(filt(it))

    if cmdargs.category == 'skills':
        it = Skills(ver).All()
        Skills(ver).dump(filt(it))

    if cmdargs.category == 'spells':
        it = Spells(ver).All()
        if cmdargs.level:
            it = Spells(ver).Level(cmdargs.level, it)
        if cmdargs.magic_school:
            it = getattr(Spells(ver), cmdargs.magic_school)(
                it if cmdargs.magic_school != 'Special' else None)

        Spells(ver).dump(filt(it))

    if cmdargs.category == 'heroclasses':
        it = Towns(ver).HeroClasses()
        Towns(ver).dump_heroclasses(filt(it))

    if cmdargs.category == 'towns':
        it = Towns(ver).All()
        Towns(ver).dump(filt(it))

    if cmdargs.category == 'hero':
        from hydracore.heroes3.model.hota.hero import HOTAHero
        hero = HOTAHero()
        hero.Name = 'Xyron'
        hero.Class = 'Heretic'
        hero.PutCreature(5, 'Arch Devil', 100)
        hero.PutCreature(6, 'Archangel', 10)
        hero.dump()

    if cmdargs.category == 'templates':
        from hydracore.heroes3.model.template import TemplateList
        templates = TemplateList()
        print('Available templates:')
        i = 0
        for template_id in sorted(templates.get_ids()):
            i += 1
            print(f'  {i}. {template_id}')
        print()

    return


