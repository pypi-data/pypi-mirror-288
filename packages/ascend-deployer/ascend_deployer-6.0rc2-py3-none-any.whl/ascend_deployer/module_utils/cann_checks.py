import glob
import os

from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util


class CANNCheck:
    def __init__(self, module, npu_info, error_messages):
        self.module = module
        self.tags = module.params.get("tags")
        self.resource_dir = os.path.join(module.params.get("ascend_deployer_work_dir"), "resources")
        self.python_version = module.params.get("python_version")
        self.packages = module.params.get("packages")
        self.npu_info = npu_info
        self.error_messages = error_messages

    @check_event
    def check_kernels(self):
        if self.npu_info.get("scene") == "infer":
            util.record_error("[ASCEND][ERROR] kernels not support infer scene", self.error_messages)
            return

        kernels_pkg = self.packages.get("kernels")
        if not kernels_pkg:
            util.record_error("[ASCEND][ERROR] Do not find kernels package, please download kernels package first.",
                              self.error_messages)
            return

        skip_tags = {"toolkit", "nnae", "auto", "dl", "pytorch_dev", "pytorch_run",
                     "tensorflow_dev", "tensorflow_run", "mindspore_scene", "offline_dev"}
        nnae_pkg = self.packages.get("nnae")
        toolkit_pkg = self.packages.get("toolkit")
        if skip_tags.intersection(set(self.tags)) and (nnae_pkg or toolkit_pkg):
            return

        script_info = os.path.basename(kernels_pkg).split("_")
        if len(script_info) < 2:
            util.record_error("[ASCEND][ERROR] Do not find kernels package, please download kernels package first.",
                              self.error_messages)
            return
        kernels_version = os.path.basename(kernels_pkg).split("_")[1]
        if (not glob.glob("/usr/local/Ascend/*/{}/*/ascend_toolkit_install.info".format(kernels_version))
                and not glob.glob("/usr/local/Ascend/*/{}/ascend_nnae_install.info".format(kernels_version))):
            util.record_error("[ASCEND][ERROR] Please install toolkit or nnae before install kernels",
                              self.error_messages)

    def check_driver_installation(self):
        ascend_info_path = "/etc/ascend_install.info"
        if not os.path.isfile(ascend_info_path):
            return
        with open(ascend_info_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "Driver_Install_Path_Param" not in line:
                    continue
                driver_install_path = line.split("=")[-1].strip()
                if not os.path.isfile(os.path.join(driver_install_path, "driver/version.info")):
                    util.record_error("[ASCEND][ERROR] The /etc/ascend_install.info file exists in the environment, "
                                      "and the file records the driver installation path. However, "
                                      "the driver/version.info does not exist in the installation path. "
                                      "Please check the driver is correctly installed.", self.error_messages)
                    return

    def check_cann_install_path_permission(self):
        install_path = "/usr/local/Ascend"
        if not os.path.isdir(install_path):
            return
        if os.stat(install_path).st_uid != 0:
            util.record_error("[ASCEND][ERROR] The owner of the cann installation dir "
                              "'/usr/local/Ascend' must be root, change the owner to root", self.error_messages)
            return

        mode = os.stat(install_path).st_mode
        permissions = oct(mode)[-3:]
        if int(permissions) != 755:
            util.record_error("[ASCEND][ERROR] When installing cann, the user and group of the installation path "
                              "must be root, and the permission must be 755. ", self.error_messages)
        return

    @check_event
    def check_cann_basic(self):
        self.check_driver_installation()
        self.check_cann_install_path_permission()

    @check_event
    def check_tfplugin(self):
        if "3.10." in self.python_version:
            util.record_error("[ASCEND][ERROR] Tfplugin dose not support python3.10.* and above. "
                              "please use a earlier python version.", self.error_messages)
