import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from simulador import Simulador
import socket
import pickle
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import numpy as np

class TransmissorGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmissor - Simulador de Camadas de Rede")
        self.simulador = Simulador()

        # Janela
        self.set_border_width(10)
        self.set_default_size(600, 400)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        # ── Host / Porta ───────────────────────────────────────────────
        host_box = Gtk.Box(spacing=5)
        host_box.pack_start(Gtk.Label(label="Host:"), False, False, 0)
        self.host_entry = Gtk.Entry()
        self.host_entry.set_text("127.0.0.1")
        host_box.pack_start(self.host_entry, True, True, 0)

        host_box.pack_start(Gtk.Label(label="Porta:"), False, False, 0)
        self.port_spin = Gtk.SpinButton()
        self.port_spin.set_range(1024, 65535)
        self.port_spin.set_value(50007)
        host_box.pack_start(self.port_spin, False, False, 0)
        vbox.pack_start(host_box, False, False, 0)

        # ── Configuração Geral ─────────────────────────────────────────
        grid = Gtk.Grid(row_spacing=6, column_spacing=6)
        grid.attach(Gtk.Label(label="Max Quadro:"), 0, 0, 1, 1)
        self.quadro_spin = Gtk.SpinButton()
        self.quadro_spin.set_range(1, 2048)
        grid.attach(self.quadro_spin, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Enquadramento:"), 0, 1, 1, 1)
        self.enq_combo = Gtk.ComboBoxText()
        for txt in ("Contagem de caracteres","FLAG+Bytes","FLAG+Bits"):
            self.enq_combo.append_text(txt)
        self.enq_combo.set_active(0)
        grid.attach(self.enq_combo, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Erro:"), 2, 1, 1, 1)
        self.erro_combo = Gtk.ComboBoxText()
        for txt in ("Paridade par","CRC-32", "Hamming"):
            self.erro_combo.append_text(txt)
        self.erro_combo.set_active(0)
        grid.attach(self.erro_combo, 3, 1, 1, 1)

        grid.attach(Gtk.Label(label="Modulação Dig.:"), 0, 2, 1, 1)
        self.mod_dig_combo = Gtk.ComboBoxText()
        for txt in ("NRZ-Polar","Manchester","Bipolar"):
            self.mod_dig_combo.append_text(txt)
        self.mod_dig_combo.set_active(0)
        grid.attach(self.mod_dig_combo, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Modulação Port.:"), 2, 2, 1, 1)
        self.mod_port_combo = Gtk.ComboBoxText()
        for txt in ("ASK","FSK","8-QAM"):
            self.mod_port_combo.append_text(txt)
        self.mod_port_combo.set_active(0)
        grid.attach(self.mod_port_combo, 3, 2, 1, 1)

        vbox.pack_start(grid, False, False, 0)

        # Frame do gráfico
        self.plot_frame = Gtk.Frame(label="Sinal Modulado")
        self.figure = Figure(figsize=(6, 2), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.plot_frame.add(self.canvas)

        vbox.pack_start(self.plot_frame, True, True, 0)  # Exibe o gráfico na interface

        # ── Entrada de Texto ────────────────────────────────────────────
        inp_frame = Gtk.Frame(label="Mensagem a Transmitir")
        self.input_entry = Gtk.Entry()
        inp_frame.add(self.input_entry)
        vbox.pack_start(inp_frame, False, False, 0)

        # ── Botões ───────────────────────────────────────────────────────
        btn_box = Gtk.Box(spacing=6)
        btn = Gtk.Button(label="Simular e Enviar")
        btn.connect("clicked", self.on_simular)
        btn_box.pack_start(btn, True, True, 0)
        btn = Gtk.Button(label="Limpar")
        btn.connect("clicked", self.on_limpar)
        btn_box.pack_start(btn, True, True, 0)
        vbox.pack_start(btn_box, False, False, 0)

        # ── Saídas ───────────────────────────────────────────────────────
        self.enlace_lbl = Gtk.Label(label="Enlace: —")
        self.fisica_lbl = Gtk.Label(label="Física: —")
        self.status_lbl = Gtk.Label(label="Status: —")
        vbox.pack_start(self.enlace_lbl, False, False, 0)
        vbox.pack_start(self.fisica_lbl, False, False, 0)
        vbox.pack_start(self.status_lbl, False, False, 0)

    def on_simular(self, _):
        texto = self.input_entry.get_text()

        # 1) Enquadramento
        tipo_enq = {
            "Contagem de caracteres": "contagem_caracteres",
            "FLAG+Bytes": "flag_insercao_bytes",
            "FLAG+Bits": "flag_insercao_bits"
        }[self.enq_combo.get_active_text()]

        # 2) Detecção ou correção de erros
        tipo_erro = {
            "Paridade par": "paridade_par",
            "CRC-32": "crc32",
            "Hamming": "hamming"
        }[self.erro_combo.get_active_text()]
        
        tamanho_max_quadro = int(self.quadro_spin.get_value())
        quadros_com_edc = self.simulador.aplicar_enquadramento(tipo_enq, texto, tamanho_max_quadro, tipo_erro)
        
        # Exibir os quadros da camada de enlace, um por linha
        quadros_str = '\n'.join(
            "[" + ' '.join(str(bit) for bit in q) + "]"
            for q in quadros_com_edc
        )
        self.enlace_lbl.set_text("Quadros:\n" + quadros_str)

        # 3) Modulação Digital (banda base)
        tipo_mod_dig = {
            "NRZ-Polar": "nrz_polar",
            "Manchester": "manchester",
            "Bipolar": "bipolar"
        }[self.mod_dig_combo.get_active_text()]
        sinais_modulados = self.simulador.modular_digital(tipo_mod_dig, quadros_com_edc)
        
        # # 4) Modulação por portadora
        # tipo_mod_port = self.mod_port_combo.get_active_text()  # ASK, FSK, 8-QAM
        # sinais_modulados = self.simulador.modular_por_portadora(tipo_mod_port, sinais_modulados)

        # Gráfico sinais modulados
        ax = self.figure.clear() or self.figure.add_subplot(111)
        ax.set_title("Sinal Modulado")
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Tempo (amostras)")
        ax.plot(sinais_modulados, drawstyle='steps-post')

        self.canvas.draw()

        # 5) Envio via TCP para o receptor
        host = self.host_entry.get_text()
        port = int(self.port_spin.get_value())
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.sendall(pickle.dumps(sinais_modulados))
            sock.close()
            self.status_lbl.set_text(f"Status: Dados enviados para {host}:{port}")
        except Exception as e:
            self.status_lbl.set_text(f"Erro TCP: {e}")



    def on_limpar(self, _):
        self.input_entry.set_text("")
        self.enlace_lbl.set_text("Enlace: —")
        self.fisica_lbl.set_text("Física: —")
        self.status_lbl.set_text("Status: —")

if __name__ == "__main__": 
    win = TransmissorGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
