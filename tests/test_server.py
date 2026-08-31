"""Integration tests against the Chatbook TCP server."""

import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import utilities

ENCODING = "latin-1"


def xor_send(sock, message):
    payload = utilities.cifrar(message)
    sock.sendall(payload.encode(ENCODING))
    data = sock.recv(65536)
    return utilities.cifrar(data.decode(ENCODING))


class ServerProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix="chatbook-")
        binary = os.path.join(ROOT, "server", "tcpserver")
        if not os.path.isfile(binary):
            raise unittest.SkipTest("server/tcpserver is not built")
        shutil.copy(binary, cls.tmpdir)
        shutil.copy(os.path.join(ROOT, "server", "credentials.txt"), cls.tmpdir)
        cls.port = 18080
        cls.proc = subprocess.Popen(
            [os.path.join(cls.tmpdir, "tcpserver"), str(cls.port)],
            cwd=cls.tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        deadline = time.time() + 3
        last_error = None
        while time.time() < deadline:
            try:
                sock = socket.create_connection(("127.0.0.1", cls.port), timeout=0.3)
                sock.close()
                break
            except OSError as exc:
                last_error = exc
                time.sleep(0.05)
        else:
            cls.proc.kill()
            raise unittest.SkipTest("server did not start: {0}".format(last_error))

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "proc", None):
            cls.proc.terminate()
            try:
                cls.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                cls.proc.kill()
        if getattr(cls, "tmpdir", None):
            shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def setUp(self):
        self.sock = socket.create_connection(("127.0.0.1", self.port), timeout=2)

    def tearDown(self):
        self.sock.close()

    def test_auth_granted_and_denied(self):
        granted = xor_send(self.sock, "auth|root|admin")
        self.assertIn("Granted", granted)
        denied = xor_send(self.sock, "auth|root|wrong")
        self.assertIn("Denied", denied)

    def test_register_and_duplicate(self):
        first = xor_send(self.sock, "registrarUsuario|newbie|secret")
        self.assertIn("successful", first.lower())
        duplicate = xor_send(self.sock, "registrarUsuario|newbie|secret")
        self.assertTrue(duplicate.startswith("Error"))

    def test_room_message_flow(self):
        xor_send(self.sock, "auth|root|admin")
        created = xor_send(self.sock, "createChatRoom|root|testhouse")
        self.assertIn("True", created)
        rooms = xor_send(self.sock, "getAllChatrooms|")
        self.assertIn("testhouse", rooms)
        mine = xor_send(self.sock, "getUserChatrooms|root")
        self.assertIn("testhouse", mine)
        sent = xor_send(self.sock, "messageSent|root->hello there|testhouse")
        self.assertIn("Message sent", sent)
        chat = xor_send(self.sock, "getChat|testhouse")
        self.assertIn("hello there", chat)
        members = xor_send(self.sock, "getChatUsers|testhouse")
        self.assertIn("root", members)
        added = xor_send(self.sock, "addUser|user1|testhouse")
        self.assertIn("Added", added)
        members = xor_send(self.sock, "getChatUsers|testhouse")
        self.assertIn("user1", members)
        removed = xor_send(self.sock, "deleteUser|user1|testhouse")
        self.assertIn("Deleted", removed)
        members = xor_send(self.sock, "getChatUsers|testhouse")
        self.assertNotIn("user1", members)

    def test_users_list(self):
        users = xor_send(self.sock, "getUsers|")
        self.assertIn("root", users)
        self.assertNotIn("//", users)


if __name__ == "__main__":
    unittest.main()
