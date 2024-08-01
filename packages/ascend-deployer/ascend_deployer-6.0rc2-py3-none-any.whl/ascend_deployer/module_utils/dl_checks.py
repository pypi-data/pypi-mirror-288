import os

from ansible.module_utils.check_output_manager import check_event

from ansible.module_utils.check_utils import CheckUtil as util
from ansible.module_utils.check_utils import CallCmdException

GB = 1024 * 1024 * 1024


class DLCheck:
    k8s_extra_space = 6 * GB
    dl_extra_space = 12 * GB
    throttle = 0.70

    def __init__(self, module, error_messages):
        self.master_group = module.params.get("master_groups")
        self.kube_vip = module.params.get("kube_vip")
        self.pod_network_cidr = module.params.get("pod_network_cidr")
        self.current_hostname = module.params.get("current_hostname")
        self.k8s_api_server_ip = module.params.get("k8s_api_server_ip")
        self.kube_interface = module.params.get("kube_interface")
        self.worker_group = module.params.get("worker_groups")
        self.host_info = module.params.get("host_info")
        self.error_messages = error_messages

    def check_space_available(self):
        sv = os.statvfs('/')
        total = (sv.f_blocks * sv.f_frsize)
        used = (sv.f_blocks - sv.f_bfree) * sv.f_frsize
        usage = float(used + self.k8s_extra_space + self.dl_extra_space) / (total or 1)
        if usage > self.throttle:
            total_gb = "{:.2f}".format(total / GB)
            used_gb = "{:.2f}".format(used / GB)
            usage = "{:.2f}".format(usage)
            msg = 'Insufficient available remaining disk space for Docker containers, filesystems, or root ' \
                  'directories. Total disk space: {} GB, used disk space: {} GB. After installation, the disk ' \
                  'usage: {}, should be below {}'.format(total_gb, used_gb, usage, self.throttle)
            util.record_error(msg, self.error_messages)

    def check_inventory(self):
        master_cnt = len(self.master_group)
        if master_cnt == 0:
            util.record_error(
                "[ASCEND][ERROR] The master node configuration information is missing,"
                " please configure the master node info. For details about the master node configuration,"
                " see the user guide.", self.error_messages)
            return

        if master_cnt % 2 == 0:
            util.record_error("[ASCEND][ERROR] the number of Master nodes must be an odd number, "
                              "for example, 1, 3, 5 ,7. Please modify the master nodes configuration.",
                              self.error_messages)
            return
        if master_cnt > 1 and not self.kube_vip:
            util.record_error("[ASCEND][ERROR] When the number of master nodes is greater than 1, "
                              "KUBE_VIP must be configured, for details about the field, see the user guide."
                              , self.error_messages)
            return

        pod_ip_ls = self.pod_network_cidr.split(".")
        if len(pod_ip_ls) != 4:
            util.record_error("[ASCEND][ERROR] Incorrect pod_network_cidr configuration, "
                              "for details about the field, see the user guide.", self.error_messages)
            return
        pod_ip_pre = ".".join(pod_ip_ls[:2])

        if self.current_hostname in self.master_group:
            if not self.k8s_api_server_ip:
                util.record_error("[ASCEND][ERROR] The master node configuration must contain k8s_api_server_ip. "
                                  "Set k8s_api_server_ip. For details about the field, see the user guide.",
                                  self.error_messages)
                return
            try:
                out = util.run_cmd('ip a')
            except CallCmdException as err:
                util.record_error("[ASCEND][[ERROR]] {}".format(str(err)), self.error_messages)
                return
            ip_info = out.decode("utf-8")
            if self.k8s_api_server_ip not in ip_info:
                util.record_error("[ASCEND][ERROR] Ensure that the value of k8s_api_server_ip "
                                  "in the master node configuration information is an existing IP in the system. "
                                  "Please modify the value of k8s_api_server_ip. "
                                  "For details about the field, see the user guide.", self.error_messages)
                return
            if len(self.master_group) > 1 and self.kube_interface and self.kube_interface not in ip_info:
                util.record_error("[ASCEND][ERROR] The kube_interface must be a exists network "
                                  "interface on master node", self.error_messages)
                return
            k8s_ip_pre = ".".join(self.k8s_api_server_ip.split(".")[:2])
            if k8s_ip_pre == pod_ip_pre:
                util.record_error("[ASCEND][ERROR] Ensure that k8s_api_server_ip and "
                                  "pod_network_cidr are in different network segments. Please change "
                                  "POD_NETWORK_CIDR to other private network, for example 10.0.0.0/16",
                                  self.error_messages)
                return
        if self.current_hostname in self.worker_group:
            curr_ip_pre = ".".join(self.current_hostname.split(".")[:2])
            if curr_ip_pre == pod_ip_pre:
                util.record_error("[ASCEND][ERROR] Ensure that k8s_api_server_ip and "
                                  "pod_network_cidr are in different network segments. Please change "
                                  "POD_NETWORK_CIDR to other private network, for example 10.0.0.0/16",
                                  self.error_messages)
        # 找到 worker_group 中不存在于 master_group 的节点, 检查该节点是否配置k8s_api_server_ip
        unique_to_worker = [node for node in self.worker_group if node not in self.master_group]
        for worker in unique_to_worker:
            if self.host_info.get(worker, {}).get('k8s_api_server_ip'):
                util.record_error(
                    "[ASCEND][ERROR] k8s_api_server_ip cannot be configured on worker nodes {}".format(worker),
                    self.error_messages)

    @check_event
    def check_dl_basic(self):
        self.check_space_available()
        self.check_inventory()

    @check_event
    def check_dns(self):
        dns_file = "/etc/resolv.conf"
        if not os.path.exists(dns_file):
            util.record_error("[ASCEND][ERROR] Please config the DNS before install DL", self.error_messages)
            return
        with open(dns_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "nameserver" in line:
                    return
            util.record_error("[ASCEND][ERROR] Please config the DNS before install DL", self.error_messages)
