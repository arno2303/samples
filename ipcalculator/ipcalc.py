import tkinter
import re


class IPCalc:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry('500x450')
        self.window.resizable(0, 0)
        self.window.title("IPv4 Calculator")
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

    @staticmethod
    def _decimal_to_binary(address):
        return [bin(x)[2:].zfill(8) for x in address]

    @staticmethod
    def _net_mask(prefix):
        mask = [0, 0, 0, 0]
        for i in range(int(prefix)):
            mask[int(i / 8)] += 1 << (7 - i % 8)
        return mask

    @staticmethod
    def _broadcast_network_address(b_ip, b_n_msk, b_msk):
        broadcast = []
        network = []
        for x, y in zip(b_ip, b_n_msk):
            broadcast.append(int(str(x), 2) | int(str(y), 2))
        for x, y in zip(b_ip, b_msk):
            network.append(int(str(x), 2) & int(str(y), 2))
        return broadcast, network

    @staticmethod
    def _range_of_hosts(network_ip, broadcast_ip):
        first_ip = network_ip[:]
        first_ip[-1] += 1
        last_ip = broadcast_ip[:]
        last_ip[-1] -= 1
        return first_ip, last_ip

    @staticmethod
    def _count_avlb_hosts(bnr_neg_msk):
        count_ones = 0
        for x in bnr_neg_msk:
            count_ones += x.count('1')
        return (2 ** count_ones) - 2

    @staticmethod
    def calculate_network(address):
        ip_address, prefix = address.split('/')
        binary_ip = IPCalc._decimal_to_binary([int(x) for x in ip_address.split('.')])
        binary_mask = IPCalc._decimal_to_binary(IPCalc._net_mask(prefix))
        binary_negation_mask = IPCalc._decimal_to_binary([255-i for i in IPCalc._net_mask(prefix)])
        broadcast_ip, network_ip = IPCalc._broadcast_network_address(binary_ip, binary_negation_mask, binary_mask)
        rng_first, rng_last = IPCalc._range_of_hosts(network_ip, broadcast_ip)
        count_free_address = IPCalc._count_avlb_hosts(binary_negation_mask)

        return {
            "Network": ".".join(map(str, network_ip)), "Broadcast": ".".join(map(str, broadcast_ip)),
            "Range": f'{".".join(map(str, rng_first))} - {".".join(map(str, rng_last))}',
            "Mask": ".".join(map(str, IPCalc._net_mask(prefix))), "Count_IP": count_free_address
        }

    def gui(self):

        def ip_validation(init, *args):
            ptr = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]' \
                  r'|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/([1-9]|[1-2][0-9]|3[0-2])$'
            if len(ip_address.get()) > 18:
                ip_address.set(ip_address.get()[:-1])
            if not re.match(ptr, ip_address.get()):
                title_text.set('Your IP Address - Not Valid')
            else:
                title_text.set("Your IP Address")
                network_details = init.calculate_network(ip_address.get())
                network_text.set(network_details["Network"])
                mask_text.set(network_details["Mask"])
                broadcast_text.set(network_details["Broadcast"])
                hosts_text.set(network_details["Count_IP"])
                ranges_text.set(network_details["Range"])

        # Top title
        title_text = tkinter.StringVar()
        title_text.set("Your IP Address")
        title = tkinter.Label(self.window, textvariable=title_text, height=3)
        title.grid(row=0, column=0, columnspan=2)

        # IP Entry
        ip_address = tkinter.StringVar()
        entry = tkinter.Entry(self.window, bd=0, bg='#ccc', justify='center', textvariable=ip_address)
        entry.grid(row=1, column=0, columnspan=2)

        # Network
        network_title = tkinter.Label(self.window, text="Network", height=2)
        network_title.grid(row=2, column=0, pady=(50, 0))

        network_text = tkinter.StringVar()
        network = tkinter.Label(self.window, textvariable=network_text, height=2)
        network.grid(row=3, column=0)

        # Mask
        mask_title = tkinter.Label(self.window, text="Mask", height=2)
        mask_title.grid(row=2, column=1, pady=(50, 0))

        mask_text = tkinter.StringVar()
        mask = tkinter.Label(self.window, textvariable=mask_text, height=2)
        mask.grid(row=3, column=1)

        # Broadcast
        broadcast_title = tkinter.Label(self.window, text="Broadcast", height=2)
        broadcast_title.grid(row=4, column=0)

        broadcast_text = tkinter.StringVar()
        broadcast = tkinter.Label(self.window, textvariable=broadcast_text, height=2)
        broadcast.grid(row=5, column=0)

        # IP Hosts Count
        hosts_title = tkinter.Label(self.window, text="Count of hosts", height=2)
        hosts_title.grid(row=4, column=1)

        hosts_text = tkinter.StringVar()
        hosts = tkinter.Label(self.window, textvariable=hosts_text, fg="green", height=2)
        hosts.grid(row=5, column=1)

        # Free host Range
        ranges_title = tkinter.Label(self.window, text="Usable hosts range", height=2)
        ranges_title.grid(row=6, column=0, columnspan=2)

        ranges_text = tkinter.StringVar()
        ranges = tkinter.Label(self.window, textvariable=ranges_text, fg="green", height=2)
        ranges.grid(row=7, column=0, columnspan=2)

        # Trace IP Entry
        args_text = (
            ip_address, title_text, network_text, mask_text,
            broadcast_text, hosts_text, ranges_text)
        ip_address.trace("w", lambda *args: ip_validation(self, *args_text))

    def start(self):
        self.gui()
        self.window.mainloop()


if __name__ == '__main__':
    app = IPCalc()
    app.start()
