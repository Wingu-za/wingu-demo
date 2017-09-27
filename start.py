#!/usr/bin/python
from keystoneauth1 import loading
from keystoneauth1 import session
from heatclient import client as heatclient
from neutronclient.v2_0 import client as neutronclient

from config import AUTH_URL, USERNAME, PASSWORD, PROJECT_ID

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=AUTH_URL,
                                username=USERNAME,
                                password=PASSWORD,
                                project_id=PROJECT_ID)
sess = session.Session(auth=auth)
heat = heatclient.Client('1', session=sess)
neutron = neutronclient.Client(session=sess)


stack_name = "testing_demo"

# Create Stack and Launch
print("Creating Stack")
try:
    heat.stacks.create(stack_name=stack_name,
                       template_url="https://raw.githubusercontent.com/TachyonProject/wingu-demo/master/demo.hot",
                       password=PASSWORD)
except Exception as e:
    print e


# Find Stack ID
stacks = heat.stacks.list()
for stack in stacks:
    if stack.stack_name == stack_name:
        stack_id = stack.id

# Find Floating IP(s) assosciate to stack resources.
print("Floating IP Addresses:")
resources = heat.resources.list(stack_id)
for resource in resources:
    if resource.resource_type == 'OS::Neutron::FloatingIP':
        ip = neutron.show_floatingip(resource.physical_resource_id)
        print("    * %s" %
              ip['floatingip']['floating_ip_address'])

# Delete Stack
#heat.stacks.delete(stack_id)
