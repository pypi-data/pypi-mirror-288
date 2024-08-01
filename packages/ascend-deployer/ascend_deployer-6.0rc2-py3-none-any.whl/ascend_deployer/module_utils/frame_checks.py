import os

from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util


class FrameCheck:

    def __init__(self, module, npu_info, error_messages):
        self.tags = module.params.get("tags")
        self.python_version = module.params.get("python_version")
        self.packages = module.params.get("packages")
        self.error_messages = error_messages
        self.npu_info = npu_info
        self.resources_dir = os.path.join(module.params.get("ascend_deployer_work_dir"), "resources")

    @check_event
    def check_torch(self):
        if self.npu_info.get("scene", "") == "a910b":
            self.check_kernels_910b()

        skip_tags = {"toolkit", "nnae", "pytorch_dev", "pytorch_run", "auto"}
        nnae_pkg = self.packages.get("nnae")
        toolkit_pkg = self.packages.get("toolkit")
        if skip_tags.intersection(set(self.tags)) and (nnae_pkg or toolkit_pkg):
            return

        toolkit_path = "/usr/local/Ascend/ascend-toolkit/set_env.sh"
        nnae_path = "/usr/local/Ascend/nnae/set_env.sh"
        if not os.path.exists(toolkit_path) and not os.path.exists(nnae_path):
            util.record_error("[ASCEND][ERROR] Please install toolkit or nnae before install pytorch.",
                              self.error_messages)

    def check_kernels_910b(self):
        # 1. Check whether kernels have been installed.
        toolkit_kernels_path = "/usr/local/Ascend/ascend-toolkit/latest/opp/built-in/op_impl/ai_core/tbe/kernel/ascend910b/"
        nnae_kernels_path = "/usr/local/Ascend/nnae/latest/opp/built-in/op_impl/ai_core/tbe/kernel/ascend910b/"
        if os.path.exists(toolkit_kernels_path) or os.path.exists(nnae_kernels_path):
            return
        # 2. Check whether the installed tags contain kernels, pytorch_dev, or pytorch_run.
        skip_tags = {"pytorch_dev", "pytorch_run", "kernels"}
        if skip_tags & set(self.tags):
            return
        # 3. Check whether the kernels package exists during installation in the auto scenario.
        kernels_pkg = self.packages.get("kernels")
        if "auto" in self.tags and kernels_pkg:
            return
        # 4. In other cases.
        util.record_error(
            "[ASCEND][ERROR] For Atlas A2 training series products, please install kernels before install pytorch.",
            self.error_messages)

    @check_event
    def check_tensorflow(self):
        if "3.10" in self.python_version:
            util.record_error("[ASCEND][ERROR] Tensorflow dose not support python3.10.* and above. "
                              "please use a earlier python version.", self.error_messages)

    @check_event
    def check_mindspore(self):
        if "3.10" in self.python_version:
            util.record_error("[ASCEND][ERROR] Mindspore dose not support python3.10.* and above. "
                              "please use a earlier python version.", self.error_messages)
