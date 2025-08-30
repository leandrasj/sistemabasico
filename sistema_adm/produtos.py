from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
import sqlite3

Builder.load_file('telas_gerenciamento/meulayout.kv')

#CADASTRO DE PRODUTOS
class TelaProdutos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Produtos",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'gerenciamento')]],
            md_bg_color = "#FF9800",
            pos_hint={"top": 1}
        )
        
        # Card principal
        main_card = MDCard(
            orientation="vertical",
            spacing="20dp",
            padding="30dp",
            size_hint=(0.9, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            elevation=3,
            md_bg_color="#FFFFFF",
            radius=[20, 20, 20, 20]
        )
        
        # Título
        title = MDLabel(
            text="Cadastrar Produto",
            font_style="H5",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        
        # Campos de entrada
        self.nome_input = MDTextField(
            hint_text='Nome do Produto',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="package-variant"
        )
        
        self.descricao_input = MDTextField(
            hint_text='Descrição',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="text"
        )
        
        self.mensagem = MDLabel(
            text='',
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        
        # Botões
        btn_cadastrar = MDRaisedButton(
            text='CADASTRAR PRODUTO',
            size_hint_y=None,
            height="50dp",
            md_bg_color="#FF9800",
            on_press=self.cadastrar_produto
        )
        
        btn_listar = MDFlatButton(
            text='Ver Lista de Produtos',
            size_hint_y=None,
            height="40dp",
            theme_text_color="Primary",
            on_press=lambda x: setattr(self.manager, 'current', 'listagem_produtos')
        )
        
        # Adicionando widgets ao card
        main_card.add_widget(title)
        main_card.add_widget(self.nome_input)
        main_card.add_widget(self.descricao_input)
        main_card.add_widget(btn_cadastrar)
        main_card.add_widget(btn_listar)
        main_card.add_widget(self.mensagem)
        
        self.add_widget(toolbar)
        self.add_widget(main_card)
    
    def cadastrar_produto(self, instance):
        nome = self.nome_input.text
        descricao = self.descricao_input.text
        
        if nome and descricao:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO produto (nome, descricao) VALUES (?, ?)", (nome, descricao))
                conn.commit()
                self.mensagem.text = 'Produto cadastrado com sucesso!'
                self.mensagem.theme_text_color = "Primary"
                self.nome_input.text = ''
                self.descricao_input.text = ''
            except sqlite3.Error as e:
                self.mensagem.text = f'Erro: {str(e)}'
                self.mensagem.theme_text_color = "Error"
            finally:
                conn.close()
        else:
            self.mensagem.text = 'Preencha todos os campos!'
            self.mensagem.theme_text_color = "Error"
            
# LISTAGEM DE SERVICOS
class ListagemProdutos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Lista de Produtos",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'produtos')]],
            md_bg_color="#FF9800",
            pos_hint={"top": 1}
        )
        
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            spacing="10dp",
            padding="20dp",
            size_hint=(1, 0.85),
            pos_hint={"y": 0}
        )
        
        self.scrollview = MDScrollView(size_hint=(1, 1))
        self.grid = MDGridLayout(
            cols=1,
            spacing="10dp",
            adaptive_height=True
        )
        self.scrollview.add_widget(self.grid)
        self.main_layout.add_widget(self.scrollview)
        
        self.add_widget(toolbar)
        self.add_widget(self.main_layout)
    
    def on_pre_enter(self, *args):
        self.atualizar_lista()
    
    def atualizar_lista(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, descricao FROM produto")
        produtos = cursor.fetchall()
        conn.close()

        if not produtos:
            empty_card = MDCard(
                size_hint_y=None,
                height="100dp",
                elevation=1,
                md_bg_color="#FFFFFF",
                radius=[10, 10, 10, 10],
                padding="20dp"
            )
            empty_label = MDLabel(
                text='Nenhum produto cadastrado.',
                halign="center",
                theme_text_color="Secondary"
            )
            empty_card.add_widget(empty_label)
            self.grid.add_widget(empty_card)
        else:
            for id_, nome, descricao in produtos:
                product_card = MDCard(
                    orientation="vertical",
                    size_hint_y=None,
                    height="120dp",
                    elevation=2,
                    md_bg_color="#FFFFFF",
                    radius=[10, 10, 10, 10],
                    padding="20dp",
                    spacing="10dp"
                )
                
                # Cabeçalho do produto
                header_layout = MDBoxLayout(
                    size_hint_y=None,
                    height="40dp",
                    spacing="10dp"
                )
                
                # Ícone do produto
                product_icon = MDIconButton(
                    icon="package-variant",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("40dp", "40dp")
                )
                
                # Informações do produto
                info_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="2dp"
                )
                
                name_label = MDLabel(
                    text=nome,
                    font_style="Subtitle1",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height="25dp"
                )
                
                desc_label = MDLabel(
                    text=descricao,
                    font_style="Caption",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height="20dp"
                )
                
                info_layout.add_widget(name_label)
                info_layout.add_widget(desc_label)
                
                # Botões de ação
                action_layout = MDBoxLayout(
                    size_hint_x=None,
                    width="80dp",
                    spacing="5dp"
                )
                
                btn_editar = MDIconButton(
                    icon="pencil",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("35dp", "35dp"),
                    on_press=lambda inst, i=id_, n=nome, d=descricao: self.popup_editar(i, n, d)
                )
                
                btn_excluir = MDIconButton(
                    icon="delete",
                    theme_icon_color="Error",
                    size_hint=(None, None),
                    size=("35dp", "35dp"),
                    on_press=lambda inst, i=id_: self.excluir_produto(i)
                )
                
                action_layout.add_widget(btn_editar)
                action_layout.add_widget(btn_excluir)
                
                header_layout.add_widget(product_icon)
                header_layout.add_widget(info_layout)
                header_layout.add_widget(action_layout)
                
                product_card.add_widget(header_layout)
                self.grid.add_widget(product_card)

    def excluir_produto(self, produto_id):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produto WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
        self.atualizar_lista()

    def popup_editar(self, produto_id, nome_atual, descricao_atual):
        content = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            padding="20dp",
            size_hint_y=None,
            height="250dp"
        )
        
        # Armazenar referências aos campos
        self.nome_field = MDTextField(
            text=nome_atual,
            hint_text="Nome do produto",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.descricao_field = MDTextField(
            text=descricao_atual,
            hint_text="Descrição",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        content.add_widget(self.nome_field)
        content.add_widget(self.descricao_field)
        
        self.dialog_editar = MDDialog(
            title="Editar Produto",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    theme_text_color="Primary",
                    on_press=lambda x: self.dialog_editar.dismiss()
                ),
                MDRaisedButton(
                    text="SALVAR",
                    md_bg_color="#FF9800",
                    on_press=lambda x: self.salvar_edicao(produto_id)
                ),
            ],
        )
        self.dialog_editar.open()

    def salvar_edicao(self, produto_id):
        # Acessar os valores dos campos
        novo_nome = self.nome_field.text.strip()
        nova_descricao = self.descricao_field.text.strip()
        
        # Validar campos
        if not novo_nome or not nova_descricao:
            # Mostrar mensagem de erro se campos estiverem vazios
            return
        
        # Atualizar no banco de dados
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE produto SET nome=?, descricao=? WHERE id=?", 
                      (novo_nome, nova_descricao, produto_id))
        conn.commit()
        conn.close()
        
        # Fechar dialog e atualizar lista
        self.dialog_editar.dismiss()
        self.atualizar_lista()
        
