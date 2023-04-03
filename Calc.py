from manimlib.imports import *

def derivative(func, x, n = 1, dx = 0.01):
    samples = [func(x + (k - n/2)*dx) for k in range(n+1)]
    while len(samples) > 1:
        samples = [
            (s_plus_dx - s)/dx
            for s, s_plus_dx in zip(samples, samples[1:])
        ]
    return samples[0]

def taylor_approximation(func, highest_term, center_point = 0):
    derivatives = [
        derivative(func, center_point, n = n)
        for n in range(highest_term + 1)
    ]
    coefficients = [
        d/math.factorial(n) 
        for n, d in enumerate(derivatives)
    ]
    return lambda x : sum([
        c*((x-center_point)**n) 
        for n, c in enumerate(coefficients)
    ])

class AIntrolas(Scene):
    CONFIG={
        "Regra":TexMobject(r"f( x )=ax+b"),
        "Regrolas":TexMobject(r"f( x )=2x+1"),
        "NesseCasoVamosConsiderar":TextMobject("a=2 e b=1"),
        "NesseCasoVamosConsiderarTrans":TextMobject("a=2 e b=1")
    }
    def construct(self):
        self.Regra.scale(2)
        self.Regrolas.scale(2)
        self.NesseCasoVamosConsiderar.scale(1.5)
        self.NesseCasoVamosConsiderarTrans.scale(1.5)
        self.NesseCasoVamosConsiderar.set_color_by_gradient(WHITE, WHITE, RED, WHITE, WHITE, WHITE, BLUE)
        self.NesseCasoVamosConsiderarTrans.set_color_by_gradient(WHITE, WHITE, RED, WHITE, WHITE, WHITE, BLUE)
        self.NesseCasoVamosConsiderar.move_to(self.Regra.get_center()+1*DOWN)
        self.NesseCasoVamosConsiderarTrans.move_to(self.Regra.get_center()+1*DOWN)
        self.Regra.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, RED, WHITE, WHITE, BLUE)
        self.Regrolas.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, RED, WHITE, WHITE, BLUE)
        NesseCaso = VGroup(*[self.NesseCasoVamosConsiderar,self.NesseCasoVamosConsiderarTrans])
        Regras = VGroup(*[self.Regra,self.Regrolas])
        self.play(Write(self.Regra),run_time=2)
        self.wait(2)
        self.play(GrowFromCenter(NesseCaso))
        self.wait(2)
        self.play(*[
            ReplacementTransform(self.NesseCasoVamosConsiderarTrans,self.Regrolas),
            ReplacementTransform(self.Regra,self.Regrolas)
            ])
        #self.play(
        #    ReplacementTransform(
        #        self.NesseCasoVamosConsiderar.copy(),
        #        ftc.get_part_by_tex("int")
        #    )
        self.wait()
        self.play(*[FadeOut(self.NesseCasoVamosConsiderarTrans),
        FadeOut(self.Regrolas),
        FadeOut(self.NesseCasoVamosConsiderar)
        ])
        self.wait(3)
#
class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))

class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 50,
        "columns": 50,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)

class CoordScreen(Scene):
    def construct(self):
        screen_grid = ScreenGrid()
        dot = Dot([1, 1, 0])
        self.add(screen_grid)
        self.play(FadeIn(dot))
        self.wait()

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            TexMobject(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob,
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )

#
class BConstruçãoDaFunção(GraphScene,MovingCameraScene):
    CONFIG = {
        "y_max" : 10,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "$x$",
        "y_axis_label" : "$f(x)$",
    }
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)
    def construct(self):
        LocalBom=np.array([0,-2,0])
        Função=TexMobject(r"f( x )=2x+1")
        Função.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, RED, WHITE, WHITE, BLUE)
        Função.move_to(LocalBom)
        self.play(Write(Função))
        self.setup_axes()
        graph = self.get_graph(lambda x : x*2+1, color = GREEN)
        littlegraph = self.get_graph(lambda x : x*2+1, x_min = 1, x_max = 2, color = GREEN)
        Ponto1=Dot().move_to(littlegraph.points[0])
        Ponto2=Dot().move_to(littlegraph.points[-1])
        Ponto1M=TextMobject("(1,3)")
        Ponto2M=TextMobject("(2,5)")
        Ponto1M.scale(0.75)
        Ponto2M.scale(0.75)
        Ponto1M.move_to(Ponto1.get_center()+0.5*UP+0.25*LEFT)
        Ponto2M.move_to(Ponto2.get_center()+0.5*UP+0.25*LEFT)
        self.play(
        	ShowCreation(graph),
            run_time = 2
        )
        self.wait()
        self.play(ReplacementTransform(graph,littlegraph))
        self.play(*[
            self.camera_frame.scale,.5,
            self.camera_frame.move_to,Ponto1,
            (Write(Ponto1)),
            (Write(Ponto1M))
        ])
        #self.add(Ponto1)
        self.wait(4)
        self.play(*[
            self.camera_frame.move_to,Ponto2,
            (Write(Ponto2)),
            (Write(Ponto2M))
        ])
        #self.add(Ponto2)
        self.wait()
    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
        #   For y
        init_label_y = 1
        end_label_y = 10
        step_y = 1
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class CExplicaçãoDaVariação(GraphScene,Scene):
    CONFIG={
        "formula":TexMobject(r"f(x)=",r"a",r"x+b"),
        "transformacao":TexMobject(r"=a"),

        "PVaria":TextMobject("Variação = ", color=RED),
        "P2Varia":TextMobject("Variação = ", color=RED),

        "Varia":TexMobject(r"\frac{ \Delta y}{ \Delta x} ", color=BLUE),
        "Ponto1":TexMobject(r"Ponto\ 1 : (1,3)", color=BLUE),
        "Ponto2":TexMobject(r"Ponto\ 2 : (2,5)", color=BLUE),
        "Ponto3":TexMobject(r"Ponto\ 3 : (0,1)", color=BLUE),
        "Test1e":TexMobject(r"Ponto\ 1 :", r"(1,3)"),
        "Test2e":TexMobject(r"Ponto\ 2 :", r"(2,5)"),
        "Test3e":TexMobject(r"Ponto\ 3 :", r"(0,1)"),

        "OutraManeira":TexMobject(r"\frac{3-5}{1-2}", color=BLUE),
        "SegundaManeira":TexMobject(r"\frac{-2}{-1}", color=BLUE),

        "ContaPont3o":TexMobject(r"\frac{5-1}{2-0}", color=BLUE),
        "ContaPont4o":TexMobject(r"\frac{4}{2}", color=BLUE),

        "Final":TexMobject(r"2", color=RED),
        "sinal":TextMobject("="),
        "Coeficiente":TexMobject(r"a", color=RED),

        "triangle":Polygon(np.array([0,0,0]),np.array([1,1,0]),np.array([1,-1,0])),
        "ladof":np.array([0,0,0]),
        "ladoy":np.array([2,0,0]),
        "ladox":np.array([2,2,0]),

        "teta":TexMobject(r"\theta"),
        "TangenteDeTeta":TexMobject(r"\tan \left (  \theta \right ) =\frac{\Delta y}{\Delta x}"),

        "y_max" : 10,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "$x$",
        "y_axis_label" : "$f(x)$",

        "FunConstante":TexMobject(r"f(x)=k"),
        "Constante":TexMobject(r"f(x)=3"),
        "Constante1":TexMobject(r"Ponto\ x_0 :", r"(x_0,3)"),
        "Constante2":TexMobject(r"Ponto\ x :", r"(x,3)"),
        "VariaC":TexMobject(r"\frac{3-3}{x_0-x}", color=BLUE),
        "Independente":TexMobject(r"\frac{0}{x_0-x}", color=BLUE),
        "PodemosAt":TexMobject(r"f(x)=ax+b"),
        "Com":TexMobject(r"a=0")

    }

    def setup(self):
        GraphScene.setup(self)
        Scene.setup(self)

    def construct(self):
        #grade=ScreenGrid()
        #self.add(grade)

        self.PVaria.scale(2)
        self.formula.scale(2)
        self.P2Varia.scale(2)
        self.Varia.scale(2)
        self.Ponto1.scale(2)
        self.Ponto2.scale(2)
        self.OutraManeira.scale(2)
        self.SegundaManeira.scale(2)
        self.Final.scale(2)
        self.sinal.scale(2)
        self.Coeficiente.scale(2)
        self.TangenteDeTeta.scale(2)
        self.Ponto3.scale(2)

        self.Test1e.scale(2)
        self.Test2e.scale(2)
        self.Test3e.scale(2)

        self.ContaPont3o.scale(2)
        self.ContaPont4o.scale(2)
        self.ContaPont3o.move_to(+2*RIGHT)
        self.ContaPont4o.move_to(+1.5*RIGHT)

        self.Varia.move_to(+2*RIGHT)
        self.OutraManeira.move_to(+2*RIGHT)
        self.SegundaManeira.move_to(+2*RIGHT)
        self.Final.move_to(+1.5*RIGHT)
        #triangle=Polygon(np.array([0,0,0]),np.array([1,1,0]),np.array([1,-1,0]))

        self.triangle.move_to(self.PVaria.get_center()+2*LEFT)
        self.sinal.move_to(self.Varia.get_center()+0.5*RIGHT)
        self.PVaria.move_to(self.Varia.get_center()+3.6*LEFT+0.02*DOWN)
        self.P2Varia.move_to(self.Varia.get_center()+3.6*LEFT+0.02*DOWN)
        self.Ponto1.move_to(self.Varia.get_center()+2*DOWN+2*LEFT)
        self.Ponto2.move_to(self.Varia.get_center()+3.1*DOWN+2*LEFT)
        self.Ponto3.move_to(self.Ponto2.get_center())
        self.Coeficiente.move_to(self.sinal.get_center()+1*RIGHT)
        self.OutraManeira.move_to(self.Varia.get_center()+0.5*RIGHT)
        self.formula.move_to(self.Varia.get_center()+2*DOWN+2*LEFT)

        self.PVaria.set_color_by_gradient(RED, RED, RED, RED, RED, RED, RED, RED, WHITE)
        self.P2Varia.set_color_by_gradient(RED, RED, RED, RED, RED, RED, RED, RED, WHITE)
        self.Ponto1.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
        self.Ponto2.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
        self.Ponto3.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
        self.formula.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, RED, WHITE, WHITE, BLUE)
        self.transformacao.set_color_by_gradient(WHITE, RED)
        self.TangenteDeTeta.set_color_by_gradient(RED,RED,RED,RED,RED,RED,WHITE,BLUE,BLUE,BLUE,BLUE,BLUE)
        #self.triangle.color=GREEN

        self.Test1e.get_part_by_tex(r"(1,3)").set_color(BLUE)
        self.Test2e.get_part_by_tex(r"(2,5)").set_color(BLUE)
        self.Test3e.get_part_by_tex(r"(0,1)").set_color(BLUE)
        self.Test1e.move_to(self.Varia.get_center()+2*DOWN+2*LEFT)
        self.Test2e.move_to(self.Varia.get_center()+3.1*DOWN+2*LEFT)
        self.Test3e.move_to(self.Ponto2.get_center())
        #Pontos para testes.

        #PontoH = Dot(self.ladof)
        #PontoY = Dot(self.ladoy)
        #PontoX = Dot(self.ladox)
        #PontoH.set_color(GREEN)
        #PontoY.set_color(RED)
        #PontoX.set_color(WHITE)

        LinhaH = Line(self.ladof,self.ladoy)
        LinhaY = Line(self.ladoy,self.ladox)
        LinhaX = Line(self.ladox,self.ladof)
        #LinhaH.scale(2)
        #LinhaY.scale(2)
        #LinhaX.scale(2)
        LinhaH.set_color(WHITE)#Era verde.
        LinhaY.set_color(WHITE)#Era vermelho.
        LinhaX.set_color(GREEN)#Era Branco.

        Deltax = TexMobject(r" \Delta x")
        Deltay = TexMobject(r" \Delta y")
        Deltax.set_color(BLUE)
        Deltay.set_color(BLUE)

        Arco = Arc(
        #    start_angle = self.example_radians,
            angle = np.pi/4,
            radius = 0.5,
            color = WHITE,
            stroke_width = 2
        )

        Arcox = Brace(LinhaY, RIGHT)
        Arcoy = Brace(LinhaH, DOWN)
        Arcox.shift(+0.45*LEFT)
        Arcoy.shift(+0.45*LEFT)
        Deltay.to_edge(DOWN)
        Deltax.move_to(Arcox.get_center()+4*DOWN+3*LEFT)
        Deltax.shift(+0.5*LEFT+0.1*DOWN)
        Deltay.shift(+0.33*RIGHT+1.75*UP)
        self.teta.shift(-2.25*UP+2.05*LEFT)
        Arco.move_to(self.teta.get_center()+0.1*DOWN+0.1*LEFT)
        self.teta.shift(-0.075*LEFT)
        Coisolas = VGroup(*[Arcox,Arcoy])
        Coisolas2 = VGroup(*[Deltax,Deltay,self.teta])

        self.TangenteDeTeta.to_corner(RIGHT)
        self.TangenteDeTeta.shift(+2.5*DOWN)


        Triangolas = VGroup(*[LinhaH,LinhaX,LinhaY])
        Triangolas.move_to(self.P2Varia.get_center()+1.5*DOWN)
        Coisolas.move_to(Triangolas.get_center()+0.2*DOWN+0.25*RIGHT)
        PrimeiroConjunto=VGroup(*[self.PVaria,self.Varia])
        Pontos=VGroup(*[self.Ponto1,self.Ponto2])
        Ponto2s=VGroup(*[self.Test1e,self.Test2e])
        Ponto2s.shift

        #Palavra "Variação"
        self.play(Write(self.PVaria),run_time=2)
        #Fórmula da variação
        self.play(Write(self.Varia),run_time=2)
        #self.play(Write(self.Ponto1),run_time=2)
        #self.play(Write(self.Ponto2),run_time=2)
        Transicao = VGroup(*[Triangolas,Coisolas,Deltax,Deltay,self.teta,Arco])
        self.wait(2)
        #Subindo a álgebra
        self.play(ShowCreation(Triangolas))
        self.wait(3)
        self.play(FadeIn(Coisolas),FadeIn(Deltax),FadeIn(Deltay))
        self.wait(4)
        self.play(FadeIn(self.teta),FadeIn(Arco))
        self.wait(3)
        self.play(ReplacementTransform(Transicao.copy(),self.TangenteDeTeta))
        self.wait(3)
        self.play(ApplyMethod(PrimeiroConjunto.shift,2.75*UP,run_time=0.5),FadeOut(Triangolas,run_time=0.5),FadeOut(Coisolas,run_time=0.5),FadeOut(Coisolas2,run_time=0.5),FadeOut(self.TangenteDeTeta,run_time=0.5),FadeOut(Arco,run_time=0.5))
        #Pontos e fórmula
        self.play(FadeIn(self.P2Varia))#Palavra "Variação"
        #self.play(FadeIn(self.Ponto1),run_time=2)
        #self.play(FadeIn(self.Ponto2),run_time=2)
        self.play(FadeIn(Ponto2s),run_time=2)
        #self.play(FadeIn(self.OutraManeira))

        #AnimacaoNice = VGroup(*[self.Delta1t.get_part_by_tex(r"10s"),self.Delta1s.get_part_by_tex(r"100m")])
        self.play(
            #FadeIn(self.OutraManeira),
            ReplacementTransform(self.Test1e.get_part_by_tex(r"(1,3)").copy(),self.OutraManeira),
            ReplacementTransform(self.Test2e.get_part_by_tex(r"(2,5)").copy(),self.OutraManeira))

        self.wait()

        #Mudando de Delta y e x para números
        self.play(ReplacementTransform(self.OutraManeira,self.SegundaManeira))
        #Mudando dos números para mais simplificados
        self.play(ReplacementTransform(self.SegundaManeira,self.Final))
        #Iniciando a relação com o a
        #self.play(FadeOut(self.Ponto1))
        #self.play(FadeOut(self.Ponto2))
        self.wait()
        self.play(FadeOut(self.Test1e),ApplyMethod(self.Test2e.shift,1.1*UP,run_time=0.5),FadeIn(self.Test3e),FadeOut(self.Final))
        self.wait(2)
        #self.play(FadeOut(self.Final,run_time=0.5))
        #self.play(Transform)
        #AnimacaoNice = VGroup(*[self.Delta1t.get_part_by_tex(r"10s"),self.Delta1s.get_part_by_tex(r"100m")])
        self.play(
            ReplacementTransform(self.Test2e.copy(),self.ContaPont3o),
            ReplacementTransform(self.Test3e.copy(),self.ContaPont3o))
        self.wait()
        self.play(
            ReplacementTransform(self.ContaPont3o,self.ContaPont4o)
        )
        self.wait(3)
        self.play(ReplacementTransform(self.ContaPont4o,self.Final))
        self.wait(2)
        self.play(FadeOut(self.Test2e),FadeOut(self.Test3e))
        #self.play(ReplacementTransform(self.Coeficiente,self.))
        #self.play(FadeOut(Pontos),run_time=1)
        self.play(FadeIn(self.formula))
        #self.play(FadeIn(self.sinal))
        self.play(ReplacementTransform(self.formula.get_part_by_tex(r"a").copy(),self.Coeficiente),FadeIn(self.sinal))
        #self.play()
        self.wait(3)
        Tudolas = VGroup(self.formula,self.Coeficiente,self.sinal,self.P2Varia,PrimeiroConjunto,self.Final)
        #self.play(FadeOut(self.formula),FadeOut(self.Coeficiente),FadeOut(self.sinal),FadeOut(PrimeiroConjunto),FadeOut(self.P2varia))
        self.play(FadeOut(Tudolas))
        self.wait(2)

        self.FunConstante.scale(2)
        self.Constante.scale(2)
        self.Constante1.scale(2)
        self.Constante2.scale(2)
        self.PodemosAt.scale(2)
        self.Com.scale(2)
        self.FunConstante.shift(+1.25*UP)
        self.Constante1.shift(-1.5*UP)
        self.Constante2.shift(-2.6*UP)
        self.Constante1.get_part_by_tex(r"(x_0,3)").set_color(BLUE)#.copy()
        self.Constante2.get_part_by_tex(r"(x,3)").set_color(BLUE)#.copy()
        self.VariaC.scale(2)
        self.Independente.scale(2)
        self.PodemosAt.scale(2)
        self.PodemosAt.set_color_by_gradient(WHITE, WHITE, WHITE, WHITE, WHITE, RED, WHITE, WHITE, BLUE)
        self.PodemosAt.shift(+2*UP)
        self.Com.set_color_by_gradient(RED,WHITE,RED)
        self.Com.scale(2)
        self.Com.move_to(self.PodemosAt.get_center()-2*UP)
        self.VariaC.shift(+1.25*UP)
        self.Independente.shift(+1.25*UP)
        PontosC = VGroup(*[self.Constante1,self.Constante2])
        self.Constante.move_to(self.FunConstante.get_center()-1*UP)
        #"VariaC":TexMobject(r"\frac{3-3}{x_0-x}", color=BLUE),
        #"Independente":TexMobject(r"\frac{0}{x_0-x}", color=BLUE),
        #"PodemosAt":TexMobject(r"f(x)=ax+b"),
        #"Com":TexMobject("Com ",r"a=0")

        self.setup_axes()
        graph = self.get_graph(lambda x : 3, color = GREEN)
        self.play(ShowCreation(graph))
        self.wait(4)
        self.play(FadeOut(graph),FadeOut(self.x_axis),FadeOut(self.y_axis))

        self.play(Write(self.FunConstante))
        self.wait(2.5)
        self.play(Write(self.Constante))
        self.wait(2)
        self.wait(3)
        self.wait(2)
        self.play(Write(PontosC),FadeOut(self.FunConstante),FadeOut(self.Constante))
        self.wait(2)
        self.play(
            ReplacementTransform(self.Constante1.get_part_by_tex(r"(x_0,3)").copy(),self.VariaC),
            ReplacementTransform(self.Constante2.get_part_by_tex(r"(x,3)").copy(),self.VariaC),
            )
        self.wait(3)
        self.play(ReplacementTransform(self.VariaC,self.Independente))
        self.wait(3)
        self.play(Write(self.PodemosAt,run_time=1.5),FadeOut(self.Constante1),FadeOut(self.Constante2),FadeOut(self.Independente))
        self.wait(3)
        self.play(Write(self.Com))
        self.wait(3)
    def setup_axes(self):
            # Add this line
        GraphScene.setup_axes(self)
            # Parametters of labels
            #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
            #   For y
        init_label_y = 1
        end_label_y = 10
        step_y = 1
            # Position of labels
            #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
            #   For y
        self.y_axis.label_direction = LEFT
            # Add labels to graph
            #   For x
        self.x_axis.add_numbers(*range(
                                            init_label_x,
                                            end_label_x+step_x,
                                            step_x


                                        ))
            #   For y
        self.y_axis.add_numbers(*range(
                                            init_label_y,
                                            end_label_y+step_y,
                                            step_y
                                        ))
            #   Add Animation
        self.play(
                ShowCreation(self.x_axis),
                ShowCreation(self.y_axis)
            )

