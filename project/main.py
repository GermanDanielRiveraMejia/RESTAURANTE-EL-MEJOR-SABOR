import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(
            text="Restaurante El Mejor Sabor",
            font_size=32
        ))

        btn = Button(text="Ver menú", size_hint=(1, 0.2))
        btn.bind(on_press=self.ir_categorias)

        layout.add_widget(btn)
        self.add_widget(layout)

    def ir_categorias(self, instance):
        self.manager.current = "categorias"



class CategoriaScreen(Screen):
    def __init__(self, categorias, **kwargs):
        super().__init__(**kwargs)
        self.categorias = categorias

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Categorías", font_size=28))

        for cat in categorias:
            btn = Button(text=cat)
            btn.bind(on_press=self.abrir_categoria)
            layout.add_widget(btn)

        self.add_widget(layout)

    def abrir_categoria(self, instance):
        self.manager.get_screen("productos").mostrar_productos(instance.text)
        self.manager.current = "productos"


class ProductoScreen(Screen):
    def __init__(self, productos, **kwargs):
        super().__init__(**kwargs)
        self.productos = productos

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(Label(text="Productos", font_size=28))

        self.scroll = ScrollView()
        self.product_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10
        )
        self.product_layout.bind(minimum_height=self.product_layout.setter('height'))

        self.scroll.add_widget(self.product_layout)
        self.layout.add_widget(self.scroll)

        btn_volver = Button(text="Volver", size_hint=(1, 0.2))
        btn_volver.bind(on_press=self.volver)
        self.layout.add_widget(btn_volver)

        self.add_widget(self.layout)

    def mostrar_productos(self, categoria):
        self.product_layout.clear_widgets()

        for p in self.productos:
            if p["categoria"] == categoria:
                texto = f'{p["nombre"]} - Lps. {p["precio"]}'
                self.product_layout.add_widget(Label(
                    text=texto,
                    size_hint_y=None,
                    height=40
                ))

    def volver(self, instance):
        self.manager.current = "categorias"



class MenuApp(App):
    def build(self):
        with open("menu.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        productos = data["productos"]
        categorias = list(set(p["categoria"] for p in productos))

        sm = ScreenManager()
        sm.add_widget(InicioScreen(name="inicio"))
        sm.add_widget(CategoriaScreen(categorias, name="categorias"))
        sm.add_widget(ProductoScreen(productos, name="productos"))

        sm.current = "inicio"
        return sm


if __name__ == "__main__":
    MenuApp().run()