# CADASTRO DE SERVICOS 
class TelaServicos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Serviços",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'gerenciamento')]],
            md_bg_color="#9C27B0",
            pos_hint={"top": 1}
        )
        
        # Card principal
        main_card = MDCard(
            orientation="vertical",
            spacing="20dp",
            padding="30dp",
            size_hint=(0.9, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            elevation=3,
            md_bg_color="#FFFFFF",
            radius=[20, 20, 20, 20]
        )
        
        # Título
        title = MDLabel(
            text="Cadastrar Serviço",
            font_style="H5",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        
        # Campo para cadastro de serviços
        self.descricao_input = MDTextField(
            hint_text='Descrição do Serviço',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="tools"
        )
        
        self.mensagem = MDLabel(
            text='',
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        
        # Botões
        btn_cadastrar = MDRaisedButton(
            text='CADASTRAR SERVIÇO',
            size_hint_y=None,
            height="50dp",
            md_bg_color="#9C27B0",
            on_press=self.cadastrar_servico
        )
        
        btn_listar = MDFlatButton(
            text='Ver Lista de Serviços',
            size_hint_y=None,
            height="40dp",
            theme_text_color="Primary",
            on_press=lambda x: setattr(self.manager, 'current', 'listagem_servicos')
        )
        
        # Adicionando widgets ao card
        main_card.add_widget(title)
        main_card.add_widget(self.descricao_input)
        main_card.add_widget(btn_cadastrar)
        main_card.add_widget(btn_listar)
        main_card.add_widget(self.mensagem)
        
        self.add_widget(toolbar)
        self.add_widget(main_card)
    
    def cadastrar_servico(self, instance):
        descricao = self.descricao_input.text
        
        if descricao:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO servicos (descricao) VALUES (?)", (descricao,))
                conn.commit()
                self.mensagem.text = 'Serviço cadastrado com sucesso!'
                self.mensagem.theme_text_color = "Primary"
                self.descricao_input.text = ''
            except sqlite3.Error as e:
                self.mensagem.text = f'Erro: {str(e)}'
                self.mensagem.theme_text_color = "Error"
            finally:
                conn.close()
        else:
            self.mensagem.text = 'Preencha a descrição do serviço!'
            self.mensagem.theme_text_color = "Error"

# LISTAGEM DE SERVICOS
class ListagemServicos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Lista de Serviços",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'servicos')]],
            md_bg_color="#9C27B0",
            pos_hint={"top": 1}
        )
        
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            spacing="10dp",
            padding="20dp",
            size_hint=(1, 0.85),
            pos_hint={"y": 0}
        )
        
        self.scrollview = MDScrollView(size_hint=(1, 1))
        self.grid = MDGridLayout(
            cols=1,
            spacing="10dp",
            adaptive_height=True
        )
        self.scrollview.add_widget(self.grid)
        self.main_layout.add_widget(self.scrollview)
        
        self.add_widget(toolbar)
        self.add_widget(self.main_layout)
    
    def on_pre_enter(self, *args):
        self.atualizar_lista()
    
    def atualizar_lista(self):
        self.grid.clear_widgets()
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao FROM servicos")
        servicos = cursor.fetchall()
        conn.close()

        if not servicos:
            empty_card = MDCard(
                size_hint_y=None,
                height="100dp",
                elevation=1,
                md_bg_color="#FFFFFF",
                radius=[10, 10, 10, 10],
                padding="20dp"
            )
            empty_label = MDLabel(
                text='Nenhum serviço cadastrado.',
                halign="center",
                theme_text_color="Secondary"
            )
            empty_card.add_widget(empty_label)
            self.grid.add_widget(empty_card)
        else:
            for id_, descricao in servicos:
                service_card = MDCard(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="80dp",
                    elevation=2,
                    md_bg_color="#FFFFFF",
                    radius=[10, 10, 10, 10],
                    padding="20dp",
                    spacing="15dp"
                )
                
                # Ícone do serviço
                icon_layout = MDBoxLayout(
                    size_hint_x=None,
                    width="40dp",
                    pos_hint={"center_y": 0.5}
                )
                
                service_icon = MDIconButton(
                    icon="tools",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("40dp", "40dp")
                )
                icon_layout.add_widget(service_icon)
                
                # Informações do serviço
                info_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="5dp"
                )
                
                desc_label = MDLabel(
                    text=descricao,
                    font_style="Subtitle1",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height="30dp"
                )
                
                info_layout.add_widget(desc_label)
                
                # Botões de ação
                action_layout = MDBoxLayout(
                    size_hint_x=None,
                    width="80dp",
                    spacing="5dp"
                )
                
                btn_editar = MDIconButton(
                    icon="pencil",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("35dp", "35dp"),
                    on_press=lambda inst, i=id_, d=descricao: self.popup_editar(i, d)
                )
                
                btn_excluir = MDIconButton(
                    icon="delete",
                    theme_icon_color="Error",
                    size_hint=(None, None),
                    size=("35dp", "35dp"),
                    on_press=lambda inst, i=id_: self.excluir_servico(i)
                )
                
                action_layout.add_widget(btn_editar)
                action_layout.add_widget(btn_excluir)
                
                service_card.add_widget(icon_layout)
                service_card.add_widget(info_layout)
                service_card.add_widget(action_layout)
                
                self.grid.add_widget(service_card)

    def excluir_servico(self, servico_id):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicos WHERE id=?", (servico_id,))
        conn.commit()
        conn.close()
        self.atualizar_lista()

    def popup_editar(self, servico_id, descricao_atual):
        content = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            padding="20dp",
            size_hint_y=None,
            height="200dp"
        )
        
        # Armazenar referência ao campo
        self.descricao_field = MDTextField(
            text=descricao_atual,
            hint_text="Descrição do serviço",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        content.add_widget(self.descricao_field)
        
        self.dialog_editar = MDDialog(
            title="Editar Serviço",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    theme_text_color="Primary",
                    on_press=lambda x: self.dialog_editar.dismiss()
                ),
                MDRaisedButton(
                    text="SALVAR",
                    md_bg_color="#9C27B0",
                    on_press=lambda x: self.salvar_edicao(servico_id)
                ),
            ],
        )
        self.dialog_editar.open()

    def salvar_edicao(self, servico_id):
        # Acessar o valor do campo
        nova_descricao = self.descricao_field.text.strip()
        
        # Validar campo
        if not nova_descricao:
            # Mostrar mensagem de erro se campo estiver vazio
            return
        
        # Atualizar no banco de dados
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE servicos SET descricao=? WHERE id=?", 
                      (nova_descricao, servico_id))
        conn.commit()
        conn.close()
        
        # Fechar dialog e atualizar lista
        self.dialog_editar.dismiss()
        self.atualizar_lista()