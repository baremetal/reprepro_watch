import logging
import os

from pyinotify import IN_CLOSE_WRITE, WatchManager, Notifier, ThreadedNotifier, ProcessEvent

from reprepro.changes import Changes
from reprepro.upload import Upload

class WatcherProcesEvent(ProcessEvent):
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.pop('logger', None) or logging.getLogger('WatcherProcesEvent')

        super(WatcherProcesEvent, self).__init__(*args, **kwargs)

    def process_IN_CLOSE_WRITE(self, event):
        path = os.path.join(event.path, event.name)

        # nothing to do if this is not the .changes file.
        if not event.name.endswith('.changes'):
            self.logger.debug('Ignoring %s' % (path,))

            return

        Upload(path, logger=self.logger).process()


class Watcher(object):
    def __init__(self, incoming_path, logger=None):
        self.incoming_path = incoming_path
        self.logger = logger or logging.getLogger('Watcher')

        self.wm = WatchManager()
        mask = IN_CLOSE_WRITE # watched events

        self.event_processor = WatcherProcesEvent(logger=self.logger)
        self.notifier = Notifier(self.wm, self.event_processor)
        wdd = self.wm.add_watch(self.incoming_path, mask, rec=True)

    def loop(self):
        """
        Check for inotify events and process then when found.

	Note, check_events() below is blocking and the loop will not complete
        until an event that is being listened for occurs.
        """
        if self.notifier.check_events():
            # read notified events and enqeue them
            self.notifier.read_events()

        # process the queue of events
        self.notifier.process_events()

    def stop(self):
         # destroy the inotify's instance on this interrupt (stop monitoring)
         self.notifier.stop()
