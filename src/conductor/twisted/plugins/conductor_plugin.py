from twisted.application.service import ServiceMaker

conductor = ServiceMaker(
    'logstore conductor', 'logstore.conductor.tap', 'Run the logstore conductor', 'logstore-conductor')