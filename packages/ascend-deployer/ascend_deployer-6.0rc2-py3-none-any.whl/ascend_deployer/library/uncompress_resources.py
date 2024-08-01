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
import getpass
import glob
import os
import platform
import pwd
import shutil
import tarfile

from ansible.module_utils.basic import AnsibleModule


class UncompressResources(object):
    mapping = {
        'ascend-device-plugin': 'device-plugin',
        'ascend-operator': 'ascend-operator',
        'clusterd': 'clusterd',
        'hccl-controller': 'hccl-controller',
        'noded': 'noded',
        'npu-exporter': 'npu-exporter',
        'resilience-controller': 'resilience-controller',
        'volcano': 'volcano',
    }

    def __init__(self):
        self.module = AnsibleModule(argument_spec=dict(
            resources_dir=dict(type='str', required=True),
            tags=dict(type='list'),
        ))
        self.resources_dir = os.path.expanduser(self.module.params['resources_dir'])
        self.tags = self.module.params['tags']
        self.arch = platform.machine()

    def clear(self, pkg_list):
        if pkg_list:
            self.module.log('dependence is installed, clear files: {}'.format(pkg_list))
            list(map(os.unlink, pkg_list))

    def install_basic_deps(self):
        if self.module.get_bin_path('dpkg'):
            prefix_cmd = "dpkg --force-all -i"
            suffix_cmd = '.deb'
        else:
            prefix_cmd = "rpm -ivh --force --nodeps --replacepkgs"
            suffix_cmd = '.rpm'
        for name in ['bzip2', 'unzip', 'tar']:
            pkg_path = os.path.join(os.path.dirname(self.resources_dir), '{}*{}'.format(name, suffix_cmd))
            pkg_list = glob.glob(pkg_path)
            if self.module.get_bin_path(name):
                self.clear(pkg_list)
                continue
            if not pkg_list:
                self.module.exit_json(msg='missing resource: {}'.format(pkg_path))
            cmd = "{} {}".format(prefix_cmd, pkg_path)
            if getpass.getuser() != 'root':
                self.module.fail_json(
                    msg='no permission to run cmd: {}, please run command with root user firstly'.format(cmd))
            self.module.run_command(cmd, use_unsafe_shell=True, check_rc=True)
            self.clear(pkg_list)

    def prepare_dirs(self):
        tags = self.tags[:]
        if 'dl' in self.tags:
            tags.extend(self.mapping.keys())
        for tag in tags:
            dir_name = self.mapping.get(tag, '')
            dir_path = os.path.join(self.resources_dir, 'mindxdl', 'dlImages', self.arch, dir_name)
            if dir_name and not os.path.exists(dir_path):
                os.makedirs(dir_path, 0o750)

    def run(self):
        os.umask(0o022)
        self.install_basic_deps()
        if os.path.exists(self.resources_dir):
            shutil.rmtree(self.resources_dir)
        dst = os.path.dirname(self.resources_dir)
        src = os.path.expanduser('~/resources_{}.tar'.format(self.arch))
        if not os.path.exists(src):
            self.module.fail_json(msg='{} is not existed'.format(src))
        with tarfile.open(src) as f:
            members = []
            uname = getpass.getuser()
            gid = os.getegid()
            gname = pwd.getpwuid(gid).pw_name
            for member in f.getmembers():
                member.uname = uname
                member.gname = gname
                member.mode &= ~0o022  # remove write permission from the group and other user
                members.append(member)
            f.extractall(dst, members)
        self.prepare_dirs()
        self.module.exit_json(changed=True, msg='uncompress ok')


if __name__ == '__main__':
    UncompressResources().run()
