# -*- coding: utf-8 -*-

import re
from datetime import datetime
from zc.datetimewidget.datetimewidget import DateWidget
from zope.app.form.browser import textwidgets
from zope.datetime import parseDatetimetz
from zope.datetime import DateTimeError
from zope.app.form.interfaces import ConversionError
from zope.app.form.browser.i18n import _

DateWidget._format = '%d/%m/%Y'
customDate = re.compile('([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})$')


def _myToFieldValue(self, input):
    """
    Normal validator (parseDatetimetz) does not work because of french
    month names or french date formatting
    """
    dateVars = re.match(customDate, input)
    if input == self._missing:
        return self.context.missing_value
    elif dateVars:
        return datetime(int(dateVars.group(3)),
                        int(dateVars.group(2)),
                        int(dateVars.group(1)))
    else:
        try:
            # TODO: Currently datetimes return in local (server)
            # time zone if no time zone information was given.
            # Maybe offset-naive datetimes should be returned in
            # this case? (DV)
            return parseDatetimetz(input)
        except (DateTimeError, ValueError, IndexError), v:
            raise ConversionError(_("Invalid datetime data"), v)

textwidgets.DatetimeWidget._toFieldValue = _myToFieldValue
