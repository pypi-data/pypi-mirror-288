#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import os

from ansible.module_utils.basic import AnsibleModule

MAX_CIRCLES = 8


class KubeProxyConfig(object):

    def __init__(self):
        self.module = AnsibleModule(argument_spec=dict(node_name=dict(type="str", required=True)))
        self.node_name = self.module.params.get("node_name")
        self.proxy_config_path = "/root/temp_proxy_config.yaml"
        self.ipvs_modules = "/etc/sysconfig/modules/ipvs.modules"
        self.ipvs_modules_dir = "/etc/sysconfig/modules"

    def run(self):
        # 获取kube-proxy配置内容
        content = self.get_proxy_config_content()
        # 将更新后的内容写入临时文件
        with open(self.proxy_config_path, "w") as f:
            f.writelines(content)

        # 生效kube-proxy配置
        self.module.run_command("kubectl apply -f {}".format(self.proxy_config_path))
        # 生成ipvs.module文件
        self.create_ipvs_modules()
        self.module.run_command("chmod 755 {}".format(self.ipvs_modules))
        self.module.run_command("bash {}".format(self.ipvs_modules))
        self.module.run_command("lsmod | grep -e ip_vs -e nf_conntrack".format(self.ipvs_modules), use_unsafe_shell=True)

        # 重启kube-proxy
        cmd = 'kubectl get pods -A --field-selector spec.nodeName={}'.format(self.node_name)
        rc, out, err = self.module.run_command(cmd)
        if rc or err or not out:
            self.module.fail_json(msg='failed to run cmd: {}, err: {}'.format(cmd, err))
        for line in out.splitlines():
            if "kube-proxy" not in line:
                continue
            namespace, name, _ = line.split(None, 2)
            delete_cmd = 'kubectl delete pod -n {} {} --force --grace-period 0'.format(namespace, name)
            self.module.run_command(delete_cmd, check_rc=True)
        # 清除临时文件
        os.unlink(self.proxy_config_path)
        return self.module.exit_json(rc=0, changed=True)

    def get_proxy_config_content(self):
        if os.path.isfile(self.proxy_config_path):
            os.unlink(self.proxy_config_path)
        with open(self.proxy_config_path, "w"):
            pass
        set_mode = "kubectl get cm -n kube-system kube-proxy -o yaml > {}".format(self.proxy_config_path)
        self.module.run_command(set_mode, use_unsafe_shell=True)
        lines = []
        with open(self.proxy_config_path, "r") as f:
            content = f.readlines()
            for line in content:
                if line.strip().startswith("mode:"):
                    lines.append("    mode: \"ipvs\"\n")
                    continue
                lines.append(line)
        return lines

    def create_ipvs_modules(self):
        if not os.path.isdir(self.ipvs_modules_dir):
            os.makedirs(self.ipvs_modules_dir)
        if os.path.isfile(self.ipvs_modules):
            os.unlink(self.ipvs_modules)

        content = ("#!/bin/bash\nmodprode -- ip_vs\nmodprode -- ip_vs_rr\nmodprode -- ip_vs_wrr\n"
                   "modprode -- ip_vs_sh\nmodprode -- nf_conntrack\n")
        with open(self.ipvs_modules, "w") as f:
            f.write(content)


if __name__ == '__main__':
    KubeProxyConfig().run()

