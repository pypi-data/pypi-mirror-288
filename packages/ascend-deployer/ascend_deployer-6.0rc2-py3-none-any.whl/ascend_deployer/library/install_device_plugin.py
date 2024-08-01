#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ===========================================================================
import os.path

from ansible.module_utils.dl import Installer
from ansible.module_utils import common_info


class DevicePluginInstaller(Installer):
    component_name = 'device-plugin'
    secret_for_harbor = 'kube-system-secret-for-harbor'

    def __init__(self):
        super(DevicePluginInstaller, self).__init__()
        self.all_yaml_files = []

    def get_yaml_path(self):
        yaml_files = []
        for root, _, files in os.walk(self.extract_dir):
            for filename in files:
                if filename.endswith('.yaml') and "1usoc" not in filename and "volcano" in filename:
                    yaml_files.append(os.path.join(root, filename))
        if not yaml_files:
            self.module.fail_json('failed to find the yaml about volcano in {}'.format(self.extract_dir))
        self.all_yaml_files.extend(sorted(yaml_files, reverse=self.use_new_k8s))
        return yaml_files[0]

    def get_modified_yaml_contents(self, yaml_file_path):
        lines = []
        image_tags = self.get_image_tags()
        with open(yaml_file_path) as f:
            if not self.use_harbor:
                return f.readlines()
            for line in f:
                for image_tag in image_tags:
                    if image_tag in line:
                        new_image_tag = '{}/{}/{}'.format(self.harbor_server, self.harbor_mindx_project, image_tag)
                        line = line.replace(image_tag, new_image_tag)
                        self.module.log(msg='replace image: {} to {}'.format(image_tag, new_image_tag))
                if 'imagePullPolicy: Never' in line:
                    line = line.replace('Never', 'IfNotPresent')
                if 'containers:' in line:
                    prefix = line.index('containers:') * ' '
                    lines.append('{}imagePullSecrets:\n'.format(prefix))
                    lines.append('{}  - name: {}\n'.format(prefix, self.secret_for_harbor))
                lines.append(line)

        return lines

    def get_labels(self):
        labels = []
        if self.arch == 'x86_64':
            labels.append('host-arch=huawei-x86')
        else:
            labels.append('host-arch=huawei-arm')
        for line in self.iter_cmd_output('lspci'):
            if 'Processing accelerators' in line:
                if 'Device d100' in line:
                    labels.append('accelerator=huawei-Ascend310')
                if 'Device d500' in line:
                    labels.append('accelerator=huawei-Ascend310P')
                if 'Device d801' in line or 'Device d802' in line:
                    labels.append('accelerator=huawei-Ascend910')
        card_nums = 0
        npu_id = '0'
        chip_id = '0'
        for line in self.iter_cmd_output('npu-smi info -m'):
            if 'Ascend' in line and line.split(None, 2) == 3:
                card_nums += 1
                if card_nums == 1:
                    npu_id, chip_id, _ = line.split(None, 2)
        board_id = ''
        for line in self.iter_cmd_output('npu-smi info -t board -i {} -c {}'.format(npu_id, chip_id)):
            if 'Board' in line and ':' in line:
                board_id = line.strip().split(':')[1].strip().lower()
                break
        if board_id in common_info.Atlas_800:
            if card_nums == 8:
                labels.append('accelerator-type=module')
            elif card_nums == 4:
                labels.append('accelerator-type=half')
        elif board_id in common_info.Atlas_800_A2 + common_info.Atlas_900_A2_PoD:
            labels.append('accelerator-type=module-910b-8')
        elif board_id in common_info.Atlas_200T_A2_Box16:
            labels.append('accelerator-type=module-910b-16')
        elif board_id in common_info.Atlas_300T:
            labels.append('accelerator-type=card')
        elif board_id in common_info.Atlas_300T_A2:
            labels.append('accelerator-type=card-910b-2')
        return labels

    def create_log_dir(self):
        """ do jobs such as creating log dir and logrotate file """
        log_path = os.path.join(self.dl_log, "devicePlugin")
        if not os.path.exists(log_path):
            os.makedirs(log_path, 0o750)
            os.chown(log_path, self.user_id, self.group_id)

    def apply_yaml(self):
        if not os.path.exists(self.yaml_dir):
            os.makedirs(self.yaml_dir, 0o755)
        for yaml_file in self.all_yaml_files:
            device_met = False
            for device_labels in self.labels.get('worker_labels', []):
                device_type = device_labels.replace("accelerator=huawei-Ascend", "")
                if device_type == "910" and "device-plugin-volcano" in yaml_file:
                    device_met = True
                    break
                if device_type + '-volcano' in yaml_file:
                    device_met = True
                    break
            if not device_met:
                continue
            basename = os.path.basename(yaml_file)
            yaml_path = os.path.join(self.yaml_dir, basename)
            with open(yaml_path, 'w') as f:
                f.writelines(self.get_modified_yaml_contents(yaml_file))
            cmd = 'kubectl apply -f {}'.format(yaml_path)
            self.module.run_command(cmd, check_rc=True)
            self.module.log(msg='apply yaml: {} for component: {}'.format(yaml_path, self.component_name))

    def create_pull_secret(self):
        create_namespace_cmd = 'kubectl create namespace kube-system'
        create_secret_cmd = 'kubectl create secret generic {} ' \
                            '--from-file=.dockerconfigjson=/root/.docker/config.json ' \
                            '--type=kubernetes.io/dockerconfigjson' \
                            ' -n kube-system'.format(self.secret_for_harbor)
        self.module.run_command(create_namespace_cmd)
        self.module.run_command(create_secret_cmd)


if __name__ == '__main__':
    DevicePluginInstaller().run()
