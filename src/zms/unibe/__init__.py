# initialize patches and security assertions on zope startup
# invoked by etc/site.zcml applying src/zms/unibe/configure.zcml
# <include zcml:condition="installed zms.unibe" package="zms.unibe" />

from zms.unibe.patches.monkey import getFuncDetails
from zms.unibe.patches.monkey import tcp_vote

from zms.unibe.agenda import OutlookConnector
from zms.unibe.agenda import AgendaBridge