class DVariaçãoDaFunçãoQuadrática(GraphScene,MovingCameraScene):
    CONFIG={
        "formula":TexMobject(r"f(x)=",r"x^2-x"),
        "fDeZero":TexMobject(r"(0,0)", color=BLUE),
        "fDeUm":TexMobject(r"(1,0)", color=BLUE),
        "fDeDois":TexMobject(r"(2,2)", color=BLUE),
        "Varia":TexMobject(r"\frac{0-0}{0-1} ", color=BLUE),
        "SegVaria":TexMobject(r"\frac{0}{-1}", color=BLUE),
        "TerVaria":TexMobject(r"0", color=BLUE),
        "Textolas":TextMobject("Variação =",color=RED),
        "V2aria":TexMobject(r"\frac{0-2}{1-2} ", color=BLUE),
        "Seg2Varia":TexMobject(r"\frac{-2}{-1}", color=BLUE),
        "Ter2Varia":TexMobject(r"2", color=BLUE),

        "y_max" : 10,
        "y_min" : 0,
        "x_max" : 5,
        "x_min" : -5,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "$x$",
        "y_axis_label" : "$f(x)$",
        "TextoSeiL" : TexMobject(r"2"),
    }
    def setup(self):
        GraphScene.setup(self)
        Scene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.formula.scale(2)
        self.fDeZero.scale(2)
        self.fDeUm.scale(2)
        self.fDeDois.scale(2)
        self.Varia.scale(2)
        self.SegVaria.scale(2)
        self.TerVaria.scale(2)
        self.Textolas.scale(2)
        self.V2aria.scale(2)
        self.Seg2Varia.scale(2)
        self.Ter2Varia.scale(2)

        self.fDeZero.move_to(+1.5*LEFT)
        self.fDeUm.move_to(-1.5*LEFT)

        Contas=VGroup(*[self.Varia,self.SegVaria,self.TerVaria])
        Contas.move_to(self.fDeUm.get_center()-0.4*LEFT)

        self.Textolas.move_to(self.fDeZero.get_center()+0.4*LEFT)

        VariaçãoNome1=VGroup(*[self.Textolas,self.Varia])
        VariaçãoNome2=VGroup(*[self.Textolas,self.SegVaria])
        VariaçãoNome3=VGroup(*[self.Textolas,self.TerVaria])

        diferenca=VGroup(*[self.fDeZero,self.fDeUm])
        diferenca2=VGroup(*[self.fDeUm,self.fDeDois])
        Tudolas=VGroup(*[VariaçãoNome3,diferenca])

        self.play(Write(self.formula))
        self.wait(2)
        self.play(ApplyMethod(self.formula.shift,2.75*UP,run_time=0.5))
        self.wait(2)
        self.play(Write(diferenca))
        self.play(ApplyMethod(diferenca.shift,+1.75*DOWN))
        self.wait(3)
        self.play(Write(self.Textolas),ReplacementTransform(diferenca.copy(),self.Varia))
        self.wait()
        self.play(ReplacementTransform(self.Varia,self.SegVaria))
        self.wait()
        self.play(ApplyMethod(self.Textolas.shift,+0.45*RIGHT))
        self.play(ReplacementTransform(self.SegVaria,self.TerVaria))
        self.wait()
        self.play(FadeOut(Tudolas),run_time=0.5)
        self.fDeUm.move_to(+1.5*LEFT)
        self.fDeDois.move_to(-1.5*LEFT)
        self.Textolas.move_to(self.fDeUm.get_center()+0.4*LEFT)
        V2ariaçãoNome1=VGroup(*[self.Textolas,self.V2aria])
        V2ariaçãoNome2=VGroup(*[self.Textolas,self.Seg2Varia])
        V2ariaçãoNome3=VGroup(*[self.Textolas,self.Ter2Varia])
        Contas2=VGroup(*[self.V2aria,self.Seg2Varia,self.Ter2Varia])
        Contas2.move_to(self.fDeDois.get_center()-0.4*LEFT)
        self.play(Write(diferenca2))
        self.play(ApplyMethod(diferenca2.shift,+1.75*DOWN))
        self.wait(3)
        self.play(Write(self.Textolas),ReplacementTransform(diferenca2.copy(),self.V2aria))
        self.wait()
        self.play(ReplacementTransform(V2ariaçãoNome1,V2ariaçãoNome2))
        self.wait()
        self.play(ApplyMethod(self.Textolas.shift,+0.45*RIGHT))
        self.play(ReplacementTransform(V2ariaçãoNome2,V2ariaçãoNome3))
        self.wait(3)
        self.play(FadeOut(V2ariaçãoNome3),FadeOut(self.fDeUm),FadeOut(self.fDeDois),FadeOut(self.formula))

        self.setup_axes()

        #self.TextoSeiL.scale(0.5)

        self.TerVaria.set_color(WHITE)
        self.TerVaria.scale(0.5)

        self.Ter2Varia.set_color(WHITE)
        self.Ter2Varia.scale(0.5)

        Raiz = Dot(self.coords_to_point(x=0,y=0))
        Raizz = Dot(self.coords_to_point(x=1,y=0))
        Raizes = Line(Raiz,Raizz)
        RaizesD = Brace(Raizes, DOWN)

        Rai2z = Dot(self.coords_to_point(x=1,y=0))
        NEG = Dot(self.coords_to_point(x=2,y=2))
        RaizesE = Line(Rai2z,NEG)
        RaizesDE = Brace(RaizesE, DOWN)
        self.TerVaria.move_to(RaizesD.get_center()+0.5*DOWN)
        self.Ter2Varia.move_to(RaizesDE.get_center()+0.5*DOWN)

        PontoEstranho = Dot(self.coords_to_point(x=2,y=0))
        Retay = Line(PontoEstranho,NEG)
        BraçoDoLado = Brace(Retay,RIGHT)
        self.TextoSeiL.move_to(BraçoDoLado.get_center()+0.5*RIGHT)
        BraçoDoLadoGrupo = VGroup(*[BraçoDoLado,self.TextoSeiL])

        #Retah = Line(Raiz,NEG)
        #Retax = Line(Raiz,PontoEstranho)

        #PontoEstranhof = Dot(self.point_to_coords(np.ndarray(PontoEstranho)))
        #Raizf = Dot(self.point_to_coords (np.ndarray(Raiz)))
        #NEGf = Dot(self.point_to_coords (np.ndarray(NEG)))

        #Triangulo = Polygon(PontoEstranhof,Raizf,NEGf)
        #Triangulo.stroke_color(WHITE)
        #Triangulo.fill_color(ORANGE)
        #Triangulo.fill_opacity(0.8)

        #Deltax = Brace(Retax,DOWN)
        #Deltay = Brace(Retay,RIGHT)

        #Triangolas = VGroup(*[Triangulo,Deltay,Deltax])
        #Marcaolas = VGroup(*[self.TerVaria,self.Ter2Varia,RaizesD,RaizesDE])


        GRAFICO = self.get_graph(lambda x : x**2-x, color = GREEN)
        self.play(ShowCreation(GRAFICO))
        self.wait()
        self.play(self.camera_frame.scale,.5,
        self.camera_frame.move_to,self.coords_to_point(x=0.5,y=0),Write(Raiz),Write(Raizz))
        self.wait()
        self.play(Write(RaizesD),Write(self.TerVaria))
        self.wait()
        self.play(self.camera_frame.move_to,self.coords_to_point(x=1,y=1),Write(NEG))
        self.wait()
        self.play(Write(BraçoDoLadoGrupo))
        self.wait()
        self.wait()
        self.play(FadeOut(GRAFICO),FadeOut(self.x_axis),FadeOut(self.y_axis),FadeOut(NEG),FadeOut(Raiz),FadeOut(Raizz),FadeOut(RaizesD),FadeOut(self.TerVaria
),FadeOut(BraçoDoLadoGrupo))
        self.wait(2)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = -5
        end_label_x = 5
        step_x = 1
        #   For y
        init_label_y = 1
        end_label_y = 10
        step_y = 1
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        Eixos = VGroup(*[self.x_axis,self.y_axis])
        Eixos.move_to(ORIGIN)
        Eixos.to_edge(DOWN)
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class ExplicaçãoDosLimites(Scene):
        CONFIG={
            "Limites":TextMobject("Limites"),
            "LimiteDePrimeiroGrau":TexMobject(r" \lim_{x \rightarrow 2 } 2x+1"),
            "SeraLimiteDePrimeiroGrau":TexMobject(r"2(2)+1"),
            "ResulLimiteDePrimeiroGrau":TexMobject(r"=5"),

            "LimiteDePrimeiroGrauin":TexMobject(r" \lim_{x \rightarrow +\infty } 2x+1"),
            #"SeraLimiteDePrimeiroGrauin":TexMobject(r"2(+\infty)+1"),
            "ResulLimiteDePrimeiroGrauin":TexMobject(r"=+\infty"),

            "LimiteDeSegundoGrau":TexMobject(r" \lim_{x \rightarrow -\infty } x^2-x"),
            "SeraLimiteDeSegundoGrau":TexMobject(r"(-\infty)^2-(-\infty)"),
            "SeraLimiteDeSegundoGra2u":TexMobject(r"\infty+\infty"),
            "ResulLimiteDeSegundoGrau":TexMobject(r"=\infty"),

            "L2imiteDeSegundoGrau":TexMobject(r" \lim_{x \rightarrow 2 } x^2-x"),
            "S2eraLimiteDeSegundoGrau":TexMobject(r"(2)^2-2"),
            "R2esulLimiteDeSegundoGrau":TexMobject(r"=2"),

            "FunEstranha":TexMobject(r"f(x) =\begin{cases}2x-1 & x \neq 2\\1 & x = 2\end{cases}"),
            "LimiteEstranho":TexMobject(r" \lim_{x \rightarrow 2 } f(x)"),
            "ResulLimiteEstranho":TexMobject(r"=3")
            }
        def construct(self):
            self.Limites.scale(2.5)
            self.LimiteDePrimeiroGrau.scale(2)
            self.ResulLimiteDePrimeiroGrau.scale(2)
            self.LimiteDePrimeiroGrauin.scale(2)
            self.ResulLimiteDePrimeiroGrauin.scale(2)
            self.LimiteDeSegundoGrau.scale(2)
            self.ResulLimiteDeSegundoGrau.scale(2)
            self.L2imiteDeSegundoGrau.scale(2)
            self.R2esulLimiteDeSegundoGrau.scale(2)
            self.FunEstranha.scale(2)
            self.LimiteEstranho.scale(2)
            self.ResulLimiteEstranho.scale(2)

            self.S2eraLimiteDeSegundoGrau.scale(2)
            self.SeraLimiteDePrimeiroGrau.scale(2)
            self.SeraLimiteDeSegundoGrau.scale(2)
            self.SeraLimiteDeSegundoGra2u.scale(2)
            self.S2eraLimiteDeSegundoGrau.move_to(self.LimiteDeSegundoGrau.get_center()+1*DOWN)
            self.SeraLimiteDePrimeiroGrau.move_to(self.LimiteDePrimeiroGrau.get_center()+1*DOWN)
            self.SeraLimiteDeSegundoGrau.move_to(self.LimiteDeSegundoGrau.get_center()+1.25*DOWN)
            self.SeraLimiteDeSegundoGra2u.move_to(self.LimiteDeSegundoGrau.get_center()+1.25*DOWN)

            self.ResulLimiteDePrimeiroGrau.move_to(self.LimiteDePrimeiroGrau.get_center()+2.35*RIGHT+0.25*UP)
            self.ResulLimiteDePrimeiroGrauin.move_to(self.LimiteDePrimeiroGrauin.get_center()+3.35*RIGHT+0.25*UP)
            self.ResulLimiteDeSegundoGrau.move_to(self.LimiteDeSegundoGrau.get_center()+3.35*RIGHT+0.1*UP)
            self.R2esulLimiteDeSegundoGrau.move_to(self.L2imiteDeSegundoGrau.get_center()+2.35*RIGHT+0.20*UP)
            self.ResulLimiteEstranho.move_to(self.LimiteEstranho.get_center()+1.75*RIGHT+0.25*UP)
            Primeiro=VGroup(*[self.LimiteDePrimeiroGrau,self.ResulLimiteDePrimeiroGrau,self.SeraLimiteDePrimeiroGrau])
            Segundo=VGroup(*[self.LimiteDePrimeiroGrauin,self.ResulLimiteDePrimeiroGrauin])
            Terceiro=VGroup(*[self.LimiteDeSegundoGrau,self.ResulLimiteDeSegundoGrau])
            #Terceiro=VGroup(*[self.LimiteDeSegundoGrau,self.ResulLimiteDeSegundoGrau,self.SeraLimiteDeSegundoGrau])
            Quarto=VGroup(*[self.L2imiteDeSegundoGrau,self.R2esulLimiteDeSegundoGrau,self.L2imiteDeSegundoGrau])
            Quinto=VGroup(*[self.FunEstranha,self.LimiteEstranho,self.ResulLimiteEstranho])
            self.play(FadeInFromDown(self.Limites))
            self.wait(3.5)
            self.play(FadeOut(self.Limites))
            #Primeiro limite.
            self.play(Write(self.LimiteDePrimeiroGrau))
            self.wait(5)
            self.play(ApplyMethod(self.LimiteDePrimeiroGrau.shift,+LEFT,run_time=0.5),ReplacementTransform(self.LimiteDePrimeiroGrau.copy(),self.SeraLimiteDePrimeiroGrau))
            self.wait(3)
            self.play(ReplacementTransform(self.SeraLimiteDePrimeiroGrau,self.ResulLimiteDePrimeiroGrau))
            self.wait()
            self.play(FadeOut(Primeiro))
            #Segundo limite.
            self.play(Write(self.LimiteDePrimeiroGrauin))
            self.wait(5)
            self.play(ApplyMethod(self.LimiteDePrimeiroGrauin.shift,+LEFT,run_time=0.5))
            self.play(Write(self.ResulLimiteDePrimeiroGrauin))
            self.wait()
            self.play(FadeOut(Segundo))
            #Terceiro limite.
            #"LimiteDeSegundoGrau":TexMobject(r" \lim_{x \rightarrow -\infty } x^2-x"),
            #"SeraLimiteDeSegundoGrau":TexMobject(r"(-\infty)^2-(-\infty)"),
            #"SeraLimiteDeSegundoGra2u":TexMobject(r"\infty+\infty"),
            #"ResulLimiteDeSegundoGrau":TexMobject(r"=\infty"),
            self.play(Write(self.LimiteDeSegundoGrau))
            self.wait(5)
            self.play(ApplyMethod(self.LimiteDeSegundoGrau.shift,+LEFT,run_time=0.5),ReplacementTransform(self.LimiteDeSegundoGrau.copy(),self.SeraLimiteDeSegundoGrau))
            self.wait(3)
            self.play(ReplacementTransform(self.SeraLimiteDeSegundoGrau,self.SeraLimiteDeSegundoGra2u))
            self.wait(3)
            self.play(ReplacementTransform(self.SeraLimiteDeSegundoGra2u,self.ResulLimiteDeSegundoGrau))
            self.wait(2)
            self.play(FadeOut(Terceiro))
            #Quarto limite.
            self.play(Write(self.L2imiteDeSegundoGrau))
            self.wait(5)
            self.play(ApplyMethod(self.L2imiteDeSegundoGrau.shift,+LEFT,run_time=0.5),ReplacementTransform(self.L2imiteDeSegundoGrau.copy(),self.S2eraLimiteDeSegundoGrau))
            self.wait(3)
            self.play(ReplacementTransform(self.S2eraLimiteDeSegundoGrau,self.R2esulLimiteDeSegundoGrau))
            self.wait()
            self.play(FadeOut(Quarto))
            #Quinto limite.(último)
            self.play(Write(self.FunEstranha))
            self.play(ApplyMethod(self.FunEstranha.shift,+2.35*DOWN,run_time=0.5))
            self.wait(2)
            self.play(Write(self.LimiteEstranho))
            self.play(ApplyMethod(self.LimiteEstranho.shift,+LEFT,run_time=0.5))
            self.wait(5)
            self.play(Write(self.ResulLimiteEstranho))
            self.wait()
            self.play(FadeOut(Quinto))
            self.wait(3)

