#!/usr/bin/python

# Copyright (c) 2024, CreativeFlow
#
# This is an example of a custom Ansible module.
# Custom modules extend Ansible's core functionality. They can be written
# in any language that can return JSON, but Python is the most common.
# Place custom modules in the `library/` directory of your project.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: custom_module_example

short_description: An example custom Ansible module.

version_added: "1.0.0"

description:
    - This module is for demonstration purposes.
    - It takes a name and a boolean as input.
    - It returns a greeting message.

options:
    name:
        description: The name to include in the greeting.
        required: true
        type: str
    is_friendly:
        description: If set to true, the greeting will be friendly.
        required: false
        type: bool
        default: false

author:
    - CreativeFlow Developer (@creativeflow)
'''

EXAMPLES = r'''
# Pass in a name
- name: Test with a name
  custom_module_example:
    name: 'World'

# Pass in a name and make it friendly
- name: Test with a friendly greeting
  custom_module_example:
    name: 'Ansible'
    is_friendly: true
'''

RETURN = r'''
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'World'
message:
    description: The greeting message that was generated.
    type: str
    returned: always
    sample: 'Goodbye, World!'
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        is_friendly=dict(type='bool', default=False)
    )

    # seed the result dictionary that will be returned from this module
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # This includes instantiation, handling arguments, exiting with results, and logging.
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with --check or --diff, we don't need to do anything
    # since this module doesn't make any changes to the system
    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['name']
    
    if module.params['is_friendly']:
        result['message'] = 'Hello, ' + module.params['name'] + '!'
    else:
        result['message'] = 'Goodbye, ' + module.params['name'] + '!'

    # in our case, the module is not idempotent as it does not make any changes
    # to the system. We just want to see the output.
    # However, if we were creating a file, we would set changed=True
    # if the file was created or modified.
    
    # use whatever logic you need to determine whether or not this module
    # made any actual changes to your target
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested a failure', **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()