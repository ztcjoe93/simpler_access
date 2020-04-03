import paramiko
import xml.etree.ElementTree as ET
import argparse
import socket
import sys
import select
import socketserver as SocketServer
import threading
import textwrap
import pdb
import os

import simple_raccess.interactive as interactive
import simple_raccess.actions as actions
import simple_raccess.main as gui_app

def indent(ele, level=0):
    line = "\n" + level*"  "
    if len(ele):
        if not ele.text or not ele.text.strip():
            ele.text = line + "  "
        if not ele.tail or not ele.tail.strip():
            ele.tail = line
        for ele in ele:
            indent(ele, level+1)
        if not ele.tail or not ele.tail.strip():
            ele.tail = line
    else:
        if level and (not ele.tail or not ele.tail.strip()):
            ele.tail = line

def port_forward(machine_data):
    class ForwardServer(SocketServer.ThreadingTCPServer):
        daemon_threads = True
        allow_reuse_address = True

    class Handler(SocketServer.BaseRequestHandler):
        def handle(self):
            try:
                chan = self.ssh_transport.open_channel(
                    "direct-tcpip",
                    (self.chain_host, self.chain_port),
                    self.request.getpeername(),
                )
            except Exception as e:
                print("Incoming request to %s:%d failed: %s"
                    % (self.chain_host, self.chain_port, repr(e))
                    )
                return
            if chan is None:
                print("Incoming request to %s:%d was rejected by the SSH server."
                    % (self.chain_host, self.chain_port)
                )
                return

            print(
                "Connected!  Tunnel open %r -> %r -> %r"
                % (
                    self.request.getpeername(),
                    chan.getpeername(),
                    (self.chain_host, self.chain_port),
                )
            )
            while True:
                r, w, x = select.select([self.request, chan], [], [])
                if self.request in r:
                    data = self.request.recv(1024)
                    if len(data) == 0:
                        break
                    chan.send(data)
                if chan in r:
                    data = chan.recv(1024)
                    if len(data) == 0:
                        break
                    self.request.send(data)

            peername = self.request.getpeername()
            chan.close()
            self.request.close()
            print("Tunnel closed from %r" % (peername,))

    def handler(chan, host, port):
        sock = socket.socket()
        try:
            sock.connect((host, port))
        except Exception as e:
            print("Forwarding request to %s:%d failed: %r" % (host, port, e))
            return

        print(
            "Connected!  Tunnel open %r -> %r -> %r"
            % (chan.origin_addr, chan.getpeername(), (host, port))
        )
        while True:
            r, w, x = select.select([sock, chan], [], [])
            if sock in r:
                data = sock.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                sock.send(data)
        chan.close()
        sock.close()
        print("Tunnel closed from %r" % (chan.origin_addr,))


    def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
        transport.request_port_forward("", server_port)
        while True:
            chan = transport.accept(1000)
            if chan is None:
                continue
            thr = threading.Thread(
                target=handler, args=(chan, remote_host, remote_port)
            )
            thr.setDaemon(True)
            thr.start()

    def forward_tunnel(local_port, remote_host, remote_port, transport):
        class SubHander(Handler):
            chain_host = remote_host
            chain_port = remote_port
            ssh_transport = transport

        ForwardServer(("", local_port), SubHander).serve_forever()

    #main()
    localhost = machine_data[3][0].text
    localport = int(machine_data[3][1].text)
    serverhost = machine_data[1].text
    serverport = int(machine_data[2].text)
    remotehost = machine_data[3][2].text
    remoteport = int(machine_data[3][3].text)
    username = machine_data[4].text
    password = machine_data[5].text

    forward_type = machine_data[3].attrib['type']

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    print("Connecting to ssh host %s:%d ..." % (serverhost, serverport))
    try:
        client.connect(
            serverhost,
            serverport,
            username=username,
            key_filename=None,
            password=password,
        )
    except Exception as e:
        print("*** Failed to connect to %s:%d: %r" % (serverhost, serverport, e))
        sys.exit(1)

    if forward_type == 'local':
        print(
            "Now forwarding port %d to %s:%d ..."
            % (localport, remotehost, remoteport)
        )

        try:
            forward_tunnel(
                localport, remotehost, remoteport, client.get_transport()
            )
        except KeyboardInterrupt:
            print("C-c: Port forwarding stopped.")
            sys.exit(0)

    elif forward_type == 'remote': 
        print(
            "Now forwarding remote port %d to %s:%d ..."
            % (localport, remotehost, remoteport)
        )

        try:
            reverse_forward_tunnel(
                remoteport, remotehost, localport, client.get_transport()
            )
        except KeyboardInterrupt:
            print("C-c: Port forwarding stopped.")
            sys.exit(0)

