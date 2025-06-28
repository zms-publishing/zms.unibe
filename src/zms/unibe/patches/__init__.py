# invoked by etc/site.zcml applying src/zms/unibe/patches/configure.zcml
# <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />

# initialize monkey patches on zope startup
from zms.unibe.patches.monkey import getFuncDetails
from zms.unibe.patches.monkey import tcp_vote

# initialize security assertions on zope startup
from zms.unibe.patches.security import assertations
