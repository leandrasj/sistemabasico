import sqlite3
import re
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.window import Window
from kivy.lang import Builder
from produtos import TelaProdutos
from produtos import ListagemProdutos
from produtos import ListagemServicos
from produtos import TelaServicos

Window.size = (350, 600)

Builder.load_file('telas_gerenciamento/meulayout.kv')

# CRIAÇÃO DE TABELAS DE BANCO DE DADOS
def inicializar_banco():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de produtos com nome e descrição
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    ''')

    # Tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela de serviços
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

#TELA DE LOGIN 
class TelaLogin(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Card principal
        main_card = MDCard(
            orientation="vertical",
            spacing="20dp",
            padding="30dp",
            size_hint=(0.9, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=3,
            md_bg_color="#FFFFFF",
            radius=[20, 20, 20, 20]
        )
        
        # Título
        title = MDLabel(
            text="Bem-vindo!",
            theme_text_color="Primary",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        main_card.add_widget(title)
        
        # Campos de entrada
        self.usuario_input = MDTextField(
            hint_text='Usuário',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="account"
        )
        
        self.senha_input = MDTextField(
            hint_text='Senha',
            password=True,
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="eye-off"
        )
        
        self.mensagem = MDLabel(
            text='',
            theme_text_color="Error",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )

        # Botões
        btn_login = MDRaisedButton(
            text='ENTRAR',
            size_hint_y=None,
            height="50dp",
            md_bg_color="#1976D2",
            on_press=self.validar_login
        )

        btn_cadastro = MDFlatButton(
            text='Não tem conta? Cadastre-se',
            size_hint_y=None,
            height="40dp",
            theme_text_color="Primary",
            on_press=lambda x: setattr(self.manager, 'current', 'cadastro')
        )

        main_card.add_widget(self.usuario_input)
        main_card.add_widget(self.senha_input)
        main_card.add_widget(btn_login)
        main_card.add_widget(self.mensagem)
        main_card.add_widget(btn_cadastro)

        self.add_widget(main_card)

    def validar_login(self, instance):
        usuario = self.usuario_input.text
        senha = self.senha_input.text

        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            self.manager.current = 'gerenciamento'
        else:
            self.mensagem.text = 'Usuário ou senha incorretos'
            
    def logotiop(self):
        self.ids.img.source = 'img/imagem02.pgn'

#TELA DE CADASTRO
class TelaCadastro(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Cadastro de Usuário",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'login')]],
            md_bg_color="#1976D2",
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

        # Campos de entrada
        self.usuario_input = MDTextField(
            hint_text='Novo usuário (mín. 4 caracteres)',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="account-plus"
        )
        
        self.senha_input = MDTextField(
            hint_text='Nova senha (mín. 6 caracteres)',
            password=True,
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="lock"
        )
        
        self.email_input = MDTextField(
            hint_text='Seu email (ex: usuario@gmail.com)',
            mode="rectangle",
            size_hint_y=None,
            height="60dp",
            icon_right="email"
        )

        self.mensagem = MDLabel(
            text='',
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="40dp"
        )

        # Botões
        btn_salvar = MDRaisedButton(
            text='SALVAR',
            size_hint_y=None,
            height="50dp",
            md_bg_color="#4CAF50",
            on_press=self.salvar_usuario
        )

        main_card.add_widget(self.usuario_input)
        main_card.add_widget(self.senha_input)
        main_card.add_widget(self.email_input)
        main_card.add_widget(btn_salvar)
        main_card.add_widget(self.mensagem)

        self.add_widget(toolbar)
        self.add_widget(main_card)

    def validar_email(self, email):
        """Verifica se o email tem um formato válido"""
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None

    def salvar_usuario(self, instance):
        usuario = self.usuario_input.text.strip()
        senha = self.senha_input.text.strip()
        email = self.email_input.text.strip()

        try:
            # Validações
            if not usuario or not senha or not email:
                raise ValueError("Todos os campos são obrigatórios!")
            
            if len(usuario) < 4:
                raise ValueError("Usuário deve ter no mínimo 4 caracteres!")
            
            if len(senha) < 6:
                raise ValueError("Senha deve ter no mínimo 6 caracteres!")
            
            if not self.validar_email(email):
                raise ValueError("Por favor, insira um e-mail válido!")

            # Conexão com o banco de dados
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            
            # Verifica se usuário ou email já existem
            cursor.execute("SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,))
            if cursor.fetchone():
                raise sqlite3.IntegrityError("Usuário já cadastrado!")
            
            # Insere no banco
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", 
                          (usuario, senha))
            conn.commit()
            
            self.mensagem.text = 'Usuário cadastrado com sucesso!'
            self.mensagem.theme_text_color = "Primary"
            self.usuario_input.text = ''
            self.senha_input.text = ''
            self.email_input.text = ''
            
        except (sqlite3.IntegrityError, ValueError) as e:
            self.mensagem.text = str(e)
            self.mensagem.theme_text_color = "Error"
        except Exception as e:
            self.mensagem.text = f'Erro inesperado: {str(e)}'
            self.mensagem.theme_text_color = "Error"
        finally:
            if 'conn' in locals():
                conn.close()

# TELA DE GERENCIAMENTO
class TelaGerenciamento(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Gerenciamento",
            right_action_items=[["logout", lambda x: setattr(self.manager, 'current', 'login')]],
            md_bg_color="#1976D2",
            pos_hint={"top": 1}
        )
        
        # Scroll para os cards
        scroll = MDScrollView(size_hint=(1, 0.85), pos_hint={"y": 0})
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding="20dp",
            adaptive_height=True
        )
        
        # Card de boas-vindas
        welcome_card = MDCard(
            orientation="vertical",
            padding="20dp",
            size_hint_y=None,
            height="120dp",
            elevation=2,
            md_bg_color="#E3F2FD",
            radius=[15, 15, 15, 15]
        )
        
        welcome_title = MDLabel(
            text="Sistema de Gerenciamento",
            font_style="H5",
            theme_text_color="Primary",
            halign="center"
        )
        
        welcome_subtitle = MDLabel(
            text="Gerencie usuários, produtos e serviços",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            halign="center"
        )
        
        welcome_card.add_widget(welcome_title)
        welcome_card.add_widget(welcome_subtitle)
        
        # Cards de navegação
        nav_cards = [
            {"title": "Usuários", "subtitle": "Gerenciar usuários do sistema", "icon": "account-group", "color": "#4CAF50", "screen": "listagem"},
            {"title": "Produtos", "subtitle": "Cadastrar e listar produtos", "icon": "package-variant", "color": "#FF9800", "screen": "produtos"},
            {"title": "Serviços", "subtitle": "Gerenciar serviços oferecidos", "icon": "tools", "color": "#9C27B0", "screen": "servicos"}
        ]
        
        main_layout.add_widget(welcome_card)
        
        for card_info in nav_cards:
            nav_card = self.create_nav_card(card_info)
            main_layout.add_widget(nav_card)
            
        scroll.add_widget(main_layout)
        self.add_widget(toolbar)
        self.add_widget(scroll)
        
    def create_nav_card(self, info):
        card = MDCard(
            orientation="horizontal",
            padding="20dp",
            spacing="20dp",
            size_hint_y=None,
            height="80dp",
            elevation=3,
            md_bg_color="#FFFFFF",
            radius=[10, 10, 10, 10],
            on_press=lambda x: setattr(self.manager, 'current', info["screen"])
        )
        
        icon_card = MDCard(
            size_hint=(None, None),
            size=("50dp", "50dp"),
            md_bg_color=info["color"],
            radius=[25, 25, 25, 25],
            elevation=0
        )
        
        icon = MDIconButton(
            icon=info["icon"],
            theme_icon_color="Custom",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        icon_card.add_widget(icon)
        
        text_layout = MDBoxLayout(
            orientation="vertical",
            spacing="5dp"
        )
        
        title = MDLabel(
            text=info["title"],
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp"
        )
        
        subtitle = MDLabel(
            text=info["subtitle"],
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        
        text_layout.add_widget(title)
        text_layout.add_widget(subtitle)
        
        card.add_widget(icon_card)
        card.add_widget(text_layout)
        
        return card

# TELA DE LISTAGEM DE USUÁRIOS
class TelaListagem(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = "#F5F5F5"
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Lista de Usuários",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, 'current', 'gerenciamento')]],
            md_bg_color="#1976D2",
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
        cursor.execute("SELECT id, usuario, senha FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        if not usuarios:
            empty_card = MDCard(
                size_hint_y=None,
                height="100dp",
                elevation=1,
                md_bg_color="#FFFFFF",
                radius=[10, 10, 10, 10],
                padding="20dp"
            )
            empty_label = MDLabel(
                text='Nenhum usuário cadastrado.',
                halign="center",
                theme_text_color="Secondary"
            )
            empty_card.add_widget(empty_label)
            self.grid.add_widget(empty_card)
        else:
            for id_, usuario, senha in usuarios:
                user_card = MDCard(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="70dp",
                    elevation=2,
                    md_bg_color="#FFFFFF",
                    radius=[10, 10, 10, 10],
                    padding="15dp",
                    spacing="10dp"
                )
                
                # Ícone do usuário
                icon_layout = MDBoxLayout(
                    size_hint_x=None,
                    width="40dp",
                    pos_hint={"center_y": 0.5}
                )
                
                user_icon = MDIconButton(
                    icon="account-circle",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("40dp", "40dp")
                )
                icon_layout.add_widget(user_icon)
                
                # Informações do usuário
                info_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="2dp"
                )
                
                name_label = MDLabel(
                    text=usuario,
                    font_style="Subtitle1",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height="25dp"
                )
                
                password_label = MDLabel(
                    text=f"Senha: {senha}",
                    font_style="Caption",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height="20dp"
                )
                
                info_layout.add_widget(name_label)
                info_layout.add_widget(password_label)
                
                # Botões de ação
                action_layout = MDBoxLayout(
                    size_hint_x=None,
                    width="120dp",
                    spacing="5dp"
                )
                
                btn_editar = MDIconButton(
                    icon="pencil",
                    theme_icon_color="Primary",
                    size_hint=(None, None),
                    size=("40dp", "40dp"),
                    on_press=lambda inst, i=id_, u=usuario, s=senha: self.popup_editar(i, u, s)
                )
                
                btn_excluir = MDIconButton(
                    icon="delete",
                    theme_icon_color="Error",
                    size_hint=(None, None),
                    size=("40dp", "40dp"),
                    on_press=lambda inst, i=id_: self.excluir_usuario(i)
                )
                
                action_layout.add_widget(btn_editar)
                action_layout.add_widget(btn_excluir)
                
                user_card.add_widget(icon_layout)
                user_card.add_widget(info_layout)
                user_card.add_widget(action_layout)
                
                self.grid.add_widget(user_card)

    def excluir_usuario(self, usuario_id):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conn.commit()
        conn.close()
        self.atualizar_lista()

    def popup_editar(self, usuario_id, usuario_atual, senha_atual):
        # Criar dialog personalizado
        content = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            padding="20dp",
            size_hint_y=None,
            height="200dp"
        )
        
        usuario_field = MDTextField(
            text=usuario_atual,
            hint_text="Nome do usuário",
            mode="rectangle"
        )
        
        senha_field = MDTextField(
            text=senha_atual,
            hint_text="Senha",
            mode="rectangle"
        )
        
        content.add_widget(usuario_field)
        content.add_widget(senha_field)
        
        dialog = MDDialog(
            title="Editar Usuário",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    theme_text_color="Primary",
                    on_press=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SALVAR",
                    md_bg_color="#1976D2",
                    on_press=lambda x: self.salvar_edicao(usuario_id, usuario_field.text, senha_field.text, dialog)
                ),
            ],
        )
        dialog.open()

    def salvar_edicao(self, usuario_id, novo_usuario, nova_senha, dialog):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET usuario=?, senha=? WHERE id=?", (novo_usuario, nova_senha, usuario_id))
        conn.commit()
        conn.close()
        dialog.dismiss()
        self.atualizar_lista()

# APLICATIVO PRINCIPAL
class MeuApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Amber"
        
        inicializar_banco()
        sm = MDScreenManager()
        sm.add_widget(TelaLogin(name='login'))
        sm.add_widget(TelaCadastro(name='cadastro'))
        sm.add_widget(TelaGerenciamento(name='gerenciamento'))
        sm.add_widget(TelaListagem(name='listagem'))
        sm.add_widget(TelaProdutos(name='produtos'))
        sm.add_widget(ListagemProdutos(name='listagem_produtos'))
        sm.add_widget(TelaServicos(name='servicos')) 
        sm.add_widget(ListagemServicos(name='listagem_servicos'))
        return sm


# EXECUTAR
if __name__ == '__main__':
    MeuApp().run()
# Fim do código                                        