class FGráficoExplicativoDosLimites(GraphScene):
    CONFIG = {
    "y_max" : 10,
    "y_min" : 0,
    "x_max" : 10,
    "x_min" : 0,
    "y_tick_frequency" : 1,
    "axes_color" : BLUE,
    "x_axis_label" : "$x$",
    "y_axis_label" : "$f(x)$",
    "LimiteEstranho":TexMobject(r" \lim_{x \rightarrow ",r"2",r" } f(x)"),
    "ResulLimiteEstranho":TexMobject(r"=3"),
    "FunEstranha":TexMobject(r"f(x) =\begin{cases}2x-1 & x \neq 2\\1 & x = 2\end{cases}", color=GREEN)

}
    def construct(self):
        #grade=ScreenGrid()
        #self.add(grade)

        self.ResulLimiteEstranho.set_color_by_gradient(WHITE, RED)
        LocalBom=np.array([1,-1.8,0])
        #PontoBom=np.array([-2.215,-0.7,0])
        self.setup_axes()
        Ponto = Dot(self.coords_to_point(x=2,y=1))#Dot(self.coords_to_point(x=0,y=0))
        #PontoDoLimite = Dot(self.coords_to_point(x=2,y=3))

        Ponto.set_color(GREEN)
        self.LimiteEstranho.scale(1.5)
        self.ResulLimiteEstranho.scale(1.5)
        self.FunEstranha.scale(1.5)
        self.ResulLimiteEstranho.move_to(self.LimiteEstranho.get_center()+2.25*RIGHT+0.25*UP)
        #self.LimiteEstranho.move_to(+1*LEFT)
        graph_1 = self.get_graph(lambda x : x*2-1, color = GREEN,x_min=0.5,x_max=1.99)#Começo da reta.
        graph_2 = self.get_graph(lambda x : 1, color=GREEN,x_min=1.99,x_max=2)#Ponto.
        graph_3 = self.get_graph(lambda x : x*2-1, color = GREEN,x_min=2.001,x_max=10)#Final da reta.

        PontoDoLimite = Dot().move_to(graph_1.points[0]).set_color(RED)

        decimal = DecimalNumber(
        0,
        num_decimal_places=3,
        )
        decimal.add_updater(lambda d: d.next_to(PontoDoLimite, UP))
        decimal.add_updater(lambda d: d.set_value(PontoDoLimite.get_center()[1]))
        #Ponto.move_to(PontoBom2)
        #PontoDoLimite.move_to(PontoBom)
        #fx=VGroup(*[graph_1,graph_3])
        Limite = VGroup(*[self.ResulLimiteEstranho,self.LimiteEstranho])
        Limite.move_to(LocalBom)
        self.FunEstranha.move_to(+2.33*RIGHT)
        Fun = VGroup(*[graph_1,Ponto,graph_3,PontoDoLimite])
        self.play(
        ShowCreation(Fun),
        run_time = 2
        )
        self.wait(3)
        self.play(MoveAlongPath(PontoDoLimite, graph_1, rate_func=linear))
        self.wait(3)
        self.play(ReplacementTransform(PontoDoLimite.copy(),Limite))
        self.wait(3)
        self.play(ReplacementTransform(Fun.copy(),self.FunEstranha))
        self.wait()
    def setup_axes(self):
    # Add this line
        GraphScene.setup_axes(self)
    # Parametters of labels
    #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
    #   For y
        init_label_y = 1
        end_label_y = 10
        step_y = 1
    # Position of labels
    #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
    #   For y
        self.y_axis.label_direction = LEFT
    # Add labels to graph
    #   For x
        self.x_axis.add_numbers(*range(
                                init_label_x,
                                end_label_x+step_x,
                                step_x


                                ))
    #   For y
        self.y_axis.add_numbers(*range(
                                init_label_y,
                                end_label_y+step_y,
                                step_y
                                ))
    #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
    )

class GFunção1x(GraphScene, MovingCameraScene):
    CONFIG = {
        "y_max" : 10,
        "y_min" : -10,
        "x_max" : 5,
        "x_min" : -5,
        "y_tick_frequency" : 2,
        "x_tick_frequency" : 1,
        "axes_color" : BLUE,
        "num_graph_anchor_points": 6000, #this is the number of points that graph manim
        "graph_origin" : ORIGIN,
        "x_axis_label" : "$x$",
        "y_axis_label" : "$f(x)$",
        "Maneira":TexMobject(r"{\frac {a} {b}}=c"),
        "Maneir2a":TexMobject(r"a=b{\times }c"),
        "LimiteDe1":TexMobject(r" \lim_{x \rightarrow 0}  \frac{1}{x} "),
        "Resul":TexMobject(r"=?"),
        "PreSub":TexMobject(r"=\frac{1}{x}"),
        "Sub1s":TexMobject(r"=\frac{1}{0}"),
        "Sub2s":TexMobject(r"1=0{\times }x")
    }
    #
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        #grade=ScreenGrid()
        #self.add(grade)
        self.camera_frame.save_state()
        self.LimiteDe1.scale(2)
        self.Resul.scale(2)
        self.PreSub.scale(2)
        self.Sub1s.scale(2)
        self.Sub2s.scale(2)
        self.Maneira.scale(2)
        self.Maneira.set_color_by_gradient(RED,WHITE,BLUE,WHITE,YELLOW)
        self.Maneir2a.set_color_by_gradient(RED,WHITE,BLUE,WHITE,YELLOW)
        self.Maneir2a.scale(2)
        self.Resul.move_to(self.LimiteDe1.get_center()+2.25*RIGHT)
        self.PreSub.move_to(self.Resul.get_center())
        self.Sub1s.move_to(self.Resul.get_center())
        self.Maneira.move_to(self.LimiteDe1.get_center()+2*UP+1*LEFT)
        self.Maneir2a.move_to(self.LimiteDe1.get_center()+2.1*UP+3*RIGHT)
        self.Sub2s.move_to(self.LimiteDe1.get_center()+2*DOWN)
        self.play(Write(self.LimiteDe1))
        self.wait(5)
        self.play(Write(self.Resul))
        self.wait(2)
        self.play(ReplacementTransform(self.Resul,self.PreSub))
        self.wait(2)
        self.play(ReplacementTransform(self.PreSub,self.Sub1s))
        self.wait(2)
        self.play(ReplacementTransform(self.LimiteDe1.copy(),self.Maneira))
        self.wait(2)
        self.play(ReplacementTransform(self.Maneira.copy(),self.Maneir2a))
        self.wait()
        self.play(ApplyMethod(self.Sub1s.set_color_by_gradient,WHITE,RED,WHITE,BLUE),ApplyMethod(self.LimiteDe1.set_color_by_gradient,YELLOW))
        self.wait()
        self.Sub2s.set_color_by_gradient(RED,WHITE,BLUE,WHITE,YELLOW)
        #self.wait()
        #self.play(ApplyMethod(self.LimiteDe1.set_color_by_gradient,YELLOW))
        #self.Sub1s.set_color_by_gradient(WHITE,RED,WHITE,BLUE)
        #self.Sub2s.set_color_by_gradient(RED,WHITE,BLUE,WHITE,YELLOW)
        #self.LimiteDe1.set_color_by_gradient(YELLOW)
        self.wait(2)
        self.play(ReplacementTransform(self.LimiteDe1.copy(),self.Sub2s))
        self.wait(2)
        Tudolas = VGroup(*[self.LimiteDe1,self.Sub2s,self.Maneira,self.Maneir2a,self.Sub1s])
        self.play(FadeOut(Tudolas))
        self.wait(2)

        self.setup_axes()

        graph = self.get_graph(lambda x : 1/x,
        color = GREEN,
        x_min = -5, # Domain 1
        x_max = -0.1
        )
        graph_2 = self.get_graph(lambda x : 1/x,
        color = GREEN,
        x_min = 0.1, # Domain 2
        x_max = 5
        )

        Ponto1M=TexMobject(r"+\infty")
        Ponto2M=TexMobject("-\infty")

        Pontox1 = Dot(self.coords_to_point(x=0,y=-2))#(0,-2)
        Pontox2 = Dot(self.coords_to_point(x=0,y=-4))#(0,-4)
        Pontox3 = Dot(self.coords_to_point(x=0,y=-6))#(0,-6)
        Pontox4 = Dot(self.coords_to_point(x=0,y=-8))#(0,-8)
        Pontox5 = Dot(self.coords_to_point(x=0,y=-10))#(0,-10)

        Pontox1t = TexMobject(r"-2")#(0,-2)
        Pontox2t = TexMobject(r"-4")#(0,-4)
        Pontox3t = TexMobject(r"-6")#(0,-6)
        Pontox4t = TexMobject(r"-8")#(0,-8)
        Pontox5t = TexMobject(r"-10")#(0,-10)

        Pontox1t.move_to(Pontox1.get_center())
        Pontox2t.move_to(Pontox2.get_center())
        Pontox3t.move_to(Pontox3.get_center())
        Pontox4t.move_to(Pontox4.get_center())
        Pontox5t.move_to(Pontox5.get_center())

        Pontox1t.scale(0.75)
        Pontox2t.scale(0.75)
        Pontox3t.scale(0.75)
        Pontox4t.scale(0.75)
        Pontox5t.scale(0.75)

        Pontosx = VGroup(*[Pontox1t,Pontox2t,Pontox3t,Pontox4t,Pontox5t])
        Pontosx.shift(+0.5*RIGHT)

        Pontoy1 = Dot(self.coords_to_point(x=-1,y=0))#(-1,0)
        Pontoy2 = Dot(self.coords_to_point(x=-2,y=0))#(-2,0)
        Pontoy3 = Dot(self.coords_to_point(x=-3,y=0))#(-3,0)
        Pontoy4 = Dot(self.coords_to_point(x=-4,y=0))#(-4,0)
        Pontoy5 = Dot(self.coords_to_point(x=-5,y=0))#(-5,0)


        Pontoy1t = TexMobject(r"-1")#(-1,0)
        Pontoy2t = TexMobject(r"-2")#(-2,0)
        Pontoy3t = TexMobject(r"-3")#(-3,0)
        Pontoy4t = TexMobject(r"-4")#(-4,0)
        Pontoy5t = TexMobject(r"-5")#(-5,0)

        Pontoy1t.scale(0.75)
        Pontoy2t.scale(0.75)
        Pontoy3t.scale(0.75)
        Pontoy4t.scale(0.75)
        Pontoy5t.scale(0.75)

        Pontoy1t.move_to(Pontoy1.get_center())
        Pontoy2t.move_to(Pontoy2.get_center())
        Pontoy3t.move_to(Pontoy3.get_center())
        Pontoy4t.move_to(Pontoy4.get_center())
        Pontoy5t.move_to(Pontoy5.get_center())
        Ponto1=Dot().move_to(graph_2.points[0])
        Pontosy = VGroup(*[Pontoy1t,Pontoy2t,Pontoy3t,Pontoy4t,Pontoy5t])
        Pontosy.shift(+0.33*UP)
        Ponto2=Dot().move_to(graph.points[-1])
        #Ponto1.set_color_by_gradient(GREEN)
        #Ponto2.set_color_by_gradient(GREEN)

        moving_dot = Dot().move_to(graph.points[0]).set_color(ORANGE)
        dot_at_start_graph = Dot().move_to(graph.points[0])
        dot_at_end_grap = Dot().move_to(graph.points[-1])

        moving_dot_2 = Dot().move_to(graph_2.points[0]).set_color(ORANGE)

        Ponto1M.move_to(moving_dot_2.get_center()+0.5*RIGHT+0.33*DOWN)
        Ponto2M.move_to(dot_at_end_grap.get_center()+0.5*LEFT+0.25*UP)

        self.play(ShowCreation(Pontosy))
        self.play(ShowCreation(Pontosx))


        self.play(
            ShowCreation(graph))
        self.play(
            ShowCreation(graph_2))
        self.wait(2)

        gráficos = VGroup(*[graph,graph_2,Ponto1,Ponto2,Ponto1M,Ponto2M])


        self.play(Write(moving_dot))
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
        self.wait()
        self.play(FadeInFromDown(Ponto2M))
        self.wait(5)
        self.play(Write(moving_dot_2))
        self.wait()
        self.play(FadeInFromDown(Ponto1M))
        self.wait(4)

        #Ponto1M=TexMobject(r"+\infty")
        #Ponto2M=TexMobject("-\infty")


        #self.wait(3)
        #self.play(*[
        #FadeOut(gráficos),
        #FadeOut(self.x_axis),
        #FadeOut(self.y_axis)
        #])
        #self.wait(3)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 5
        step_x = 1
        #   For y
        init_label_y = 2
        end_label_y = 10
        step_y = 2
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(init_label_x,end_label_x+step_x,step_x))
        #   For y
        self.y_axis.add_numbers(*range(init_label_y,end_label_y+step_y,step_y))
        #   Add Animation
        self.play(
                ShowCreation(self.x_axis),
                ShowCreation(self.y_axis)
        )

