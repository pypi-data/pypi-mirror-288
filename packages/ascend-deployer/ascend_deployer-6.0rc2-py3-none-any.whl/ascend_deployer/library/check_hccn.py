import os

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util
from ansible.module_utils.check_utils import CallCmdException

CARD_CODE_MAP = {"310p": "d500", "910": "d801", "910b": "d802"}


class HccnCheck:

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                device_ips=dict(type='str', required=False)
            ))
        self.device_ips = self.module.params.get("device_ips")
        self.card = util.get_card()
        self.error_messages = []

    @check_event
    def check_hccn(self):
        code = CARD_CODE_MAP.get(self.card)
        if not code:
            return
        cmd = "lspci | grep {}".format(code)
        try:
            out = util.run_cmd(cmd, util.GREP_RETURN_CODE)
        except CallCmdException as err:
            util.record_error("[ASCEND][[ERROR]] {}".format(str(err)))
            return
        if len(out.splitlines()) != len(self.device_ips.split(",")):
            util.record_error(
                "[ASCEND][ERROR] The number of deviceip is inconsistent with the number of NPU in position. "
                "Please check whether the NPU cards are in position or whether deviceip "
                "in inventory_file is correctly configured.", self.error_messages)

    def run(self):
        self.check_hccn()
        if self.error_messages:
            return self.module.fail_json('\n'.join(self.error_messages))
        self.module.exit_json(changed=True, rc=0)


if __name__ == '__main__':
    HccnCheck().run()