def connect(**kwargs):
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 
    root = ET.parse(xml_file).getroot()

    if kwargs['m_id'] == 0:     
        print("\n{:<2} {:^20} {:<15}\n{}".format("Id", "Machine", "Host", "="*40))
        for index, machine in enumerate(root, start=1):
            print("{:<2} {:^20} {:<15}".format(str(index), machine[0].text, machine[1].text))

        while True:
            try:
                usr_input = int(input())
                if not (usr_input-1 < 0 or usr_input-1 >= len(root)):
                    print(root[usr_input-1][0].text + " selected.")
                    break
                else:
                    raise exception
            except:
                print("Please enter a valid integer")
    
        machine = root[usr_input-1]
    else:
        machine = root[int(kwargs['m_id'])-1]

    # check for forward
    if len(machine[3]) > 0:
        port_forward(machine)


    else:
        machine_info = {
                    'hostname': machine[1].text,
                    'port': machine[2].text,
                    'username': machine[4].text,
                    'password': machine[5].text,
                    'key_filename': machine[6].text 
                    }

        hostname, port, username, password, key = machine[1].text, machine[2].text,\
            machine[4].text, machine[5].text, machine[6].text

        tunneling = False
        # check for jumphosts
        jumphosts = machine[7]
        if len(jumphosts) > 0:
            tunneling ^= tunneling

            for machine in jumphosts:
                tunnel_name, tunnel_host, tunnel_port, tunnel_user, tunnel_pass, tunnel_key = [x.text for x in machine]

        if tunneling:
            jumpbox = paramiko.SSHClient()
            jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            jumpbox.connect(tunnel_host, username=tunnel_user, password=tunnel_pass)
            jumpbox_transport = jumpbox.get_transport()
            jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", (hostname, 22), (tunnel_host, 22))
            machine_info['sock'] = jumpbox_channel

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if password == None:
                ssh_client.connect(**machine_info)
            #    ssh_client.connect(hostname=hostname, username=username,
            #            port=port, key_filename=key)
            else:
                ssh_client.connect(**machine_info)
            #    ssh_client.connect(hostname=hostname, username=username,
            #            port=port, password=password, sock=jumpbox_channel)
        finally:
            print(f'Successfully connected to {hostname}:{port}')
        channel = ssh_client.invoke_shell()
        interactive.posix_shell(channel)
        ssh_client.close()

def write_machine(info):
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 
    root = ET.parse(xml_file).getroot()

    machine = ET.Element("machine")

    machine_name = ET.SubElement(machine, "name")
    machine_name.text = info['name'] 
    machine_host = ET.SubElement(machine, "host")
    machine_host.text = info['host']
    machine_port = ET.SubElement(machine, "port")
    machine_port.text = info['port']

    if info['forward'] != "":
        machine_forward = ET.SubElement(machine, "forward")
        machine_forward.set('type', info['forward']['type'])
        machine_localhost = ET.SubElement(machine_forward, "localhost")
        machine_localhost.text = info['forward']['localhost'] 
        machine_localport = ET.SubElement(machine_forward, "localport")
        machine_localport.text = info['forward']['localport']
        machine_remotehost = ET.SubElement(machine_forward, "remotehost")
        machine_remotehost.text = info['forward']['remotehost']
        machine_remoteport = ET.SubElement(machine_forward, "remoteport")
        machine_remoteport.text = info['forward']['remoteport']
    else:
        machine_forward = ET.SubElement(machine, "forward")
        machine_forward.text = ""
        
    machine_username = ET.SubElement(machine, "username")
    machine_username.text = info['username']
    machine_password = ET.SubElement(machine, "password")
    machine_password.text = info['password']
    machine_key = ET.SubElement(machine, "key")
    machine_key.text = info['key'] if info['key'] != "" else ""
    jumphosts = ET.SubElement(machine, "jumphosts")

    if info['tunnel'] != "":
        for jump_machine in info['tunnel']:
            jumphost = ET.SubElement(jumphosts, "jumphost")
            jumphost_name = ET.SubElement(jumphost, "name")
            jumphost_name.text = jump_machine['name']
            jumphost_host = ET.SubElement(jumphost, "host")
            jumphost_host.text = jump_machine['host']
            jumphost_port = ET.SubElement(jumphost, "port")
            jumphost_port.text = jump_machine['port']
            jumphost_user = ET.SubElement(jumphost, "username")
            jumphost_user.text = jump_machine['username']
            jumphost_pass = ET.SubElement(jumphost, "password")
            jumphost_pass.text = jump_machine['password']
            jumphost_key = ET.SubElement(jumphost, "key") 
            jumphost_key.text = jump_machine['key']

    root.insert(len(root), machine)

    indent(root)
    with open(xml_file, 'wb') as f:
        f.write(ET.tostring(root))