class HCenaDoCarro(GraphScene,Scene):
    CONFIG = {
        "should_transition_to_graph" : True,
        "show_distance" : True,
        "point_A" : DOWN+4*LEFT,
        "point_B" : DOWN+5*RIGHT,
        "stroke_color" : WHITE,
        "fill_color" : ORANGE,
        "fill_opacity" : 0.8,
        "distancia":TexMobject(r"100m"),
        "time_label":TextMobject("Tempo em segundos\ =", "\ 0"),

        "VeloMedia":TextMobject("Velocidade média"),
        "RVeloMedia":TexMobject(r"= \frac{\Delta s}{\Delta t} "),

        "Deltas":TexMobject(r"\Delta s=100m"),
        "Deltat":TexMobject(r"\Delta t=10s"),
        "Delta1t":TexMobject(r"\Delta t=", r"10s"),
        "Delta1s":TexMobject(r"\Delta s=", r"100m"),

        "Contolas":TexMobject(r"= \frac{100m}{10s}"),
        "Contolas2":TexMobject(r"= 10 m/s"),

        "y_max" : 100,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 10,
        "axes_color" : BLUE,
        "x_axis_label" : "Tempo (segundos)",
        "y_axis_label" : "Espaço percorrido (metros)",
    }

    def setup(self):

        Scene.setup(self)
        GraphScene.setup(self)

    def construct(self):
        A = Dot(self.point_A)
        B = Dot(self.point_B)
        line = Line(self.point_A, self.point_B)
        VGroup(A, B, line).set_color(WHITE)

        self.time_label.shift(+2*UP)
        self.time_label.get_part_by_tex(r"0").shift(+0.2*RIGHT)



        self.circle = Circle(
            stroke_color = self.stroke_color,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.move_to(A.get_center()+UP)#self.circle.move_to(A.get_center()+1.333*UP)

        self.add(A, B, line, self.circle, self.time_label)
        #self.introduce_added_mobjects()

        self.play(
            ApplyMethod(self.circle.shift,9*RIGHT,run_time=10),
            IncrementNumber(self.time_label[1], run_time = 11),
            )

        distance_brace = Brace(line, UP)
        distância = TextMobject(r"100m")
        self.distancia.move_to(distance_brace.get_center()+0.5*UP)

        self.play(
                GrowFromCenter(distance_brace),
                Write(self.distancia)
            )
        self.wait(5)
        self.play(FadeOut(self.circle),
            FadeOut(self.time_label),
            FadeOut(self.distancia),
            FadeOut(distance_brace),
            FadeOut(A),
            FadeOut(B),
            FadeOut(line))
        self.wait(5)

        self.Deltas.scale(2)
        self.Deltat.scale(2)
        self.Contolas.scale(2)
        self.Contolas2.scale(2)
        self.Deltas.shift(+2.75*LEFT)
        self.Deltat.shift(-2.75*LEFT)
        Deltas = VGroup(*[self.Deltas,self.Deltat])
        Deltas.shift(-1*UP)
        Seilá = VGroup(*[self.Deltas,self.Deltat,self.Contolas,self.Contolas2,self.VeloMedia])
        self.Deltat.set_color(BLUE)
        self.Deltas.set_color(BLUE)
        self.Contolas.set_color_by_gradient(WHITE,BLUE,BLUE,WHITE,BLUE,BLUE)
        self.Contolas2.set_color_by_gradient(WHITE,BLUE,BLUE,BLUE,BLUE,BLUE)

        self.Contolas.shift(+3*RIGHT+1*UP)
        self.Contolas2.shift(+3*RIGHT+0.95*UP)

        #Função dois, introdução à derivadas.
        #self.setup_axes()#O círculo buga.

        self.VeloMedia.scale(2)
        self.RVeloMedia.scale(2)
        self.RVeloMedia.set_color_by_gradient(WHITE,BLUE,BLUE,WHITE,BLUE,BLUE)
        self.VeloMedia.shift(+3*LEFT)
        self.RVeloMedia.shift(+2.75*RIGHT)
        ConjuVelo = VGroup(*[self.VeloMedia,self.RVeloMedia])
        ConjuVelo.shift(+1*UP)

        self.Delta1s.shift(+2.75*LEFT)
        self.Delta1t.shift(-2.75*LEFT)
        self.Delta1s.scale(2)
        self.Delta1t.scale(2)
        Delta2s = VGroup(*[self.Delta1s,self.Delta1t])
        Delta2s.set_color(BLUE)
        Delta2s.shift(-1*UP)
        AnimacaoNice = VGroup(*[self.Delta1t.get_part_by_tex(r"10s"),self.Delta1s.get_part_by_tex(r"100m")])


        self.play(Write(ConjuVelo))
        self.wait(3)
        #self.play(Write(Deltas))
        self.play(Write(Delta2s))
        self.wait(3)
        #self.play(ReplacementTransform(self.RVeloMedia,self.Contolas))
        self.play(
            ReplacementTransform(AnimacaoNice.copy(),self.Contolas),
            ReplacementTransform(self.RVeloMedia,self.Contolas))
        self.wait()
        self.play(ReplacementTransform(self.Contolas,self.Contolas2))
        self.play(FadeOut(Seilá),FadeOut(Delta2s))

        self.setup_axes()

        #self.x_axis_label.set_color(BLUE)
        #self.y_axis_label.set_color(BLUE)

        #Derivada = self.get_graph(lambda x : -0.2*x**2+x*2,  x_min = 0, x_max = 5,color = GREEN)
        Doidolas = self.get_graph(lambda x : 0.0161919688394*x**5-0.403306331726*x**4+3.12344340977*x**3-6.6331277853*x**2+5.39289849159*x+0.13790309014*np.sin(x),color=GREEN)
        #DoidolasDerivada = self.get_derivative_graph(Doidolas)
        self.play(ShowCreation(Doidolas))
        self.wait(3)
        #self.play(ShowCreation(DoidolasDerivada))

        T3 = Dot(self.coords_to_point(x=3,y=12.0998139142))

        T3x = Dot(self.coords_to_point(x=3,y=0))
        T3y = Dot(self.coords_to_point(x=0,y=12.0998139142))
        T3Lx = DashedLine(T3,T3x)
        T3Ly = DashedLine(T3,T3y)
        LinhaT3 = VGroup(*[T3,T3Lx,T3Ly])
        LinhaT3.set_color(ORANGE)

        T8 = Dot(self.coords_to_point(x=7,y=87.9586358044))

        T8x = Dot(self.coords_to_point(x=7,y=0))
        T8y = Dot(self.coords_to_point(x=0,y=87.9586358044))
        T8Lx = DashedLine(T8,T8x)
        T8Ly = DashedLine(T8,T8y)
        LinhaT8 = VGroup(*[T8,T8Lx,T8Ly])
        LinhaT8.set_color(ORANGE)

        self.play(Write(LinhaT3))
        self.wait(3)
        self.play(Write(LinhaT8))
        self.wait(3)
        self.play(FadeOut(LinhaT8),FadeOut(LinhaT3),FadeOut(self.x_axis),FadeOut(self.y_axis),FadeOut(Doidolas))
        self.wait(5)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
        #   For y
        init_label_y = 10
        end_label_y = 100
        step_y = 10
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class IDerivada(GraphScene,MovingCameraScene):
    CONFIG = {
        "y_max" : 7,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "Tempo (segundos)",
        "y_axis_label" : "Espaço percorrido (metros)",
   }

    def setup(self):
       GraphScene.setup(self)
       MovingCameraScene.setup(self)
    def construct(self):
       self.setup_axes()
       self.camera_frame.save_state()

       VeloIns = Dot(self.coords_to_point(x=4,y=4.8))
       VeloInsx = Dot(self.coords_to_point(x=4,y=0))
       VeloInsy = Dot(self.coords_to_point(x=0,y=4.8))
       VeloInsLx = DashedLine(VeloIns,VeloInsx)
       VeloInsLy = DashedLine(VeloIns,VeloInsy)
       LinhaVeloIns = VGroup(*[VeloIns,VeloInsLx,VeloInsLy])
       LinhaVeloIns.set_color(ORANGE)

       DoidolasN = self.get_graph(lambda x : -0.2*x**2+2*x, color=GREEN)
       self.play(Write(DoidolasN))
       self.wait(3)
       self.play(Write(LinhaVeloIns))
       self.wait(5)
       self.play(FadeOut(LinhaVeloIns),self.camera_frame.scale,.5,self.camera_frame.move_to,self.coords_to_point(x=4,y=4.8))
       self.wait(5)
       self.play(self.camera_frame.scale,.2)
       self.wait()
       self.play(self.camera_frame.scale,.1)
       self.wait()
       self.play(self.camera_frame.scale,.05)
       self.wait(3)
       self.play(Restore(self.camera_frame))
       self.wait()
       self.play(FadeOut(self.x_axis),FadeOut(DoidolasN),FadeOut(self.y_axis))
       self.wait(2)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
        #   For y
        init_label_y = 1
        end_label_y = 5
        step_y = 1
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class JDerivaçãoDaDerivada(MovingCameraScene):
    CONFIG = {
        "Fun":TexMobject(r"f(x)=- \frac{x^2}{5} +2x"),
        "VeloInsFun":TexMobject(r"\frac{f(x+\Delta x)-f(x)}{\Delta x} "),
        "FunSubs":TexMobject(r"\frac{- \frac{(x+\Delta x)^2}{5} +2(x+\Delta x)-(- \frac{x^2}{5} +2x)}{\Delta x} "),
        "FunSubsIZ":TexMobject(r"\frac{- 0.2(x+\Delta x)^2 +2(x+\Delta x)-(- 0.2x^2 +2x)}{\Delta x} "),
        "VeloInsFunLim":TexMobject(r" \lim_{\Delta x \rightarrow 0} \frac{f(x+\Delta x)-f(x)}{\Delta x} "),

        "VeloInsFunLi2m":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2(x+\Delta x)^2 +2(x+\Delta x)-(- 0.2x^2 +2x)}{\Delta x} "),#Função Original
        #"formula":TexMobject(r"f(x)=",r"a",r"x+b"),
        #"VeloProduto":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2(x^2+2x\Delta x+\Delta x^2)",r"+2x",r"+2\Delta x+ 0.2x^2",r"-2x",r"}{\Delta x}"),
        #"LimiteEstranho":TexMobject(r" \lim_{x \rightarrow ",r"2",r" } f(x)"),
        "VeloProduto":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2(x^2+2x\Delta x+\Delta x^2) +2x +2\Delta x+ 0.2x^2  -2x }{\Delta x} "),#Produto notável
        "VeloProdut2o":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2x^2-0.2 \times 2x\Delta x-0.2 \times \Delta x^2 +2\Delta x+ 0.2x^2 }{\Delta x} "),
        "VeloProdut3o":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{-0.2 \times 2x\Delta x-0.2 \times \Delta x^2 +2\Delta x }{\Delta x} "),
        "VeloProdut4o":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{\Delta x(-0.2 \times 2x-0.2\Delta x + 2 )}{\Delta x} "),
        "VeloProdut5o":TexMobject(r"\lim_{\Delta x \rightarrow 0} -0.2 \times 2x-0.2\Delta x + 2 "),
        "VeloProdut6o":TexMobject(r"-0.2 \times 2x-0.2 \times 0 + 2 "),
        "VeloProdut7o":TexMobject(r"-0.2 \times 2x + 2 "),

        "FunDerivadaF":TexMobject(r"f'(x)"),
        "FunDerivada":TexMobject(r"f'(x)=-0.2 \times 2x + 2 "),
        "FunDerivad2a":TexMobject(r"f'(4)=-0.2 \times 2(4) + 2 "),
        "FunDerivad3a":TexMobject(r"f'(4)=-0.2 \times 8 + 2 "),
        "FunDerivad4a":TexMobject(r"f'(4)=-1.6 + 2 "),
        "FunDerivad5a":TexMobject(r"f'(4)=0.4"),
        }

    def construct(self):
        self.Fun.scale(2)
        self.VeloInsFun.scale(2)
        self.FunSubs.scale(1.45)
        self.FunSubsIZ.scale(1.45)
        self.VeloInsFunLim.scale(2)
        self.VeloInsFun.set_color(ORANGE)
        self.VeloInsFun.shift(+DOWN)
        self.VeloInsFunLim.set_color(ORANGE)
        self.VeloInsFunLi2m.scale(1)

        self.FunDerivada.scale(2)
        self.FunDerivad2a.scale(2)
        self.FunDerivad3a.scale(2)
        self.FunDerivad4a.scale(2)
        self.FunDerivad5a.scale(2)

        self.FunDerivada.shift(DOWN)
        self.FunDerivad2a.shift(DOWN)
        self.FunDerivad3a.shift(DOWN)
        self.FunDerivad4a.shift(DOWN)
        self.FunDerivad5a.shift(DOWN)

        self.Fun.shift(+2*UP)#Levantando a função.
        self.Fun.set_color(YELLOW)

        self.camera_frame.save_state()

        self.FunSubs.set_color_by_gradient(BLUE,PURPLE)
        self.FunSubsIZ.set_color_by_gradient(BLUE,PURPLE)
        self.VeloInsFunLi2m.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProduto.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut2o.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut3o.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut4o.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut5o.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut6o.set_color_by_gradient(BLUE,PURPLE)
        self.VeloProdut7o.set_color_by_gradient(BLUE,PURPLE)

        self.FunDerivada.set_color(RED)
        self.FunDerivad2a.set_color(RED)
        self.FunDerivad3a.set_color(RED)
        self.FunDerivad4a.set_color(RED)
        self.FunDerivad5a.set_color(RED)

        self.VeloInsFun.shift(+3*DOWN)
        self.VeloInsFunLim.shift(+3*DOWN)

        #"Fun":TexMobject(r"f(x)=- \frac{x^2}{5} +2x"),
        #"VeloInsFun":TexMobject(r"\frac{f(x+\Delta x)-f(x)}{\Delta x} "),
        #"FunSubs":TexMobject(r"\frac{- \frac{(x+\Delta x)^2}{5} +2(x+\Delta x)-(- \frac{x^2}{5} +2x)}{\Delta x} "),
        #"FunSubsIZ":TexMobject(r"\frac{- 0.2(x+\Delta x)^2 +2(x+\Delta x)-(- 0.2x^2 +2x)}{\Delta x} "),
        #"VeloInsFunLim":TexMobject(r" \lim_{\Delta x \rightarrow 0} \frac{f(x+\Delta x)-f(x)}{\Delta x} "),
        #"VeloInsFunLi2m":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2(x+\Delta x)^2 +2(x+\Delta x)-(- 0.2x^2 +2x)}{\Delta x} "),
        #"VeloInsFunLi2mNaoDa":TexMobject(r"\lim_{\Delta x \rightarrow 0} \frac{- 0.2(x+0)^2 +2(x+0)-(- 0.2x^2 +2x)}{0} "),


        #self.camera_frame.move_to, s,
        #          self.camera_frame.set_width,s.get_width()*2

        self.play(FadeInFromDown(self.Fun),
        self.camera_frame.move_to,self.Fun,
        self.camera_frame.set_width,self.Fun.get_width()*1.2
        )
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        self.play(FadeIn(self.VeloInsFun),
        self.camera_frame.move_to,self.VeloInsFun,
        self.camera_frame.set_width,self.VeloInsFun.get_width()*1.2
        )
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        #self.play(self.camera_frame.set_width, text.get_width() * 1.2)
        self.play(ReplacementTransform(self.VeloInsFun,self.FunSubs),
        self.camera_frame.move_to,self.FunSubs,
        self.camera_frame.set_width,self.FunSubs.get_width()*1.2
        )
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        self.play(ReplacementTransform(self.FunSubs,self.FunSubsIZ),
        self.camera_frame.move_to,self.FunSubsIZ,
        self.camera_frame.set_width,self.FunSubsIZ.get_width()*1.2
        )
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        self.play(FadeIn(self.VeloInsFunLim),
        self.camera_frame.move_to,self.VeloInsFunLim,
        self.camera_frame.set_width,self.VeloInsFunLim.get_width()*1.2
        )
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        self.play(ReplacementTransform(self.FunSubsIZ,self.VeloInsFunLi2m),FadeOut(self.VeloInsFunLim),
        self.camera_frame.move_to,self.VeloInsFunLi2m,
        self.camera_frame.set_width,self.VeloInsFunLi2m.get_width()*1.2
        )
        self.wait(5)
        #self.play(Restore(self.camera_frame))
        #self.wait(5)
        self.play(ReplacementTransform(self.VeloInsFunLi2m,self.VeloProduto),self.camera_frame.set_width, self.VeloProduto.get_width() *1.2)
        self.wait(5)
        self.play(Restore(self.camera_frame))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProduto,self.VeloProdut2o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut2o,self.VeloProdut3o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut3o,self.VeloProdut4o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut4o,self.VeloProdut5o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut5o,self.VeloProdut6o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut6o,self.VeloProdut7o))
        self.wait(5)
        self.play(ReplacementTransform(self.VeloProdut7o,self.FunDerivada))
        self.wait(5)
        self.play(ApplyMethod(self.FunDerivada.shift,+1*UP))

        self.FunDerivad2a.shift(+1*UP)
        #self.FunDerivad2a.shift(+1*UP)
        self.FunDerivad3a.shift(+1*UP)
        self.FunDerivad4a.shift(+1*UP)
        self.FunDerivad5a.shift(+1*UP)

        self.wait(5)
        self.play(ReplacementTransform(self.FunDerivada,self.FunDerivad2a))
        self.wait(5)
        self.play(ReplacementTransform(self.FunDerivad2a,self.FunDerivad3a))
        self.wait(5)
        self.play(ReplacementTransform(self.FunDerivad3a,self.FunDerivad4a))
        self.wait(5)
        self.play(ReplacementTransform(self.FunDerivad4a,self.FunDerivad5a))
        self.wait(5)
        self.play(FadeOut(self.FunDerivad5a),FadeOut(self.Fun))
        self.wait(5)

