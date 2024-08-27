
# Angry Birds Clone

Este é um clone simples do jogo Angry Birds feito em Python usando Pygame.

## Instalação

Você pode instalar este pacote diretamente do GitHub:

```sh
pip install git+https://github.com/feijonts/angry_birds_clone.git
```

## Uso

Depois de instalado, você pode iniciar o jogo executando:

```sh
angry_birds_clone
```

## Requisitos

- Python 3.6 ou superior
- Pygame 2.0.0 ou superior

## Estrutura do Projeto

```
angry_birds_clone/
│
├── angry_birds_clone/
│   ├── __init__.py
│   ├── defeat_screen.py
│   ├── game_screen.py
│   ├── main.py
│   ├── menu_screen.py
│   ├── settings.py
│   └── assets/
│       ├── bird.png
│       ├── porco.png
│       ├── planet.png
│       └── heart.png
│
├── setup.py
├── README.md
└── MANIFEST.in
```

## Descrição

Este projeto é uma implementação simples do famoso jogo Angry Birds usando Python e Pygame. O jogador controla um pássaro que deve ser lançado em direção aos porcos, tentando destruí-los todos. O jogo inclui física básica, elementos interativos e uma tela de derrota que permite reiniciar o jogo.

## Funcionalidades

- Lançamento do pássaro com física simulada
- Planetas com gravidade que afetam a trajetória do pássaro
- Porcos que podem ser destruídos ao serem atingidos
- Limite de tentativas baseado na quantidade de porcos
- Sistema de vidas representado por corações na tela
- Tela de derrota com opção de reiniciar o jogo

## Contribuindo

Se você quiser contribuir com este projeto, sinta-se à vontade para fazer um fork do repositório e enviar um pull request.

## Contato

- **Autor**: João Whitaker Citino & Matheus Porto
- **Email**: joaocitino10@gmail.com
- **GitHub**: [feijonts](https://github.com/feijonts)
