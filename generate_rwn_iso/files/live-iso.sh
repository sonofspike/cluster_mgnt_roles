#!/bin/bash

firstboot_args='console=tty0 rd.neednet=1'
kernel_args=''

# Remove any existing VGs and PVs
# vgremove removes a volume group
for vg in $(vgs -o name --noheadings) ; do vgremove -y $vg ; done
# pvremove wipes the label on a device so that LVM will no longer recognise it as a physical volume
for pv in $(pvs -o name --noheadings) ; do pvremove -y $pv ; done

#TODO: Wipeout all disks
#lsblk
#dd if=/dev/zero of=/dev/sda bs=4M count=3 conv=sync

# use the first block device
first_block_dev=$(lsblk -lpdn -o NAME | grep [s,v]d[a-z] | head -n1)
if [[ $first_block_dev ]]; then
    install_device=$first_block_dev
    wipefs --all $install_device
    echo "Using device ${install_device} for installation"
else
    echo "Can't find block device for installation"
    exit 1
fi

cmd="coreos-installer install --firstboot-args=\"${firstboot_args} ${kernel_args}\" --ignition=/root/config.ign ${install_device}"
bash -c "$cmd"
if [ "$?" == "0" ] ; then
  echo "Install Succeeded!"
  reboot
else
  echo "Install Failed!"
  exit 1
fi