class KDerivada(GraphScene):
    CONFIG = {
        "y_max" : 7,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "Tempo (segundos)",
        "y_axis_label" : "Espaço percorrido (metros)",

        "FormulaReta":TexMobject(r"r(x)=f'(x_0)(x-x_0)+f(x_0)"),
        "Reta":TexMobject(r"r(x)=f'(4)(x-4)+f(4)"),
        "Reta2":TexMobject(r"r(x)=0.4(x-4)+4.8"),
        "Reta3":TexMobject(r"r(x)=0.4x-(0.4)4+4.8"),
        "Reta4":TexMobject(r"r(x)=0.4x-1.6+4.8"),
        "Reta5":TexMobject(r"r(x)=0.4x+3.2"),

        "Velocidade":TexMobject(r"f'(x)=",r"-0.4",r"x + 2"),
        "Acelera":TexMobject(r"a=-0.4"),
        "AceleraFun":TexMobject(r"f''(x)=-0.4"),
   }

    def setup(self):
       GraphScene.setup(self)

    def construct(self):

        self.FormulaReta.set_color(ORANGE)
        self.Reta.set_color(ORANGE)
        self.Reta2.set_color(ORANGE)
        self.Reta3.set_color(ORANGE)
        self.Reta4.set_color(ORANGE)
        self.Reta5.set_color(ORANGE)

        self.Velocidade.scale(2)
        self.Velocidade.set_color_by_gradient(BLUE,PURPLE)
        self.AceleraFun.scale(2)
        self.AceleraFun.set_color_by_gradient(BLUE,PURPLE)
        self.Acelera.scale(2)
        self.Acelera.move_to(self.Velocidade.get_center()+1*DOWN)

        self.FormulaReta.scale(2)
        self.Reta.scale(2)
        self.Reta2.scale(2)
        self.Reta3.scale(2)
        self.Reta4.scale(2)
        self.Reta5.scale(2)

        self.play(Write(self.FormulaReta))
        self.wait(2)
        self.play(ReplacementTransform(self.FormulaReta,self.Reta))
        self.wait(2)
        self.play(ReplacementTransform(self.Reta,self.Reta2))
        self.wait(2)
        self.play(ReplacementTransform(self.Reta2,self.Reta3))
        self.wait(2)
        self.play(ReplacementTransform(self.Reta3,self.Reta4))
        self.wait(2)
        self.play(ReplacementTransform(self.Reta4,self.Reta5))
        self.wait(2)
        self.play(FadeOut(self.Reta5))
        self.wait(3)

        self.setup_axes()

        VeloIns = Dot(self.coords_to_point(x=4,y=4.8))
        VeloInsx = Dot(self.coords_to_point(x=4,y=0))
        VeloInsy = Dot(self.coords_to_point(x=0,y=4.8))
        VeloInsLx = DashedLine(VeloIns,VeloInsx)
        VeloInsLy = DashedLine(VeloIns,VeloInsy)
        LinhaVeloIns = VGroup(*[VeloIns,VeloInsLx,VeloInsLy])
        LinhaVeloIns.set_color(ORANGE)

        DoidolasN = self.get_graph(lambda x : -0.2*x**2+2*x, color=GREEN)
        DoidolasD = self.get_graph(lambda x : 0.4*x+3.2, color=ORANGE)
        Constante = self.get_graph(lambda x : 5 , color=ORANGE)
        Velo = self.get_graph(lambda x : -0.4*x + 2 , color=YELLOW)

        self.play(Write(DoidolasN))
        self.wait(3)
        self.play(FadeIn(DoidolasD))
        self.wait(3)
        #self.play(ApplyWave(DoidolasN))
        self.play(Write(LinhaVeloIns))
        self.wait(5)
        self.play(FadeOut(LinhaVeloIns))
        self.wait(5)
        self.play(FadeOut(DoidolasD))
        self.wait()
        self.play(FadeIn(Constante))
        self.wait(2)
        self.play(FadeOut(Constante))
        self.wait(2)
        self.play(Write(Velo),Write(self.Velocidade))
        self.wait()
        self.play(ReplacementTransform(self.Velocidade.get_part_by_tex("-0.4").copy(),self.Acelera))
        self.wait()
        self.play(FadeOut(self.Velocidade))
        self.wait()
        self.play(ReplacementTransform(self.Acelera.copy(),self.AceleraFun))
        self.wait()
        self.play(FadeOut(self.x_axis),FadeOut(DoidolasN),FadeOut(self.y_axis),FadeOut(self.Acelera),FadeOut(Velo))
        self.wait(2)
        self.play(FadeOut(self.AceleraFun))
        self.wait(2)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
        #   For y
        init_label_y = 1
        end_label_y = 5
        step_y = 1
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )


class LCírculo(ZoomedScene,MovingCameraScene):
#    CONFIG = {
#        "Area":TexMobject(r"A=\pi r^2"),
#        "Circun":TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi(r+dr)^2-\pi r^2}{dr} "),
#        "Circun2":TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi(r^2+2r(dr)+dr^2)-\pi r^2}{dr} "),
#        "Circun3":TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi r^2 +2 \pi r(dr)+\pi dr^2-\pi r^2}{dr} "),
#        "Circun4":TexMobject(r"\lim_{dr \rightarrow 0} \frac{2 \pi r(dr)+\pi dr^2}{dr} "),
#        "Circun5":TexMobject(r"\lim_{dr \rightarrow 0} \frac{dr(2 \pi r+\pi dr)}{dr} "),
#        "Circun6":TexMobject(r"\lim_{dr \rightarrow 0} 2 \pi r+\pi dr "),
#        "Circun7":TexMobject(r"2 \pi r+\pi 0 "),
#        "Circun8":TexMobject(r"2 \pi r"),
#        "Circun9":TexMobject(r"C=2 \pi r"),
#
#        #"VersSim"
#
#        "point_B" : DOWN+5*RIGHT,
#        "stroke_color" : WHITE,
#        "fill_color" : ORANGE,
#                }

    #def setup(self):
    #    self.ZoomedScene()
    #    self.MovingCameraScene()

    def construct(self):

        self.Area=TexMobject(r"A=\pi r^2")
        self.Circun=TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi(r+dr)^2-\pi r^2}{dr} ")
        self.Circun2=TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi(r^2+2r(dr)+dr^2)-\pi r^2}{dr} ")
        self.Circun3=TexMobject(r"\lim_{dr \rightarrow 0} \frac{\pi r^2 +2 \pi r(dr)+\pi dr^2-\pi r^2}{dr} ")
        self.Circun4=TexMobject(r"\lim_{dr \rightarrow 0} \frac{2 \pi r(dr)+\pi dr^2}{dr} ")
        self.Circun5=TexMobject(r"\lim_{dr \rightarrow 0} \frac{dr(2 \pi r+\pi dr)}{dr} ")
        self.Circun6=TexMobject(r"\lim_{dr \rightarrow 0} 2 \pi r+\pi dr ")
        self.Circun7=TexMobject(r"2 \pi r+\pi 0 ")
        self.Circun8=TexMobject(r"2 \pi r")
        self.Circun9 = TexMobject(r"C=2 \pi r")

        self.Derivada = TexMobject(r" \lim_{ \Delta x \rightarrow 0}  \frac{f(x+\Delta x) - f(x)}{\Delta x} ")
        self.DerivadaFun = TexMobject(r"y=f(x)")
        self.Derivada2 = TexMobject(r"\frac{dy}{dx}")
        self.Derivada3 = TexMobject(r"\frac{d}{dr} (\pi r^2)=2\pi r")
        Derivadas = VGroup(*[self.Derivada,self.DerivadaFun,self.Derivada2,self.Derivada3])
        Derivadas.scale(2)


        self.camera_frame.save_state()
        self.circle = Circle(stroke_color = WHITE,fill_color = ORANGE,fill_opacity=0.5,radius=2.75)
        self.circle2 = Circle(stroke_color = WHITE,fill_color = ORANGE,fill_opacity=0.5,radius=2.5)
        circle = Circle(stroke_color = WHITE,fill_color = RED,fill_opacity=1,radius=2.5)
        dr = TexMobject(r"dr")
        dr.scale(0.25)

        #Ponto1 = Dot()
        #Ponto2 = Dot()
        #Ponto1.shift(circle.get_center()+2.5*DOWN)
        #Ponto2.shift(circle.get_center()+2.75*DOWN)
        #Linha = Line(Ponto1,Ponto2)
        #DrBra = Brace(Linha,RIGHT)


        Fórmulas = VGroup(*[self.Circun,self.Circun2,self.Circun3,self.Circun4,self.Circun5,self.Circun6,self.Circun7,self.Circun8])
        #self.Area.shift(+1.5*LEFT)
        self.Area.set_color(YELLOW)
        self.Area.scale(2)
        Fórmulas.scale(2)
        Fórmulas.shift(+10*LEFT)
        Fórmulas.set_color_by_gradient(BLUE,PURPLE)

        self.Circun9.set_color_by_gradient(YELLOW_C,ORANGE)
        self.Circun9.scale(2)
        self.Circun9.shift(self.Circun.get_center()+2*UP)

        self.play(ShowCreation(circle))
        self.wait(5)
        self.play(FadeIn(self.circle))
        #self.wait(5)
        #self.play(ReplacementTransform(self.circle,circle.copy(),run_time=10))
        self.wait()
        self.play(ReplacementTransform(circle.copy(),self.Area),run_time=0.5)
        self.wait()
        self.play(Write(self.Circun),self.camera_frame.move_to,self.Circun)
        self.wait()
        self.play(ReplacementTransform(self.Circun,self.Circun2),self.camera_frame.move_to,self.Circun2)
        self.wait()
        self.play(ReplacementTransform(self.Circun2,self.Circun3))
        self.wait()
        self.play(ReplacementTransform(self.Circun3,self.Circun4))
        self.wait()
        self.play(ReplacementTransform(self.Circun4,self.Circun5))
        self.wait()
        self.play(ReplacementTransform(self.Circun5,self.Circun6))
        self.wait()
        self.play(ReplacementTransform(self.Circun6,self.Circun7))
        self.wait()
        self.play(ReplacementTransform(self.Circun7,self.Circun8))
        self.wait()
        self.play(ReplacementTransform(self.Circun8.copy(),self.Circun9))
        self.wait()
        dr.shift(2.65*DOWN)
        #dr.shift(DrBra.get_center(),+0.33*RIGHT)
        self.play(Restore(self.camera_frame))
        self.wait()
        self.activate_zooming(animate=False)
        self.play(self.zoomed_camera.frame.shift, 2.55 * DOWN)
        self.wait()
        self.play(Write(dr))
        self.wait()
        self.play(FadeOut(dr))
        self.wait()
        self.play(ReplacementTransform(self.circle,self.circle2,run_time=5))
        self.wait(5)
        self.play(FadeOut(self.Area),FadeOut(self.circle),FadeOut(self.circle2),FadeOut(circle),Restore(self.camera_frame))

