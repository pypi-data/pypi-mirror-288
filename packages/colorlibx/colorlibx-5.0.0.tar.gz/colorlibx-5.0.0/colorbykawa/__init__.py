import re
import builtins

class ColorByKawa:
    def __init__(self):
        # Основные и яркие цвета
        self.Reset = "\033[0m"
        self.Black = "\033[30m"
        self.Red = "\033[31m"
        self.Green = "\033[32m"
        self.Yellow = "\033[33m"
        self.Blue = "\033[34m"
        self.Magenta = "\033[35m"
        self.Cyan = "\033[36m"
        self.White = "\033[37m"
        self.Gray = "\033[90m"
        self.RedLight = "\033[91m"
        self.GreenLight = "\033[92m"
        self.YellowLight = "\033[93m"
        self.BlueLight = "\033[94m"
        self.MagentaLight = "\033[95m"
        self.CyanLight = "\033[96m"
        self.WhiteLight = "\033[97m"
        self.BlackBright = "\033[30;1m"
        self.RedBright = "\033[31;1m"
        self.GreenBright = "\033[32;1m"
        self.YellowBright = "\033[33;1m"
        self.BlueBright = "\033[34;1m"
        self.MagentaBright = "\033[35;1m"
        self.CyanBright = "\033[36;1m"
        self.WhiteBright = "\033[37;1m"

        # Цвета из палитры 256 цветов
        self.Colors256 = {
            'Orange': "\033[38;5;208m",
            'Purple': "\033[38;5;128m",
            'Turquoise': "\033[38;5;48m",
            'Brown': "\033[38;5;94m",
            'Pink': "\033[38;5;205m",
            'LightGray': "\033[38;5;250m",
            'DarkGray': "\033[38;5;235m",
            'LightRed': "\033[38;5;9m",
            'LightGreen': "\033[38;5;10m",
            'LightYellow': "\033[38;5;11m",
            'LightBlue': "\033[38;5;12m",
            'LightMagenta': "\033[38;5;13m",
            'LightCyan': "\033[38;5;14m",
            'LightWhite': "\033[38;5;15m",
            'DarkRed': "\033[38;5;88m",
            'DarkGreen': "\033[38;5;22m",
            'DarkYellow': "\033[38;5;136m",
            'DarkBlue': "\033[38;5;24m",
            'DarkMagenta': "\033[38;5;54m",
            'DarkCyan': "\033[38;5;6m",
            'DarkWhite': "\033[38;5;7m",
            'SkyBlue': "\033[38;5;39m",
            'SeaGreen': "\033[38;5;36m",
            'Indigo': "\033[38;5;54m",
            'Coral': "\033[38;5;204m",
            'Beige': "\033[38;5;230m",
            'Lime': "\033[38;5;10m",
            'Cherry': "\033[38;5;196m",
            'Salmon': "\033[38;5;209m",
            'Olive': "\033[38;5;58m",
            'Tan': "\033[38;5;180m",
            'IndigoBlue': "\033[38;5;69m",
            'Wheat': "\033[38;5;229m",
            'Honeydew': "\033[38;5;152m",
            'Mint': "\033[38;5;159m",
            'Rose': "\033[38;5;201m",
            'Moccasin': "\033[38;5;230m",
            'Caramel': "\033[38;5;130m",
            'Lavender': "\033[38;5;207m",
            'Mauve': "\033[38;5;171m",
            'Goldenrod': "\033[38;5;220m",
            'Ivory': "\033[38;5;230m",
            'Aquamarine': "\033[38;5;80m",
            'Raspberry': "\033[38;5;125m",
            'Cantaloupe': "\033[38;5;214m",
            'Ash': "\033[38;5;246m",
            'Chocolate': "\033[38;5;94m",
            'Emerald': "\033[38;5;2m",
            'Ruby': "\033[38;5;124m",
            'TerraCotta': "\033[38;5;174m",
            'MintGreen': "\033[38;5;119m",
            'Blush': "\033[38;5;217m",
            'Tangerine': "\033[38;5;208m",
            'Auburn': "\033[38;5;52m",
            'Coffee': "\033[38;5;94m",
            'Papaya': "\033[38;5;215m",
            'CherryRed': "\033[38;5;196m",
            'Cinnamon': "\033[38;5;130m",
            'Daffodil': "\033[38;5;226m",
            'MossGreen': "\033[38;5;28m",
            'Aubergine': "\033[38;5;54m",
            'Lilac': "\033[38;5;138m",
            'MoonYellow': "\033[38;5;220m",
            'Eggplant': "\033[38;5;55m",
            'PapayaWhip': "\033[38;5;229m",
            'Granite': "\033[38;5;236m",
            'Khaki': "\033[38;5;143m",
            'Sunflower': "\033[38;5;226m",
            'MauveTaupe': "\033[38;5;153m",
            'Fuchsia': "\033[38;5;201m",
        }

        # Объединение всех цветов в один словарь
        self.color_tags = {
            **self.Colors256,
            'Black': self.Black,
            'Red': self.Red,
            'Green': self.Green,
            'Yellow': self.Yellow,
            'Blue': self.Blue,
            'Magenta': self.Magenta,
            'Cyan': self.Cyan,
            'White': self.White,
            'Gray': self.Gray,
            'RedLight': self.RedLight,
            'GreenLight': self.GreenLight,
            'YellowLight': self.YellowLight,
            'BlueLight': self.BlueLight,
            'MagentaLight': self.MagentaLight,
            'CyanLight': self.CyanLight,
            'WhiteLight': self.WhiteLight,
            'BlackBright': self.BlackBright,
            'RedBright': self.RedBright,
            'GreenBright': self.GreenBright,
            'YellowBright': self.YellowBright,
            'BlueBright': self.BlueBright,
            'MagentaBright': self.MagentaBright,
            'CyanBright': self.CyanBright,
            'WhiteBright': self.WhiteBright,
            'RESET': self.Reset,  # Добавлено для поддержки {k.RESET}
        }

    def _replace_color_tags(self, text):
        # Регулярные выражения для поиска маркеров цвета
        color_tag_pattern = re.compile(r'\{k\.(\w+)\}')
        hex_tag_pattern = re.compile(r'\{k\.HEX\((#[0-9A-Fa-f]{6})\)\}')
        rgb_tag_pattern = re.compile(r'\{k\.RGB\((\d{1,3}),(\d{1,3}),(\d{1,3})\)\}')

        def replace_color_tag(match):
            color_name = match.group(1)
            return self.color_tags.get(color_name, self.Reset)

        def replace_hex_tag(match):
            hex_code = match.group(1)
            return self._hex_to_ansi(hex_code)

        def replace_rgb_tag(match):
            r, g, b = map(int, match.groups())
            return self._rgb_to_ansi(r, g, b)

        # Заменяем маркеры на ANSI-коды
        text = color_tag_pattern.sub(replace_color_tag, text)
        text = hex_tag_pattern.sub(replace_hex_tag, text)
        text = rgb_tag_pattern.sub(replace_rgb_tag, text)
        return text

    def _hex_to_ansi(self, hex_code):
        hex_code = hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return f"\033[38;2;{r};{g};{b}m"

    def _rgb_to_ansi(self, r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    def __call__(self, text):
        return self._replace_color_tags(text)

# Глобальный экземпляр класса
color = ColorByKawa()

# Сохраняем оригинальную функцию print
original_print = builtins.print

def print_colored(text):
    """Функция для печати текста с цветами."""
    formatted_text = color(text) + color.Reset
    original_print(formatted_text)

# Переопределяем встроенную функцию print сразу при импорте
builtins.print = print_colored

