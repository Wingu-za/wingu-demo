#!/usr/bin/python
from keystoneauth1 import loading
from keystoneauth1 import session
from heatclient import client as heatclient
from neutronclient.v2_0 import client as neutronclient

from config import AUTH_URL, USERNAME, PASSWORD, PROJECT_ID, STACKNAME

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=AUTH_URL,
                                username=USERNAME,
                                password=PASSWORD,
                                project_id=PROJECT_ID)
sess = session.Session(auth=auth)
heat = heatclient.Client('1', session=sess)
neutron = neutronclient.Client(session=sess)


# Find Stack ID
stacks = heat.stacks.list()
for stack in stacks:
    if stack.stack_name == STACKNAME:
        stack_id = stack.id

# Delete Stack
heat.stacks.delete(stack_id)