class MEsfera(ThreeDScene):
    CONFIG = {
        "DFuncionas":TextMobject("Derivadas")
    }
    def construct(self):
        #DFuncionas=TextMobject("Derivadas")
        self.DFuncionas.scale(2.5)
        self.Derivada = TexMobject(r" \lim_{ \Delta x \rightarrow 0}  \frac{f(x+\Delta x) - f(x)}{\Delta x} ")
        self.DerivadaFun = TexMobject(r"y=f(x)")
        self.Derivada2 = TexMobject(r"\frac{dy}{dx}")
        self.Derivada3 = TexMobject(r"\frac{d}{dr} (\pi r^2)=2\pi r")
        Derivadas = VGroup(*[self.Derivada,self.DerivadaFun,self.Derivada2,self.Derivada3])
        Derivadas.scale(2)
        self.Derivada.shift(+1*UP)
        self.Derivada2.shift(+1*UP)
        self.DerivadaFun.shift(+1*DOWN)
        self.Derivada.set_color_by_gradient(BLUE,PURPLE)
        self.DerivadaFun.set_color_by_gradient(BLUE,PURPLE)
        self.Derivada2.set_color_by_gradient(BLUE,PURPLE)
        self.Derivada3.set_color_by_gradient(BLUE,PURPLE)


        #self.play(FadeInFromDown(self.DFuncionas))
        #self.wait(3.5)
        #self.play(FadeOut(self.DFuncionas))
        #self.wait()
        self.play(Write(self.Derivada))
        self.wait()
        self.play(ReplacementTransform(self.Derivada,self.Derivada2))
        self.wait()
        self.play(Write(self.DerivadaFun))
        self.wait()
        self.play(FadeOut(self.DerivadaFun),FadeOut(self.Derivada2))
        self.wait()
        self.play(Write(self.Derivada3))
        self.wait()
        self.play(FadeOut(self.Derivada3))
        self.wait(5)

        circle = Circle(stroke_color = WHITE,fill_color = RED,fill_opacity=1,radius=2.5)
        axes = ThreeDAxes()
        sphere = ParametricSurface(
        lambda u, v: np.array([
        1.5 * np.cos(u) * np.cos(v),
        1.5 * np.cos(u) * np.sin(v),
        1.5 * np.sin(u)
        ]), v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
        checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )
        sphere1 = ParametricSurface(
        lambda u, v: np.array([
        2 * np.cos(u) * np.cos(v),
        2 * np.cos(u) * np.sin(v),
        2 * np.sin(u)
        ]), v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
        checkerboard_colors=[GREEN_D, GREEN_E], resolution=(15, 32),fill_opacity=1
        )

        sphere2 = ParametricSurface(
        lambda u, v: np.array([
        2 * np.cos(u) * np.cos(v),
        2 * np.cos(u) * np.sin(v),
        2 * np.sin(u)
        ]), v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
        checkerboard_colors=[GREEN_D, GREEN_E], resolution=(15, 32),fill_opacity=0.5
        )

        text3d=TexMobject(r"V = \frac{4}{3} \pi r^3")
        Text = TexMobject(r"\frac{d}{dr} ( \frac{4}{3} \pi r^3)=4\pi r^2")
        Text.set_color_by_gradient(BLUE,PURPLE)
        text3d.to_corner(UL)
        Text.move_to(text3d.get_center()+1*DOWN+0.8*RIGHT)


        self.play(FadeInFromDown(circle))#,FadeIn(axes))
        self.wait(2)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        #self.play(Write(axes),ReplacementTransform(circle,sphere))
        self.play(ReplacementTransform(circle,sphere))
        #self.play(ShowCreation(sphere))
        self.wait(2)
        #self.play(Write(text3d))
        self.add_fixed_in_frame_mobjects(text3d)
        self.wait(2)
        self.play(ShowCreation(sphere1))
        self.wait(2)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.play(ReplacementTransform(sphere1,sphere2,run_time=5))
        self.wait(3)
        self.play(ReplacementTransform(sphere2,sphere,run_time=5))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(Text)
        #self.stop_ambient_camera_rotation()
        #self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait(5)
        self.play(FadeOut(sphere),FadeOut(Text),FadeOut(text3d))
        self.wait(5)

class NIntegralConstante(GraphScene):
    CONFIG = {
        "y_max" : 25,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 5,
        "axes_color" : WHITE,
        "x_axis_label" : "Tempo (segundos)",
        "y_axis_label" : "Velocidade",

        "Velocidade":TexMobject(r"V(t)",r"=10"),

        "Contolas":TexMobject(r"10",r"\times",r" 6",r"=",r"60m"),


        "lower_bound":0,
        "upper_bound":6,
        "n_riemann_iterations" : 6,
    }
    def construct(self):
        self.show_f_dx_sum()
    def construct(self):
        self.Velocidade.scale(2)

        self.Velocidade.get_part_by_tex(r"=10").set_color_by_gradient(WHITE,BLUE,BLUE)

        self.play(Write(self.Velocidade))
        self.wait()
        self.play(ApplyMethod(self.Velocidade.shift,2.65*UP))
        self.setup_axes()
        Baixo = Dot(self.coords_to_point(x=6,y=0))
        Alto = Dot(self.coords_to_point(x=6,y=10))

        PrimeiroPonto = Dot(self.coords_to_point(x=0,y=0))
        SegundoPonto = Dot(self.coords_to_point(x=0,y=10))
        Linha = DashedLine(Baixo,Alto)
        Linha2 = Line(PrimeiroPonto,SegundoPonto)


        self.Contolas.move_to(Alto.get_center()+LEFT+0.5*UP)
        
        Graph = self.get_graph(lambda x : 10,x_min=0,x_max=6,color=GREEN)
        Area = self.get_area(Graph,0,6)

        self.play(ShowCreation(Graph))
        self.wait()
        self.play(ShowCreation(Area))
        Pontos = VGroup(*[Alto,Linha])
        self.wait()
        self.play(ShowCreation(Pontos))

        self.Contolas.get_part_by_tex(r"10").set_color(BLUE)
        #self.play(ApplyMethod(self.Velocidade.get_part_by_tex(r"=10").set_color_by_gradient(WHITE,BLUE,BLUE)))
        self.Contolas.get_part_by_tex(r"6").set_color(GREEN)
        self.Contolas.scale(2)

        conta = VGroup(*[self.Contolas.get_part_by_tex(r"60"),self.Contolas.get_part_by_tex(r"=")])

        self.wait()
        self.play(
            ReplacementTransform(Alto.copy(),self.Contolas.get_part_by_tex(r"10")),
            ReplacementTransform(Graph.copy(),self.Contolas.get_part_by_tex(r"6")),
            Write(self.Contolas.get_part_by_tex(r"\times")),
            #Write(self.Contolas.get_part_by_tex(r"60")),
            #Write(self.Contolas.get_part_by_tex(r"=")),
            FadeOut(self.x_axis),
            FadeOut(self.y_axis),
            FadeOut(Pontos),
            FadeOut(Graph),
            ReplacementTransform(Area,conta),
            )
        self.wait()
        self.play(
            FadeOut(self.Contolas.get_part_by_tex(r"10")),
            FadeOut(self.Contolas.get_part_by_tex(r"6")),
            FadeOut(self.Contolas.get_part_by_tex(r"\times")),
            FadeOut(self.Contolas.get_part_by_tex(r"=")),
            )
        self.wait(0.25)
        #self.play(ApplyMethod(self.Contolas.get_part_by_tex(r"60m").shift,self.Velocidade.get_center()+1*DOWN))
        self.play(ApplyMethod(self.Contolas.get_part_by_tex(r"60m").shift,+2*LEFT))

        self.wait(5)
        self.play(FadeOut(self.Velocidade),FadeOut(self.Contolas.get_part_by_tex(r"60m")))
        self.wait()

    def show_f_dx_sum(self):
        kwargs = {
            "x_min" : self.lower_bound,
            "x_max" : self.upper_bound,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        low_opacity = 0.25
        start_rect_index = 3
        num_shown_sum_steps = 5

        self.rect_list = self.get_riemann_rectangles_list(
            self.Graph, self.n_riemann_iterations,
        )
        rects = self.rects = self.rect_list[0]
        rects.save_state()

        start_rect = rects[start_rect_index]
        f_brace = Brace(start_rect, LEFT, buff = 0)
        dx_brace = Brace(start_rect, DOWN, buff = 0)
        f_brace.label = f_brace.get_text("$f(x)$")
        dx_brace.label = dx_brace.get_text("$dx$")

        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5, **kwargs
        )

        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
        )
        self.play(*[
            ApplyMethod(
                rect.set_fill, None, 
                1 if rect is start_rect else low_opacity
            )
            for rect in rects
        ])
        self.play(*it.chain(
            list(map(GrowFromCenter, [f_brace, dx_brace])),
            list(map(Write, [f_brace.label, dx_brace.label])),
        ))
        self.wait()
        for i in range(start_rect_index+1, last_rect_index):
            self.play(
                rects[i-1].set_fill, None, low_opacity,
                rects[i].set_fill, None, 1,
                f_brace.set_height, rects[i].get_height(),
                f_brace.next_to, rects[i], LEFT, 0,
                dx_brace.next_to, rects[i], DOWN, 0,
                *[
                    MaintainPositionRelativeTo(brace.label, brace)
                    for brace in (f_brace, dx_brace)
                ]
            )
        self.wait()
        self.play(*it.chain(
            list(map(FadeOut, [
                f_brace, dx_brace, 
                f_brace.label, dx_brace.label
            ])),
            [rects.set_fill, None, kwargs["fill_opacity"]]
        ))
 

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
        #   For y
        init_label_y = 5
        end_label_y = 25
        step_y = 5
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class OIntegral(GraphScene):
    CONFIG = {
        "y_max" : 10,
        "y_min" : 0,
        "x_max" : 5,
        "x_min" : 0,
        "y_tick_frequency" : 2,
        "axes_color" : WHITE,
        "x_axis_label" : "Tempo (segundos)",
        "y_axis_label" : "Velocidade",
        "Velocidade2":TexMobject(r"V(t)",r"= - t^2+5t"),
        "Diferencial":TexMobject(r"\frac{ds}{dt}",r"=",r"V(t)"),
        "Diferencia2l":TexMobject(r"\int\frac{ds}{dt}",r"=",r"\int - t^2+5t dt"), 
        "Diferencia3l":TexMobject(r"s(t)",r"=",r"\int - t^2+5t dt"),
    }
    def construct(self):
        self.Velocidade2.scale(2)
        self.Diferencia2l.scale(2)
        self.Diferencial.scale(2)
        self.Diferencia3l.scale(2)
        #self.Diferencia4l.scale(2)
        
        self.Velocidade2.get_part_by_tex(r"V(t)").set_color(GREEN)
        self.Diferencial.get_part_by_tex(r"V(t)").set_color(GREEN)
        self.Diferencial.get_part_by_tex(r"\frac{ds}{dt}").set_color_by_gradient(YELLOW,YELLOW,WHITE,BLUE,BLUE)
        self.Diferencia2l.get_part_by_tex(r"\int\frac{ds}{dt}").set_color_by_gradient(WHITE,YELLOW,YELLOW,WHITE,BLUE,BLUE)
        self.Diferencia3l.get_part_by_tex(r"s(t)").set_color_by_gradient(YELLOW,WHITE,WHITE,WHITE)
        
        self.play(Write(self.Velocidade2))
        self.wait()
        self.play(ApplyMethod(self.Velocidade2.shift,2.65*UP))
        self.wait()
        self.play(
            Write(self.Diferencial.get_part_by_tex(r"\frac{ds}{dt}")),
            ReplacementTransform(self.Velocidade2.get_part_by_tex(r"V(t)").copy(),self.Diferencial.get_part_by_tex(r"V(t)")),
            Write(self.Diferencial.get_part_by_tex(r"=")),
            )
        self.wait(3)
        self.play(ReplacementTransform(self.Diferencial,self.Diferencia2l))
        self.wait(3)
        self.play(ReplacementTransform(self.Diferencia2l,self.Diferencia3l))
        self.wait(3)
        self.play(FadeOut(self.Diferencia3l),FadeOut(self.Velocidade2))
        self.wait(2)
        self.setup_axes()
        Graph2 = self.get_graph(lambda x : -1*x**2+5*x,x_min=0,x_max=5,color=GREEN)
        Baixolas = self.get_graph(lambda x : 0,x_min=0,x_max=5,color=GREEN)

        AreaEstranha = self.get_area(Baixolas,0,5)
        AreaOlas = self.get_riemann_rectangles(
            Graph2,
            x_min=0,
            x_max=5,
            dx=0.1,
            input_sample_type="left",
            stroke_width=0.1,
            stroke_color=WHITE,
            fill_opacity=1
            )
        AreaOlas2 = self.get_riemann_rectangles(
            Graph2,
            x_min=0,
            x_max=5,
            dx=0.02,
            input_sample_type="left",
            stroke_width=0.0000000001,
            stroke_color=WHITE,
            fill_opacity=1
            )

        Area = self.get_area(Graph2,0,5)

        self.wait()
        self.play(ShowCreation(Graph2))
        self.wait(2)
        self.play(ApplyWave(Graph2))
        self.wait(2)
        self.add(AreaEstranha)
        self.play(ReplacementTransform(AreaEstranha,AreaOlas))
        self.wait(2)
        self.play(ReplacementTransform(AreaOlas,AreaOlas2))
        self.wait(2)
        self.play(FadeOut(AreaOlas2),FadeOut(Graph2),FadeOut(self.x_axis),FadeOut(self.y_axis))
        self.wait(5)

    def setup_axes(self):
        # Add this line
        GraphScene.setup_axes(self)
        # Parametters of labels
        #   For x
        init_label_x = 1
        end_label_x = 5
        step_x = 1
        #   For y
        init_label_y = 2
        end_label_y = 10
        step_y = 2
        # Position of labels
        #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
        #   For y
        self.y_axis.label_direction = LEFT
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x


                                    ))
        #   For y
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class PTeoremaFundamentalDoCálculo(GraphScene):
    CONFIG = {
        "lower_bound" : 1,
        "upper_bound" : 7,
        "lower_bound_color" : RED,
        "upper_bound_color" : GREEN,
        "n_riemann_iterations" : 6,
    }

    def construct(self):
        self.add_graph_and_integral()
        self.show_f_dx_sum()
        self.show_rects_approaching_area()
        self.write_antiderivative()
        self.show_integral_considering_continuum()
        self.show_antiderivative_considering_bounds()

    def add_graph_and_integral(self):
        self.setup_axes()
        integral = TexMobject("\\int", "^b", "_a", "f(x)", "\\,dx")
        integral.next_to(ORIGIN, LEFT)
        integral.to_edge(UP)
        integral.set_color_by_tex("a", self.lower_bound_color)
        integral.set_color_by_tex("b", self.upper_bound_color)
        #graph = self.get_graph(
        #    lambda x : -0.01*x*(x-3)*(x-6)*(x-12) + 3,
        #)
        graph = self.get_graph(lambda x : -0.3125*x**2+2.8125*x,x_min=-10,x_max=10,color=GREEN)
        self.add(integral, graph)
        self.graph = graph
        self.integral = integral

        self.bound_labels = VGroup()
        self.v_lines = VGroup()
        for bound, tex in (self.lower_bound, "a"), (self.upper_bound, "b"):
            label = integral.get_part_by_tex(tex).copy()
            label.scale(1.5)
            label.next_to(self.coords_to_point(bound, 0), DOWN)
            v_line = self.get_vertical_line_to_graph(
                bound, graph, color = label.get_color()
            )

            self.bound_labels.add(label)
            self.v_lines.add(v_line)
            self.add(label, v_line)

    def show_f_dx_sum(self):
        kwargs = {
            "x_min" : self.lower_bound,
            "x_max" : self.upper_bound,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        low_opacity = 0.25
        start_rect_index = 3
        num_shown_sum_steps = 5
        last_rect_index = start_rect_index + num_shown_sum_steps + 1

        self.rect_list = self.get_riemann_rectangles_list(
            self.graph, self.n_riemann_iterations, **kwargs
        )
        rects = self.rects = self.rect_list[0]
        rects.save_state()

        start_rect = rects[start_rect_index]
        f_brace = Brace(start_rect, LEFT, buff = 0)
        dx_brace = Brace(start_rect, DOWN, buff = 0)
        f_brace.label = f_brace.get_text("$f(x)$")
        dx_brace.label = dx_brace.get_text("$dx$")

        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5, **kwargs
        )

        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
        )
        self.play(*[
            ApplyMethod(
                rect.set_fill, None, 
                1 if rect is start_rect else low_opacity
            )
            for rect in rects
        ])
        self.play(*it.chain(
            list(map(GrowFromCenter, [f_brace, dx_brace])),
            list(map(Write, [f_brace.label, dx_brace.label])),
        ))
        self.wait()
        for i in range(start_rect_index+1, last_rect_index):
            self.play(
                rects[i-1].set_fill, None, low_opacity,
                rects[i].set_fill, None, 1,
                f_brace.set_height, rects[i].get_height(),
                f_brace.next_to, rects[i], LEFT, 0,
                dx_brace.next_to, rects[i], DOWN, 0,
                *[
                    MaintainPositionRelativeTo(brace.label, brace)
                    for brace in (f_brace, dx_brace)
                ]
            )
        self.wait()
        self.play(*it.chain(
            list(map(FadeOut, [
                f_brace, dx_brace, 
                f_brace.label, dx_brace.label
            ])),
            [rects.set_fill, None, kwargs["fill_opacity"]]
        ))

    def show_rects_approaching_area(self):
        for new_rects in self.rect_list:
            self.transform_between_riemann_rects(
                self.rects, new_rects
            )

    def write_antiderivative(self):
        deriv = TexMobject(
            "{d", "F", "\\over\\,", "dx}", "(x)", "=", "f(x)"
        )
        deriv_F = deriv.get_part_by_tex("F")
        deriv.next_to(self.integral, DOWN, MED_LARGE_BUFF)
        rhs = TexMobject(*"=F(b)-F(a)")
        rhs.set_color_by_tex("a", self.lower_bound_color)
        rhs.set_color_by_tex("b", self.upper_bound_color)
        rhs.next_to(self.integral, RIGHT)

        self.play(Write(deriv))
        self.wait(2)
        self.play(*it.chain(
            [
                ReplacementTransform(deriv_F.copy(), part)
                for part in rhs.get_parts_by_tex("F")
            ],
            [
                Write(VGroup(*rhs.get_parts_by_tex(tex)))
                for tex in "=()-"
            ]
        ))
        for tex in "b", "a":
            self.play(ReplacementTransform(
                self.integral.get_part_by_tex(tex).copy(),
                rhs.get_part_by_tex(tex)
            ))
            self.wait()
        self.wait(2)

        self.deriv = deriv
        self.rhs = rhs

    def show_integral_considering_continuum(self):
        self.play(*[
            ApplyMethod(mob.set_fill, None, 0.2)
            for mob in (self.deriv, self.rhs)
        ])
        self.play(
            self.rects.restore,
            run_time = 3,
            rate_func = there_and_back
        )
        self.wait()
        for x in range(2):
            self.play(*[
                ApplyFunction(
                    lambda m : m.shift(MED_SMALL_BUFF*UP).set_fill(opacity = 1),
                    rect,
                    run_time = 3,
                    rate_func = squish_rate_func(
                        there_and_back,
                        alpha, alpha+0.2
                    )
                )
                for rect, alpha in zip(
                    self.rects, 
                    np.linspace(0, 0.8, len(self.rects))
                )
            ])
        self.wait()

    def show_antiderivative_considering_bounds(self):
        self.play(
            self.integral.set_fill, None, 0.5,
            self.deriv.set_fill, None, 1,
            self.rhs.set_fill, None, 1,
        )
        for label, line in reversed(list(zip(self.bound_labels, self.v_lines))):
            new_line = line.copy().set_color(YELLOW)
            label.save_state()
            self.play(label.set_color, YELLOW)
            self.play(ShowCreation(new_line))
            self.play(ShowCreation(line))
            self.remove(new_line)
            self.play(label.restore)
        self.wait()
        self.play(self.integral.set_fill, None, 1)
        self.wait(3)

