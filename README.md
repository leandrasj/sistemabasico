# 📱 Sistema de Gerenciamento Mobile - Portfolio Edition

> Um aplicativo mobile moderno desenvolvido com Python, Kivy e KivyMD com interface Material Design

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Kivy](https://img.shields.io/badge/Kivy-2.3.1-green.svg)
![KivyMD](https://img.shields.io/badge/KivyMD-1.1.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Sobre o Projeto

Este é um **aplicativo mobile multiplataforma** desenvolvido para demonstrar habilidades em desenvolvimento mobile com Python. O app implementa um sistema completo de gerenciamento com interface moderna seguindo as diretrizes do Material Design.

### ✨ Características Principais

- 🎨 **Interface Moderna**: Design Material seguindo as melhores práticas do Google
- 📱 **Responsivo**: Interface adaptável para diferentes tamanhos de tela
- 🔐 **Sistema de Autenticação**: Login e cadastro de usuários com validação
- 📊 **CRUD Completo**: Gerenciamento de usuários, produtos e serviços
- 🗄️ **Banco de Dados**: SQLite integrado para persistência de dados
- 🔄 **Navegação Fluida**: Transições suaves entre telas
- 🎯 **UX Otimizada**: Feedback visual e validação de formulários

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.12+ | Linguagem principal de desenvolvimento |
| **Kivy** | 2.3.1 | Framework para aplicações multiplataforma |
| **KivyMD** | 1.1.1 | Biblioteca de componentes Material Design |
| **SQLite** | 3.x | Banco de dados local |

## 🏗️ Arquitetura do Aplicativo

```
📁 versao_atual/
├── 📄 main.py                    # Aplicação principal e telas base
├── 📄 produtos.py               # Módulo de produtos e serviços
├── 🗃️ banco.db                 # Banco de dados SQLite
├── 📁 img/
│   └── 🖼️ logo.png            # Logo da aplicação
└── 📁 telas_gerenciamento/
    └── 📄 meulayout.kv         # Estilos e temas
```

## 🚀 Funcionalidades

### 🔐 Autenticação
- **Login seguro** com validação de credenciais
- **Cadastro de usuários** com validação de email e senha
- **Criptografia básica** para proteção de dados

### 👥 Gerenciamento de Usuários
- Lista todos os usuários cadastrados
- Edição inline de informações
- Exclusão com confirmação
- Interface em cards com ícones

### 📦 Gestão de Produtos
- Cadastro com nome e descrição
- Listagem em cards visuais
- Sistema completo de CRUD
- Validação de formulários

### 🔧 Controle de Serviços
- Cadastro de serviços oferecidos
- Interface otimizada para mobile
- Gestão completa com edição/exclusão

## 🎨 Design System

### Paleta de Cores
- **Azul Principal**: `#1976D2` - Elementos primários
- **Laranja Secundário**: `#FF9800` - Produtos e destaques  
- **Roxo Accent**: `#9C27B0` - Serviços e ações especiais
- **Verde Sucesso**: `#4CAF50` - Estados positivos
- **Cinza Claro**: `#F5F5F5` - Backgrounds e cards

### Componentes Visuais
- **Cards elevados** com sombras suaves
- **Botões com bordas arredondadas**
- **Campos de texto no estilo Material**
- **Ícones consistentes** do Material Design
- **Toolbar com navegação intuitiva**

## 📱 Capturas de Tela

### Tela de Login
- Interface limpa e moderna
- Logo centralizado
- Campos com validação visual
- Botões com feedback tátil

### Dashboard Principal
- Cards de navegação coloridos
- Ícones informativos
- Layout responsivo
- Acesso rápido às funcionalidades

### Gerenciamento
- Listas em cards visuais
- Ações inline (editar/excluir)
- Diálogos modais elegantes
- Feedback visual imediato

## 🔧 Como Executar

### Pré-requisitos
```bash
pip install kivy kivymd
```

### Execução
```bash
cd versao_atual
python main.py
```

## 📈 Melhorias Implementadas

Esta versão "Portfolio Edition" inclui as seguintes melhorias visuais e funcionais:

### 🎨 Interface
- ✅ Migração completa para KivyMD
- ✅ Implementação do Material Design 3.0
- ✅ Paleta de cores moderna e consistente
- ✅ Cards com elevação e sombras
- ✅ Ícones vetoriais integrados

### 📱 UX/UI
- ✅ Toolbar com navegação clara
- ✅ Feedback visual em todas as ações
- ✅ Diálogos modais para edição
- ✅ Validação de formulários em tempo real
- ✅ Mensagens de erro/sucesso estilizadas

### 🔧 Código
- ✅ Arquitetura modular organizada
- ✅ Tratamento robusto de erros
- ✅ Código comentado e documentado
- ✅ Boas práticas de desenvolvimento
- ✅ Compatibilidade multiplataforma

## 📋 Casos de Uso

Este aplicativo demonstra competências em:

- **Desenvolvimento Mobile**: Criação de apps nativos com Python
- **Design de Interface**: Implementação de Material Design
- **Gerenciamento de Estado**: Navegação entre telas e dados
- **Banco de Dados**: Integração com SQLite
- **Validação**: Formulários e entrada de dados
- **UX Design**: Interface intuitiva e responsiva

## 🤝 Contribuições

Este projeto foi desenvolvido como demonstração de habilidades em desenvolvimento mobile. Sugestões e melhorias são sempre bem-vindas!

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido com ❤️ usando Python, Kivy e KivyMD**

*Portfolio de Desenvolvimento Mobile - 2024*