"""sopel-rep

Karma plugin for Sopel IRC bots, cloning the behavior of an old mIRC script.

Copyright 2015-2024 dgw
"""
from __future__ import annotations

import re
import time

from sopel import plugin
from sopel.config.types import BooleanAttribute, StaticSection, ValidatedAttribute
from sopel.tools import Identifier, time as time_tools


r_nick = r'[a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}'


class RepSection(StaticSection):
    cooldown = ValidatedAttribute('cooldown', int, default=3600)
    admin_cooldown = BooleanAttribute('admin_cooldown', default=True)


def setup(bot):
    bot.config.define_section('rep', RepSection)


def configure(config):
    config.define_section('rep', RepSection)
    config.rep.configure_setting(
        'cooldown',
        "How often should users be allowed to change someone's rep, in seconds?",
    )
    config.rep.configure_setting(
        'admin_cooldown',
        "Should bot admins also have to obey that cooldown?",
    )


@plugin.rule(r'^(?P<command></?3)\s+(%s)\s*$' % r_nick)
@plugin.ctcp('ACTION')
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def heart_cmd(bot, trigger):
    luv_h8(bot, trigger, trigger.group(2), 'h8' if '/' in trigger.group(1) else 'luv')


@plugin.rule(r'.*?(?:(%s)(\+{2}|-{2})).*?' % r_nick)
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def karma_cmd(bot, trigger):
    if re.match('^({prefix})({cmds})'.format(prefix=bot.config.core.prefix, cmds='|'.join(luv_h8_cmd.commands)),
                trigger.group(0)):
        return  # avoid processing commands if people try to be tricky
    for (nick, act) in re.findall(r'(?:(%s)(\+{2}|-{2}))' % r_nick, trigger.raw):
        if luv_h8(bot, trigger, nick, 'luv' if act == '++' else 'h8', warn_nonexistent=False):
            break


@plugin.commands('luv', 'h8')
@plugin.example(".luv johnnytwothumbs")
@plugin.example(".h8 d-bag")
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def luv_h8_cmd(bot, trigger):
    if not trigger.group(3):
        bot.reply("No user specified.")
        return
    target = Identifier(trigger.group(3))
    luv_h8(bot, trigger, target, trigger.group(1))


def luv_h8(bot, trigger, target, which, warn_nonexistent=True):
    target = verified_nick(bot, target, trigger.sender)
    which = which.lower()  # issue #18
    pfx = change = selfreply = None  # keep PyCharm & other linters happy
    if not target:
        if warn_nonexistent:
            command = which
            try:  # because a simple "trigger.group('command') or which" doesn't work
                command = trigger.group('command')
            except IndexError:  # why can't you just return None, re.group()?
                pass
            bot.reply("You can only %s someone who is here." % command)
        return False
    if (
        not (trigger.admin and not bot.settings.rep.admin_cooldown)
        and rep_too_soon(bot, trigger.nick)
    ):
        return False
    if which == 'luv':
        selfreply = "No narcissism allowed!"
        pfx, change = 'in', 1
    if which == 'h8':
        selfreply = "Go to 4chan if you really hate yourself!"
        pfx, change = 'de', -1
    if not (pfx and change and selfreply):  # safeguard against leaving something in the above mass-None assignment
        bot.say("Logic error! Please report this to %s." % bot.config.core.owner)
        return
    if is_self(bot, trigger.nick, target):
        bot.reply(selfreply)
        return False

    possessive = 'my' if target == bot.nick else target + "'s"
    if bot.db.get_nick_value(target, 'rep_locked'):
        bot.reply("Sorry, %s reputation has been locked by an admin." % possessive)
        return False
    rep = mod_rep(bot, trigger.nick, target, change)
    bot.say("%s has %screased %s reputation score to %d" % (trigger.nick, pfx, possessive, rep))
    return True


@plugin.commands('rep')
@plugin.example(".rep johnnytwothumbs")
def show_rep(bot, trigger):
    target = trigger.group(3) or trigger.nick
    rep = get_rep(bot, target)
    if rep is None:
        bot.say("%s has no reputation score yet." % target)
        return
    bot.say("%s's current reputation score is %d." % (target, rep))


@plugin.commands('replock', 'repunlock')
@plugin.example('.replock BullyingVictim')
@plugin.require_admin('Only bot admins may manage reputation locks')
def manage_locks(bot, trigger):
    target = trigger.group(3)
    if not target:
        bot.reply("I need a nickname!")
        return
    if 'un' in trigger.group(1):  # .repunlock command used
        bot.db.set_nick_value(Identifier(target), 'rep_locked', False)
        bot.say("Unlocked rep for %s." % target)
    else:  # .replock command used
        bot.db.set_nick_value(Identifier(target), 'rep_locked', True)
        bot.say("Locked rep for %s." % target)


# helpers
def get_rep(bot, target):
    return bot.db.get_nick_value(Identifier(target), 'rep_score')


def set_rep(bot, caller, target, newrep):
    bot.db.set_nick_value(Identifier(target), 'rep_score', newrep)
    bot.db.set_nick_value(Identifier(caller), 'rep_used', time.time())


def mod_rep(bot, caller, target, change):
    rep = get_rep(bot, target) or 0
    rep += change
    set_rep(bot, caller, target, rep)
    return rep


def get_rep_used(bot, nick):
    return bot.db.get_nick_value(Identifier(nick), 'rep_used') or 0


def set_rep_used(bot, nick):
    bot.db.set_nick_value(Identifier(nick), 'rep_used', time.time())


def rep_used_since(bot, nick):
    now = time.time()
    last = get_rep_used(bot, nick)
    return abs(last - now)


def rep_too_soon(bot, nick):
    since = rep_used_since(bot, nick)
    cooldown = bot.settings.rep.cooldown
    if since < cooldown:
        bot.notice("You can change someone's rep again %s." % time_tools.seconds_to_human(-(cooldown - since)), nick)
        return True
    else:
        return False


def is_self(bot, nick, target):
    nick = Identifier(nick)
    target = Identifier(target)
    if nick == target:
        return True  # shortcut to catch common goofballs
    try:
        nick_id = bot.db.get_nick_id(nick, False)
        target_id = bot.db.get_nick_id(target, False)
    except ValueError:
        return False  # if either nick doesn't have an ID, they can't be in a group
    return nick_id == target_id


def verified_nick(bot, nick, channel):
    if not all([nick, channel]):
        # `bot` is always going to be a thing, but `nick` or `channel` could be empty
        # and that means verification should immediately fail
        return ''  # not None; see below

    nick = re.search(r_nick, nick).group(0)
    if not nick:
        return ''  # returning None would mean the returned value can't be compared with ==
    if nick not in bot.channels[channel].users:
        if nick.endswith('--'):
            if nick[:-2] in bot.channels[channel].users:
                return Identifier(nick[:-2])
        return ''  # see above
    return Identifier(nick)
