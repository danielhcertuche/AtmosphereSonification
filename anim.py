from manim import *
import numpy as np
import joblib

## Cargamos los datos

## El completo espectro de la atmósfera
full_spec = joblib.load('full_spec.pkl')

## Por molécula
# read txt file
CO2 = np.loadtxt('CO2.txt')
CO2 = CO2[::-1]
wn = full_spec[0]
wl = 1e4 / wn
f = full_spec[1]
f = f[::-1]
f = f - np.min(CO2)
wl = wl[::-1]

# eje x, normalizado, es decir todos los puntos deben estar para un gráfico de 20x10
norm_wl = np.linspace(1, 21, len(wl))
# eje y
norm_f = f / max(f) * 10 + 1

# Escalar los flujos al rectángulo
def norm(mol):
    x = mol - np.min(mol)
    norm_mol = x / max(f) * 10 + 1
    return norm_mol

# read txt file
CO2 = np.loadtxt('CO2.txt')
CO2 = CO2[::-1]
CO2 = norm(CO2)

H2O = np.loadtxt('H2O.txt')
H2O = H2O[::-1]
H2O = norm(H2O)

CH4 = np.loadtxt('CH4.txt')
CH4 = CH4[::-1]
CH4 = norm(CH4)

O2 = np.loadtxt('O2.txt')
O2 = O2[::-1]
O2 = norm(O2)

O3 = np.loadtxt('O3.txt')
O3 = O3[::-1]
O3 = norm(O3)

N2 = np.loadtxt('N2.txt')
N2 = N2[::-1]
N2 = norm(N2)

## Datos de las moléculas
mols = ("CO2", "H2O", "CH4", "O2", "O3", "N2")
data = {"CO2": CO2, "H2O": H2O, "CH4": CH4, "O2": O2, "O3": O3, "N2": N2}


## ANIMACIÓN
class SimpleAxes(Scene):
    def construct(self):
        
        # Título del gráfico
        tilte = Tex("Modern Earth's Atmosphere spectrum", font_size=36)
        tilte.to_edge(UP)
        self.play(Write(tilte))
        self.wait(1)
        # Crear los ejes
        axes = Axes(
            x_range=[1, 21, 1],  # Rango del eje X de 1 a 21
            y_range=[1, 11, 1],  # Rango del eje Y de 1 a 11
            axis_config={
                "include_ticks": False,  # No incluir ticks
                "font_size": 16,  # Tamaño de letra más pequeño
            },
            tips=False,
        )
        
        # Crear las líneas de los ejes
        x_axis_line = axes.get_x_axis()
        y_axis_line = axes.get_y_axis()

        # Crear etiquetas usando Tex
        x_label = Tex(r"Wavelength", font_size=24)
        y_label = Tex(r"Transit depth", font_size=24)
        
        # Posicionar las etiquetas
        y_label.move_to(axes.coords_to_point(-0.3, 6))
        # Posicionar las etiquetas
        x_label.move_to(axes.coords_to_point(11, -0.3))
        
        # Girar la etiqueta del eje Y
        y_label.rotate(PI / 2)

        # Animar la aparición de las líneas de los ejes desde el origen
        self.play(Create(axes))
        self.play(Write(x_label), Write(y_label))
        
        # Colores para cada molécula
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

        #----------------
        ## ANIMACIÓN DE PRESENTAR LAS MOLÉCULAS
        # Añadir los nombres de las moléculas
        molecule_labels = [r"CO$_2$", r"H$_2$O", r"CH$_4$", r"O$_2$", r"O$_3$", r"N$_2$"]
        for i, mol in enumerate(molecule_labels):
            # Crear la etiqueta grande en el centro
            large_label = Tex(mol, font_size=48, color=colors[i])
            large_label.move_to(ORIGIN)
            
            # Crear la etiqueta pequeña en la esquina superior derecha
            small_label = Tex(mol, font_size=24, color=colors[i])
            small_label.to_edge(UP+RIGHT)
            small_label.shift(DOWN * i * 0.5)
            
            # Animar la transición de grande en el centro a pequeña en la esquina
            self.play(Write(large_label))
            self.wait(0.5) # Esperar un segundo
            self.play(Transform(large_label, small_label))
            self.remove(large_label)
            self.add(small_label)
            
            
        #----------------
        # ANIMAR LAS LÍNEAS
        # Crear una línea para cada molécula
        lines = {}
        for i, mol in enumerate(mols):
            norm_mol = data[mol]
            lines[mol] = VMobject()
            lines[mol].set_points_as_corners([axes.coords_to_point(norm_wl[0], norm_mol[0])])
            lines[mol].set_color(colors[i])
            self.add(lines[mol])

        # Animar las líneas añadiendo un punto cada 0.5 segundos
        for j in range(1, len(norm_wl)):  # 
            animations = []
            for i, mol in enumerate(mols):
                norm_mol = data[mol]
                new_line = Line(
                    start=axes.coords_to_point(norm_wl[j-1], norm_mol[j-1]),
                    end=axes.coords_to_point(norm_wl[j], norm_mol[j]),
                    color=colors[i],
                )
                new_line.set_opacity(0.6)
                animations.append(Create(new_line, run_time=60/90))
                lines[mol].add(new_line)
                
                # Crear y animar el círculo transparente
                if norm_mol[j] >= 1.6:
                    circle = Circle(radius=0.1, color=colors[i],
                                    fill_opacity=0.05, stroke_width=2,
                                    stroke_opacity=0.6)
                    circle.move_to(axes.coords_to_point(norm_wl[j], norm_mol[j]))
                    grow = circle.animate(rate_func=there_and_back, run_time=60/180*2/3).scale(3)
                    fade = FadeOut(circle, run_time=60/180)  # Doble del tiempo
                    animations.append(grow)
                    animations.append(fade)
            self.play(*animations,run_time=60/180)

        self.wait(2)


        

        
        

if __name__ == "__main__":
    from manim import config, tempconfig
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = SimpleAxes()
        scene.render()
