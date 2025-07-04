import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import socket, threading, pickle

from simulador import Simulador

class ReceptorGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor - Simulador de Camadas de Rede")
        self.set_border_width(10)
        self.set_default_size(600, 500)

        self.sim = Simulador()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        # ── Host / Porta ──────────────────────────────────────────────────
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

        # ── Camada de Enlace: Enquadramento + EDC ────────────────────────
        grid_enlace = Gtk.Grid(row_spacing=6, column_spacing=12)
        # Enquadramento
        grid_enlace.attach(Gtk.Label(label="Enquadramento:"), 0, 0, 1, 1)
        self.enq_combo = Gtk.ComboBoxText()
        for txt in ("Contagem de caracteres","FLAG+Bytes","FLAG+Bits"):
            self.enq_combo.append_text(txt)
        self.enq_combo.set_active(0)
        grid_enlace.attach(self.enq_combo, 1, 0, 1, 1)
        # EDC
        grid_enlace.attach(Gtk.Label(label="Detecção/Correção:"), 2, 0, 1, 1)
        self.erro_combo = Gtk.ComboBoxText()
        for txt in ("Paridade par","CRC-32","Hamming"):
            self.erro_combo.append_text(txt)
        self.erro_combo.set_active(0)
        grid_enlace.attach(self.erro_combo, 3, 0, 1, 1)

        vbox.pack_start(grid_enlace, False, False, 0)

        # ── Camada Física: Modulação Digital + Portadora ────────────────
        grid_fisica = Gtk.Grid(row_spacing=6, column_spacing=12)
        # Modulação Digital
        grid_fisica.attach(Gtk.Label(label="Modulação Dig.:"), 0, 0, 1, 1)
        self.mod_dig_combo = Gtk.ComboBoxText()
        for txt in ("NRZ-Polar","Manchester","Bipolar"):
            self.mod_dig_combo.append_text(txt)
        self.mod_dig_combo.set_active(0)
        grid_fisica.attach(self.mod_dig_combo, 1, 0, 1, 1)
        # Modulação Port.
        grid_fisica.attach(Gtk.Label(label="Modulação Port.:"), 2, 0, 1, 1)
        self.mod_port_combo = Gtk.ComboBoxText()
        for txt in ("ASK","FSK","8-QAM"):
            self.mod_port_combo.append_text(txt)
        self.mod_port_combo.set_active(0)
        grid_fisica.attach(self.mod_port_combo, 3, 0, 1, 1)

        vbox.pack_start(grid_fisica, False, False, 0)

        # ── Botão Ouvir ─────────────────────────────────────────────────
        btn_ouvir = Gtk.Button(label="Ouvir Conexão")
        btn_ouvir.connect("clicked", self.on_ouvir)
        vbox.pack_start(btn_ouvir, False, False, 0)

        # ── Saídas ───────────────────────────────────────────────────────
        self.recebidos_label = Gtk.Label(label="Quadros recebidos:\n—")
        self.texto_label    = Gtk.Label(label="Texto recebido: —")
        self.status_label   = Gtk.Label(label="Status: Aguardando...")
        vbox.pack_start(self.recebidos_label, False, False, 0)
        vbox.pack_start(self.texto_label, False, False, 0)
        vbox.pack_start(self.status_label, False, False, 0)

    def on_ouvir(self, _):
        host = self.host_entry.get_text()
        port = int(self.port_spin.get_value())
        self.status_label.set_text(f"Status: Aguardando em {host}:{port} …")
        thread = threading.Thread(target=self.listen_thread, args=(host, port), daemon=True)
        thread.start()

    def listen_thread(self, host, port):
        try:
            # 1) Recebe sinal modulado inteiro
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(1)
            conn, _ = sock.accept()
            data = b""
            while True:
                part = conn.recv(4096)
                if not part:
                    break
                data += part
            conn.close()

            sinais_modulados = pickle.loads(data)

            # # 2) Demodulação por portadora
            # tipo_mod_port = self.mod_port_combo.get_active_text()
            # sinais_bb = self.sim.demodular_portadora(tipo_mod_port, sinais_modulados)

            # 3) Demodulação digital (banda-base)
            tipo_mod_dig = {
                "NRZ-Polar": "nrz_polar",
                "Manchester": "manchester",
                "Bipolar": "bipolar"
            }[self.mod_dig_combo.get_active_text()]
            bitstream = self.sim.demodular_digital(tipo_mod_dig, sinais_modulados)

            # 4) Remoção de EDC e Desenquadramento
            tipo_enq  = {
                "Contagem de caracteres": "contagem_caracteres",
                "FLAG+Bytes": "flag_insercao_bytes",
                "FLAG+Bits": "flag_insercao_bits"
            }[self.enq_combo.get_active_text()]

            tipo_erro = {
                "Paridade par": "paridade_par",
                "CRC-32": "crc32",
                "Hamming": "hamming"
            }[self.erro_combo.get_active_text()]

            quadros_sem_enlace = self.sim.remover_edc_e_desenquadrar(
                tipo_enq, tipo_erro, bitstream
            )

            # 5) Bits → Texto
            texto = self.sim.bits_para_texto(quadros_sem_enlace)

            # Atualiza UI na thread principal
            quadros_str = ["".join(str(b) for b in q) for q in quadros_sem_enlace]
            GLib.idle_add(self.update_ui, quadros_str, texto)

        except Exception as e:
            GLib.idle_add(self.status_label.set_text, f"Erro: {e}")

    def update_ui(self, quadros_str, texto):
        self.recebidos_label.set_text("Texto em bits:\n" + "\n".join(quadros_str))
        self.texto_label.set_text("Texto recebido: " + texto)
        self.status_label.set_text("Status: Mensagem recebida")


if __name__ == "__main__":
    win = ReceptorGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
