# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_helloworld
# Purpose:      To learn spiderfoot API
#
# Author:      Conner 'rediacc' Baughman conbau15@gmail.com
#
# Created:     15/4/2016
# Copyright:   (c) Conner Baughman 2016
# Licence:     GPL
# -------------------------------------------------------------------------------

from sflib import SpiderFoot, SpiderFootPlugin, SpiderFootEvent
import urllib
import json as m_json


class sfp_helloworld(SpiderFootPlugin):
    """Helloworld:Investigate:Does not do anything at the moment."""

    # Default options
    opts = {"pages": 1,
	    "fetchlinks": True
 }

    # Option descriptions
    optdescs = {
        "pages": "Number of pages to go through",
	"fetchlinks": True
    }

    # Be sure to completely clear any class variables in setup()
    # or you run the risk of data persisting between scan runs.

    # Target
    results = list()

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = list()

        for opt in userOpts.keys():
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    # * = be notified about all events.
    def watchedEvents(self):
        return ["INTERNET_NAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["SEARCH_ENGINE_WEB_CONTENTS"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data
        # If you are processing TARGET_WEB_CONTENT from sfp_spider, this is how you 
        # would get the source of that raw data (e.g. a URL.)
        # eventSource = event.sourceEvent.data

        self.sf.debug("Received event, " + eventName + ", from " + srcModuleName)

	pages = self.sf.googleIterate("site:" + eventData, dict(limit=self.opts['pages'],
                                                               useragent=self.opts['_useragent'],
                                                               timeout=self.opts['_fetchtimeout']))

    		

        # Notify other modules of what you've found
        evt = SpiderFootEvent("SEARCH_ENGINE_WEB_CONTENTS", 'Google results:', self.__name__, event)
        self.notifyListeners(evt)

    # If you intend for this module to act on its own (e.g. not solely rely
    # on events from other modules, then you need to have a start() method
    # and within that method call self.checkForStop() to see if you've been
    # politely asked by the controller to stop your activities (user abort.)

# End of sfp_XXX class
