from tkinter.messagebox import NO
import pyxel
import time

#画面遷移用の定数
SCENE_TITLE = 0	#タイトル画面
SCENE_PLAY = 1	#ゲーム画面
SCENE_END = 2


    

class App:
    def __init__(self):
        pyxel.init(192, 128, title="Stolen Tricolor",fps=60)
        pyxel.load("Stolen Tricolor.pyxres")                      #editorデータ読み込み(コードと同じフォルダにある)
        self.backgraund_x = 0
        self.player_x = 16
        self.player_y = 64
        self.player_dy = 0
        self.is_alive = True
        self.player_life = 8
        self.player_score = 0
        self.scene = SCENE_TITLE                       #画面遷移の初期化
        self.whiteStar = [(i * 60, pyxel.rndi(8, 80), pyxel.rndi(0, 2), True) for i in range(3)]
        self.yerrowStar = [(i * 60, pyxel.rndi(8, 80), pyxel.rndi(0, 2), True) for i in range(1)]
        self.firstAttack = [(i * 60, pyxel.rndi(8, 80), pyxel.rndi(0, 2), True) for i in range(1)]
        self.secondAttack = [(i * 60, pyxel.rndi(8, 80), pyxel.rndi(0, 2), True) for i in range(2)]
        self.thirdAttack = [(i * 60, pyxel.rndi(8, 80), pyxel.rndi(0, 2), True) for i in range(4)]
        self.cloud = [(i * 60, pyxel.rndi(8, 40), pyxel.rndi(0, 2), True) for i in range(2)]
        self.bird = [(i * 60, pyxel.rndi(8, 40), pyxel.rndi(0, 2), True) for i in range(2)]
        self.flower = [(i * 60, pyxel.rndi(8, 40), pyxel.rndi(0, 2), True) for i in range(2)]
        self.plane = [(i * 60, pyxel.rndi(8, 40), pyxel.rndi(0, 2), True) for i in range(2)]
        pyxel.run(self.update, self.draw)              #実行開始 更新関数 描画関数


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #処理の画面分岐
        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_PLAY:
            self.update_play()
        elif self.scene == SCENE_END:
            self.update_end()


    def update_title(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY
            pyxel.playm(2, loop = True)



    def update_play(self):
        if self.player_life == 0:
            pyxel.stop()
            pyxel.play(1,8)
            self.scene = SCENE_END
        
        if self.backgraund_x == -1856 and self.player_x > 150:
            pyxel.stop()
            pyxel.play(0,9)
            self.scene = SCENE_END
        self.update_player()



    def update_end(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(1,1)
            self.scene = SCENE_TITLE
            self.player_life = 8
            self.backgraund_x = 0
            self.player_score = 0
            self.player_x = 16
            self.player_y = 64


    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(self.player_y - 2, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = max(self.player_y + 2, 0)

        if self.player_y < 8 or self.player_y > 80:
            if self.player_y > 80:
                    self.player_y = 80
            else:
                self.player_y = 8

        if self.player_x > 162:
            self.player_x = 162


        if self.backgraund_x > -1856:
            self.backgraund_x -= 0.25
        else:
            self.backgraund_x = -1856
            
        for i, v in enumerate(self.whiteStar):
            self.whiteStar[i] = self.update_item(*v)
        
        for i, v in enumerate(self.yerrowStar):
            self.yerrowStar[i] = self.update_rare_item(*v)
        
        if self.backgraund_x > -448:
            for i, v in enumerate(self.firstAttack):
                self.firstAttack[i] = self.update_first_attack(*v)
            for i, v in enumerate(self.cloud):
                self.cloud[i] = self.update_cloud(*v)
        if -350 > self.backgraund_x > -1040:
            for i, v in enumerate(self.secondAttack):
                self.secondAttack[i] = self.update_second_attack(*v)
            for i, v in enumerate(self.bird):
                self.bird[i] = self.update_bird(*v)
        if -950 > self.backgraund_x > -1600:
            for i, v in enumerate(self.thirdAttack):
                self.thirdAttack[i] = self.update_third_attack(*v)
            for i, v in enumerate(self.flower):
                self.flower[i] = self.update_flower(*v)
        if  self.backgraund_x < -1500:
            for i, v in enumerate(self.firstAttack):
                self.firstAttack[i] = self.update_first_attack(*v)
            for i, v in enumerate(self.secondAttack):
                self.secondAttack[i] = self.update_second_attack(*v)
            for i, v in enumerate(self.thirdAttack):
                self.thirdAttack[i] = self.update_third_attack(*v)
            for i, v in enumerate(self.plane):
                self.plane[i] = self.update_plane(*v)
        elif self.backgraund_x == -1800:
            None


    def update_item(self, x, y, kind, is_alive):
        #スター
        if is_alive and abs(x - self.player_x) < 16 and abs(y - self.player_y) < 16:
            is_alive = False
            self.player_score += (kind + 1) * 10
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(1,1)

        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 80)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_rare_item(self, x, y, kind, is_alive):
        #スター
        if is_alive and abs(x - self.player_x) < 16 and abs(y - self.player_y) < 16:
            is_alive = False
            self.player_score += (kind + 1) * 100
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(1,1)

        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 80)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_first_attack(self, x, y, kind, is_alive):
        #攻撃
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.player_life -= 1
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(1,2)
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 80)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_second_attack(self, x, y, kind, is_alive):
        #攻撃
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.player_life -= 1
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(1,2)
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 80)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_third_attack(self, x, y, kind, is_alive):
        #攻撃
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.player_life -= 1
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(1,2)
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 80)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_cloud(self, x, y, kind, is_alive):
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 40)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_bird(self, x, y, kind, is_alive):
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 40)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_flower(self, x, y, kind, is_alive):
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 40)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def update_plane(self, x, y, kind, is_alive):
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 40)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)


    def draw(self):
        #描画の画面分岐
        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_PLAY:
            self.draw_player()
        elif self.scene == SCENE_END:
            self.draw_end()



    def draw_title(self):
        pyxel.cls(0)
        pyxel.blt(19, 20, 2, 0, 0, 152, 64, 1)
        pyxel.text(65, 113,"- PRESS SPECE -", 7) 


    def draw_player(self):
            pyxel.bltm(self.backgraund_x, 0, 0, 0, 0, 2048, 128, None)
            if self.player_life == 8:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(16, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(24, 0, 0, 15, 64, 9, 8, 1)
            elif self.player_life == 7:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(16, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(24, 0, 0, 15, 72, 9, 8, 1)
            elif self.player_life == 6:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(16, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)
            elif self.player_life == 5:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(16, 0, 0, 15, 72, 9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)
            elif self.player_life == 4:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(16, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)
            elif self.player_life == 3:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 15, 72, 9, 8, 1)
                pyxel.blt(16, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)
            elif self.player_life == 2:
                pyxel.blt(0, 0, 0, 15, 64, 9, 8, 1)
                pyxel.blt(8, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(16, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)
            elif self.player_life == 1:
                pyxel.blt(0, 0, 0, 15, 72, 9, 8, 1)
                pyxel.blt(8, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(16, 0, 0, 3, 235,  9, 8, 1)
                pyxel.blt(24, 0, 0, 3, 235,  9, 8, 1)

            show_score = str(self.player_score).zfill(3)
            show_score = "Score : " + show_score
            pyxel.text(40, 0,show_score, 7)
            
            for x, y, kind, is_alive in self.whiteStar:
                if is_alive:
                    pyxel.blt(x, y, 0, 40, 0, 16, 16, 1)
                    
            for x, y, kind, is_alive in self.yerrowStar:
                if is_alive:
                    pyxel.blt(x, y, 0, 40, 24, 16, 16, 1)
                    
            if self.backgraund_x > -448:
                for x, y, kind, is_alive in self.firstAttack:
                    if is_alive:
                        pyxel.blt(x, y, 1, 0, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.cloud:
                        pyxel.blt(x, y, 0, 40, 73, 16, 11, 1)
            if -350 > self.backgraund_x > -1040:
                for x, y, kind, is_alive in self.secondAttack:
                    if is_alive:
                        pyxel.blt(x, y, 1, 24, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.bird:
                        pyxel.blt(x, y, 0, 16, 98, 16, 13, 6)
            if -950 > self.backgraund_x > -1600:
                for x, y, kind, is_alive in self.thirdAttack:
                    if is_alive:
                        pyxel.blt(x, y, 1, 48, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.flower:
                        pyxel.blt(x, y, 0, 25, 34, 9, 9, 1)
            if  self.backgraund_x < -1500:
                for x, y, kind, is_alive in self.thirdAttack:
                        if is_alive:
                            pyxel.blt(x, y, 1, 48, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.secondAttack:
                    if is_alive:
                        pyxel.blt(x, y, 1, 24, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.firstAttack:
                    if is_alive:
                        pyxel.blt(x, y, 1, 0, 0, 16, 16, 1)
                for x, y, kind, is_alive in self.plane:
                        pyxel.blt(x, y, 0, 0, 42, 16, 12, 1)


            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 31, 32, 1)


    def draw_end(self):
            pyxel.cls(0)
            if self.player_life == 0:
                pyxel.blt(60, 30, 0, 176, 16, 64, 40, 0)
                show_score = str(self.player_score).zfill(3)
                show_score = "Your Score : " + show_score
                pyxel.text(60, 85,show_score, 6)
                pyxel.text(40, 110,"- PRESS SPECE (TO TITLE) -", 7)
            else:
                pyxel.cls(1)
                pyxel.blt(60, 30, 0, 128, 200, 66, 32, 0)
                show_score = str(self.player_score).zfill(3)
                show_score = "Your Score : " + show_score
                pyxel.text(60, 85,show_score, 6)
                pyxel.text(40, 110,"- PRESS SPECE (TO TITLE) -", 7)

App()