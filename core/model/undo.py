# Copyright 2019 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from core.model._ccore import UndoStep
from core.util import extract

class Action:
    """A unit of change that can be undone and redone.

    In here, we store changes that happened to a document in the form of sets
    containing instances.  These set's are not documented individually to
    reduce verbosity, but there's 3 types (``added``, ``changed`` and
    ``deleted``) of sets for each supported instance (``accounts``,
    ``transactions``, ``schedules``).

    For ``added`` and ``deleted``, it's rather easy. The set contains instances directly. For
    ``change``, it's different. The set contains 2-sized tuples ``(instance, backup)``. Whenever
    we're about to make a change to something, we copy it first and store that backup. Then, when
    we undo our action, we can use our backup.

    To create an action, you can operate on set attributes directly for ``added`` and ``deleted``,
    but you should use convenience method for ``changed``. They perform the copying for you.

    :param str description: A description of the action which will be shown to the user. Example:
                            "Add Transaction", which will show as "Undo Add Transaction".
    """
    def __init__(self, description):
        self.description = description
        self.added_accounts = set()
        self.changed_accounts = set()
        self.deleted_accounts = set()
        self.added_transactions = set()
        self.changed_transactions = set()
        self.deleted_transactions = set()
        self.added_schedules = set()
        self.changed_schedules = set()
        self.deleted_schedules = set()

    def change_accounts(self, accounts):
        """Record imminent changes to ``accounts``."""
        self.changed_accounts |= set(accounts)

    def change_schedule(self, schedule):
        """Record imminent changes to ``schedule``."""
        self.changed_schedules.add(schedule)

    def change_transactions(self, transactions, schedules):
        """Record imminent changes to ``transactions``.

        If any of the transactions are a :class:`.Spawn`, also record a change to their related
        schedule.
        """
        spawns, normal = extract(lambda t: t.is_spawn, transactions)
        for t in normal:
            self.changed_transactions.add(t)
        for spawn in spawns:
            for schedule in schedules:
                if schedule.contains_spawn(spawn):
                    self.change_schedule(schedule)

    def change_entries(self, entries, schedules):
        """Record imminent changes to ``entries``."""
        self.change_transactions({e.transaction for e in entries}, schedules)


class Undoer:
    """Manages undo/redo operation for a document.

    Note: We hold references to all those instance collections passed during initialization rather
    than the :class:`.Document` itself to avoid circular references. But yes, initialisation
    arguments must come straight from document attributes.

    How it works is that it holds a list of :class:`.Action` and a pointer to our current action
    (most of the time, it's the last action). When we undo or redo an action, we use the information
    we has stored in our action and make proper modifications, then move our action index.
    """
    def __init__(self, accounts, transactions, scheduled):
        self._actions = []
        self._accounts = accounts
        self._transactions = transactions
        self._scheduled = scheduled
        self._index = -1
        self._save_point = None

    # --- Private
    def _do_adds(self, schedules):
        for schedule in schedules:
            self._scheduled.append(schedule)

    def _do_deletes(self, schedules):
        for schedule in schedules:
            self._scheduled.remove(schedule)

    # --- Public
    def can_redo(self):
        """Whether we can redo.

        In other words, whether we have at least one action and that our current action pointer
        isn't pointing on the last one.
        """
        return self._index < -1

    def can_undo(self):
        """Whether we can undo.

        In other words, whether we have at least one action that hasn't been undone already.
        """
        return -self._index <= len(self._actions)

    def clear(self):
        """Clear our action list."""
        self._actions = []

    def undo_description(self):
        """Textual description of the action to be undone next."""
        if self.can_undo():
            return self._actions[self._index].description

    def redo_description(self):
        """Textual description of the action to be redone next."""
        if self.can_redo():
            return self._actions[self._index + 1].description

    def set_save_point(self):
        """Specify at which point we saved last.

        This allows us to determine whether the document should be considered :attr:`modified`.

        Call this method whenever the document is saved.
        """
        self._save_point = self._actions[-1] if self._actions else None

    def record(self, action):
        """Record an action and add it to the list.

        If we're not currently pointing at the end of the list (if we have undone actions before
        recording our new action), discard all actions following the current one before recording
        our new action.

        :param action: Action to be recorded.
        :type action: :class:`Action`
        """
        action.undostep = UndoStep(
            action.added_accounts,
            action.deleted_accounts,
            action.changed_accounts,
            action.added_transactions,
            action.deleted_transactions,
            action.changed_transactions,
            list(action.changed_schedules))
        if self._index < -1:
            self._actions = self._actions[:self._index + 1]
        self._actions.append(action)
        self._index = -1

    def undo(self):
        """Undo the next action to be undone.

        If our last action was :meth:`record`, then we undo that action. If it was :meth:`undo`,
        then we undo the action that came before it. If it was :meth:`redo`, then we re-undo that
        action and decrease our pointer to the previous action.

        Make sure you can call this with :meth:`can_undo` first.
        """
        assert self.can_undo()
        action = self._actions[self._index]
        action.undostep.undo(self._accounts, self._transactions)
        self._do_adds(action.deleted_schedules)
        self._do_deletes(action.added_schedules)
        self._transactions.clear_cache()
        self._index -= 1

    def redo(self):
        """Redo the next action to be redone.

        This can only be performed if we've done :meth:`undo` before. We redo that action and
        increase our pointer to the next action.

        Make sure you can call this with :meth:`can_redo` first.
        """
        assert self.can_redo()
        action = self._actions[self._index + 1]
        action.undostep.redo(self._accounts, self._transactions)
        self._do_adds(action.added_schedules)
        self._do_deletes(action.deleted_schedules)
        self._transactions.clear_cache()
        self._index += 1

    # --- Properties
    @property
    def modified(self):
        """Whether we can consider our document modified.

        A document is modified if the current action pointer doesn't point to the same action as
        when :meth:`set_save_point` was last called.
        """
        return self._save_point is not self._actions[self._index] if self.can_undo() else self._save_point is not None

