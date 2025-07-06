#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transmissor

Este módulo implementa a interface gráfica e lógica do lado transmissor de um simulador
das camadas de enlace e física de redes.

Funcionalidades:
- Entrada de mensagem textual
- Enquadramento (contagem, flag+bytes, flag+bits)
- Controle e correção de erros (paridade, CRC-32, Hamming)
- Modulação digital (NRZ-Polar, Manchester, Bipolar)
- Modulação por portadora (ASK, FSK, 8-QAM)
- Envio de sinal digital via socket TCP
- Visualização dos sinais modulados em gráficos
"""

# GTK e interface gráfica
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Comunicação e utilitários
import socket
import pickle
import numpy as np

# Módulos do simulador
from simulador import Simulador
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

# Modulações de portadora
from camada_fisica.modulador import CamadaFisica
from camada_fisica.modulacoes.ask import ASK
from camada_fisica.modulacoes.fsk import FSK
from camada_fisica.modulacoes.qam import QAM8

class TransmissorGUI(Gtk.Window):
    """Janela principal do transmissor"""

    def __init__(self):
        super().__init__(title="Transmissor - Simulador TR1")
        self.set_border_width(10)
        self.simulador = Simulador()

        # Layout principal usando grid
        grid = Gtk.Grid(column_spacing=6, row_spacing=6, margin=6)
        grid.set_column_homogeneous(True)
        self.add(grid)

        # Campo de entrada de mensagem
        grid.attach(Gtk.Label(label="Mensagem:"), 0, 0, 1, 1)
        self.input_entry = Gtk.Entry(); self.input_entry.set_text("o")
        grid.attach(self.input_entry, 1, 0, 3, 1)

        # Checkbox para mostrar apenas o payload
        self.payload_only_cb = Gtk.CheckButton(label="Mostrar apenas payload")
        grid.attach(self.payload_only_cb, 0, 1, 2, 1)

        # Combobox para tipo de enquadramento
        grid.attach(Gtk.Label(label="Enquadramento:"), 0, 2, 1, 1)
        self.enq_combo = Gtk.ComboBoxText()
        for txt in ["Contagem de caracteres", "FLAG+Bytes", "FLAG+Bits"]:
            self.enq_combo.append_text(txt)
        self.enq_combo.set_active(0)
        grid.attach(self.enq_combo, 1, 2, 1, 1)

        # SpinButton para tamanho de quadro
        grid.attach(Gtk.Label(label="Tamanho quadro:"), 2, 2, 1, 1)
        self.quadro_spin = Gtk.SpinButton(adjustment=Gtk.Adjustment(8, 1, 1024, 1, 10, 0), climb_rate=1, digits=0)
        grid.attach(self.quadro_spin, 3, 2, 1, 1)

        # Combobox para tipo de detecção/correção de erros
        grid.attach(Gtk.Label(label="Controle de Erro:"), 0, 3, 1, 1)
        self.erro_combo = Gtk.ComboBoxText()
        for txt in ["Paridade Par", "CRC-32", "Hamming"]:
            self.erro_combo.append_text(txt)
        self.erro_combo.set_active(0)
        grid.attach(self.erro_combo, 1, 3, 1, 1)

        # Combobox para modulação digital
        grid.attach(Gtk.Label(label="Modulação Digital:"), 2, 3, 1, 1)
        self.mod_dig_combo = Gtk.ComboBoxText()
        for txt in ["NRZ-Polar", "Manchester", "Bipolar"]:
            self.mod_dig_combo.append_text(txt)
        self.mod_dig_combo.set_active(0)
        grid.attach(self.mod_dig_combo, 3, 3, 1, 1)

        # Combobox para modulação por portadora
        grid.attach(Gtk.Label(label="Modulação Portadora:"), 0, 4, 1, 1)
        self.mod_port_combo = Gtk.ComboBoxText()
        for txt in ["ASK", "FSK", "8-QAM"]:
            self.mod_port_combo.append_text(txt)
        self.mod_port_combo.set_active(0)
        grid.attach(self.mod_port_combo, 1, 4, 1, 1)

        # Botões de simular e limpar
        btn_sim = Gtk.Button(label="Simular"); btn_sim.connect("clicked", self.on_simular)
        btn_lim = Gtk.Button(label="Limpar"); btn_lim.connect("clicked", self.on_limpar)
        grid.attach(btn_sim, 2, 4, 1, 1)
        grid.attach(btn_lim, 3, 4, 1, 1)

        # Label com os quadros gerados
        self.enlace_lbl = Gtk.Label(label="Quadros: —"); self.enlace_lbl.set_xalign(0)
        grid.attach(self.enlace_lbl, 0, 5, 4, 1)

        # Área de gráficos com matplotlib
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_hexpand(True); self.canvas.set_vexpand(True)
        grid.attach(self.canvas, 0, 6, 4, 1)

        # Campos para conexão TCP
        grid.attach(Gtk.Label(label="Host:"), 0, 7, 1, 1)
        self.host_entry = Gtk.Entry(); self.host_entry.set_text('localhost')
        grid.attach(self.host_entry, 1, 7, 1, 1)
        grid.attach(Gtk.Label(label="Porta:"), 2, 7, 1, 1)
        self.port_spin = Gtk.SpinButton(adjustment=Gtk.Adjustment(50007, 1, 65535, 1, 10, 0), climb_rate=1, digits=0)
        grid.attach(self.port_spin, 3, 7, 1, 1)

        # Label de status da conexão
        self.status_lbl = Gtk.Label(label="Status: —"); grid.attach(self.status_lbl, 0, 8, 4, 1)

        self.show_all()

    def on_simular(self, _):
        """Executa o processo de simulação da transmissão"""

        # Obtém mensagem e parâmetros da interface
        texto = self.input_entry.get_text().strip()
        tipo_enq = {
            "Contagem de caracteres": "contagem_caracteres",
            "FLAG+Bytes": "flag_insercao_bytes",
            "FLAG+Bits": "flag_insercao_bits"
        }[self.enq_combo.get_active_text()]
        tipo_edc = {
            "Paridade Par": "paridade_par",
            "CRC-32": "crc_32",
            "Hamming": "hamming"
        }[self.erro_combo.get_active_text()]
        tam = int(self.quadro_spin.get_value())

        # Aplica enquadramento e EDC
        quadros = self.simulador.aplicar_enquadramento(tipo_enq, texto, tam, tipo_edc)
        self.enlace_lbl.set_text("Quadros: " + ' '.join(''.join(str(b) for b in q) for q in quadros))

        # Constrói stream de bits
        if self.payload_only_cb.get_active():
            bits_stream = [int(bit) for char in texto for bit in format(ord(char), '08b')]
            title_suffix = "(payload only)"
        else:
            bits_stream = [b for q in quadros for b in q]
            title_suffix = "(full stream)"

        # Modulação digital (banda base)
        tipo_mod = {
            "NRZ-Polar": "nrz_polar",
            "Manchester": "manchester",
            "Bipolar": "bipolar"
        }[self.mod_dig_combo.get_active_text()]
        res_d = self.simulador.modular_digital(tipo_mod, [bits_stream])
        if isinstance(res_d, tuple) and len(res_d) == 2:
            t_d, sinal_d = res_d
        else:
            sinal_d = np.array(res_d)
            t_d = np.arange(len(sinal_d))

        # Modulação por portadora
        tipo_mp = self.mod_port_combo.get_active_text()
        if tipo_mp == "ASK":
            modp = CamadaFisica(ASK(freq_portadora=5.0, amostras_por_bit=100))
        elif tipo_mp == "FSK":
            modp = CamadaFisica(FSK(freq_p_bit0=3.0, freq_p_bit1=7.0, amostras_por_bit=100))
        else:  # 8-QAM
            modp = CamadaFisica(QAM8(freq_portadora=5.0, amostras_por_simbolo=100))

        res_p = modp.transmitir(bits_stream)
        if isinstance(res_p, tuple) and len(res_p) == 2:
            t_p, sinal_p = res_p
        else:
            sinal_p = np.array(res_p)
            t_p = np.arange(len(sinal_p))

        # Plotagem dos gráficos
        self.figure.clf()

        # Sinal digital
        ax1 = self.figure.add_subplot(211)
        ax1.plot(t_d, sinal_d, drawstyle='steps-post')
        ax1.set_title(f"Digital {title_suffix}")
        ax1.set_ylabel("Amplitude")
        n = len(bits_stream)
        ax1.set_xticks(np.arange(n) * (len(sinal_d) / n))
        ax1.set_xticklabels([f"b{i}" for i in range(n)], rotation=90)

        # Sinal modulado
        ax2 = self.figure.add_subplot(212)
        ax2.plot(t_p, sinal_p)
        ax2.set_title(f"Portadora {title_suffix}")
        ax2.set_ylabel("Amplitude")
        ax2.set_xlabel("Tempo (s)")
        mod = modp.modulador
        spb = getattr(mod, 'amostras_por_bit', getattr(mod, 'amostras_por_simbolo', 1))
        ax2.set_xticks(np.arange(n) * spb)
        ax2.set_xticklabels([f"b{i}" for i in range(n)], rotation=90)

        self.figure.tight_layout()
        self.canvas.draw()

        # Envio do sinal digital via socket TCP
        try:
            s = socket.socket()
            s.connect((self.host_entry.get_text(), int(self.port_spin.get_value())))
            s.sendall(pickle.dumps(sinal_d))
            s.close()
            self.status_lbl.set_text("Status: Enviado")
        except Exception as e:
            self.status_lbl.set_text(f"Erro TCP: {e}")

    def on_limpar(self, _):
        """Limpa a interface gráfica e os campos"""
        self.input_entry.set_text("")
        self.enlace_lbl.set_text("Quadros: —")
        self.payload_only_cb.set_active(False)
        self.figure.clf()
        self.canvas.draw()
        self.status_lbl.set_text("Status: —")

# Execução principal
if __name__ == "__main__":
    win = TransmissorGUI()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
