import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from simulador import Simulador


class SimuladorInterface(Gtk.Window):
    def __init__(self):
        self.simulador = Simulador()
        Gtk.Window.__init__(self, title="Simulador de Camadas de Rede")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Configurações Gerais
        config_frame = Gtk.Frame(label="Configuração Geral")
        config_grid = Gtk.Grid(row_spacing=5, column_spacing=10, margin=10)
        config_frame.add(config_grid)

        self.quadro_spin = Gtk.SpinButton()
        self.quadro_spin.set_range(1, 2048)
        self.edc_spin = Gtk.SpinButton()
        self.edc_spin.set_range(1, 64)

        self.enquadramento_combo = Gtk.ComboBoxText()
        self.enquadramento_combo.append_text("Contagem de caracteres")
        self.enquadramento_combo.append_text("FLAG + Inserção de bytes")
        self.enquadramento_combo.append_text("FLAG + Inserção de bits")
        self.enquadramento_combo.set_active(0)

        self.erro_combo = Gtk.ComboBoxText()
        self.erro_combo.append_text("Paridade par")
        self.erro_combo.append_text("CRC-32")
        self.erro_combo.append_text("Hamming")
        self.erro_combo.set_active(0)

        self.modulacao_digital_combo = Gtk.ComboBoxText()
        self.modulacao_digital_combo.append_text("NRZ-Polar")
        self.modulacao_digital_combo.append_text("Manchester")
        self.modulacao_digital_combo.append_text("Bipolar")
        self.modulacao_digital_combo.set_active(0)

        self.modulacao_analogica_combo = Gtk.ComboBoxText()
        self.modulacao_analogica_combo.append_text("ASK")
        self.modulacao_analogica_combo.append_text("FSK")
        self.modulacao_analogica_combo.append_text("8-QAM")
        self.modulacao_analogica_combo.set_active(0)

        config_grid.attach(Gtk.Label(label="Tamanho Máximo de Quadro:"), 0, 0, 1, 1)
        config_grid.attach(self.quadro_spin, 1, 0, 1, 1)
        config_grid.attach(Gtk.Label(label="Tamanho do EDC:"), 2, 0, 1, 1)
        config_grid.attach(self.edc_spin, 3, 0, 1, 1)
        config_grid.attach(Gtk.Label(label="Tipo de Enquadramento:"), 0, 1, 1, 1)
        config_grid.attach(self.enquadramento_combo, 1, 1, 1, 1)
        config_grid.attach(Gtk.Label(label="Detecção/Correção de Erros:"), 2, 1, 1, 1)
        config_grid.attach(self.erro_combo, 3, 1, 1, 1)
        config_grid.attach(Gtk.Label(label="Modulação Digital:"), 0, 2, 1, 1)
        config_grid.attach(self.modulacao_digital_combo, 1, 2, 1, 1)
        config_grid.attach(Gtk.Label(label="Modulação Analógica:"), 2, 2, 1, 1)
        config_grid.attach(self.modulacao_analogica_combo, 3, 2, 1, 1)

        main_box.pack_start(config_frame, False, False, 0)

        # Entrada de Texto
        entrada_frame = Gtk.Frame(label="Entrada de Texto (Transmissor)")
        self.input_entry = Gtk.Entry()
        entrada_frame.add(self.input_entry)
        main_box.pack_start(entrada_frame, False, False, 0)

        # Botões
        button_box = Gtk.Box(spacing=10)
        simular_button = Gtk.Button(label="Simular")
        simular_button.connect("clicked", self.simular)
        limpar_button = Gtk.Button(label="Limpar")
        limpar_button.connect("clicked", self.limpar)
        button_box.pack_start(simular_button, True, True, 0)
        button_box.pack_start(limpar_button, True, True, 0)
        main_box.pack_start(button_box, False, False, 0)

        # Notebook com etapas intermediárias
        notebook = Gtk.Notebook()
        self.enlace_label = Gtk.Label(label="Saída da Camada de Enlace")
        self.fisica_label = Gtk.Label(label="Saída da Camada Física")
        self.rx_label = Gtk.Label(label="Saída do Receptor")

        notebook.append_page(self.enlace_label, Gtk.Label(label="Camada de Enlace"))
        notebook.append_page(self.fisica_label, Gtk.Label(label="Camada Física"))
        notebook.append_page(self.rx_label, Gtk.Label(label="Receptor"))

        main_box.pack_start(notebook, True, True, 0)

        # Saída Final
        saida_frame = Gtk.Frame(label="Saída Final do Receptor")
        self.output_label = Gtk.Label(label="")
        saida_frame.add(self.output_label)
        main_box.pack_start(saida_frame, False, False, 0)

    def simular(self, button):
        texto = self.input_entry.get_text()
        tipo_gui = self.enquadramento_combo.get_active_text()

        # Mapeia o texto do ComboBox para o identificador do simulador
        if tipo_gui == "Contagem de caracteres":
            tipo = "contagem_caracteres"
        elif tipo_gui == "FLAG + Inserção de bytes":
            tipo = "flag_insercao_bytes"
        else:
            tipo = "flag_insercao_bits"

        quadros = self.simulador.aplicar_enquadramento(tipo, texto)

        # Transforma os quadros (listas de inteiros) em strings de bits para exibição
        quadros_str = [''.join(str(b) for b in quadro) for quadro in quadros]
        resultado = "\n".join(f"Quadro {i+1}: {q}" for i, q in enumerate(quadros_str))

        self.enlace_label.set_text(resultado)
        self.fisica_label.set_text("Física: (ainda não implementado)")
        self.rx_label.set_text("Rx: (ainda não implementado)")
        self.output_label.set_text("Texto final: (ainda não implementado)")


    def limpar(self, button):
        self.input_entry.set_text("")
        self.output_label.set_text("")
        self.enlace_label.set_text("Saída da Camada de Enlace")
        self.fisica_label.set_text("Saída da Camada Física")
        self.rx_label.set_text("Saída do Receptor")

win = SimuladorInterface()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