def add_machine(**kwargs):
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 
    root = ET.parse(xml_file).getroot()

    if kwargs['xml'] == 0:
        #no xml files passed in as argument
        print("\nAdding a machine\n{}".format("-"*25))
        name = input("Machine Name: ")
        host = input("Host: ")
        port = input("Port: ")

        forward = True if input("Port-forwarding? (y/n): ") == 'y' else False
        
        if forward:
            forward_type = 'remote' if input("Local or Remote? (l/r): ") == 'r' else 'local'
            localhost = input("Local host: ")
            localport = input("Local port: ")
            remotehost = input("Remote host: ")
            remoteport = input("Remote port: ")

        username = input("Username: ")
        password = input("Password: ")
        key = True if input("Any keys? (y/n): ") == 'y' else False
        key_path = input("Enter path: ") if key else ""
        jumphost = True if input("Jumping? (y/n): ") == 'y' else False
        
        jump_machines = []
        if jumphost:
            while True:
                print("\nAdd a machine to jump to\n{}".format("-"*25))
                j_name = input("Machine Name: ") 
                j_host = input("Host: ")
                j_port = input("Port: ")
                j_username = input("Username: ")
                j_password = input("Password: ")
                j_key = True if input("Any keys? (y/n): ") == 'y' else False
                j_key_path = input("Enter path: ") if j_key else ""

                jump_machines.append({
                    'name': j_name, 
                    'host': j_host, 
                    'port': j_port,
                    'username': j_username, 
                    'password': j_password, 
                    'key': j_key_path if j_key else ""
                    })

                prompt = input("\nJumping to another? (y/n)")
                if prompt == 'n':
                    break
                elif prompt == 'y':
                    pass
                else:
                    print("Invalid option")

        machine = ET.Element("machine")

        machine_name = ET.SubElement(machine, "name")
        machine_name.text = name
        machine_host = ET.SubElement(machine, "host")
        machine_host.text = host
        machine_port = ET.SubElement(machine, "port")
        machine_port.text = port 

        if forward:
            machine_forward = ET.SubElement(machine, "forward")
            machine_forward.set('type', forward_type)
            machine_localhost = ET.SubElement(machine_forward, "localhost")
            machine_localhost.text = localhost
            machine_localport = ET.SubElement(machine_forward, "localport")
            machine_localport.text = localport
            machine_remotehost = ET.SubElement(machine_forward, "remotehost")
            machine_remotehost.text = remotehost
            machine_remoteport = ET.SubElement(machine_forward, "remoteport")
            machine_remoteport.text = remoteport
        else:
            machine_forward = ET.SubElement(machine, "forward")
            machine_forward.text = ""

        machine_username = ET.SubElement(machine, "username")
        machine_username.text = username 
        machine_password = ET.SubElement(machine, "password")
        machine_password.text = password 
        machine_key = ET.SubElement(machine, "key")
        machine_key.text = key_path if key is True else ""
        jumphost_machines = ET.SubElement(machine, "jumphosts")

        for jump in jump_machines:
            j_machine = ET.SubElement(jumphost_machines, "jumphost")
            jump_name = ET.SubElement(j_machine, "name")
            jump_name.text = jump['name']
            jump_host = ET.SubElement(j_machine, "host")
            jump_host.text = jump['host']
            jump_port = ET.SubElement(j_machine, "port")
            jump_port.text = jump['port']
            jump_user = ET.SubElement(j_machine, "username")
            jump_user.text = jump['username']
            jump_pass = ET.SubElement(j_machine, "password")
            jump_pass.text = jump['password']
            jump_key = ET.SubElement(j_machine, "key") 
            jump_key.text = jump['key']

        root.insert(len(root), machine)
    else:
        provided_file = ET.parse(kwargs['xml']).getroot()
        root.insert(len(root), provided_file)

    indent(root)
    with open(xml_file, 'wb') as f:
        f.write(ET.tostring(root))

