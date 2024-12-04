#!venv/bin/python

import argparse
import attr


@attr.s
class SSHHost:
  alias = attr.ib()
  name = attr.ib()
  pub_addr = attr.ib()
  pub_port = attr.ib()
  username = attr.ib()

  def render(self):
    return (
      f"Host {self.alias}\n"
      f"    HostName {self.pub_addr}\n"
      f"    Port {self.pub_port}\n"
      f"    User {self.username}\n"
    )

def main(args, aliases):
  with open(args.jcl_file) as fh:
    data = fh.read()

  for line in data.split('\n'):
    splitline = line.split(',')
    if len(splitline) < 9:
      continue
    if splitline[0] == 'Alias':
      continue
    if splitline[2] != 'SSH':
      continue
    alias = splitline[0]
    my_alias = aliases.get(alias)
    if my_alias:
      alias = my_alias
    ssh_host = SSHHost(
      alias=alias,
      name=splitline[1],
      pub_addr=splitline[5],
      pub_port=splitline[6],
      username=splitline[8],
    )
    print(ssh_host.render())

def get_aliases(args):
  aliases = {}
  if args.aliasfile:
    with open(args.aliasfile) as fh:
      data = fh.read()
    for line in data.split('\n'):
      splitline = line.split(':')
      if len(splitline)>1:
        aliases[splitline[0]] = splitline[1]
  return aliases

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=(
    "This script will create an SSH config file to allow easier access to a JCL environment. "
    "After adding your public address to the environment, you will receive an automated email "
    "with an attached CSV file containing access information to the VMs in your environment. "
    "Save that CSV file and run this script against it to create the SSH config. It will also "
    "optionally you to map the JCL instance names to more meaningful names in the config file.\n\n"
    "To use this config file: ssh -F <the created SSH config file> <JCL instance name or alias>"
  ))
  parser.add_argument("jcl_file", help="The CSV file saved from the JCL Email")
  parser.add_argument("-a", "--aliasfile", help="Alias mapping file. One mapping per line formatted like - jclalias:preferredalias")
  args = parser.parse_args()
  aliases = get_aliases(args)
  main(args, aliases)  