class QCalculandoArea(MovingCameraScene):
    CONFIG = {
        "Diferencia4l":TexMobject(r"s(t)",r"=",r" - \frac{t^3}{3} + \frac{5t^2}{2} +C"),
        "Derivada":TexMobject(r"s(t)",r"=",r"\int_0^5 - t^2+5t \space dt"),
        "DiferencialMesmo":TexMobject(r"- \frac{5^3}{3} + \frac{5(5)^2}{2} +C-(- \frac{0^3}{3} + \frac{5(0)^2}{2} +C)"),
        "DiferencialMesmo2":TexMobject(r"- \frac{5^3}{3} + \frac{5(5)^2}{2}"),
        "DiferencialMesmo3":TexMobject(r"- \frac{5^3}{3} + \frac{5(5)^2}{2}"),
        "DiferencialMesmo4":TexMobject(r"- \frac{250}{6}+ \frac{375}{6}  "),
        "DiferencialMesmo5":TexMobject(r"\frac{-250+375}{6}"),
        "DiferencialMesmo6":TexMobject(r"\frac{125}{6}"),
        "DiferencialMesmo7":TexMobject(r"\frac{125}{6} metros")
    }
    def construct(self):
        self.Diferencia4l.scale(2)
        self.Derivada.scale(2)
        #self.DiferencialMesmo.scale(2)
        self.DiferencialMesmo2.scale(2)
        self.DiferencialMesmo3.scale(2)
        self.DiferencialMesmo4.scale(2)
        self.DiferencialMesmo5.scale(2)
        self.DiferencialMesmo6.scale(2)
        self.DiferencialMesmo7.scale(2)
        self.Diferencia4l.to_edge(UP)
        self.Derivada.to_edge(DOWN)

        self.Derivada.get_part_by_tex(r"\int_0^5 - t^2+5t").set_color_by_gradient(BLUE,GREEN)
        self.Diferencia4l.get_part_by_tex(r"s(t)").set_color_by_gradient(YELLOW,WHITE,WHITE,WHITE)
        self.Derivada.get_part_by_tex(r"s(t)").set_color_by_gradient(YELLOW,WHITE,WHITE,WHITE)
        
        self.DiferencialMesmo.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo2.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo3.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo4.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo5.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo6.set_color_by_gradient(BLUE,GREEN)
        self.DiferencialMesmo7.set_color_by_gradient(BLUE,GREEN)

        self.play(FadeIn(self.Diferencia4l))
        self.wait(2)
        self.play(FadeIn(self.Derivada))
        self.wait(2)
        self.play(Write(self.DiferencialMesmo))
        self.wait(2)
        self.play(ReplacementTransform(self.DiferencialMesmo,self.DiferencialMesmo2))
        self.wait(2)
        self.play(ReplacementTransform(self.DiferencialMesmo2,self.DiferencialMesmo3))
        self.wait(2)
        self.play(ReplacementTransform(self.DiferencialMesmo3,self.DiferencialMesmo4))
        self.wait(2)
        self.play(ReplacementTransform(self.DiferencialMesmo4,self.DiferencialMesmo5))
        self.wait(2)
        self.play(ReplacementTransform(self.DiferencialMesmo5,self.DiferencialMesmo6))
        self.wait(2)
        self.play(
            ReplacementTransform(self.DiferencialMesmo6,self.DiferencialMesmo7),
            FadeOut(self.Derivada),
            FadeOut(self.Diferencia4l),
            self.camera_frame.move_to,self.DiferencialMesmo7,
            self.camera_frame.set_width,self.DiferencialMesmo7.get_width()*2
            )
        self.wait(5)

class RSomaCírculo(Scene):#Explicar que a área de um círculo é a soma de todas as circunferências dentro do círculo.
    CONFIG = {
        "Soma":TexMobject(r"\int_0^r2\pi r \space dr ",r"= \pi r^2"),
    }
    def construct(self):
        circulo = Circle(radius=1.5,stroke_color=WHITE,fill_color=BLUE_E,fill_opacity=1)#stroke_color = WHITE,fill_color = ORANGE,fill_opacity=0.5,radius=2.75
        circo = Circle(radius=1.5,stroke_color=WHITE,fill_opacity=0.5)
        circo.set_color_by_gradient(BLUE,GREEN)
        ponto = SmallDot(circulo.get_center())
        self.Soma.scale(2)
        circo.move_to(circulo.get_center())
        self.Soma.move_to(circulo.get_center()+1*DOWN)
        #self.play(FadeOut(self.Velocidade),FadeOut(self.Contolas.get_part_by_tex(r"60m")))

        self.play(ShowCreation(circulo))
        self.wait(2)
        self.play(ReplacementTransform(ponto,circo),run_time=2)
        self.wait()
        self.play(ReplacementTransform(circo,ponto),run_time=2)
        self.wait()
        self.play(ApplyMethod(circulo.shift,1*UP),ApplyMethod(ponto.shift,1*UP))
        self.wait()
        self.play(FadeIn(self.Soma))
        self.wait(5)

class SDiferençaDeDificuldade(MovingCameraScene):
    CONFIG = {
    "Fácil":TexMobject(r" \frac{d}{dx}{(\sqrt[{}] {\tan(x)}}) ",r"= \frac{\sec(x)^2}{2 \enspace \sqrt[{}] {\tan(x)}} "),
    "Difícil":TexMobject(r" \int \sqrt[{}] {\tan(x)} \space dx = \frac{\sqrt[{}] {2}  \arctan( \frac{\tan(x)-1}{\sqrt[{}] {2\tan(x)}} )}{2} + \frac{\sqrt[{}] {2} \ln(\lvert \frac{\tan(x)+1-{\sqrt {2\tan(x)}}}{\tan(x)+1+{\sqrt {2\tan(x)}}}  \rvert)}{4} +C")

   }
    def construct(self):
        self.Fácil.scale(3)
        self.Fácil.set_color_by_gradient(BLUE,PURPLE)
        self.Difícil.scale(3)
        self.Difícil.set_color_by_gradient(BLUE,GREEN)

        self.play(self.camera_frame.set_width,self.Difícil.get_width()*0.65)#self.play(Write(self.Fácil.get_part_by_tex(r" \frac{d}{dx}{(\sqrt[{}] {\tan(x)}}) ")))
        self.play(Write(self.Fácil))
        self.wait(5)
        self.play(ReplacementTransform(self.Fácil,self.Difícil),self.camera_frame.set_width,self.Difícil.get_width()*1)
        
        self.wait(5)

class TSegundaDerivadaGraficamente(GraphScene):
    CONFIG = {
        "x1" : 0,
        "x2" : 4,
        "x3" : 8,
        "y" : 4,
        "deriv_color" : YELLOW,
        "second_deriv_color" : GREEN,
    }
    def construct(self):
        self.force_skipping()

        self.setup_axes()
        self.draw_f()
        self.show_derivative()
        self.write_second_derivative()
        self.show_curvature()

        self.revert_to_original_skipping_status()
        self.contrast_big_and_small_concavity()

    def draw_f(self):
        def func(x):
            return 0.1*(x-self.x1)*(x-self.x2)*(x-self.x3) + self.y

        graph = self.get_graph(func)
        graph_label = self.get_graph_label(graph, "f(x)")

        self.play(
            ShowCreation(graph, run_time = 2),
            Write(
                graph_label,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            )
        )
        self.wait()

        self.graph = graph
        self.graph_label = graph_label

    def show_derivative(self):
        deriv = TexMobject("\\frac{df}{dx}")
        deriv.next_to(self.graph_label, DOWN, MED_LARGE_BUFF)
        deriv.set_color(self.deriv_color)
        ss_group = self.get_secant_slope_group(
            1, self.graph,
            dx = 0.01,
            secant_line_color = self.deriv_color
        )

        self.play(
            Write(deriv),
            *list(map(ShowCreation, ss_group))
        )
        self.animate_secant_slope_group_change(
            ss_group, target_x = self.x3,
            run_time = 5
        )
        self.wait()
        self.animate_secant_slope_group_change(
            ss_group, target_x = self.x2,
            run_time = 3
        )
        self.wait()

        self.ss_group = ss_group
        self.deriv = deriv

    def write_second_derivative(self):
        second_deriv = TexMobject("\\frac{d^2 f}{dx^2}")
        second_deriv.next_to(self.deriv, DOWN, MED_LARGE_BUFF)
        second_deriv.set_color(self.second_deriv_color)
        points = [
            self.input_to_graph_point(x, self.graph)
            for x in (self.x2, self.x3)
        ]
        words = TextMobject("Change to \\\\ slope")
        words.next_to(
            center_of_mass(points), UP, 1.5*LARGE_BUFF
        )
        arrows = [
            Arrow(words.get_bottom(), p, color = WHITE)
            for p in points
        ]

        self.play(Write(second_deriv))
        self.wait()
        self.play(
            Write(words),
            ShowCreation(
                arrows[0], 
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            run_time = 2
        )
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x3,
            run_time = 3,
            added_anims = [
                Transform(
                    *arrows, 
                    run_time = 3,
                    path_arc = 0.75*np.pi
                ),
            ]
        )
        self.play(FadeOut(arrows[0]))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x2,
            run_time = 3,
        )

        self.second_deriv_words = words
        self.second_deriv = second_deriv

    def show_curvature(self):
        positive_curve, negative_curve = [
            self.get_graph(
                self.graph.underlying_function,
                x_min = x_min,
                x_max = x_max,
                color = color,
            ).set_stroke(width = 6)
            for x_min, x_max, color in [
                (self.x2, self.x3, PINK),
                (self.x1, self.x2, RED),
            ]
        ]
        dot = Dot()
        def get_dot_update_func(curve):
            def update_dot(dot):
                dot.move_to(curve.points[-1])
                return dot
            return update_dot

        self.play(
            ShowCreation(positive_curve, run_time = 3),
            UpdateFromFunc(dot, get_dot_update_func(positive_curve))
        )
        self.play(FadeOut(dot))
        self.wait()
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x3,
            run_time = 4,
            added_anims = [Animation(positive_curve)]
        )

        self.play(*list(map(FadeOut, [self.ss_group, positive_curve])))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x1,
            run_time = 0
        )
        self.play(FadeIn(self.ss_group))
        self.play(
            ShowCreation(negative_curve, run_time = 3),
            UpdateFromFunc(dot, get_dot_update_func(negative_curve))
        )
        self.play(FadeOut(dot))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x2,
            run_time = 4,
            added_anims = [Animation(negative_curve)]
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            self.graph, self.ss_group, 
            negative_curve, self.second_deriv_words
        ])))

    def contrast_big_and_small_concavity(self):
        colors = color_gradient([GREEN, WHITE], 3)
        x0, y0 = 4, 2
        graphs = [
            self.get_graph(func, color = color)
            for color, func in zip(colors, [
                lambda x : 5*(x - x0)**2 + y0,
                lambda x : 0.2*(x - x0)**2 + y0,
                lambda x : (x-x0) + y0,
            ])
        ]
        arg_rhs_list = [
            TexMobject("(", str(x0), ")", "=", str(rhs))
            for rhs in (10, 0.4, 0)
        ]
        for graph, arg_rhs in zip(graphs, arg_rhs_list):
            graph.ss_group = self.get_secant_slope_group(
                x0-1, graph, 
                dx = 0.001,
                secant_line_color = YELLOW
            )
            arg_rhs.move_to(self.second_deriv.get_center(), LEFT)
            graph.arg_rhs = arg_rhs
        graph = graphs[0]

        v_line = DashedLine(*[
            self.coords_to_point(x0, 0),
            self.coords_to_point(x0, y0),
        ])
        input_label = TexMobject(str(x0))
        input_label.next_to(v_line, DOWN)

        self.play(ShowCreation(graph, run_time = 2))
        self.play(
            Write(input_label),
            ShowCreation(v_line)
        )
        self.play(
            ReplacementTransform(
                input_label.copy(),
                graph.arg_rhs.get_part_by_tex(str(x0))
            ),
            self.second_deriv.next_to, graph.arg_rhs.copy(), LEFT, SMALL_BUFF,
            Write(VGroup(*[
                submob
                for submob in graph.arg_rhs
                if submob is not graph.arg_rhs.get_part_by_tex(str(x0))
            ]))
        )
        self.wait()
        self.play(FadeIn(graph.ss_group))
        self.animate_secant_slope_group_change(
            graph.ss_group, target_x = x0 + 1,
            run_time = 3,
        )
        self.play(FadeOut(graph.ss_group))
        self.wait()
        for new_graph in graphs[1:]:
            self.play(Transform(graph, new_graph))
            self.play(Transform(
                graph.arg_rhs,
                new_graph.arg_rhs,
            ))
            self.play(FadeIn(new_graph.ss_group))
            self.animate_secant_slope_group_change(
                new_graph.ss_group, target_x = x0 + 1,
                run_time = 3,
            )
            self.play(FadeOut(new_graph.ss_group))

