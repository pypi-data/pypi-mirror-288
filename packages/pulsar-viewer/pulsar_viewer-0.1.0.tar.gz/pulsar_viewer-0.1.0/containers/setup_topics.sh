set -e
set -x

TENANT=tests
NS=integration
TOPIC=pulsar-poller-tests
ADMIN_URL="http://pulsar:8080"

# workaround for flaky cluster healthcheck
sleep 5

# Create the tenant.
bin/pulsar-admin --admin-url $ADMIN_URL tenants create $TENANT

# Create the namespace.
# Prevents reader errors when there are no messages.
bin/pulsar-admin --admin-url $ADMIN_URL namespaces create $TENANT/$NS

# Set infinite retention for the topics under public/default.
# Prevents messages disappearing from history if there are no subscribers.
bin/pulsar-admin --admin-url $ADMIN_URL namespaces set-retention --size=-1 --time=-1 $TENANT/$NS

# Create the topic.
# Prevents reader errors when there are no messages.
bin/pulsar-admin --admin-url $ADMIN_URL topics create "persistent://$TENANT/$NS/$TOPIC"
