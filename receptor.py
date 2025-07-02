import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import socket
import threading
import pickle
from camada_enlace.Enquadramento.camada_enlace import CamadaEnlace
from camada_enlace.Enquadramento.enquadrador import ContagemCaracteres, InsercaoBytes, InsercaoBits

class ReceptorGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor - Simulador de Camadas de Rede")
        self.set_border_width(10)
        self.set_default_size(600, 400)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        # Host / Porta
        host_box = Gtk.Box(spacing=5)
        host_box.pack_start(Gtk.Label(label="Host:"), False, False, 0)
        self.host_entry = Gtk.Entry()
        self.host_entry.set_text("0.0.0.0")
        host_box.pack_start(self.host_entry, True, True, 0)

        host_box.pack_start(Gtk.Label(label="Porta:"), False, False, 0)
        self.port_spin = Gtk.SpinButton()
        self.port_spin.set_range(1024, 65535)
        self.port_spin.set_value(50007)
        host_box.pack_start(self.port_spin, False, False, 0)
        vbox.pack_start(host_box, False, False, 0)

        # Enquadramento (mesma configuração do transmissor)
        enq_box = Gtk.Box(spacing=5)
        enq_box.pack_start(Gtk.Label(label="Enquadramento:"), False, False, 0)
        self.enq_combo = Gtk.ComboBoxText()
        for txt in ("Contagem de caracteres","FLAG+Bytes","FLAG+Bits"):
            self.enq_combo.append_text(txt)
        self.enq_combo.set_active(0)
        enq_box.pack_start(self.enq_combo, False, False, 0)
        vbox.pack_start(enq_box, False, False, 0)

        # Botão Ouvir
        btn_ouvir = Gtk.Button(label="Ouvir Conexão")
        btn_ouvir.connect("clicked", self.on_ouvir)
        vbox.pack_start(btn_ouvir, False, False, 0)

        # Labels de saída
        self.recebidos_label = Gtk.Label(label="Quadros recebidos:\n—")
        self.texto_label = Gtk.Label(label="Texto recebido: —")
        self.status_label = Gtk.Label(label="Status: Aguardando...")
        vbox.pack_start(self.recebidos_label, False, False, 0)
        vbox.pack_start(self.texto_label, False, False, 0)
        vbox.pack_start(self.status_label, False, False, 0)

    def on_ouvir(self, _):
        host = self.host_entry.get_text()
        port = int(self.port_spin.get_value())
        self.status_label.set_text(f"Status: Aguardando em {host}:{port} ...")
        thread = threading.Thread(target=self.listen_thread, args=(host, port), daemon=True)
        thread.start()

    def listen_thread(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(1)
            conn, addr = sock.accept()
            data = b""
            while True:
                part = conn.recv(4096)
                if not part:
                    break
                data += part
            conn.close()

            quadros = pickle.loads(data)

            # Seleciona o enquadrador conforme escolha
            tipo = self.enq_combo.get_active_text()
            if tipo == "Contagem de caracteres":
                eq = ContagemCaracteres()
            elif tipo == "FLAG+Bytes":
                eq = InsercaoBytes()
            else:
                eq = InsercaoBits()
            camada = CamadaEnlace(eq)

            # Desenquadra todos os quadros e reconstrói o bitstream
            bitstream = []
            quadros_str = []
            bits = camada.desenquadrar(quadros)
            bitstream.extend(bits)

            # Converte bits de volta em texto
            texto = ""
            for i in range(0, len(bitstream), 8):
                byte = bitstream[i:i+8]
                if len(byte) < 8:
                    break
                valor = int("".join(str(b) for b in byte), 2)
                texto += chr(valor)

            GLib.idle_add(self.update_ui, quadros_str, texto)
        except Exception as e:
            GLib.idle_add(self.status_label.set_text, f"Erro: {e}")

    def update_ui(self, quadros_str, texto):
        self.recebidos_label.set_text("Quadros recebidos:\n" + "\n".join(quadros_str))
        self.texto_label.set_text("Texto recebido: " + texto)
        self.status_label.set_text("Status: Mensagem recebida com sucesso")

if __name__ == "__main__":
    win = ReceptorGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