class UComoLerANotação(GraphScene, ReconfigurableScene):
    CONFIG = {
        "x_max" : 5,
        "dx" : 0.4,
        "x" : 2,
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def setup(self):
        for base in self.__class__.__bases__:
            base.setup(self)

    def construct(self):
        self.force_skipping()

        self.add_graph()
        self.take_two_steps()
        self.show_dfs()
        self.show_ddf()
        self.revert_to_original_skipping_status()
        self.show_proportionality_to_dx_squared()
        self.write_second_derivative()

    def add_graph(self):
        self.setup_axes()
        graph = self.get_graph(lambda x : x**2)
        graph_label = self.get_graph_label(
            graph, "f(x)", 
            direction = LEFT,
            x_val = 3.3
        )
        self.add(graph, graph_label)

        self.graph = graph

    def take_two_steps(self):
        v_lines = [
            self.get_vertical_line_to_graph(
                self.x + i*self.dx, self.graph,
                line_class = DashedLine,
                color = WHITE
            )
            for i in range(3)
        ]
        braces = [
            Brace(VGroup(*v_lines[i:i+2]), buff = 0)
            for i in range(2)
        ]
        for brace in braces:
            brace.dx = TexMobject("dx")
            max_width = 0.7*brace.get_width()
            if brace.dx.get_width() > max_width:
                brace.dx.set_width(max_width)
            brace.dx.next_to(brace, DOWN, SMALL_BUFF)

        self.play(ShowCreation(v_lines[0]))
        self.wait()
        for brace, line in zip(braces, v_lines[1:]):
            self.play(
                ReplacementTransform(
                    VectorizedPoint(brace.get_corner(UP+LEFT)),
                    brace,
                ),
                Write(brace.dx, run_time = 1),
            )
            self.play(ShowCreation(line))
        self.wait()

        self.v_lines = v_lines
        self.braces = braces

    def change_step_size(self):
        self.transition_to_alt_config(dx = 0.6)
        self.transition_to_alt_config(dx = 0.01, run_time = 3)

    def show_dfs(self):
        dx_lines = VGroup()
        df_lines = VGroup()
        df_dx_groups = VGroup()
        df_labels = VGroup()
        for i, v_line1, v_line2 in zip(it.count(1), self.v_lines, self.v_lines[1:]):
            dx_line = Line(
                v_line1.get_bottom(),
                v_line2.get_bottom(),
                color = GREEN
            )
            dx_line.move_to(v_line1.get_top(), LEFT)
            dx_lines.add(dx_line)

            df_line = Line(
                dx_line.get_right(),
                v_line2.get_top(),
                color = YELLOW
            )
            df_lines.add(df_line)
            df_label = TexMobject("df_%d"%i)
            df_label.set_color(YELLOW)
            df_label.scale(0.8)
            df_label.next_to(df_line.get_center(), UP+LEFT, MED_LARGE_BUFF)
            df_arrow = Arrow(
                df_label.get_bottom(),
                df_line.get_center(),
                buff = SMALL_BUFF,
            )
            df_line.label = df_label
            df_line.arrow = df_arrow
            df_labels.add(df_label)

            df_dx_groups.add(VGroup(df_line, dx_line))

        for brace, dx_line, df_line in zip(self.braces, dx_lines, df_lines):
            self.play(
                VGroup(brace, brace.dx).next_to,
                dx_line, DOWN, SMALL_BUFF,
                FadeIn(dx_line),
            )
            self.play(ShowCreation(df_line))
            self.play(
                ShowCreation(df_line.arrow),
                Write(df_line.label)
            )
            self.wait(2)

        self.df_dx_groups = df_dx_groups
        self.df_labels = df_labels

    def show_ddf(self):
        df_dx_groups = self.df_dx_groups.copy()
        df_dx_groups.generate_target()
        df_dx_groups.target.arrange(
            RIGHT, 
            buff = MED_LARGE_BUFF,
            aligned_edge = DOWN
        )
        df_dx_groups.target.next_to(
            self.df_dx_groups, RIGHT, 
            buff = 3,
            aligned_edge = DOWN
        )

        df_labels = self.df_labels.copy()
        df_labels.generate_target()
        h_lines = VGroup()
        for group, label in zip(df_dx_groups.target, df_labels.target):
            label.next_to(group.get_right(), LEFT, SMALL_BUFF)
            width = df_dx_groups.target.get_width() + MED_SMALL_BUFF
            h_line = DashedLine(ORIGIN, width*RIGHT)
            h_line.move_to(
                group.get_corner(UP+RIGHT)[1]*UP + \
                df_dx_groups.target.get_right()[0]*RIGHT,
                RIGHT
            )
            h_lines.add(h_line)
            max_height = 0.8*group.get_height()
            if label.get_height() > max_height:
                label.set_height(max_height)


        ddf_brace = Brace(h_lines, LEFT, buff = SMALL_BUFF)
        ddf = ddf_brace.get_tex("d(df)", buff = SMALL_BUFF)
        ddf.scale(
            df_labels[0].get_height()/ddf.get_height(), 
            about_point = ddf.get_right()
        )
        ddf.set_color(MAROON_B)

        self.play(
            *list(map(MoveToTarget, [df_dx_groups, df_labels])),
            run_time = 2
        )
        self.play(ShowCreation(h_lines, run_time = 2))
        self.play(GrowFromCenter(ddf_brace))
        self.play(Write(ddf))
        self.wait(2)

        self.ddf = ddf

    def show_proportionality_to_dx_squared(self):
        ddf = self.ddf.copy()
        ddf.generate_target()
        ddf.target.next_to(self.ddf, UP, LARGE_BUFF)
        rhs = TexMobject(
            "\\approx", "(\\text{Alguma constante})", "(dx)^2"
        )
        rhs.scale(0.8)
        rhs.next_to(ddf.target, RIGHT)

        example_dx = TexMobject(
            "dx = 0.01 \\Rightarrow (dx)^2 = 0.0001"
        )
        example_dx.scale(0.8)
        example_dx.to_corner(UP+RIGHT)

        self.play(MoveToTarget(ddf))
        self.play(Write(rhs))
        self.wait()
        self.play(Write(example_dx))
        self.wait(2)
        self.play(FadeOut(example_dx))

        self.ddf = ddf
        self.dx_squared = rhs.get_part_by_tex("dx")

    def write_second_derivative(self):
        ddf_over_dx_squared = TexMobject(
            "{d(df)", "\\over", "(dx)^2}"
        )
        ddf_over_dx_squared.scale(0.8)
        ddf_over_dx_squared.move_to(self.ddf, RIGHT)
        ddf_over_dx_squared.set_color_by_tex("df", self.ddf.get_color())
        parens = VGroup(
            ddf_over_dx_squared[0][1],
            ddf_over_dx_squared[0][4],
            ddf_over_dx_squared[2][0],
            ddf_over_dx_squared[2][3],
        )

        right_shifter = ddf_over_dx_squared[0][0]
        left_shifter = ddf_over_dx_squared[2][4]

        exp_two = TexMobject("2")
        exp_two.set_color(self.ddf.get_color())
        exp_two.scale(0.5)
        exp_two.move_to(right_shifter.get_corner(UP+RIGHT), LEFT)
        exp_two.shift(MED_SMALL_BUFF*RIGHT)
        pre_exp_two = VGroup(ddf_over_dx_squared[0][2])

        self.play(
            Write(ddf_over_dx_squared.get_part_by_tex("over")),
            *[
                ReplacementTransform(
                    mob, 
                    ddf_over_dx_squared.get_part_by_tex(tex),
                    path_arc = -np.pi/2,                    
                )
                for mob, tex in [(self.ddf, "df"), (self.dx_squared, "dx")]
            ]
        )
        self.wait(2)
        self.play(FadeOut(parens))
        self.play(
            left_shifter.shift, 0.2*LEFT,
            right_shifter.shift, 0.2*RIGHT,
            ReplacementTransform(pre_exp_two, exp_two),
            ddf_over_dx_squared.get_part_by_tex("over").scale_in_place, 0.8
        )
        self.wait(2)

class VVelocidadeAceleraçãoArrancada(GraphScene):
    CONFIG = {
        "Velocidade":TexMobject(r" \frac{ds}{dt} =",r"V",r"(t)"),
        "Aceleração":TexMobject(r" \frac{d^2s}{dt^2} =",r"a(t)"),
        "Arrancada":TexMobject(r" \frac{d^3s}{dt^3} =",r"A",r"(t)"),

        "y_max" : 10,
        "y_min" : 0,
        "x_max" : 10,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "axes_color" : BLUE,
        "x_axis_label" : "$x$",
        "y_axis_label" : "$f(x)$",
    }
    def construct(self):
        self.Velocidade.scale(2)
        self.Aceleração.scale(2)
        self.Arrancada.scale(2)

        self.Velocidade.get_part_by_tex(r"V").set_color(BLUE)
        self.Aceleração.get_part_by_tex(r"a(t)").set_color_by_gradient(YELLOW,WHITE,WHITE,WHITE)
        self.Arrancada.get_part_by_tex(r"A").set_color(ORANGE)

        self.Velocidade.shift(+2.4*UP)
        self.Arrancada.shift(+2.4*DOWN)

        self.play(Write(self.Velocidade))
        self.wait(2)
        self.play(ReplacementTransform(self.Velocidade.copy(),self.Aceleração))
        self.wait(2)
        self.play(ReplacementTransform(self.Aceleração.copy(),self.Arrancada))
        self.wait(4)
        self.play(FadeOut(self.Velocidade),FadeOut(self.Aceleração),FadeOut(self.Arrancada))
        self.wait(2)

        self.setup_axes()
        Momento = self.get_graph(lambda x : 0.00167126359263*x**4-0.0449282229551*x**3+0.299101765222*x**2+0.712726991276*x ,x_min=0,color=GREEN)
        Velocidade = self.get_derivative_graph(Momento)
        Velocidade.set_color(BLUE)
        Aceleração = self.get_derivative_graph(Velocidade)
        Aceleração.set_color(YELLOW)
        Arrancada = self.get_derivative_graph(Aceleração)
        Arrancada.set_color(ORANGE)

        self.play(ShowCreation(Momento))
        self.wait(2)
        self.play(ReplacementTransform(Momento.copy(),Velocidade))
        self.wait(2)
        self.play(ReplacementTransform(Velocidade.copy(),Aceleração))
        self.wait(2)
        self.play(ReplacementTransform(Aceleração.copy(),Arrancada))
        self.wait(5)
        self.play(FadeOut(Momento),FadeOut(Velocidade),FadeOut(Arrancada),FadeOut(self.x_axis),FadeOut(self.y_axis),FadeOut(Aceleração))

    def setup_axes(self):
    # Add this line
        GraphScene.setup_axes(self)
    # Parametters of labels
    #   For x
        init_label_x = 1
        end_label_x = 10
        step_x = 1
    #   For y
        init_label_y = 1
        end_label_y = 10
        step_y = 1
    # Position of labels
    #   For x
        self.x_axis.label_direction = DOWN #DOWN is default
    #   For y
        self.y_axis.label_direction = LEFT
    # Add labels to graph
    #   For x
        self.x_axis.add_numbers(*range(
                                init_label_x,
                                end_label_x+step_x,
                                step_x


                                ))
    #   For y
        self.y_axis.add_numbers(*range(
                                init_label_y,
                                end_label_y+step_y,
                                step_y
                                ))
    #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
    )

class WExemploDeAproximação(GraphScene):
    CONFIG = {
        "function" : lambda x : np.exp(-x**2),
        "function_tex" : "e^{-x^2}", 
        "function_color" : BLUE,
        "order_sequence" : [0, 2, 4],
        "center_point" : 0,
        "approximation_terms" : ["1 ", "-x^2", "+\\frac{1}{2}x^4"],
        "approximation_color" : GREEN,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -1,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }
    def construct(self):
        self.setup_axes()
        func_graph = self.get_graph(self.function,self.function_color)
        Apro1 = self.get_graph(lambda x : 1)
        Apro2 = self.get_graph(lambda x : 1-x**2)
        Apro3 = self.get_graph(lambda x : 1-x**2+0.5*x**4)

        near_text = TexMobject(r"x=0")
        near_text.to_corner(UP + RIGHT)
        near_text.add_background_rectangle()
        equation = TexMobject(r"e^{-x^2}",r"\approx 1",r"-x^2",r"+\frac{1}{2}x^4")
        equation1 = TexMobject(r"-x^2")
        equation.next_to(near_text, DOWN, MED_LARGE_BUFF)
        equation.to_edge(RIGHT)
        near_text.next_to(equation, UP, MED_LARGE_BUFF)
        equation.shift(+0.5*LEFT)
        equation1.move_to(equation.get_center()+0.33*RIGHT+0.05*UP)

        self.play(ShowCreation(func_graph),Write(equation.get_part_by_tex(r"e^{-x^2}")))
        self.wait(2)
        self.play(
            ReplacementTransform(func_graph.copy(),Apro1),
            Write(equation.get_part_by_tex(r"\approx 1")),
            Write(near_text)
            )
        self.wait(2)
        self.play(
            ReplacementTransform(Apro1,Apro2),
            Write(equation1)
            )
        self.wait(2)
        self.play(ReplacementTransform(Apro2,Apro3),Write(equation.get_part_by_tex(r"+\frac{1}{2}x^4")))
        self.wait(4)
        self.play(FadeOut(Apro3),FadeOut(equation),FadeOut(equation1),FadeOut(func_graph),FadeOut(self.x_axis),FadeOut(self.y_axis))

class YMiniatura(GraphScene):
    CONFIG = {
        "lower_bound" : 1,
        "upper_bound" : 7,
        "lower_bound_color" : RED,
        "upper_bound_color" : GREEN,
        "n_riemann_iterations" : 6,
    }

    def construct(self):
        self.add_graph_and_integral()
        self.show_f_dx_sum()
        self.show_rects_approaching_area()
    
    def add_graph_and_integral(self):
        self.setup_axes()
        integral = TexMobject("\\int", "^b", "_a", "f(x)", "\\,dx")
        derivada = TexMobject(r" \frac{d}{dx} (f(x))")
        integral.next_to(ORIGIN, LEFT)
        integral.to_edge(UP)
        derivada.move_to(integral.get_center()+1*LEFT)
        integral.set_color_by_tex("a", self.lower_bound_color)
        integral.set_color_by_tex("b", self.upper_bound_color)
        graph = self.get_graph(lambda x : -0.3125*x**2+2.8125*x,x_min=-10,x_max=10,color=GREEN)
        Graph = self.get_graph(lambda x : 1.5625*x+1.25)
        Graph.set_color(YELLOW)
        graph2 = self.get_derivative_graph(graph)
        graph2.set_color(BLUE)
        derivada.move_to(integral.get_center()+1*LEFT+1*DOWN)
        self.add(graph,graph2,Graph,integral,derivada)
        self.graph = graph
        self.integral = integral

        self.bound_labels = VGroup()
        self.v_lines = VGroup()
        for bound, tex in (self.lower_bound, "a"), (self.upper_bound, "b"):
            label = integral.get_part_by_tex(tex).copy()
            label.scale(1.5)
            label.next_to(self.coords_to_point(bound, 0), DOWN)
            v_line = self.get_vertical_line_to_graph(
                bound, graph, color = label.get_color()
            )

            self.bound_labels.add(label)
            self.v_lines.add(v_line)
            self.add(label, v_line)

    def show_f_dx_sum(self):
        kwargs = {
            "x_min" : self.lower_bound,
            "x_max" : self.upper_bound,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        low_opacity = 0.25
        start_rect_index = 3
        num_shown_sum_steps = 5
        last_rect_index = start_rect_index + num_shown_sum_steps + 1

        self.rect_list = self.get_riemann_rectangles_list(
            self.graph, self.n_riemann_iterations, **kwargs
        )
        rects = self.rects = self.rect_list[0]
        rects.save_state()

        start_rect = rects[start_rect_index]
        f_brace = Brace(start_rect, LEFT, buff = 0)
        dx_brace = Brace(start_rect, DOWN, buff = 0)
        f_brace.label = f_brace.get_text("$f(x)$")
        dx_brace.label = dx_brace.get_text("$dx$")

        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5, **kwargs
        )

        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
        )
        self.play(*[
            ApplyMethod(
                rect.set_fill, None, 
                1 if rect is start_rect else low_opacity
            )
            for rect in rects
        ])
        self.play(*it.chain(
            list(map(GrowFromCenter, [f_brace, dx_brace])),
            list(map(Write, [f_brace.label, dx_brace.label])),
        ))
        self.wait()
        for i in range(start_rect_index+1, last_rect_index):
            self.play(
                rects[i-1].set_fill, None, low_opacity,
                rects[i].set_fill, None, 1,
                f_brace.set_height, rects[i].get_height(),
                f_brace.next_to, rects[i], LEFT, 0,
                dx_brace.next_to, rects[i], DOWN, 0,
                *[
                    MaintainPositionRelativeTo(brace.label, brace)
                    for brace in (f_brace, dx_brace)
                ]
            )
        self.wait()
        self.play(*it.chain(
            list(map(FadeOut, [
                f_brace, dx_brace, 
                f_brace.label, dx_brace.label
            ])),
            [rects.set_fill, None, kwargs["fill_opacity"]]
        ))

    def show_rects_approaching_area(self):
        for new_rects in self.rect_list:
            self.transform_between_riemann_rects(
                self.rects, new_rects
            )

