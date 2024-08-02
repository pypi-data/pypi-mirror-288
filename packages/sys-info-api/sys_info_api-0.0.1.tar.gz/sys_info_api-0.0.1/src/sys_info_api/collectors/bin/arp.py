
from typing import List
from system_information.common import MetricNotAvailable
import system_information.utils.cmd as cmd


def list_neighbors(interface: str = None) -> List[dict]:
	"""
	Get neighbors via a passive ARP scan

	raises MetricNotAvailable
	"""

	neighbors = []

	command = ['arp', '-a']

	if interface is not None:
		command += ['-i', interface]

	try:
		result = cmd.run_output(command)
		if result.startswith('arp: '):
			# "arp: in # entries no match found"
			return neighbors

		result = result.split("\n")
	except cmd.CmdExecException:
		raise MetricNotAvailable

	for line in result:
		# Formatted in HOSTNAME (IP) at MAC [TYPE] on [INTERFACE]
		parts = line.split(" ")

		if len(parts) > 5:
			mac = parts[3]
			hostname = parts[0]
			ip = parts[1][1:-1]

			# Process the output, some systems are weird
			# (looking at you MacOS)
			if hostname == '?':
				hostname = None

			if mac == '<incomplete>':
				mac = None
			elif mac == '(incomplete)':
				mac = None
			elif mac == 'ff:ff:ff:ff:ff:ff':
				mac = None
			else:
				# MacOS will shorten the MAC address by removing prepended 0's
				mac_fragments = mac.split(':')
				for i in range(len(mac_fragments)):
					if len(mac_fragments[i]) == 1:
						mac_fragments[i] = '0' + mac_fragments[i]
				mac = ':'.join(mac_fragments)

			if ip.startswith('224.0'):
				ip = None
			elif ip.startswith('169.254'):
				ip = None

			# At least mac and ip are required
			if mac is not None and ip is not None:
				neighbors.append({
					'hostname': hostname,
					'ip': ip,
					'mac': mac
				})

	return neighbors
