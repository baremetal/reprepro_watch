import logging
import os

from sh import ErrorReturnCode, reprepro as reprepro_sh
from shutil import move

from reprepro.changes import Changes

class Upload(object):
    def __init__(self, path, logger=None):
        self.logger = logger or logging.getLogger('Upload')
        self.path = path

        self.logger.debug('Path: %s' % (self.path,))

        self.changes = Changes(self.path)

    def cleanup(self):
        """
        """

        incoming_path = os.path.dirname(self.path)
        repository_root = os.path.dirname(incoming_path)
        processed_path = os.path.join(repository_root, 'processed')

        # move the changes file itself
        dest_path = os.path.join(processed_path, os.path.basename(self.path))
        self.move(self.path, dest_path)

        # move all the files referenced in the changes file
        for changes_file in self.changes.files:
            src_path = os.path.join(incoming_path, changes_file.filename)
            dest_path = os.path.join(processed_path, changes_file.filename)

            self.move(src_path, dest_path)

    def move(self, src, dest):
        self.logger.debug('Moving %s to %s' % (src, dest))
        move(src, dest)

    def process(self):
        """
        Process the specified .changes file using the reprepro command
        """

        try:
            self.run_reprepro()
        except Exception, exc:
            self.logger.exception(exc)
        finally:
            self.cleanup()

    def run_reprepro(self):
        repository_base = os.path.dirname(os.path.dirname(self.path))

        self.logger.info("Processing: %s" % (self.path,))

        distribution = self.changes['Distribution']

        try:
            for line in reprepro_sh("-b", repository_base, "include", distribution, self.path, _iter=True):
                self.logger.debug(line)
        except ErrorReturnCode, exc:
            error_message = exc.stderr.strip()
            self.logger.error('Error running reprepro command: %s' % (error_message,))

        self.logger.info("Completed: %s" % (self.path,))