def show_machines():
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 
    root = ET.parse(xml_file).getroot()

    def txt_wrapper(params):
        wrap_size = [5, 20, 20, 10, 15, 20, 20, 20, 10]
        print("{:<5} {:<20} {:<20} {:<10} {:<15} {:<20} {:<20} {:<20} {:<10}".format(
            *[textwrap.wrap(string, depth)[0] if string != "" else "" for string, depth in zip(params, wrap_size)]
            ))


    def border():
        print("="*150)

    info = []
    txt_wrapper(["Id", "Machine", "Host", "Port", "Forward", "Username",
        "Password", "Key", "Jumphost"])
    border()
    
    for index, machine in enumerate(root, start=1):
        machine_information = [
                str(index),
                machine[0].text,
                machine[1].text,
                machine[2].text,
                machine[3].attrib['type'] if len(machine[3])>0 else "",
                machine[4].text,
                "" if machine[5].text == None else machine[5].text,
                "" if machine[6].text == None else machine[6].text,
                "True" if len(machine[7])>0 else "False"
                ]
        txt_wrapper(machine_information)
        info.append(machine_information[1:])

        port_forward = machine[3]
        if len(port_forward) > 0:
            txt_wrapper([
                    "",
                    "local ->",
                    f"{port_forward[0].text}:{port_forward[1].text}",
                    "",
                    "remote ->",
                    f"{port_forward[2].text}:{port_forward[3].text}",
                    "","",""
                ])
            print()

        jumphosts = machine[7]
        if len(jumphosts) > 0:
            for jump in jumphosts:
                txt_wrapper([
                        "",
                        jump[0].text,
                        jump[1].text,
                        jump[2].text,
                        "",
                        jump[3].text,
                        "" if jump[4].text == None else jump[4].text,
                        "" if jump[5].text == None else jump[5].text,
                        ""
                    ])

    #print(info)
    return info

def delete_machine(**kwargs):
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 
    root = ET.parse(xml_file).getroot()

    if kwargs['m_id'] != 0:
        if len(root) < kwargs['m_id'] or kwargs['m_id'] <= 0:
            print("Unable to find a relevant machine with the specified ID.")
        else:
            machine = root[kwargs['m_id'] - 1]
            print("Deleting the following connection:\n{}\nID#{} - {}@{}".format(
                    "-"*40, kwargs['m_id'], machine[0].text, machine[1].text
                ))
            if 'gui' not in kwargs:
                choose = input("Are you sure you wish to delete? (y/n): ")
                if choose == 'y':
                    root.remove(machine)
                    with open(xml_file, 'wb') as f:
                        f.write(ET.tostring(root))
                elif choose == 'n':
                    pass
            else:
                root.remove(machine)
                with open(xml_file, 'wb') as f:
                    f.write(ET.tostring(root))

if __name__ == "__main__":
    xml_file = os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/base.xml') 

    if not os.path.isfile(xml_file):
        #create base XML file with <machines> tag
        base_info= ET.Element("machines")
        with open(xml_file, 'wb') as f:
            f.write(ET.tostring(base_info))
        
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gui', action='store_true', help='Runs application in GUI mode')
    parser.add_argument('-l', '--list', action='store_true', help='List all added machines')
    parser.add_argument('-a', '--add', nargs='?', metavar='xml-path', action=actions.connect_act, help='Add a machine (via xml) to the list')
    parser.add_argument('-c', '--connect', nargs='?', metavar='machine id', action=actions.connect_act, type=int, help='Connect to a machine')
    parser.add_argument('-d', '--delete', nargs='?', metavar='machine id', action=actions.delete_act, type=int, help='Delete a machine from the list')
    args = parser.parse_args()
    print(args)

    if args.gui:
        gui_app.run()
    if args.connect != None:
        connect(m_id=args.connect)
    elif args.list:
        show_machines()
    elif args.add != None:
        add_machine(xml=args.add)
    elif args.delete != None:
        delete_machine(m_id=args.delete)
